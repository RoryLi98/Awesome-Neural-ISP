"""Chinese Markdown exports, using the same records and links as the English edition."""
from __future__ import annotations

from isp_data import WEIGHT_STATUSES


def code(p, link, md):
    if not p.get('code'):
        return '待发布' if p['status'] == 'coming-soon' else '—'
    label = {'unofficial': '非官方代码', 'coming-soon': '代码仓库（待发布）'}.get(p['status'], '代码')
    return link(label, p['code']) + (f"<br><sub>{md(p['framework'])}</sub>" if p.get('framework') else '')


def paper(p, link, md):
    text = f"**{link(p['name'], p['paper'])}**<br>{md(p['title'])}"
    if p.get('original_title') and p['original_title'] != p['title']:
        text += f"<br><sub>{md(p['original_title'])}</sub>"
    text += f"<br><sub>{md(p['tldr'])}"
    if p.get('note'):
        text += f" <i>备注：{md(p['note'])}</i>"
    return text + '</sub>'


def readme(d):
    from build import GENERATED, link, md, slug, sort_papers, stats, weights_cell
    cfg, cats, s = d['config'], d['categories'], stats(d)
    pages = (cfg.get('site') or f"https://{cfg['owner']}.github.io/{cfg['repo']}/").rstrip('/') + '/zh-CN.html'
    ref = {c['id']: f"[{c['short']}](#{slug(c['title'])})" for c in cats}
    L = [GENERATED, '', '# Awesome Neural ISP · 中文', '', '[English](README.md) · **简体中文**', '',
         f"**{cfg['tagline']}**", '',
         f"[交互式论文库]({pages}) · [预训练权重索引](WEIGHTS.zh-CN.md) · [ISP 入门](guide/isp-101.zh-CN.md) · [贡献指南](CONTRIBUTING.zh-CN.md)", '',
         '这份目录覆盖完整神经 ISP、RAW 图像复原、颜色与色调处理、可控渲染、逆向 ISP、机器视觉成像与参数调优。'
         '每篇论文记录公开代码和预训练权重状态，权重链接以官方仓库为依据。中文标题为阅读辅助译名，同时保留正式英文标题与方法名，便于检索和引用。', '',
         f"目前共 **{s['n']} 篇论文**，其中 **{s['code']} 篇有公开代码**（含非官方实现），**{s['weights']} 篇提供预训练权重**，另有 **{s['datasets']} 个数据集**。", '',
         f"文献更新：**{cfg.get('literature_updated', cfg['checked'])}**；最近一次全面代码与权重链接核验：**{cfg['checked']}**。"
         '新增条目另行核验，详见[来源与更新记录](guide/literature-update-2026-10-28.md)。', '',
         '**表格说明。** 各分类内先列有权重的论文，再列仅有代码或未公开代码的论文；各组按年份降序排列。'
         '“仓库内”表示检查点直接保存在仓库中；“非官方”表示第三方实现；“待发布”表示占位仓库或尚未发布实现；“—”表示未发现公开代码。', '',
         '## 目录', '', '- [ISP 入门](#isp-入门)', '- [研究脉络](#研究脉络)', '- [论文](#论文)']
    for c in cats:
        ps = d['papers'][c['id']]
        nw = sum(p['status'] in WEIGHT_STATUSES for p in ps)
        L.append(f"  - [{c['title']}](#{slug(c['title'])})（{len(ps)} 篇，{nw} 篇有权重）")
    L += ['- [数据集](#数据集)', '- [工具与开源 ISP](#工具与开源-isp)', '- [学习资料](#学习资料)',
          '- [相关目录](#相关目录)', '- [贡献](#贡献)', '- [关于本目录](#关于本目录)', '- [许可](#许可)', '',
          '## ISP 入门', '', '传感器记录带噪声的线性马赛克信号，每个像素只感知一种颜色；ISP 将其变成可直接显示的图像。'
          '[完整指南](guide/isp-101.zh-CN.md)逐步介绍这些阶段，并提供可运行的 [NumPy 简易管线](guide/minimal_isp.py)。', '',
          '```mermaid', 'flowchart LR',
          '    S[传感器 RAW] --> B[黑电平] --> N[去噪] --> W[白平衡] --> D[去马赛克] --> C[颜色矩阵] --> T[色调与伽马] --> O[sRGB]', '```', '',
          '| 传统阶段 | 作用 | 相关研究 |', '|:--|:--|:--|',
          '| 黑电平、坏点、镜头阴影 | 消除传感器偏移与光学衰减 | 通常保留传统方法 |',
          f"| 去噪 | 去除泊松–高斯传感器噪声 | {ref['denoise']} · {ref['lowlight']} · {ref['burst']} · {ref['video']} |",
          f"| 去马赛克 | 插值重建每个像素缺失的两个颜色通道 | {ref['demosaic']} |",
          f"| 白平衡、颜色校正、色调与伽马 | 校正光源颜色并映射至显示空间 | {ref['color']} |",
          f"| 完整管线 | RAW 输入，sRGB 输出 | {ref['e2e']} · {ref['mobile']} |",
          f"| 可控渲染 | 暴露编辑参数、相机条件或可替换模块 | {ref['controllable']} |",
          f"| 逆向管线 | 从 sRGB 重建 RAW | {ref['inverse']} |",
          f"| 面向机器的输出 | 服务检测、分割等任务 | {ref['task']} |",
          f"| ISP 参数 | 自动优化与传统控制基线 | {ref['tuning']} |", '', '## 研究脉络', '']
    for t in d['trends']:
        L.append(f"- **{t['title']}。** {t['text']} <sub>代表工作：{md(t['examples'])}</sub>")
    L += ['', '## 论文', '']
    for c in cats:
        ps = sort_papers(d['papers'][c['id']])
        L += [f"### {c['title']}", '', c['description'], '']
        for with_weights, heading in [(True, '提供预训练权重'), (False, '仅有代码或尚未公开')]:
            group = [p for p in ps if (p['status'] in WEIGHT_STATUSES) == with_weights]
            if not group:
                continue
            L += [f'**{heading}（{len(group)}）**', '',
                  '| 论文 | 发表信息 | 代码 |' + (' 权重 |' if with_weights else ''),
                  '|:--|:--|:--|' + (':--|' if with_weights else '')]
            for p in group:
                row = f"| {paper(p, link, md)} | {md(p['venue'])} {p['year']} | {code(p, link, md)} |"
                L.append(row + (f' {weights_cell(p)} |' if with_weights else ''))
            L.append('')
        L += ['[返回目录](#目录)', '']
    L += ['## 数据集', '', '| 数据集 | 年份 | 采集方式 | 规模 | 用途 | 链接 |', '|:--|:--|:--|:--|:--|:--|']
    for x in sorted(d['datasets'], key=lambda x: ([c['id'] for c in cats].index(x.get('task', 'e2e')), -x['year'])):
        L.append(f"| **{md(x['name'])}**<br><sub>{md(x.get('source'))}</sub> | {x['year']} | {md(x.get('capture'))} | {md(x.get('size'))} | {md(x['use'])} | [数据集]({x['url']}) |")
    L += ['', '## 工具与开源 ISP', '']
    for kind, label in [('raw', 'RAW 读写'), ('isp', '传统 ISP 管线与算法'), ('learned', '神经 ISP 工具箱'), ('editor', 'RAW 编辑器')]:
        items = [t for t in d['tools'] if t.get('kind', 'isp') == kind]
        if items:
            L += [f'**{label}**', '']
            L += [f"- {link(t['name'], t['url'])}：{t['description']}" + (f" <sub>{md(t['language'])}</sub>" if t.get('language') else '') for t in items]
            L.append('')
    L += ['## 学习资料', '']
    for key, label in [('tutorials', '教程与综述'), ('books', '书籍')]:
        L += [f'**{label}**', '']
        L += [f"- {link(x['name'], x['url'])} — {x['by']}。{x['description']}" for x in d['resources'][key]]
        L.append('')
    L += ['**各阶段的经典文献**', '']
    for g in d['resources']['classic']:
        L += [f"- {g['stage']}"]
        L += [f"  - {link(x['name'], x['url'])} — {x['by']}" for x in g['items']]
    L += ['', '## 相关目录', '']
    L += [f"- {link(x['name'], x['url'])}：{x['description']}" for x in d['resources']['related_lists']]
    L += ['', '## 贡献', '', '欢迎补充遗漏论文、新发布权重或失效链接。英文源数据位于 [`data/`](data/)，中文译文位于 '
          '[`data/i18n/`](data/i18n/)。中英文 README、权重索引与网页统一生成。条目格式、分类边界和维护方式见[贡献指南](CONTRIBUTING.zh-CN.md)。', '',
          '## 关于本目录', '', '**收集方式。** 初始目录筛选了 CVF Open Access 的 CVPR、ICCV、WACV 及 NTIRE、Mobile AI、MIPI、AIM 等工作坊，'
          '并参考 ECVA、NeurIPS、arXiv 关键词搜索与相关论文目录。此次更新复查近期 RAW/ISP 论文及官方代码仓库，'
          '具体来源和变更见[更新记录](guide/literature-update-2026-10-28.md)。', '',
          f"**代码与权重。** 全面仓库核验日期为 {cfg['checked']}，新增或修订条目的核验日期在备注或更新记录中注明。"
          '权重链接及网盘提取码来自官方说明；未下载或运行检查点。托管文件可能变化，权重仍受各作者许可约束。', '',
          '**覆盖范围。** 本目录不是穷尽式综述；新近会议论文和仅在期刊发表的工作可能遗漏。通常不收录仅在 sRGB 上评测的通用复原骨干、'
          '完全不涉及 RAW 的一般去噪或弱光增强、RAW 域 NeRF/3DGS，以及多光谱或偏振去马赛克。与 ISP 成像直接相关的颜色模块与传统控制基线会保留并注明定位。', '',
          '## 许可', '', '本目录以 [CC0 1.0](LICENSE) 发布。在法律允许范围内，贡献者放弃本目录的著作权及相关权利；所链接论文、代码和模型仍适用各自许可。', '']
    return '\n'.join(L)


