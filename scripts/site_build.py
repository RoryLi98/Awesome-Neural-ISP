"""Self-contained, bilingual research library. No client dependencies or fetches."""
from __future__ import annotations

import html
import json
import re

from isp_data import ROOT, all_papers

UI = {
    'en': {
        'skip': 'Skip to the library', 'directory': 'An open research library',
        'browse': 'Browse research', 'all': 'All papers', 'whole': 'THE WHOLE PIPELINE',
        'restoration': 'RESTORATION & CAPTURE', 'rendering': 'COLOR & REPRESENTATION', 'systems': 'SYSTEMS & EVALUATION',
        'resources': 'Resources', 'guide': 'ISP, explained', 'contribute': 'Contribute a paper',
        'eyebrow': 'COMPUTATIONAL PHOTOGRAPHY / OPEN KNOWLEDGE',
        'hero1': 'From sensor to', 'hero2': 'something worth seeing.',
        'intro': 'A field guide to neural image signal processing. Explore the papers, code, and pretrained models shaping how cameras see.',
        'explore': 'Explore the library', 'readGuide': 'Start with ISP 101',
        'papers': 'papers', 'code': 'with code', 'weights': 'with weights', 'datasets': 'datasets',
        'diagram': 'The imaging pipeline, from a sensor mosaic through a learned ISP to a rendered image.',
        'raw': 'SENSOR MOSAIC', 'neural': 'NEURAL ISP', 'rgb': 'RENDERED IMAGE', 'signal': 'One signal. Many possibilities.',
        'spotlight': 'RESEARCH SPOTLIGHT', 'spotTitle': 'Put the controls back in the pipeline.',
        'spotText': 'User-guided rendering, camera conditioning, and modular neural ISPs. A dedicated home for controllable imaging.',
        'spotLink': 'Explore Controllable Neural ISP',
        'library': 'The research library', 'libraryDesc': 'Find a starting point. Follow an idea. Build on what is open.',
        'tabPapers': 'Papers', 'tabDatasets': 'Datasets', 'tabTools': 'Tools', 'tabLearn': 'Learn',
        'search': 'Search papers, methods, topics…', 'searchLabel': 'Search the research library',
        'availability': 'Availability', 'anyStatus': 'All releases', 'weightsOnly': 'With weights', 'codeOnly': 'With public code', 'unreleased': 'Not released',
        'year': 'Year', 'anyYear': 'All years', 'host': 'Weight host', 'anyHost': 'All hosts',
        'sort': 'Sort by', 'newest': 'Newest first', 'ready': 'Weights first', 'az': 'Name A–Z',
        'reset': 'Reset filters', 'showing': 'Showing', 'of': 'of', 'results': 'results',
        'more': 'Show more papers', 'empty': 'No results for this combination.', 'emptyHint': 'Try a broader search or reset your filters.',
        'paper': 'Paper', 'officialCode': 'Code', 'unofficialCode': 'Unofficial code', 'comingCode': 'Repository · coming soon',
        'details': 'Notes & downloads', 'note': 'Note', 'source': 'Capture / source', 'size': 'Size', 'download': 'Dataset',
        'W': 'Weights available', 'R': 'Weights in repo', 'C': 'Code available', 'U': 'Unofficial code', 'S': 'Coming soon', 'N': 'No public code',
        'framework': 'Framework', 'original': 'Original title', 'threads': 'Research threads', 'threadsDesc': 'Ideas connecting the literature.',
        'tutorials': 'Tutorials & surveys', 'books': 'Books', 'classic': 'Foundations', 'related_lists': 'Related libraries',
        'toolRaw': 'RAW I/O', 'toolIsp': 'Classical ISP', 'toolLearned': 'Learned ISP', 'toolEditor': 'RAW editors',
        'about': 'About the library', 'aboutText': 'Research spanning full camera pipelines, RAW restoration, controllable rendering, inverse ISPs, and imaging for machine vision. Each paper has one primary topic; adjacent work is connected through the topic descriptions.',
        'dates': 'Literature update', 'checked': 'Full code / weight audit',
        'audit': 'New and revised entries are checked against primary sources. The dates distinguish the literature update from the earlier full link audit. Checkpoints have not been downloaded or executed.',
        'coverage': 'This is a curated index, not an exhaustive survey. Journal-only work and newly released proceedings may be missing.',
        'updateLog': 'Sources & update notes', 'footer': 'An open map of computational imaging.',
        'menu': 'Browse topics', 'language': '中文', 'repo': 'GitHub', 'otherHost': 'Other hosts', 'breadcrumb': 'Awesome lists', 'index': 'INDEX',
        'noscript': 'Enable JavaScript for filters, or read the complete static Markdown library.',
    },
    'zh-CN': {
        'skip': '跳至论文库', 'directory': '开放的计算成像论文库',
        'browse': '浏览研究', 'all': '全部论文', 'whole': '完整成像管线',
        'restoration': '图像复原与采集', 'rendering': '色彩与图像表示', 'systems': '系统优化与评测',
        'resources': '学习资源', 'guide': '读懂 ISP', 'contribute': '贡献论文',
        'eyebrow': '计算摄影 / 开放知识', 'hero1': '从传感器信号，', 'hero2': '到值得看见的影像。',
        'intro': '一份神经图像信号处理研究指南。探索塑造相机成像的论文、开源代码与预训练模型。',
        'explore': '探索论文库', 'readGuide': '从 ISP 入门开始',
        'papers': '篇论文', 'code': '项公开代码', 'weights': '项预训练权重', 'datasets': '个数据集',
        'diagram': '成像流程示意：传感器马赛克信号经神经 ISP 处理，生成渲染图像。',
        'raw': '传感器马赛克', 'neural': '神经 ISP', 'rgb': '渲染图像', 'signal': '一份信号，多种表达。',
        'spotlight': '研究专题', 'spotTitle': '让成像管线重新拥有可调控的空间。',
        'spotText': '面向用户的渲染控制、相机条件化与模块化神经 ISP。在独立专题中梳理可控成像。',
        'spotLink': '探索可控神经 ISP',
        'library': '研究论文库', 'libraryDesc': '找到起点，追踪思路，从开放成果出发。',
        'tabPapers': '论文', 'tabDatasets': '数据集', 'tabTools': '工具', 'tabLearn': '学习资料',
        'search': '搜索论文、方法、主题…', 'searchLabel': '搜索研究论文库',
        'availability': '开放状态', 'anyStatus': '全部开放状态', 'weightsOnly': '有预训练权重', 'codeOnly': '有公开代码', 'unreleased': '尚未公开',
        'year': '年份', 'anyYear': '全部年份', 'host': '权重托管', 'anyHost': '全部托管平台',
        'sort': '排序', 'newest': '最新优先', 'ready': '权重优先', 'az': '名称 A–Z',
        'reset': '重置筛选', 'showing': '显示', 'of': '/', 'results': '条结果',
        'more': '显示更多论文', 'empty': '没有符合当前条件的结果。', 'emptyHint': '试试更宽泛的关键词，或重置筛选条件。',
        'paper': '论文', 'officialCode': '代码', 'unofficialCode': '非官方代码', 'comingCode': '代码仓库 · 待发布',
        'details': '备注与下载', 'note': '备注', 'source': '采集方式 / 来源', 'size': '规模', 'download': '数据集',
        'W': '权重可下载', 'R': '仓库内含权重', 'C': '代码已公开', 'U': '非官方实现', 'S': '待发布', 'N': '未发现公开代码',
        'framework': '框架', 'original': '原文标题', 'threads': '研究脉络', 'threadsDesc': '串联文献的几条线索。',
        'tutorials': '教程与综述', 'books': '书籍', 'classic': '基础文献', 'related_lists': '相关论文库',
        'toolRaw': 'RAW 读写', 'toolIsp': '传统 ISP', 'toolLearned': '神经 ISP', 'toolEditor': 'RAW 编辑器',
        'about': '关于论文库', 'aboutText': '涵盖完整相机管线、RAW 图像复原、可控渲染、逆向 ISP 与面向机器视觉的成像。每篇论文只归入一个主要主题，相关方向通过分类说明串联。',
        'dates': '文献更新', 'checked': '代码与权重全面核验',
        'audit': '新增与修订条目依据一手来源核验。文献更新日期与此前的全面链接核验日期分开记录。权重文件未下载或运行。',
        'coverage': '这是一份精选索引，并非穷尽式综述；仅在期刊发表的工作与新发布的会议论文可能尚未收录。',
        'updateLog': '来源与更新记录', 'footer': '共同绘制开放的计算成像地图。',
        'menu': '浏览主题', 'language': 'English', 'repo': 'GitHub', 'otherHost': '其他平台', 'breadcrumb': '精选论文目录', 'index': '索引',
        'noscript': '开启 JavaScript 即可使用筛选；也可以阅读完整的静态 Markdown 论文库。',
    },
}


