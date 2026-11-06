# 贡献指南

[English](CONTRIBUTING.md) · [返回中文目录](README.zh-CN.md)

感谢你帮助完善论文目录并维护有效链接。所有条目均保存在 [`data/`](data/) 下的 YAML 文件中；`README.md`、`README.zh-CN.md`、权重索引和 `docs/` 中的交互网页由这些数据生成，**请不要直接修改生成的文件**。

## 快速开始

1. Fork 本仓库并创建分支。
2. 修改 `data/papers/` 下相应的分类文件，文件选择见下表。
3. 同步 `data/i18n/` 中对应的中文内容。论文正式英文标题仍保留在英文源数据中，中文标题是辅助阅读的译名。
4. 安装依赖，重新生成并验证：

   ```bash
   pip install -r requirements.txt
   python scripts/build.py
   python scripts/check_research.py
   python scripts/build.py --check
   ```

5. 一并提交 YAML 源数据、译文和重新生成的中英文文档、网页，然后发起拉取请求。CI 会执行 `python scripts/build.py --check`；数据不合法或生成文件未同步时，检查将失败。

不方便提交 PR，也可以通过 [添加论文](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=add-paper.yml) 或 [报告失效链接](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=broken-link.yml) 表单提交 issue。

## 应该修改哪个文件？

| 文件 | 分类 |
|:--|:--|
| `data/papers/e2e.yaml` | 端到端 RAW→sRGB |
| `data/papers/denoise.yaml` | RAW 去噪与噪声建模 |
| `data/papers/lowlight.yaml` | 弱光成像与曝光校正 |
| `data/papers/demosaic.yaml` | 去马赛克与重马赛克 |
| `data/papers/restoration.yaml` | RAW 去模糊与其他复原 |
| `data/papers/super-resolution.yaml` | RAW 超分辨率与重采样 |
| `data/papers/burst.yaml` | 连拍融合与 HDR 成像 |
| `data/papers/video.yaml` | RAW 视频 |
| `data/papers/white-balance.yaml` | 白平衡与颜色恒常性 |
| `data/papers/color.yaml` | 颜色校正、色调与修图 |
| `data/papers/inverse.yaml` | 逆向 ISP 与 RAW 合成 |
| `data/papers/compression.yaml` | RAW 压缩与联合编码 |
| `data/papers/task.yaml` | 面向机器视觉的 ISP |
| `data/papers/tuning.yaml` | ISP 参数与管线优化 |
| `data/papers/report.yaml` | 挑战报告、综述与评测 |
| `data/collections.yaml` | 跨任务专题定义 |
| `data/facets.yaml` | 双语筛选标签 |
| `data/research.yaml` | 证据、专题归属、阅读笔记、引文与数据集关联 |
| `data/datasets.yaml` | 数据集 |
| `data/tools.yaml` | 工具 |
| `data/resources.yaml` | 学习资源 |
| `data/trends.yaml` | 研究脉络 |

按主要评测目标与贡献确定唯一的**任务主分类**。可控与移动端 / 高效 ISP 是允许交叉的专题，归属存于 `data/research.yaml`；不要通过复制论文建立专题。见[分类规则与完整审计](guide/classification-2026-11-05.zh-CN.md)。

区分相机 / 拍摄条件化与显式用户控制。自动预测或调参本身不代表用户编辑；仅处理颜色的模块和逆向重建保留在各自主分类。支持多目标的通用优化器归参数调优，围绕特定下游任务的方法归机器视觉。

没有独立论文的参赛方案，按相同资源格式加入报告的 `implementations` 列表，并保留原内部名称对应的中文翻译；代码与权重状态汇总到唯一报告文献。

## 论文条目格式

```yaml
- name: LiteISPNet                         # 翻译与搜索使用的稳定内部标识，不作为显示标题
  title: Learning RAW-to-sRGB Mappings With Inaccurately Aligned Supervision
  venue: ICCV                             # CVPR、ICCV、ECCV、NeurIPS、arXiv 等
  year: 2021
  paper: https://openaccess.thecvf.com/...  # 优先使用 CVF、ECVA 或出版商页面，其次是 arXiv 摘要页
  code: https://github.com/cszhilu1998/RAW-to-sRGB
  status: weights                         # 状态说明见下表
  weights:                                # weights 或 weights-in-repo 状态必填
    - label: ZRR / SR-RAW pretrained models (Google Drive)
      url: https://drive.google.com/drive/folders/...
    - label: Mirror (Baidu, code abcd)      # 网盘提取码写在标签中
      url: https://pan.baidu.com/s/...
  framework: PyTorch                      # 可选
  tldr: Explain the challenge, specific method and concrete contribution in 1-2 concise sentences.
  note: Optional practical remark.
```

`tldr` 应按“挑战 → 具体模型或机制 → 贡献”用一至两句概括，英文通常为 25–55 词。CNN、Transformer、Mamba、扩散等结构必须依据论文或官方项目确认，不能从 PyTorch 等实现框架推断。数据集和报告应说明数据、协议及评测贡献，不要套用模型描述，也不添加缺乏依据的排名和数值。`note` 用于必要的使用说明，例如权重对应 TPAMI 扩展版本。

