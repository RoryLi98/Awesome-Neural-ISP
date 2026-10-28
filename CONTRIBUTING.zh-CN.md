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
   python scripts/build.py --check
   ```

5. 一并提交 YAML 源数据、译文和重新生成的中英文文档、网页，然后发起拉取请求。CI 会执行 `python scripts/build.py --check`；数据不合法或生成文件未同步时，检查将失败。

不方便提交 PR，也可以通过 [添加论文](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=add-paper.yml) 或 [报告失效链接](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=broken-link.yml) 表单提交 issue。

## 应该修改哪个文件？

| 文件 | 分类 |
|:--|:--|
| `data/papers/e2e.yaml` | 端到端 RAW-to-sRGB |
| `data/papers/controllable.yaml` | 可控神经 ISP |
| `data/papers/mobile.yaml` | 移动端与轻量化 ISP |
| `data/papers/denoise.yaml` | RAW 去噪与噪声建模 |
| `data/papers/lowlight.yaml` | 弱光 RAW 增强 |
| `data/papers/demosaic.yaml` | 去马赛克、联合复原与 RAW 超分辨率 |
| `data/papers/burst.yaml` | 连拍与 HDR |
| `data/papers/video.yaml` | RAW 视频 |
| `data/papers/color.yaml` | 白平衡、颜色与色调 |
| `data/papers/inverse.yaml` | 逆向 ISP、RAW 重建与压缩 |
| `data/papers/task.yaml` | 面向机器视觉的 ISP |
| `data/papers/tuning.yaml` | ISP 参数调优 |
| `data/papers/report.yaml` | 挑战赛与综述 |
| `data/datasets.yaml` | 数据集 |
| `data/tools.yaml` | 工具与开源 ISP |
| `data/resources.yaml` | 教程、书籍、经典论文与相关目录 |
| `data/trends.yaml` | 研究脉络 |
| `data/i18n/papers.zh-CN.yaml` | 论文标题、摘要、备注与权重标签的中文译文 |
| `data/i18n/resources.zh-CN.yaml` | 分类、数据集、工具、学习资料与研究脉络的中文译文 |

一篇论文适用于多个分类时，以**主要贡献**确定唯一的主分类，避免重复收录。文件中的条目顺序不影响结果，构建程序会自动排序。

“可控神经 ISP”关注推理时可由用户、参考图像、明确的相机参数或风格条件改变输出的学习式成像过程。自动搜索固定 ISP 参数、为下游检测任务优化处理顺序等工作，通常仍属于参数调优或机器视觉分类；不能仅因为方法包含可学习参数就归入可控 ISP。分类依据应来自论文或官方项目说明。

## 论文条目格式

```yaml
- name: LiteISPNet                         # 短名称，通常是方法名或缩写
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
  tldr: One neutral sentence describing the method.
  note: Optional practical remark.
```

英文源数据中的 `tldr` 用一句中性描述概括方法，建议为 12–28 个英文单词；`note` 用于必要的使用说明，例如权重实际对应论文的 TPAMI 扩展版本。中文译文应准确对应源内容，不增加未经来源支持的结论。

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