def site(d, lang='en'):
    cfg = d['config']
    ui = UI[lang]
    repo = f"https://github.com/{cfg['owner']}/{cfg['repo']}"
    suffix = '.zh-CN' if lang == 'zh-CN' else ''
    ps = []
    status = {'weights': 'W', 'weights-in-repo': 'R', 'code': 'C', 'unofficial': 'U', 'coming-soon': 'S', 'no-code': 'N'}
    for cat, p in all_papers(d):
        ps.append(dict(n=p['name'], t=p['title'], en=p.get('original_title', ''), ens=p.get('original_tldr', ''),
                       v=p['venue'], y=p['year'], c=cat['id'], s=p['tldr'], p=p['paper'],
                       g=p.get('code', ''), st=status[p['status']], w=p.get('weights', []),
                       note=p.get('note', ''), fw=p.get('framework', '')))
    payload = dict(papers=ps, categories=d['categories'], datasets=d['datasets'], tools=d['tools'],
                   trends=d['trends'], resources=d['resources'])
    counts = dict(NP=len(ps), NCODE=sum(p['st'] in 'WRCU' for p in ps), NW=sum(p['st'] in 'WR' for p in ps), ND=len(d['datasets']))
    data_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    ui_json = json.dumps(ui, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    replacements = {**{k: str(v) for k, v in counts.items()}, **ui,
                    'LANG': lang, 'TITLE': 'Awesome Neural ISP' + (' · 中文' if suffix else ''),
                    'REPO': repo, 'GUIDE': f'{repo}/blob/main/guide/isp-101{suffix}.md',
                    'CONTRIBUTE': f'{repo}/blob/main/CONTRIBUTING{suffix}.md',
                    'README': f'{repo}/blob/main/README{suffix}.md',
                    'LOG': f'{repo}/blob/main/guide/literature-update-2026-10-28.md',
                    'CHECKED': cfg['checked'], 'UPDATED': cfg.get('literature_updated', cfg['checked']),
                    'ALT': 'index.html' if suffix else 'zh-CN.html',
                    'DATA': data_json, 'UI': ui_json,
                    'STYLE': (ROOT / 'scripts/site_style.css').read_text(encoding='utf-8'),
                    'SCRIPT': (ROOT / 'scripts/site_script.js').read_text(encoding='utf-8')}
    template = (ROOT / 'scripts/site_template.html').read_text(encoding='utf-8')
    return re.sub(r'__([A-Za-z][A-Za-z0-9_]*)__',
                  lambda m: replacements[m[1]] if m[1] in ('DATA', 'UI', 'STYLE', 'SCRIPT') else html.escape(replacements[m[1]], quote=True), template)
