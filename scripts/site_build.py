"""Self-contained, bilingual research library. No client dependencies or fetches."""
from __future__ import annotations

import html
import json
import re
from collections import Counter

from isp_data import ROOT, all_papers, resources, release_status, weights, paper_id, has_code, has_weights


def display_note(note):
    """Keep availability caveats, leaving audit timestamps in the source records."""
    note = re.sub(r'\s*\(checked \d{4}-\d{2}-\d{2}\)|（核验日期：\d{4}-\d{2}-\d{2}）', '', note)
    note = re.sub(r'\d{4}-\d{2}-\d{2} 核验时[，,]\s*', '', note)
    note = re.sub(r' on \d{4}-\d{2}-\d{2}(?=\.)', '', note)
    return note


def display_summary(p, meta, lang):
    if meta.get('summary'):
        return meta['summary'][lang]
    reading = meta.get('reading', {}).get(lang)
    if reading:
        return (' ' if lang == 'en' else '').join(reading[k] for k in ('challenge', 'method', 'contribution'))
    return p['tldr']


def venue_name(venue):
    """Normalize display variants without merging main, workshop or Findings tracks."""
    for workshop in ('CVPRW', 'ICCVW', 'ECCVW', 'WACVW'):
        if venue == workshop or venue.startswith(workshop + ' '):
            return workshop
    if 'SIGGRAPH Asia' in venue:
        return 'SIGGRAPH Asia'
    if 'SIGGRAPH' in venue:
        return 'SIGGRAPH'
    if venue in ('TOG', 'ACM TOG'):
        return 'ACM TOG'
    if venue.startswith('AAAI ('):
        return 'AAAI'
    return venue


def venue_id(venue):
    return re.sub(r'[^a-z0-9]+', '-', venue_name(venue).lower()).strip('-')


def venue_group(venue):
    if venue in ('CVPR', 'ICCV', 'ECCV', 'WACV', 'BMVC', 'ACCV'):
        return 'venueVision'
    if venue in ('NeurIPS', 'ICLR', 'AAAI'):
        return 'venueLearning'
    if venue in ('CVPRW', 'ICCVW', 'ECCVW', 'WACVW', 'CVPR Findings'):
        return 'venueWorkshops'
    if venue in ('SIGGRAPH', 'SIGGRAPH Asia', 'ACM MM', 'ICIP', 'ICCP', 'CIC'):
        return 'venueImaging'
    if venue == 'arXiv':
        return 'venuePreprints'
    if venue in ('IEEE TIP', 'IEEE TPAMI', 'IEEE TCSVT', 'IEEE OJSP', 'IEEE Access', 'IEEE SPL',
            'IEEE TMM', 'IEEE TCI', 'IET Image Processing',
            'ACM TOG', 'TMLR', 'IJCV', 'JOSA A', 'Inverse Probl. Imaging',
            'J. Comput. Appl. Math.', 'ACM Computing Surveys'):
        return 'venueJournals'
    return 'venueOther'

