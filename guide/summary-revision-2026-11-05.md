# Paper summaries and layout / 论文总结与排版 · 2026-11-05

[English library](../README.md) · [中文论文库](../README.zh-CN.md) · [Previous literature refresh / 前次文献更新](literature-update-2026-10-28.md)

**Subsequent classification audit / 后续分类复核：** The 419 summaries now describe 417 unique publications and two nested challenge implementations; 133 publications have linked weights, including one explicitly labeled third-party implementation. / 419 条总结对应 417 篇独立文献与两项合并保留的参赛实现；133 篇有权重，其中 1 篇为明确标识的第三方实现。See / 详见 [English classification audit](classification-2026-11-05.md) · [中文分类审计](classification-2026-11-05.zh-CN.md)。

All **419 English summaries and 419 Chinese summaries** were rewritten around the research challenge, specific method and concrete contribution. Architecture names are taken from the abstract, paper or official project; reports and datasets describe their protocols and data contributions. This is a summary/metadata revision, not a new literature search or full checkpoint-link audit. The previous literature and full-link-audit dates are retained.

本次按“挑战、具体方法、贡献”改写 **419 条英文总结及对应的 419 条中文总结**。结构名称依据摘要、论文或官方项目，报告和数据集则说明协议与数据贡献。本次是总结和元数据修订，保留此前文献增补及全面链接核验日期。

The website and both Markdown editions now lead with full official English titles. The Chinese edition adds reading translations. Internal search aliases are retained as stable keys, without being displayed as paper headings. Compact metadata and full-width summaries replace the separate right column and duplicate nickname/title lines.

网页与中英文 Markdown 均使用正式完整英文标题，中文版另附辅助译名。内部搜索别名保留为稳定标识，不再作为论文标题。元数据合为紧凑一行，总结使用完整宽度，取消独立右栏和重复简称行。

## Source checks / 来源核对

Existing paper links were the starting point. arXiv and CVF abstracts supplied most method descriptions; official projects supplied implementation-specific details. Where publisher pages were unavailable, DOI metadata and indexed publisher abstracts were cross-checked through Crossref/OpenAlex. Full-paper reading was targeted to ambiguities; this revision does not claim full-text replication of every paper.

以现有论文链接为起点，主要依据 arXiv、CVF 摘要及官方项目。出版商页面无法访问时，通过 Crossref/OpenAlex 交叉核对 DOI 元数据及收录的出版商摘要；有歧义时查正文，不声称已逐篇复现或通读全部论文。

