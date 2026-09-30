"""Load and validate the YAML data under data/.

Everything the README, WEIGHTS.md and the interactive page show comes from here.
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import re

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
PAPER_KEYS = ('name', 'title', 'venue', 'year', 'paper', 'code', 'status', 'weights', 'framework', 'tldr', 'note')
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
    )


def validate(d) -> list[str]:
    """Return a list of human-readable problems; empty means the data is valid."""
    errs: list[str] = []
    ids = [c['id'] for c in d['categories']]
    files = sorted(p.stem for p in (DATA / 'papers').glob('*.yaml'))
    for extra in set(files) - set(ids):
        errs.append(f'data/papers/{extra}.yaml is not listed in data/categories.yaml')
    this_year = _dt.date.today().year
    seen: dict[str, str] = {}
    for cid, items in d['papers'].items():
        if not isinstance(items, list):
            errs.append(f'data/papers/{cid}.yaml must be a YAML list')
            continue
        for i, p in enumerate(items):
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