显示标题直接使用论文正式完整英文标题，中文译名作为阅读辅助；不要自拟论文名称。`name` 仅作为已有翻译与搜索的稳定内部标识。链接指向挑战报告的方案条目，使用报告标题，并在总结中明确具体方案。中文总结应与英文保持相同技术事实。

### 状态值

| `status` | 使用条件 |
|:--|:--|
| `weights` | 官方 README 提供可下载的预训练权重链接 |
| `weights-in-repo` | 权重文件直接提交在仓库中；请链接到对应目录 |
| `code` | 官方代码已公开，但未找到预训练权重 |
| `unofficial` | 只有第三方实现；`code` 指向该实现 |
| `coming-soon` | 仓库目前是占位页面，或声明代码将发布 |
| `no-code` | 未找到公开代码 |

构建会拒绝不符合规则的条目，例如 `status: weights` 却没有 `weights`，或 `no-code` 条目同时填写了 `code` 链接。

## 收录范围

收录：

- 替代、辅助或调优相机 ISP 某个阶段或完整流水线的学习方法；
- 直接处理 RAW 传感器数据的方法，包括去噪、去马赛克、连拍融合、弱光、RAW 视频，以及 RAW 检测和分割；
- 逆向 ISP、RAW 重建与 RAW 压缩；
- 与 ISP 相关的挑战赛报告、综述和数据集。

不收录：

- 仅在 sRGB 基准上评估的通用图像复原骨干网络；
- 完全不涉及 RAW 数据的弱光增强或去噪；
- RAW 域 NeRF 或 3D Gaussian Splatting 三维重建；
- 多光谱、高光谱或偏振去马赛克。

## 权重链接

- 从官方 README 或项目主页复制链接。若权重来自其他来源，在 `note` 中注明；除非作者明确认可，否则优先标记为 `unofficial`。
- 网盘提取码保留在标签中，例如 `Mirror (Baidu, code abcd)`。
- 不要把权重文件上传到本仓库。
- 区分文献更新日期与链接检查日期。补充几篇论文不代表全站权重已经重新核验。

## 文字与翻译风格

- 英文源数据和中文译文均保持中性，不使用“全新”“最先进”“优于所有方法”等宣传措辞，说明方法实际做了什么。
- 英文标题和方法名称采用论文原始大小写；中文页面保留方法缩写及正式英文标题，方便检索与引用。
- 一篇论文只保留一个条目。有独立仓库的挑战赛获胜方案可以与挑战赛报告分别收录。
- 中文版覆盖标题、方法摘要、备注、分类说明、数据集与学习资料，避免只翻译界面而让正文仍为英文。

## 维护说明

- 建议的 GitHub 仓库简介：`Neural camera ISPs with code and pretrained weights: RAW denoising, demosaicing, white balance, RAW-to-sRGB, inverse ISP and ISP tuning, plus a classical ISP primer.`
- 建议主题标签：`awesome-list`、`neural-isp`、`learned-isp`、`camera-isp`、`image-signal-processing`、`raw-image`、`computational-photography`、`low-level-vision`。
- 网站地址：[https://ruilin.li/Awesome-Neural-ISP/](https://ruilin.li/Awesome-Neural-ISP/)。
- `config.yaml` 保存用于徽章和链接的 GitHub 所有者、仓库名，以及交互页面公开地址 `site`；修改后运行 `python scripts/build.py`。
- 交互网页入口为 `docs/index.html`。首次发布时，在 **Settings → Pages → Build and deployment → Deploy from a branch** 中选择 `main` 分支的 `/docs` 目录。
- `.github/workflows/ci.yml` 验证每次推送与 PR；`.github/workflows/links.yml` 每周一运行 [lychee](https://github.com/lycheeverse/lychee)，发现失效链接时创建 issue，配置位于 `lychee.toml`。
- 人工重新检查全量链接后，更新 `config.yaml` 中的 `checked`；仅补充文献时应单独更新文献日期。

## 研究标注

筛选值定义于 `data/facets.yaml`。每个已赋标签都需在 `evidence` 中保留有来源依据的摘录；缺少标注表示未知，不表示不存在。不能从实现框架或方法简称猜测结构。阅读笔记需在 `en` 和 `zh-CN` 中同时填写 `challenge`、`method`、`contribution` 与编者阅读提示 `limits`。数据集关联使用准确的数据集名称。BibTeX 必须保留来源作者或编者信息及 `bibtex_source`，不得编造作者、页码或会议版本。

分别用 `summary_updated`、`taxonomy_updated` 记录摘要与分类修订；`literature_updated`、`checked` 分别保留给文献增补和全面链接核验。

较长的网页摘要可在 `data/research.yaml` 中填写 `summary.en`、`summary.zh-CN`，并用 `summary_source` 指向论文原始来源。用通俗正文解释具体机制的作用，两种语言保持相同事实。网页优先使用长摘要，其次整合已有挑战、方法和贡献笔记，最后使用精简 `tldr`。核验日期保留在源记录中，不展示在单篇卡片内。

`data/navigation.yaml` 定义双语侧栏四个大类。每个任务与跨任务入口应恰好出现一次，导航归组不改变论文归属。会议筛选依据条目的 `venue`，需准确区分主会、Workshop、Findings、期刊和预印本；`scripts/site_build.py` 为多选归一化已有名称变体，卡片仍保留原始发表信息。