| Corrected or expanded record / 修订条目 | Evidence / 依据 |
|:--|:--|
| 2-Shots in the Dark: Low-Light Denoising with Minimal Data Acquisition | [Abstract](https://arxiv.org/abs/2512.03245): one noisy image and one dark frame **per ISO**, Poisson shot noise and Fourier spectral sampling. / 每个 ISO 一张噪声图和一张暗帧，泊松散粒噪声与傅里叶频谱采样。 |
| RMFA-Net: A Neural ISP for Real RAW to RGB Image Reconstruction | [Abstract](https://arxiv.org/abs/2406.11469): implicit black-level correction, three-channel split and Retinex tone mapping; replaces the inaccurate “multi-frequency attention fusion” summary. / 修正原有“多频注意力融合”描述。 |
| NODE: Extreme Low Light Raw Image Denoising using a Noise Decomposition Network | [Abstract](https://arxiv.org/abs/1909.05249) explicitly distinguishes defective-pixel, Gaussian and Poisson noise; the earlier signal-dependent/independent description was insufficient. / 摘要明确分别处理坏点、Gaussian 与 Poisson 噪声。 |
| Make Explicit Calibration Implicit: Calibrate Denoiser Instead of the Noise Model | [arXiv](https://arxiv.org/abs/2308.03448): uses the linked paper's current formal title for the LED record. / LED 使用所链接文献的正式标题。 |
| MW-ISPNet and MWRCANet solution records | Their publications are challenge reports. Headings now use those reports' official titles; summaries identify the specific solutions. / 使用挑战报告正式标题，在总结中说明具体方案。 |
| EvRAW: Event-guided Structural and Color Modeling for RAW-to-sRGB Image Reconstruction | [DOI](https://doi.org/10.1145/3746027.3754983), [indexed publisher abstract](https://api.openalex.org/works/https://doi.org/10.1145/3746027.3754983): event-motion structural enhancement and region/channel color correction. |
| Camera-Specific Imaging Simulation for Raw Domain Image Super Resolution | [DOI](https://doi.org/10.1145/3746027.3754785): subgraph-decomposed simulation and LatentKAN with stagewise feature fusion. |
| Prior Metadata-Driven RAW Reconstruction: Eliminating the Need for Per-Image Metadata | [DOI](https://doi.org/10.1145/3664647.3680819): compact offline reference pool, pixel search and neural reconstruction; replaces a generic camera-metadata description. |
| Generalizing ISP Model by Unsupervised Raw-to-raw Mapping | [DOI](https://doi.org/10.1145/3664647.3681666), [official implementation](https://github.com/ydxxxx/Unsupervised-Raw-to-raw-Mapping): CSTPP and CycleGAN-style learning. Public-code count corrected to **206** after checking the official README. / 核对官方 README 后公开代码数量修正为 **206**。 |
| Neural Photo-Finishing | [DOI](https://doi.org/10.1145/3550454.3555526): separate neural proxies for legacy finishing stages. |
| Hyperparameter Optimization in Black-box Image Processing using Differentiable Proxies | [DOI](https://doi.org/10.1145/3306346.3322996): predicts evaluation metrics from configurations, rather than necessarily reproducing every image-processing stage. / 直接学习配置到指标的映射。 |
| Lookup Table meets Local Laplacian Filter: Pyramid Reconstruction Network for Tone Mapping | [Official project](https://github.com/fengzhang427/LLF-LUT): low-resolution Transformer weight prediction plus learned local Laplacian filtering; existing weights still refer to the TPAMI extension. |
| MIPI 2024 Challenge on Demosaic for HybridEVS Camera: Methods and Results | [PDF, pages 1–2](https://arxiv.org/pdf/2405.04867): the webpage abstract mentions a different track; the PDF verifies HybridEVS demosaicing, event/defect-pixel correction and 800 training pairs. / 网页摘要误提其他赛道，按 PDF 正文核对。 |

Validation uses the strict bilingual build plus browser checks for full titles, title sorting, filters, language state, downloads, offline use and horizontal overflow at desktop/tablet/mobile widths. Downloadable checkpoints were not executed as part of editorial revision.

验证采用严格双语构建及浏览器检查，覆盖完整标题、按标题排序、筛选、语言状态、下载、离线使用及桌面/平板/手机宽度溢出。

## Expanded website abstracts / 网页摘要扩写

The latest 24 publications in the default year/title ordering now have longer English and Chinese editorial abstracts in `data/research.yaml`, each linked to its primary source through `summary_source`. The expansions explain the challenge, what each named mechanism does, and the contribution without adding unsupported architecture or performance claims. Another 13 publications integrate the challenge/method/contribution content of existing reading notes into prose, for 37 longer website entries in total. The remaining publications retain their previously revised summaries; the compact Markdown summaries are unchanged by this pass. The 15 original structured reading-note records, including editorial limitations, remain available in source data.

默认按年份与标题排序的最新 24 篇文献，已在 `data/research.yaml` 中补充中英文长摘要，并用 `summary_source` 记录论文原始来源。扩写解释研究挑战、具体机制的作用和贡献，不补造结构或性能结论。另 13 篇将已有阅读笔记中的挑战、方法、贡献整合成连贯正文，网页共 37 篇使用较长摘要。其余条目保留此前改写的总结，Markdown 的精简摘要本轮不变。15 篇原有结构化阅读笔记及编者限制说明保留在源数据中。

Card metadata and all documented tags share one naturally wrapping line. The title is the only paper link; code, all weights and related datasets occupy a compact resource row. Framework labels, Paper/Copy-link actions, repeated reading tables and per-card audit timestamps are removed. Download caveats and their dated source records are preserved. Both languages use the same layout.

卡片元数据和已核实标签放在同一行并自然换行，标题直接链接论文；代码、全部权重及关联数据集使用紧凑资源行。移除框架标签、重复论文入口、复制链接、重复阅读表格和卡片内核验日期，保留下载限制及源数据中的日期记录。中英文使用同一布局。