UI = {'en': {'skip': 'Skip to the library',
        'directory': 'An open research library',
        'browse': 'Browse research',
        'all': 'All publications',
        'whole': 'THE WHOLE PIPELINE',
        'restoration': 'RESTORATION & CAPTURE',
        'rendering': 'COLOR & REPRESENTATION',
        'systems': 'SYSTEMS & EVALUATION',
        'resources': 'Resources',
        'guide': 'ISP, explained',
        'contribute': 'Contribute a paper',
        'eyebrow': 'COMPUTATIONAL PHOTOGRAPHY / OPEN KNOWLEDGE',
        'hero1': 'Neural ISP,',
        'hero2': 'organized for research.',
        'intro': 'Papers, methods and released models across the camera pipeline.',
        'explore': 'Explore the library',
        'readGuide': 'Start with ISP 101',
        'papers': 'unique publications',
        'code': 'with code',
        'weights': 'with weights',
        'datasets': 'datasets',
        'diagram': 'The imaging pipeline, from a sensor mosaic through a learned ISP to a rendered image.',
        'raw': 'SENSOR MOSAIC',
        'neural': 'NEURAL ISP',
        'rgb': 'RENDERED IMAGE',
        'signal': 'One signal. Many possibilities.',
        'library': 'Research library',
        'libraryDesc': 'Browse by research area; combine venue, year and method filters.',
        'tabPapers': 'Publications',
        'tabDatasets': 'Datasets',
        'tabTools': 'Tools',
        'tabLearn': 'Learn',
        'search': 'Search papers, methods, topics…',
        'searchLabel': 'Search the research library',
        'availability': 'Availability',
        'anyStatus': 'All releases',
        'weightsOnly': 'With weights',
        'codeOnly': 'With public code',
        'unreleased': 'Not released',
        'year': 'Year',
        'anyYear': 'All years',
        'host': 'Weight host',
        'anyHost': 'All hosts',
        'sort': 'Sort by',
        'newest': 'Newest first',
        'ready': 'Weights first',
        'az': 'Title A–Z',
        'reset': 'Reset filters',
        'showing': 'Showing',
        'of': 'of',
        'results': 'results',
        'more': 'Show more papers',
        'empty': 'No results for this combination.',
        'emptyHint': 'Try a broader search or reset your filters.',
        'officialCode': 'Code',
        'unofficialCode': 'Unofficial code',
        'comingCode': 'Repository · coming soon',
        'note': 'Note',
        'source': 'Capture / source',
        'size': 'Size',
        'download': 'Dataset',
        'W': 'Weights available',
        'R': 'Weights in repo',
        'C': 'Code available',
        'U': 'Unofficial code',
        'S': 'Coming soon',
        'N': 'No public code',
        'original': 'Original title',
        'threads': 'Research threads',
        'threadsDesc': 'Ideas connecting the literature.',
        'tutorials': 'Tutorials & surveys',
        'books': 'Books',
        'classic': 'Foundations',
        'related_lists': 'Related libraries',
        'toolRaw': 'RAW I/O',
        'toolIsp': 'Classical ISP',
        'toolLearned': 'Learned ISP',
        'toolEditor': 'RAW editors',
        'about': 'About the library',
        'aboutText': 'Each publication has one primary task. Controllable and mobile/efficient ISPs are overlapping '
                     'collections; model, training, signal and control tags are independent filters. Challenge '
                     'implementations are attached to their reports and do not increase the publication count. Code '
                     'and weight totals include explicitly labeled third-party releases.',
        'dates': 'Literature update',
        'checked': 'Full code / weight audit',
        'audit': 'Literature additions, summary revisions, classification changes and the last full code/weight audit '
                 'are dated separately. Tags and reading notes link back to primary sources.',
        'coverage': 'This is a curated index, not an exhaustive survey. Journal-only work and newly released '
                    'proceedings may be missing.',
        'updateLog': 'Sources & update notes',
        'footer': 'An open map of computational imaging.',
        'menu': 'Browse topics',
        'language': '中文',
        'repo': 'GitHub',
        'otherHost': 'Other hosts',
        'breadcrumb': 'Awesome lists',
        'index': 'INDEX',
        'noscript': 'Enable JavaScript for filters, or read the complete static Markdown library.',
        'focus': 'CROSS-TASK COLLECTIONS',
        'classification': 'Classification criteria',
        'advanced': 'More filters',
        'active': 'Active filters',
        'clearOne': 'Remove filter',
        'anyArchitecture': 'All model families',
        'anyControl': 'All control interfaces',
        'anySupervision': 'All training methods',
        'anySignal': 'All signal types',
        'unlabeled': 'Not annotated',
        'facetHelp': 'Tags describe documented components; missing tags mean not annotated. Camera conditioning does '
                     'not imply an interactive editor.',
        'challenge': 'Challenge',
        'method': 'Specific method',
        'contribution': 'Contribution',
        'limits': 'Reading notes · editorial',
        'sourceLink': 'Primary source',
        'implementation': 'Implementations documented in this report',
        'relatedDatasets': 'Related datasets',
        'summaryDate': 'Summary revision',
        'taxonomyDate': 'Classification audit',
        'taxonomyLog': 'Classification rules & full audit',
        'summaryLog': 'Summary revision notes',
        'paperCount': 'Unique publications',
        'unofficialWeights': 'Unofficial code & weights',
        'downloadWeights': 'Pretrained weights',
        'venue': 'Venues',
        'allVenues': 'All venues',
        'selectedVenues': 'Venues selected',
        'venueHelp': 'Select any combination. No selection includes all venues. Workshops, Findings and preprints are separate from main conferences.',
        'venuePreset': 'CVPR + ICCV + ECCV',
        'clearVenues': 'Clear venue selection',
        'venueVision': 'Computer vision conferences',
        'venueLearning': 'Machine learning & AI',
        'venueImaging': 'Graphics, imaging & multimedia',
        'venueWorkshops': 'Workshops & Findings',
        'venueJournals': 'Journals',
        'venuePreprints': 'Preprints',
        'venueOther': 'Other venues'},
 'zh-CN': {'skip': '跳至论文库',
           'directory': '开放的计算成像论文库',
           'browse': '浏览研究',
           'all': '全部文献',
           'whole': '完整成像管线',
           'restoration': '图像复原与采集',
           'rendering': '色彩与图像表示',
           'systems': '系统优化与评测',
           'resources': '学习资源',
           'guide': '读懂 ISP',
           'contribute': '贡献论文',
           'eyebrow': '计算摄影 / 开放知识',
           'hero1': '神经 ISP，',
           'hero2': '从论文到研究思路。',
           'intro': '按成像任务查找论文、具体方法与已发布模型。',
           'explore': '探索论文库',
           'readGuide': '从 ISP 入门开始',
           'papers': '篇独立文献',
           'code': '篇附代码',
           'weights': '篇附权重',
           'datasets': '个数据集',
           'diagram': '成像流程示意：传感器马赛克信号经神经 ISP 处理，生成渲染图像。',
           'raw': '传感器马赛克',
           'neural': '神经 ISP',
           'rgb': '渲染图像',
           'signal': '一份信号，多种表达。',
           'library': '研究论文库',
           'libraryDesc': '按研究方向浏览，组合会议、年份与方法筛选。',
           'tabPapers': '文献',
           'tabDatasets': '数据集',
           'tabTools': '工具',
           'tabLearn': '学习资料',
           'search': '搜索论文、方法、主题…',
           'searchLabel': '搜索研究论文库',
           'availability': '开放状态',
           'anyStatus': '全部开放状态',
           'weightsOnly': '有预训练权重',
           'codeOnly': '有公开代码',
           'unreleased': '尚未公开',
           'year': '年份',
           'anyYear': '全部年份',
           'host': '权重托管',
           'anyHost': '全部托管平台',
           'sort': '排序',
           'newest': '最新优先',
           'ready': '权重优先',
           'az': '标题 A–Z',
           'reset': '重置筛选',
           'showing': '显示',
           'of': '/',
           'results': '条结果',
           'more': '显示更多论文',
           'empty': '没有符合当前条件的结果。',
           'emptyHint': '试试更宽泛的关键词，或重置筛选条件。',
           'officialCode': '代码',
           'unofficialCode': '非官方代码',
           'comingCode': '代码仓库 · 待发布',
           'note': '备注',
           'source': '采集方式 / 来源',
           'size': '规模',
           'download': '数据集',
           'W': '权重可下载',
           'R': '仓库内含权重',
           'C': '代码已公开',
           'U': '非官方实现',
           'S': '待发布',
           'N': '未发现公开代码',
           'original': '原文标题',
           'threads': '研究脉络',
           'threadsDesc': '串联文献的几条线索。',
           'tutorials': '教程与综述',
           'books': '书籍',
           'classic': '基础文献',
           'related_lists': '相关论文库',
           'toolRaw': 'RAW 读写',
           'toolIsp': '传统 ISP',
           'toolLearned': '神经 ISP',
           'toolEditor': 'RAW 编辑器',
           'about': '关于论文库',
           'aboutText': '每篇文献只有一个任务主分类；可控与移动端 / 高效 ISP '
                        '按能力与部署条件交叉归集。模型、训练方式、信号和控制接口独立筛选。挑战赛实现合并在对应报告下，不重复增加文献计数。代码与权重统计包含明确标识的第三方实现。',
           'dates': '文献更新',
           'checked': '代码与权重全面核验',
           'audit': '分别记录文献新增、摘要修订、分类调整与最近一次全面代码 / 权重核验的日期。标签与阅读笔记可追溯至论文原始来源。',
           'coverage': '这是一份精选索引，并非穷尽式综述；仅在期刊发表的工作与新发布的会议论文可能尚未收录。',
           'updateLog': '来源与更新记录',
           'footer': '共同绘制开放的计算成像地图。',
           'menu': '浏览主题',
           'language': 'English',
           'repo': 'GitHub',
           'otherHost': '其他平台',
           'breadcrumb': '精选论文目录',
           'index': '索引',
           'noscript': '开启 JavaScript 即可使用筛选；也可以阅读完整的静态 Markdown 论文库。',
           'focus': '跨任务研究',
           'classification': '分类依据',
           'advanced': '更多筛选',
           'active': '当前筛选',
           'clearOne': '移除筛选',
           'anyArchitecture': '全部模型类型',
           'anyControl': '全部控制接口',
           'anySupervision': '全部训练方式',
           'anySignal': '全部信号类型',
           'unlabeled': '尚未标注',
           'facetHelp': '标签描述原文有依据的组成部分；缺少标签表示尚未标注。相机条件化不等于交互式编辑。',
           'challenge': '针对的挑战',
           'method': '具体方法',
           'contribution': '主要贡献',
           'limits': '阅读提示 · 编者',
           'sourceLink': '论文原始来源',
           'implementation': '本报告收录的实现资源',
           'relatedDatasets': '相关数据集',
           'summaryDate': '摘要修订',
           'taxonomyDate': '分类复核',
           'taxonomyLog': '分类规则与完整审计',
           'summaryLog': '摘要修订记录',
           'paperCount': '独立文献',
           'unofficialWeights': '非官方代码与权重',
           'downloadWeights': '权重下载',
           'venue': '会议与期刊',
           'allVenues': '全部会议与期刊',
           'selectedVenues': '已选会议 / 期刊',
           'venueHelp': '可同时勾选多个，未选时显示全部。Workshop、Findings 和预印本与主会分别筛选。',
           'venuePreset': 'CVPR + ICCV + ECCV',
           'clearVenues': '清空会议筛选',
           'venueVision': '计算机视觉会议',
           'venueLearning': '机器学习与人工智能',
           'venueImaging': '图形学、成像与多媒体',
           'venueWorkshops': 'Workshop 与 Findings',
           'venueJournals': '期刊',
           'venuePreprints': '预印本',
           'venueOther': '其他发表场所'}}

