"""Strict Chinese content overlay; English remains the bibliographic source."""
from __future__ import annotations

import copy
import re

from isp_data import ROOT, _load


def chinese(d):
    papers = _load(ROOT / 'data/i18n/papers.zh-CN.yaml')
    content = _load(ROOT / 'data/i18n/resources.zh-CN.yaml')
    out = copy.deepcopy(d)
    errors = []

    def overlay(target, translations, key, fields, where):
        translated = translations.get(key, {})
        for field in fields:
            if not target.get(field):
                continue
            if not isinstance(translated.get(field), str) or not translated[field].strip():
                errors.append(f'{where}: missing Chinese {field}')
            else:
                target[field] = translated[field]

    names = {p['name'] for ps in d['papers'].values() for p in ps}
    for extra in set(papers) - names:
        errors.append(f'Chinese paper no longer exists: {extra}')
    for ps in out['papers'].values():
        for p in ps:
            p['original_title'] = p['title']
            p['original_tldr'] = p['tldr']
            overlay(p, papers, p['name'], ('title', 'tldr', 'note'), p['name'])
            for field in ('title', 'tldr'):
                if not re.search(r'[\u3400-\u9fff]', p[field]):
                    errors.append(f'{p["name"]}: {field} lacks a Chinese translation')
            labels = papers.get(p['name'], {}).get('weight_labels', [])
            weights = p.get('weights') or []
            if len(labels) != len(weights):
                errors.append(f'{p["name"]}: Chinese weight label count differs')
            for weight, label in zip(weights, labels):
                if not isinstance(label, str) or not label.strip():
                    errors.append(f'{p["name"]}: empty Chinese weight label')
                else:
                    weight['label'] = label
    for c in out['categories']:
        overlay(c, content.get('categories', {}), c['id'], ('title', 'short', 'description'), c['id'])
    for section, identity in [('categories', 'id'), ('datasets', 'name'), ('tools', 'name')]:
        expected = {item[identity] for item in d[section]}
        actual = set(content.get(section, {}))
        for extra in actual - expected:
            errors.append(f'{section}: Chinese key no longer exists: {extra}')
    for item in out['datasets']:
        overlay(item, content.get('datasets', {}), item['name'], ('source', 'capture', 'size', 'use'), item['name'])
    for item in out['tools']:
        overlay(item, content.get('tools', {}), item['name'], ('description',), item['name'])
    for key in ('trends',):
        translated = content.get(key, [])
        if len(translated) != len(out[key]):
            errors.append(f'{key}: Chinese item count differs')
        else:
            for i, (original, trans) in enumerate(zip(out[key], translated)):
                for field in ('title', 'text', 'examples'):
                    if not isinstance(trans.get(field), str) or not trans[field].strip():
                        errors.append(f'{key} #{i}: missing {field}')
                    else:
                        original[field] = trans[field]
    resources = content.get('resources', {})
    for kind, originals in out['resources'].items():
        translated = resources.get(kind, [])
        if len(translated) != len(originals):
            errors.append(f'resources.{kind}: Chinese item count differs')
            continue
        for i, (original, trans) in enumerate(zip(originals, translated)):
            if kind == 'classic':
                if not trans.get('stage') or len(trans.get('items', [])) != len(original['items']):
                    errors.append(f'classic #{i}: incomplete translation')
                    continue
                original['stage'] = trans['stage']
                for j, item in enumerate(original['items']):
                    if trans['items'][j].get('url') != item['url']:
                        errors.append(f'classic {i}/{j}: translated resource URL/order differs')
                    overlay(item, {j: trans['items'][j]}, j, ('name',), f'classic {i}/{j}')
            else:
                if trans.get('url') != original['url']:
                    errors.append(f'{kind} #{i}: translated resource URL/order differs')
                overlay(original, {i: trans}, i, ('name', 'description'), f'{kind} #{i}')
    overlay(out['config'], {'config': content.get('config', {})}, 'config', ('tagline',), 'config')
    if errors:
        raise ValueError('Incomplete Chinese content:\n  ' + '\n  '.join(errors))
    return out
