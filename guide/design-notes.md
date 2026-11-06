# Website design notes / 网页设计说明

Reference pages inspected on **2026-10-28**: [Linear](https://linear.app/) for typography, restrained borders and navigation; [Anthropic Research](https://www.anthropic.com/research) for organizing research content. These are information-design references, not copied assets or scripts.

**2026-10-28** 查看了 [Linear](https://linear.app/) 的字体层级、细边框与导航，以及 [Anthropic Research](https://www.anthropic.com/research) 的研究内容组织。参考信息设计原则，没有复制素材或脚本。

## Current layout · 2026-11-05 / 当前布局

- A compact introduction replaces the tall hero and imaging illustration. Metrics lead directly into search and results; collection shortcuts do not repeat above the library.
- The sidebar has four stable research groups: full ISP/controllable imaging, restoration/multi-frame imaging, color/RAW representation, and vision tasks/system optimization. Controllable ISP appears with full pipelines; mobile/efficient ISP appears with system optimization. Every existing navigation entry appears once, without collection badges or a mixed popularity ranking. Counts retain total coverage; primary publication assignments remain unchanged.
- The full official English title is the heading in both languages; Chinese translations appear underneath. Search aliases remain internal.
- Each card has one wrapping metadata line (year, venue, task, model/control/training/signal tags and release status), the full linked title, a full-width prose summary, and a compact wrapping resource line. Tags share the first line whenever space permits; frameworks and duplicate Paper/Copy-link actions are removed.
- A checkbox venue picker allows any combination, with a CVPR + ICCV + ECCV shortcut. Selected venues are ORed; task/year/method filters are ANDed. Workshop and Findings tracks remain separate from main conferences; journals and arXiv have their own groups. Each venue has a removable chip. Selections survive reloads, language changes and task navigation. The panel closes on outside click or Escape and fits desktop/mobile widths.
- Search stays visible while scrolling. Removable filter chips show active conditions; less common filters and classification explanations expand on demand.
- Challenge, mechanism and contribution are explained in continuous prose, without repeating the short summary in a labeled reading table. The newest 24 entries have expanded bilingual abstracts; 13 other entries reuse the substantive content of their existing bilingual reading notes. The code link sits immediately after release status in the metadata line; the pair wraps together. All weights and related datasets share the resource line, which is omitted when empty. Availability caveats remain, with audit timestamps retained only in source data and audit records.
- URL parameters preserve topic, facets, search and language state. Stable per-publication links open a single record; implementation aliases resolve to their parent report through search.
- Datasets, tools and learning resources remain separate searchable views. The page renders 24 publications initially and supports progressive disclosure.
- Both HTML files embed all data, styles and scripts. No CDN, remote font, analytics or application server is required.
- Responsive checks cover 320, 390, 768, 1024 and 1440 px. Navigation supports keyboard focus and Escape; controls have accessible names, visible focus and reduced-motion handling.

- 用简洁页头替代高大首屏与流程插图；统计之后直接进入检索与结果，顶部不再重复专题入口。
- 左侧按四个稳定大类分组：完整 ISP 与可控成像、图像复原与多帧成像、色彩处理与 RAW 表示、视觉任务与系统优化。可控 ISP 放在完整管线旁，移动端 / 高效 ISP 放在系统优化组。保留全部导航入口且各出现一次，移除“专题”角标和混排的热门排序；数字仍表示总收录量，论文主分类不变。
- 中英文统一以正式英文标题为主标题，中文版附辅助译名；旧检索别名只作内部标识。
- 每张卡片依次展示紧凑元数据行（年份、会议、任务、模型/控制/训练/信号标签及开放状态）、可点击的正式标题、全宽连贯摘要、紧凑资源行。宽度允许时标签同处首行，空间不足时自然换行；移除实现框架、重复“论文”入口和复制链接。
- 会议 / 期刊支持复选框多选，提供 CVPR + ICCV + ECCV 快捷组合；多个发表场所取并集，与任务、年份、方法等条件取交集。Workshop、Findings 与主会分开，期刊和 arXiv 单列；各项可独立移除，刷新、切换语言和切换分类保留所选条件。面板支持点击外部或 Escape 关闭，并适配桌面与手机。
- 搜索在滚动时保持可见；筛选条件可逐项移除，较少使用的条件和分类依据按需展开。
- 挑战、机制和贡献用连贯正文说明，取消重复短摘要的标签式阅读表格。最新 24 条扩写双语摘要，另 13 条整合已有双语阅读笔记的实质内容。代码链接紧随首行开放状态，二者作为一组换行；全部权重和关联数据集在资源行自然排列，无资源时不生成空行；保留下载限制等使用备注，核验时间留在源数据与审计记录中。
- URL 保留主题、标签、关键词与语言状态；每篇文献有固定链接，参赛实现别名可以检索到所属报告。
- 数据集、工具与学习资料独立检索；首次展示 24 篇，再按需增加。
- 两份 HTML 内嵌数据、样式与脚本，无 CDN、远程字体、统计脚本或服务端依赖。
- 检查 320、390、768、1024、1440 像素宽度，支持键盘焦点、Escape、可访问名称与减少动画偏好。

Taxonomy decisions and full bilingual audit / 分类依据与双语完整审计：[English](classification-2026-11-05.md) · [中文](classification-2026-11-05.zh-CN.md)。

Navigation groups are configured in `data/navigation.yaml` and validated to cover each of the 15 primary tasks and two cross-task views exactly once. Group headings organize browsing; they do not introduce duplicate publications or imply that cross-task membership is a mutually exclusive task. Venue normalization uses the stored `venue` field, preserving original labels on paper cards. It groups workshop-name variants such as CVPRW (NTIRE/MAI/MIPI), AAAI oral papers and SIGGRAPH/TOG conference variants without inferring publication venue from an arXiv URL.

导航大类由 `data/navigation.yaml` 定义，构建检查 15 个任务主分类与 2 个跨任务入口恰好各出现一次。分组只组织浏览，不增加重复文献，也不把跨任务能力误作互斥任务。会议归一化依据已存储的 `venue`，卡片保留原始发表信息：合并 CVPRW (NTIRE/MAI/MIPI)、AAAI Oral 与 SIGGRAPH/TOG 会议名称变体，但不根据 arXiv 链接推断发表场所。
