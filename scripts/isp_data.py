"""Load and validate the YAML data under data/.

Everything the README, WEIGHTS.md and the interactive page show comes from here.
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import re
import hashlib
from urllib.parse import urlsplit, unquote

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

STATUSES = {
    'weights': 'README links to downloadable pretrained weights',
    'weights-in-repo': 'pretrained weights are committed in the repository',
    'code': 'official code, no pretrained weights found',
    'unofficial': 'third-party implementation',
    'coming-soon': 'repository is a placeholder or says code is coming',
    'no-code': 'no public code found',
}
WEIGHT_STATUSES = ('weights', 'weights-in-repo')
PAPER_KEYS = ('name', 'title', 'venue', 'year', 'paper', 'code', 'status', 'weights', 'framework', 'tldr', 'note', 'implementations')
REQUIRED = ('name', 'title', 'venue', 'year', 'paper', 'status', 'tldr')
URL = re.compile(r'^https?://\S+$')


class DataError(Exception):
    pass


def _load(path: pathlib.Path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f) or []


def load():
    """Return a dict with config, categories, papers (by category), datasets, tools, resources, trends."""
    cfg = _load(ROOT / 'config.yaml')
    cats = _load(DATA / 'categories.yaml')
    papers = {c['id']: _load(DATA / 'papers' / f"{c['id']}.yaml") for c in cats}
    return dict(
        config=cfg,
        categories=cats,
        papers=papers,
        datasets=_load(DATA / 'datasets.yaml'),
        tools=_load(DATA / 'tools.yaml'),
        resources=_load(DATA / 'resources.yaml'),
        trends=_load(DATA / 'trends.yaml'),
        collections=_load(DATA / 'collections.yaml'),
        navigation=_load(DATA / 'navigation.yaml'),
        facets=_load(DATA / 'facets.yaml'),
        research=_load(DATA / 'research.yaml'),
    )


def publication_key(url):
    """Normalize known primary-source identities, including arXiv PDF/version URLs."""
    parsed = urlsplit(url)
    host = parsed.netloc.lower().removeprefix('www.')
    path = unquote(parsed.path).rstrip('/')
    if host in ('arxiv.org', 'export.arxiv.org'):
        path = re.sub(r'^/(abs|pdf)/', '', path)
        return 'arxiv:' + re.sub(r'v\d+$', '', path.removesuffix('.pdf'))
    if host in ('doi.org', 'dx.doi.org'):
        return 'doi:' + path.lstrip('/').lower()
    return host + path


def paper_id(p):
    slug = re.sub(r'[^a-z0-9]+', '-', p['name'].lower()).strip('-')
    return 'paper-' + (slug or hashlib.sha1(p['name'].encode()).hexdigest()[:12])


def resources(p):
    """A publication may document separately released challenge implementations."""
    return [p, *p.get('implementations', [])]


def release_status(p):
    rank = ['weights', 'weights-in-repo', 'code', 'unofficial', 'coming-soon', 'no-code']
    return min((r['status'] for r in resources(p)), key=rank.index)


def has_code(p):
    return any(r['status'] in ('weights', 'weights-in-repo', 'code', 'unofficial') for r in resources(p))


def has_weights(p):
    return any(bool(r.get('weights')) for r in resources(p))


def weights(p):
    return [dict(w, label=(r['name'] + ' · ' if r is not p else '') + w['label'])
            for r in resources(p) for w in r.get('weights', [])]


def validate(d) -> list[str]:
    """Return a list of human-readable problems; empty means the data is valid."""
    errs: list[str] = []
    ids = [c['id'] for c in d['categories']]
    collection_ids = [c['id'] for c in d['collections']]
    if len(ids) != len(set(ids)) or len(collection_ids) != len(set(collection_ids)) or set(ids) & set(collection_ids):
        errs.append('Primary categories and cross-task collections need unique, disjoint ids')
    nav_topics = [topic for group in d['navigation'] for topic in group['topics']]
    if len(nav_topics) != len(set(nav_topics)) or set(nav_topics) != set(ids + collection_ids):
        errs.append('Navigation must include each task and cross-task view exactly once')
    for group in d['navigation']:
        if set(group.get('label', {})) != {'en', 'zh-CN'} or any(not v.strip() for v in group['label'].values()):
            errs.append('Navigation groups need labels in both languages')
    files = sorted(p.stem for p in (DATA / 'papers').glob('*.yaml'))
    for extra in set(files) - set(ids):
        errs.append(f'data/papers/{extra}.yaml is not listed in data/categories.yaml')
    this_year = _dt.date.today().year
    seen: dict[str, str] = {}
    publications, anchors = {}, set()
    for cid, items in d['papers'].items():
        if not isinstance(items, list):
            errs.append(f'data/papers/{cid}.yaml must be a YAML list')
            continue
        for i, p in enumerate(items):
            key = publication_key(p['paper'])
            if key in publications:
                errs.append(f"Duplicate publication: {p['name']} and {publications[key]}; nest implementations under the publication")
            publications[key] = p['name']
            anchor = paper_id(p)
            if anchor in anchors:
                errs.append(f'Duplicate paper anchor: {anchor}')
            anchors.add(anchor)
        for i, p in enumerate(r for publication in items for r in resources(publication)):
            where = f"data/papers/{cid}.yaml #{i + 1} ({p.get('name', '?')})"
            for k in REQUIRED:
                if p.get(k) in (None, ''):
                    errs.append(f'{where}: missing "{k}"')
            for k in p:
                if k not in PAPER_KEYS:
                    errs.append(f'{where}: unknown key "{k}"')
            st = p.get('status')
            if st not in STATUSES:
                errs.append(f'{where}: status "{st}" must be one of {", ".join(STATUSES)}')
            if st in WEIGHT_STATUSES and not p.get('weights'):
                errs.append(f'{where}: status "{st}" needs at least one entry under "weights"')
            if p.get('weights') and st not in (*WEIGHT_STATUSES, 'unofficial'):
                errs.append(f'{where}: weight links require weights, weights-in-repo or explicitly unofficial status')
            if st in ('code', 'unofficial') and not p.get('code'):
                errs.append(f'{where}: status "{st}" needs a "code" URL')
            if st == 'no-code' and p.get('code'):
                errs.append(f'{where}: has a "code" URL but status is "no-code"')
            y = p.get('year')
            if not isinstance(y, int) or not 1990 <= y <= this_year + 1:
                errs.append(f'{where}: year "{y}" is not a plausible integer year')
            for k in ('paper', 'code'):
                if p.get(k) and not URL.match(p[k]):
                    errs.append(f'{where}: "{k}" is not an http(s) URL')
            for w in p.get('weights') or []:
                if not isinstance(w, dict) or not w.get('label') or not URL.match(str(w.get('url', ''))):
                    errs.append(f'{where}: each weights entry needs "label" and an http(s) "url"')
            name = str(p.get('name', '')).lower()
            if name in seen:
                errs.append(f'{where}: name duplicates {seen[name]}')
            seen[name] = where
    names = {p['name'] for _, p in all_papers(d)}
    collection_ids = {c['id'] for c in d['collections']}
    datasets = {ds['name'] for ds in d['datasets']}
    for name, meta in d['research'].items():
        if name not in names:
            errs.append(f'Research metadata has no publication: {name}')
        for facet in ('architecture', 'supervision', 'signal', 'control'):
            values = meta.get(facet, [])
            if not isinstance(values, list) or len(set(values)) != len(values):
                errs.append(f'{name}: {facet} must be a list without duplicates')
                continue
            for value in values:
                if value not in d['facets'][facet]['values']:
                    errs.append(f'{name}: unknown {facet} value {value}')
                if not meta.get('evidence', {}).get(value):
                    errs.append(f'{name}: {value} needs source evidence')
        for cid in meta.get('collections', []):
            if cid not in collection_ids:
                errs.append(f'{name}: unknown collection {cid}')
        for ds in meta.get('datasets', []):
            if ds not in datasets:
                errs.append(f'{name}: unknown dataset {ds}')
        reading = meta.get('reading', {})
        summary = meta.get('summary', {})
        if summary and (not isinstance(summary, dict) or set(summary) != {'en', 'zh-CN'} or any(
                not isinstance(v, str) or not v.strip() for v in summary.values()) or
                not URL.match(meta.get('summary_source', ''))):
            errs.append(f'{name}: expanded summary needs both languages and a primary-source URL')
        if reading and (set(reading) != {'en', 'zh-CN'} or any(
                set(reading[lang]) != {'challenge', 'method', 'contribution', 'limits'} or
                any(not isinstance(v, str) or not v.strip() for v in reading[lang].values()) for lang in reading)):
            errs.append(f'{name}: reading notes need challenge/method/contribution/limits in both languages')
        if meta.get('bibtex') and (not URL.match(meta.get('bibtex_source', '')) or
                                  not re.search(r'@\w+\s*\{', meta['bibtex']) or
                                  not re.search(r'author\s*=|editor\s*=', meta['bibtex'], re.I)):
            errs.append(f'{name}: BibTeX needs a primary citation source and source author/editor metadata')
    for i, ds in enumerate(d['datasets']):
        for k in ('name', 'year', 'url', 'use'):
            if not ds.get(k):
                errs.append(f'data/datasets.yaml #{i + 1}: missing "{k}"')
        if ds.get('task') and ds['task'] not in ids:
            errs.append(f'data/datasets.yaml #{i + 1}: task "{ds["task"]}" is not a category id')
    for i, t in enumerate(d['tools']):
        for k in ('name', 'url', 'description'):
            if not t.get(k):
                errs.append(f'data/tools.yaml #{i + 1}: missing "{k}"')
    return errs


def all_papers(d):
    """Yield (category, paper) in README order."""
    for c in d['categories']:
        for p in d['papers'][c['id']]:
            yield c, p