def weights_md(d):
    from build import GENERATED, link, md, sort_papers, stats, weights_cell
    L = [GENERATED, '', '# 预训练权重索引', '', '[English](WEIGHTS.md) · [中文论文目录](README.zh-CN.md)', '',
         f"收录提供预训练权重的 **{stats(d)['weights']} 篇论文**，按主题归类。链接来自官方仓库，最近一次全面核验日期为 "
         f"{d['config']['checked']}；新增与修订项的检查时间见备注或[更新记录](guide/literature-update-2026-10-28.md)。权重文件未下载或运行。", '']
    for c in d['categories']:
        ps = [p for p in sort_papers(d['papers'][c['id']]) if p['status'] in WEIGHT_STATUSES]
        if not ps:
            continue
        L += [f"## {c['title']}", '', '| 模型 | 发表信息 | 权重 | 代码 | 框架 |', '|:--|:--|:--|:--|:--|']
        for p in ps:
            note = f"<br><sub>{md(p['note'])}</sub>" if p.get('note') else ''
            L.append(f"| **{link(p['name'], p['paper'])}**{note} | {md(p['venue'])} {p['year']} | {weights_cell(p)} | {code(p, link, md)} | {md(p.get('framework') or '—')} |")
        L.append('')
    return '\n'.join(L)
