# Website design notes / 网页设计说明

References inspected in a desktop browser on **2026-10-28**:

- [Linear](https://linear.app/): strong typographic hierarchy, restrained borders, consistent spacing and persistent navigation within its product preview.
- [Anthropic Research](https://www.anthropic.com/research): generous whitespace, topic summaries and readable editorial organization of a large research collection.

参考页面已于 **2026-10-28** 在桌面浏览器中查看：Linear 的标题层级、细边框与导航组织，以及 Anthropic Research 的留白、主题概览和研究目录编排。
参考的是信息组织原则；没有复制页面素材或引入它们的脚本。

The library uses a quiet gray-blue palette, serif editorial headings and a compact sans-serif reading interface.
The small sensor → neural ISP → rendered-image diagram is built with local HTML/CSS. It is a schematic, not a photographic result or a model comparison.

页面使用灰蓝配色、衬线标题与清晰的无衬线阅读区域。传感器 → 神经 ISP → 渲染图像的小图以 HTML/CSS 绘制，仅用于说明流程，并非模型效果对比。

- Topic navigation groups the literature into whole-pipeline, restoration/capture, color/representation and systems/evaluation areas.
- One searchable library replaces separate long, overlapping paper and weight tables. Topic, release status, year and weight host combine; sorting supports newest, weights first and name.
- Search and filters are encoded in the URL and preserved across language changes. Chinese records retain original English titles for citation and search.
- Each view initially renders 24 papers, with an explicit “show more” control. Notes and all weight URLs remain available in expandable details.
- Datasets, tools and learning resources have their own views. Research trends remain visible below the library.
- Both HTML files embed data, styles and scripts: no CDN, font download, analytics or application server is required.
- Mobile navigation supports keyboard focus and Escape; controls have labels and visible focus; reduced-motion preferences are respected.

主题导航按完整管线、复原与采集、色彩与表示、系统与评测组织。统一检索同时组合主题、开放状态、年份与权重平台，支持最新、权重优先及名称排序。
筛选状态保存在 URL 中，切换语言仍保留；中文条目同时显示正式英文标题。每次先展示 24 篇，可继续展开；备注与全部权重链接保留在详情里。
数据集、工具和学习资料有独立视图。两份 HTML 均内嵌全部内容，无需 CDN、外部字体或服务端即可使用。
