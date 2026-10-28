# Contributing

[English](CONTRIBUTING.md) · [简体中文](CONTRIBUTING.zh-CN.md)

Thanks for helping keep this list complete and its links alive. Every entry lives in a YAML file under
[`data/`](data/); `README.md`, `WEIGHTS.md` and the interactive page in `docs/` are generated from those files, so
please **do not edit the generated files by hand**.

## Quick start

1. Fork the repository and create a branch.
2. Edit the right file under `data/papers/` (see the table below).
3. Regenerate and validate:

   ```bash
   pip install -r requirements.txt
   python scripts/build.py
   ```

4. Add or update the corresponding Chinese content in `data/i18n/` (see **Bilingual content** below).
   Commit the YAML change together with both READMEs, both weight indexes and both HTML pages, and open a
   pull request. CI runs `python scripts/build.py --check` and fails if the data is invalid or the generated files are
   out of date.

Not comfortable with a PR? Open an issue with the [Add a paper](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=add-paper.yml) or
[Report a broken link](https://github.com/RoryLi98/Awesome-Neural-ISP/issues/new?template=broken-link.yml) form instead.

## Which file?

| File | Section |
|:--|:--|
| `data/papers/e2e.yaml` | End-to-end RAW-to-sRGB |
| `data/papers/controllable.yaml` | Controllable Neural ISP |
| `data/papers/mobile.yaml` | Mobile & lightweight ISP |
| `data/papers/denoise.yaml` | RAW denoising & noise modeling |
| `data/papers/lowlight.yaml` | Low-light RAW enhancement |
| `data/papers/demosaic.yaml` | Demosaicing, joint restoration & RAW super-resolution |
| `data/papers/burst.yaml` | Burst & HDR |
| `data/papers/video.yaml` | RAW video |
| `data/papers/color.yaml` | White balance, color & tone |
| `data/papers/inverse.yaml` | Inverse ISP, RAW reconstruction & compression |
| `data/papers/task.yaml` | ISP for machine vision |
| `data/papers/tuning.yaml` | ISP parameter tuning |
| `data/papers/report.yaml` | Challenges & surveys |
| `data/datasets.yaml` | Datasets |
| `data/tools.yaml` | Tools & open-source ISPs |
| `data/resources.yaml` | Tutorials, books, classical papers, related lists |

If a paper fits several sections, put it where its main contribution is. Entry order inside a file does not matter;
the build sorts them.

**Controllable Neural ISP** covers explicit user controls, replaceable learned rendering stages and camera/style
conditioning. These are different control interfaces: a metadata-conditioned model is not necessarily an interactive
editor. Automatic content-dependent parameter prediction belongs in `tuning`; methods optimized for downstream
task rewards belong in `task`. Color-only modules and edit-aware inverse methods stay in `color` and `inverse`,
with cross-references in the category descriptions. Move entries instead of duplicating them.

## Paper entry format

```yaml
- name: LiteISPNet                      # short name shown in bold (method name or acronym)
  title: Learning RAW-to-sRGB Mappings With Inaccurately Aligned Supervision
  venue: ICCV                           # CVPR, ICCV, ECCV, NeurIPS, CVPRW (NTIRE), IEEE TIP, arXiv, ...
  year: 2021
  paper: https://openaccess.thecvf.com/...   # prefer CVF / ECVA / publisher page, else arXiv abs page
  code: https://github.com/cszhilu1998/RAW-to-sRGB   # official repository, if any
  status: weights                       # see below
  weights:                              # required when status is weights or weights-in-repo
    - label: ZRR / SR-RAW pretrained models (Google Drive)
      url: https://drive.google.com/drive/folders/...
    - label: Mirror (Baidu, code 8sq1)  # put extraction codes in the label
      url: https://pan.baidu.com/s/...
  framework: PyTorch                    # optional
  tldr: One neutral sentence on what the paper does, ideally 12-28 words.
  note: Optional practical remark (e.g. "weights are for the TPAMI extension").
```

### Status values

| `status` | Use when |
|:--|:--|
| `weights` | the official README links to downloadable checkpoints |
| `weights-in-repo` | checkpoint files are committed to the repository (link the folder) |
| `code` | official code is public, but no pretrained weights were found |
| `unofficial` | only a third-party implementation exists (`code` points to it) |
| `coming-soon` | the repository is a placeholder or says code will be released |
| `no-code` | no public code was found |

The build refuses entries that break these rules (for example `status: weights` without any `weights`, or a `code`
URL on a `no-code` entry).

## What belongs here

Included:

- learned methods that replace, assist or tune a stage of the camera ISP, or the whole ISP;
- methods that operate on RAW sensor data (denoising, demosaicing, burst merging, low-light, RAW video, RAW for
  detection or segmentation);
- inverse ISPs, RAW reconstruction and RAW compression;
- ISP-related challenge reports, surveys and datasets.

Out of scope:

- general image-restoration backbones evaluated only on sRGB benchmarks;
- low-light enhancement or denoising that never touches RAW data;
- RAW-domain NeRF / 3D Gaussian splatting reconstruction;
- multispectral, hyperspectral or polarization demosaicing.

## Weight links

- Copy links from the official README or project page. If you found a checkpoint elsewhere, mention the source in
  `note` and prefer `unofficial` status unless the authors endorse it.
- Keep extraction codes (Baidu, PKU disk) in the label, e.g. `Mirror (Baidu, code abcd)`.
- Do not upload checkpoints to this repository.

## Style

- Maintain English source records and complete Chinese overlays, in a neutral tone: no "novel", "state-of-the-art" or "outperforms". Describe what the method does.
- Use the paper's own capitalization for titles and method names.
- One entry per paper; challenge-winning solutions that have their own repository may be listed next to the report.

## Bilingual content

- `data/i18n/papers.zh-CN.yaml` maps the exact paper `name` to translated `title`, `tldr`, and `note` (when present),
  plus `weight_labels` in the same order as the source weights. Keep official method names; translate descriptive text.
- `data/i18n/resources.zh-CN.yaml` covers categories, datasets, tools, trends and learning resources. Identity keys,
  bibliographic values and links come from the English source. Resource lists retain the source ordering.
- `scripts/localization.py` rejects missing translations and mismatched counts. `python scripts/build.py --check`
  checks all six generated outputs: `README.md`, `README.zh-CN.md`, `WEIGHTS.md`, `WEIGHTS.zh-CN.md`,
  `docs/index.html` and `docs/zh-CN.html`.
- Website sources are `scripts/site_template.html`, `scripts/site_style.css`, `scripts/site_script.js` and
  `scripts/site_build.py`. Generated pages embed all data, styles and scripts and work without a server or CDN.
- Keep `config.yaml`'s `checked` date for a full code/weight audit; use `literature_updated` for literature refreshes.
  Record sources and per-entry checks in an update note, instead of implying all links were rechecked.

## For maintainers

- Suggested GitHub repository settings (the **About** box): description `Neural camera ISPs with code and pretrained weights: RAW denoising, demosaicing, white balance, RAW-to-sRGB, inverse ISP and ISP tuning, plus a classical ISP primer.`; topics `awesome-list`, `neural-isp`, `learned-isp`, `camera-isp`, `image-signal-processing`, `raw-image`, `computational-photography`, `low-level-vision`; website `https://ruilin.li/Awesome-Neural-ISP/`.
- `config.yaml` holds the GitHub owner and repository name used in badges, and `site`, the public URL of the
  interactive page. After changing it, run `python scripts/build.py`.
- The interactive page is `docs/index.html`. Enable it once under **Settings → Pages → Build and deployment →
  Deploy from a branch → `main` / `docs`**.
- `.github/workflows/ci.yml` validates every push and pull request. `.github/workflows/links.yml` runs
  [lychee](https://github.com/lycheeverse/lychee) every Monday and opens an issue if links are broken; its settings
  are in `lychee.toml`.
- When you re-check links by hand, update `checked` in `config.yaml`.
