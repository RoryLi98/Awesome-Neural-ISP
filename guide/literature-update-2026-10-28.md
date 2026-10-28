# Literature refresh / 文献更新 · 2026-10-28

[English index](../README.md) · [中文目录](../README.zh-CN.md)

This refresh adds **4 papers**, moves **9 existing entries** without duplication, and corrects publication metadata.
The library now contains **419 papers, 205 with public code, 132 with pretrained weights, and 29 datasets**.
It is a targeted literature refresh, not a fresh audit of every existing download link.
`literature_updated` is **2026-10-28**; the last full code/weight audit (`checked`) remains **2026-10-11**.

本次新增 **4 篇论文**，重新归类 **9 条已有记录**，并修订部分出版信息，没有重复计数。
目录现包含 **419 篇论文、205 项公开代码、132 项预训练权重与 29 个数据集**。
这是针对近期文献与分类的更新；没有将全部旧链接的核验日期改成今天。
文献更新日期为 **2026-10-28**，最近一次全面代码／权重核验日期仍为 **2026-10-11**。

## New entries / 新增条目

| Paper / 论文 | Primary category / 主分类 | Verified sources and release status / 核验来源与开放状态 |
|:--|:--|:--|
| **RIECR** — Unified RAW Image Exposure Correction and Restoration via Linear Illumination and Frequency-Adaptive Enhancement | Low-light RAW / 弱光 RAW 与曝光复原 | [arXiv, submitted 2026-10-20](https://arxiv.org/abs/2610.28191), [full text](https://arxiv.org/html/2610.28191v1), [author repository](https://github.com/yingkai-zhang/RIECR). The repository description labels ACAIT 2026, but its tree contains only `README.md`; marked **coming-soon**, without claiming code or weights are available. 仓库仅有 README，标记“待发布”；正式会议出版信息未独立确认，暂以 arXiv 收录。 |
| **Neural Block-wise Auto-exposure** — Neural Block-wise Auto-exposure for Single-Shot High Dynamic Range Imaging | Burst & HDR / 连拍与 HDR | [arXiv](https://arxiv.org/abs/2610.18733), [revised full text, 2026-10-16](https://arxiv.org/html/2610.18733v2). Predicts exposure for 16 × 16 sensor blocks and compares RAW/sRGB previews. No official implementation or checkpoint link found in the paper or repository search; marked **no-code**. 依据预览图预测分块曝光，未发现公开实现或权重。 |
| **EMOVIS** — Emotion-Optimized Image Processing | ISP Parameter Tuning / ISP 参数调优 | [arXiv](https://arxiv.org/abs/2605.03131), [ICIP 2026 DOI](https://doi.org/10.1109/ICIP61757.2026.11630415), [official repository](https://github.com/dorbarber79/EMOVIS). README and source tree include the RAW pipeline (`emovis/isp.py`, `process.py`). Marked **code**. This is a conventional, training-free control baseline; it is not labeled a neural model and needs no learned checkpoints. 传统 ISP 的情绪控制基线，代码已公开，不把无需训练的参数表计为模型权重。 |
| **PQDynamicISP** — Dynamically Controlled Image Signal Processor for Any Image Sensors Pursuing Perceptual Quality | ISP Parameter Tuning / ISP 参数调优 | [arXiv, 2024](https://arxiv.org/abs/2403.10091), [full text](https://arxiv.org/html/2403.10091v1). An older omission found while checking the boundary of “controllable.” Predicts image-dependent global/local ISP parameters; no official implementation found. 补充分类梳理中发现的 2024 年遗漏工作；自动条件化预测不等同于面向用户的编辑界面。 |

Availability statements describe what was found on **2026-10-28**, not a guarantee that code does not exist elsewhere.
No weights were downloaded or executed. New dataset claims inside papers were not turned into downloadable dataset entries when no release was verified.

上述开放状态表示 **2026-10-28** 的检索与核验结果，并不保证其他位置不存在代码。
权重文件未下载或运行。论文中提出、但未确认已发布下载入口的数据集没有作为“可下载数据集”新增。

## Controllable Neural ISP / 可控神经 ISP

The existing list already contained relevant work, but it was split between end-to-end and low-light processing.
The new category is a **primary home for five existing papers**, with two explicit kinds of control:

已有目录并非没有相关论文，而是分散在端到端与弱光处理分类。新专题集中收录以下 **5 篇已有论文**，并明确区分两类控制：

| Work / 工作 | Control interface / 控制方式 | Primary evidence / 一手依据 |
|:--|:--|:--|
| CtrlISP | User-guided brightness/style through cascaded differentiable modules / 通过级联可微模块控制弱光图像的亮度与风格 | [CVPR 2026 Findings paper](https://openaccess.thecvf.com/content/CVPR2026F/html/Zhang_CtrlISP_Rescuing_Low-Light_RAW_Images_via_Controllable_Neural_ISP_CVPRF_2026_paper.html) |
| Modular Neural ISP | Replaceable learned stages, explicit editing controls, picture styles and repeated rendering / 可替换的学习模块、交互编辑、图像风格与重复渲染 | [paper](https://arxiv.org/abs/2512.08564), [official implementation and GUI](https://github.com/mahmoudnafifi/modular_neural_isp) |
| ParamISP | EXIF parameters condition forward/inverse ISP networks; not inherently a GUI / EXIF 参数条件化正向与逆向网络，不等同于交互编辑器 | [paper](https://arxiv.org/abs/2312.13313), [official code](https://github.com/woo525/ParamISP) |
| MetaISP | Device/style selection, metadata and device-style interpolation / 设备与风格选择、元数据条件化及设备风格插值 | [official README](https://github.com/vccimaging/MetaISP): `--infedev`, `--iso_exp`, `--latent`, `--latent_n` inference controls |
| Uni-ISP | Device-aware embeddings unify forward/inverse camera rendering / 用设备感知嵌入统一多相机正向与逆向成像 | [paper and journal reference](https://arxiv.org/abs/2406.01003), [TIP DOI](https://doi.org/10.1109/TIP.2025.3607617) |

Related work stays in the category that best describes its main contribution:

- **NILUT, white-balance editing:** color modules, under White Balance, Color & Tone.
- **Edit-aware RAW reconstruction:** inverse imaging, under Inverse ISP.
- **PQDynamicISP, EMOVIS and automatic tuning:** parameter tuning or conventional control.
- **POS-ISP:** moved from tuning to ISP for Machine Vision, because downstream task rewards drive sequence optimization. [Paper](https://arxiv.org/abs/2604.06938).
- **RAW vs RGB Restoration Benchmark, Reference-free ISP Evaluation, Small-Pixel Neural ISP:** moved from end-to-end methods to Challenges & Surveys, which also covers benchmarks, evaluation and imaging studies. [Restoration benchmark](https://arxiv.org/abs/2609.02831), [reference-free evaluation](https://arxiv.org/abs/2607.23321), [small-pixel study](https://arxiv.org/abs/2606.07675).

相邻工作按主要贡献保留或调整：NILUT／白平衡编辑属于颜色模块，编辑感知 RAW 重建属于逆向成像；自动参数预测与传统用户控制属于参数调优。
POS-ISP 的序列优化由下游任务奖励驱动，因此从调优移至机器视觉。
RAW/RGB 复原比较、无参考 ISP 评测与小像素时代研究属于基准、评测或成像实验研究，移入同时覆盖这些内容的“挑战赛与综述”类。

## Metadata corrections / 元数据修订

- **Modular Neural ISP:** changed from arXiv 2025 to **SIGGRAPH Asia 2026**, based on the official repository's acceptance announcement and BibTeX. The 2025 arXiv identifier is retained. The official `denoising/models` and `photofinishing/models` directories still list `.pth` checkpoints.
- **Uni-ISP:** changed the journal year from 2024 to **2025**. arXiv explicitly records *IEEE Transactions on Image Processing*, vol. 34, pp. 6126–6137, 2025. The original preprint remains dated 2024.
- **Small-Pixel Neural ISP:** corrected the summary to describe its controlled simulations across five pixel sizes and low-SNR multi-frame experiments, and restored the full official subtitle, “How Shrinking Pixels Push Optics to the Limit and Neural Restoration Pushes Back.”

Modular Neural ISP 根据官方接收公告与引用信息更新为 **SIGGRAPH Asia 2026**，仍保留最初的 arXiv 链接；两处模型目录的检查点文件列表仍存在。
Uni-ISP 根据 arXiv 中的期刊记录修正为 **TIP 2025**，避免把预印本年份当成期刊年份。
小像素研究补回完整副标题，并将摘要修订为对受控模拟与多帧实验的具体描述。

## Search scope / 检索范围

Searches used reverse-chronological arXiv title/abstract results for `neural ISP`, `controllable ISP`,
`image signal processing`, `image signal processor`, `RAW-to-sRGB`, `RAW image`, `RAW exposure` and `ISP`.
Candidate papers were compared against existing entries, then checked on arXiv, CVF and official repositories.
GitHub repository searches helped locate implementations; repository trees distinguish placeholders from released code.
This does not claim exhaustive coverage of all 2026 conferences or journals. RAW-domain 3D Gaussian splatting,
unrelated ISP networking papers and generic sRGB enhancement were excluded from this update.

检索使用上述关键词按时间倒序筛选 arXiv，先与已有记录去重，再核对 arXiv、CVF 与官方仓库。
GitHub 仓库搜索用于发现实现，并检查文件树以区别占位仓库与实际代码。
此次更新不宣称穷尽所有 2026 年会议及期刊；RAW 域 3D Gaussian splatting、网络服务商领域的 ISP 论文与一般 sRGB 增强未纳入。