def site(d, lang='en'):
    cfg = d['config']
    ui = UI[lang]
    repo = f"https://github.com/{cfg['owner']}/{cfg['repo']}"
    suffix = '.zh-CN' if lang == 'zh-CN' else ''
    ps = []
    status = {'weights': 'W', 'weights-in-repo': 'R', 'code': 'C', 'unofficial': 'U', 'coming-soon': 'S', 'no-code': 'N'}
    for cat, p in all_papers(d):
        meta = d['research'].get(p['name'], {})
        implementations = [dict(n=r['name'], s=r['tldr'], g=r.get('code', '')) for r in p.get('implementations', [])]
        ps.append(dict(id=paper_id(p), n=p['name'], t=p['title'], en=p.get('original_title', ''), ens=p.get('original_tldr', ''),
                       v=p['venue'], vk=venue_id(p['venue']), y=p['year'], c=cat['id'], s=display_summary(p, meta, lang), p=p['paper'],
                       g=next((r['code'] for r in resources(p) if r.get('code')), ''), st=status[release_status(p)], hw=has_weights(p), w=weights(p),
                       note=display_note(p.get('note', '')), impl=implementations,
                       facets={key: meta.get(key, []) for key in ('architecture','supervision','signal','control')},
                       collections=meta.get('collections', []), ds=meta.get('datasets', [])))
    facets = {key: dict(label=f['label'][lang], values={v:labels[lang] for v,labels in f['values'].items()}) for key,f in d['facets'].items()}
    venue_counts = Counter(venue_name(p['venue']) for _,p in all_papers(d))
    venue_priority = ['CVPR', 'ICCV', 'ECCV', 'WACV', 'BMVC', 'ACCV', 'NeurIPS', 'ICLR', 'AAAI', 'ACM MM', 'SIGGRAPH', 'SIGGRAPH Asia']
    venues = [dict(id=venue_id(v), title=v, group=venue_group(v), count=n) for v,n in sorted(
        venue_counts.items(), key=lambda row: (venue_priority.index(row[0]) if row[0] in venue_priority else len(venue_priority), -row[1], row[0]))]
    payload = dict(papers=ps, categories=d['categories'] + [dict(c, kind='collection') for c in d['collections']],
                   navigation=[dict(id=g['id'], label=g['label'][lang], topics=g['topics']) for g in d['navigation']],
                   venues=venues, facets=facets, datasets=d['datasets'], tools=d['tools'], trends=d['trends'], resources=d['resources'])
    counts = dict(NP=len(ps), NCODE=sum(has_code(p) for _,p in all_papers(d)), NW=sum(has_weights(p) for _,p in all_papers(d)), ND=len(d['datasets']))
    data_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    ui_json = json.dumps(ui, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    replacements = {**{k: str(v) for k, v in counts.items()}, **ui,
                    'LANG': lang, 'TITLE': 'Awesome Neural ISP' + (' · 中文' if suffix else ''),
                    'REPO': repo, 'GUIDE': f'{repo}/blob/main/guide/isp-101{suffix}.md',
                    'CONTRIBUTE': f'{repo}/blob/main/CONTRIBUTING{suffix}.md',
                    'README': f'{repo}/blob/main/README{suffix}.md',
                    'LOG': f'{repo}/blob/main/guide/literature-update-2026-10-28.md',
                    'CHECKED': cfg['checked'], 'UPDATED': cfg.get('literature_updated', cfg['checked']),
                    'SUMMARY_UPDATED': cfg['summary_updated'], 'TAXONOMY_UPDATED': cfg['taxonomy_updated'],
                    'TAXONOMY_LOG': f'{repo}/blob/main/guide/classification-2026-11-05{suffix}.md',
                    'SUMMARY_LOG': f'{repo}/blob/main/guide/summary-revision-2026-11-05.md',
                    'ALT': 'index.html' if suffix else 'zh-CN.html',
                    'DATA': data_json, 'UI': ui_json,
                    'STYLE': (ROOT / 'scripts/site_style.css').read_text(encoding='utf-8'),
                    'SCRIPT': (ROOT / 'scripts/site_script.js').read_text(encoding='utf-8')}
    template = (ROOT / 'scripts/site_template.html').read_text(encoding='utf-8')
    return re.sub(r'__([A-Za-z][A-Za-z0-9_]*)__',
                  lambda m: replacements[m[1]] if m[1] in ('DATA', 'UI', 'STYLE', 'SCRIPT') else html.escape(replacements[m[1]], quote=True), template)
