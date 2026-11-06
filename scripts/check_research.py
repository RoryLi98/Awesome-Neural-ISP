"""Regression checks for publication identity, taxonomy boundaries and bilingual resources."""
from __future__ import annotations

import copy
import csv
import re
import unittest

import isp_data
import localization
from build import stats, weights_md
from chinese_markdown import weights_md as chinese_weights_md
from site_build import venue_name, venue_id


class ResearchChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = isp_data.load()
        cls.by_name = {p['name']: (c['id'],p) for c,p in isp_data.all_papers(cls.d)}
        cls.zh = localization.chinese(cls.d)

    def test_valid_sources(self):
        self.assertEqual(isp_data.validate(self.d), [])

    def test_venue_tracks_stay_distinct(self):
        self.assertEqual(venue_name('CVPRW (NTIRE)'), 'CVPRW')
        self.assertEqual(venue_name('ECCVW (AIM)'), 'ECCVW')
        self.assertEqual(venue_name('AAAI (Oral)'), 'AAAI')
        self.assertEqual(venue_name('ACM TOG (SIGGRAPH Asia)'), 'SIGGRAPH Asia')
        self.assertEqual(venue_name('SIGGRAPH (TOG)'), 'SIGGRAPH')
        self.assertEqual(venue_name('TOG'), 'ACM TOG')
        self.assertEqual(len({venue_id(v) for v in ['CVPR', 'CVPRW (NTIRE)', 'CVPR Findings', 'arXiv']}), 4)
        canonical = {venue_name(p['venue']) for _, p in isp_data.all_papers(self.d)}
        self.assertEqual(len(canonical), len({venue_id(v) for v in canonical}))

    def test_navigation_preserves_all_research_areas(self):
        d = copy.deepcopy(self.d)
        d['navigation'][0]['topics'].append('e2e')
        self.assertTrue(any('Navigation must include' in e for e in isp_data.validate(d)))

    def test_versioned_arxiv_is_one_publication(self):
        self.assertEqual(isp_data.publication_key('https://arxiv.org/pdf/2312.13313v3.pdf?download=1'),
                         isp_data.publication_key('http://export.arxiv.org/abs/2312.13313v1'))
        self.assertEqual(isp_data.publication_key('https://dx.doi.org/10.1145/ABC'),
                         isp_data.publication_key('https://doi.org/10.1145/abc'))

    def test_duplicate_publication_rejected(self):
        d = copy.deepcopy(self.d)
        p = copy.deepcopy(self.by_name['ParamISP'][1])
        p['name'] = 'Accidental duplicated publication'
        p['paper'] = p['paper'] + 'v2'
        d['papers']['e2e'].append(p)
        self.assertTrue(any('Duplicate publication' in e for e in isp_data.validate(d)))

    def test_primary_task_boundaries(self):
        expected = {'DPED':'color','DiR':'restoration','StereoISP':'demosaic',
                    'RawNIND':'denoise','Rawformer':'inverse','RAWIC':'compression',
                    'Single-Frame HDR ISP':'burst','Raw/sRGB HDR Video':'video',
                    'JDD Burst Fine-tune':'demosaic','PyNET-QxQ':'demosaic',
                    'DNF':'lowlight','CtrlISP':'lowlight','DRIFT':'burst',
                    'POS-ISP':'task','ReconfigISP':'tuning','MW-ISPNet':None}
        for name,cid in expected.items():
            with self.subTest(name=name):
                self.assertEqual(self.by_name.get(name,(None,))[0], cid)

    def test_conditions_are_not_user_controls(self):
        for name in ['ParamISP','MetaISP','Uni-ISP','CRISPnet']:
            m = self.d['research'][name]
            self.assertIn('controllable', m['collections'])
            self.assertIn('camera-conditioned', m['control'])
            self.assertNotIn('user-parameters', m['control'])
        for name in ['CtrlISP','Modular Neural ISP','DRIFT','Neural Photo-Finishing']:
            self.assertIn('user-parameters', self.d['research'][name]['control'])
        for name in ['PQDynamicISP','ISPW / LiteISP-in-the-wild','MBISPLD','NILUT']:
            self.assertNotIn('controllable', self.d['research'].get(name,{}).get('collections',[]))

    def test_implementation_resources_survive_in_both_exports(self):
        zh_by_name = {p['name']:p for _,p in isp_data.all_papers(self.zh)}
        for parent,child in [('AIM 2020 ISP','MW-ISPNet'),('NTIRE 2020 Real Denoising','MWRCANet')]:
            p = self.by_name[parent][1]
            r, = p['implementations']
            self.assertEqual(r['name'], child)
            self.assertEqual(len(r['weights']), 2)
            self.assertTrue(r['code'].startswith('https://github.com/'))
            self.assertTrue(isp_data.has_code(p))
            self.assertTrue(isp_data.has_weights(p))
            z, = zh_by_name[parent]['implementations']
            self.assertEqual(z['code'], r['code'])
            self.assertEqual([w['url'] for w in z['weights']], [w['url'] for w in r['weights']])
            self.assertRegex(z['tldr'], r'[\u3400-\u9fff]')
            self.assertNotEqual(z['weights'][0]['label'], r['weights'][0]['label'])

    def test_weight_exports_include_every_publication(self):
        count = stats(self.d)['weights']
        en = weights_md(self.d)
        zh = chinese_weights_md(self.zh)
        self.assertEqual(len(re.findall(r'^\| \*\*',en,re.M)), count)
        self.assertEqual(len(re.findall(r'^\| \*\*',zh,re.M)), count)
        for _,p in isp_data.all_papers(self.d):
            for w in isp_data.weights(p):
                self.assertIn(w['url'], en)
                self.assertIn(w['url'], zh)

    def test_unsubstantiated_tag_rejected(self):
        d = copy.deepcopy(self.d)
        d['research']['NILUT']['evidence'].pop('implicit')
        self.assertTrue(any('implicit needs source evidence' in e for e in isp_data.validate(d)))

    def test_third_party_weights_keep_their_provenance(self):
        p = self.by_name['Residual JDSR'][1]
        self.assertEqual(p['status'], 'unofficial')
        self.assertTrue(isp_data.has_weights(p))
        self.assertIn(p['weights'][0]['url'], weights_md(self.d))
        self.assertIn('unofficial', weights_md(self.d))

    def test_bilingual_reading_notes_and_citations(self):
        for name,m in self.d['research'].items():
            if m.get('reading'):
                for text in m['reading']['zh-CN'].values():
                    self.assertRegex(text,r'[\u3400-\u9fff]',name)
            if m.get('bibtex'):
                self.assertTrue(m['bibtex_source'].startswith('https://'))
                self.assertRegex(m['bibtex'],r'(?i)author\s*=|editor\s*=')

    def test_complete_classification_snapshot(self):
        with (isp_data.ROOT/'guide/classification-audit-2026-11-05.csv').open(encoding='utf-8-sig',newline='') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len({r['name'] for r in rows}))
        for r in rows:
            self.assertEqual(self.by_name[r['name']][0],r['primary'])
            self.assertEqual(self.by_name[r['name']][1]['title'],r['official_title'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
