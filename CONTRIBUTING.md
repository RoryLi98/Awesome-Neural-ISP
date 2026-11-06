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
   python scripts/check_research.py
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
| `data/papers/e2e.yaml` | End-to-End RAW-to-sRGB |
| `data/papers/denoise.yaml` | RAW Denoising & Noise Modeling |
| `data/papers/lowlight.yaml` | Low-Light Rendering & Exposure Correction |
| `data/papers/demosaic.yaml` | Demosaicing & Remosaicing |
| `data/papers/restoration.yaml` | RAW Deblurring & Other Restoration |
| `data/papers/super-resolution.yaml` | RAW Super-Resolution & Resampling |
| `data/papers/burst.yaml` | Burst & HDR Imaging |
| `data/papers/video.yaml` | RAW Video |
| `data/papers/white-balance.yaml` | White Balance & Color Constancy |
| `data/papers/color.yaml` | Color Correction, Tone & Retouching |
| `data/papers/inverse.yaml` | Inverse ISP & RAW Synthesis |
| `data/papers/compression.yaml` | RAW Compression & Joint Coding |
| `data/papers/task.yaml` | ISP for Machine Vision |
| `data/papers/tuning.yaml` | ISP Parameter & Pipeline Optimization |
| `data/papers/report.yaml` | Challenges, Surveys & Evaluation |
| `data/collections.yaml` | Cross-task collection definitions |
| `data/facets.yaml` | Bilingual facet labels |
| `data/research.yaml` | Evidence, collection membership, reading notes, citations, dataset associations |
| `data/datasets.yaml` | Datasets |
| `data/tools.yaml` | Tools |
| `data/resources.yaml` | Learning resources |
| `data/trends.yaml` | Research threads |

Assign one **primary task** by the main evaluated contribution. Controllable and mobile/efficient ISPs are overlapping collections, stored in `data/research.yaml`; do not duplicate papers in separate files. See the [classification rules and full audit](guide/classification-2026-11-05.md).

Keep camera/capture conditioning distinct from exposed user controls. Automatic prediction or optimization alone does not imply user editing. Color-only controls and inverse reconstruction retain their primary tasks. General-purpose multi-objective optimizers belong in tuning; a specific downstream-task objective belongs in machine vision.

A challenge solution without its own publication is an `implementations` resource on the report, using the same resource schema. Add its translation under its existing internal name; code and weight availability aggregate to the one publication.

## Paper entry format

```yaml
- name: LiteISPNet                      # stable internal key / search alias; not the display heading
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
  tldr: Explain the challenge, specific method and concrete contribution in 1-2 concise sentences.
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
- Display the paper's full official title, with its original capitalization. Do not invent display names. `name` is a stable internal key used by translations and search; an existing alias is not a paper title.
- Summaries should explain **challenge → specific mechanism/model → contribution**, usually in 25–55 English words. Verify architecture labels (CNN, Transformer, Mamba, diffusion, etc.) from the paper or official project; a PyTorch implementation does not identify an architecture. Describe benchmark/data/protocol contributions for reports and datasets. Avoid unsupported rankings and numbers.
- Chinese summaries must preserve the same technical facts. Keep the official English title as the heading and use the Chinese translation as reading assistance. When an entry links to a challenge report rather than a standalone solution paper, use the report's title and identify the solution in the summary.
- One entry per unique publication. Nest separately released challenge solutions under their report; a repository does not constitute another publication.

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

## Research annotations

Facet values come from `data/facets.yaml`; attach an explicit source-grounded excerpt under `evidence` for every assigned value. Missing annotations mean unknown, not absent. Do not identify architecture from a framework or from a model nickname. Reading notes need `challenge`, `method`, `contribution` and editorial `limits` in both `en` and `zh-CN`. Dataset associations must reference exact dataset names. BibTeX must retain source author/editor metadata and a `bibtex_source` URL; do not invent authors, pages or a conference version.

Use `summary_updated` and `taxonomy_updated` for those revisions; keep `literature_updated` and `checked` for literature additions and a full link audit respectively.

Longer website abstracts may be provided in `data/research.yaml` as `summary.en` and `summary.zh-CN`, with a `summary_source` primary-source URL. Explain each technical mechanism in accessible prose and keep the two languages factually aligned. The website uses these in place of the compact `tldr`; otherwise it integrates existing challenge/method/contribution notes, then falls back to `tldr`. Audit dates remain in source records, not in individual cards.

`data/navigation.yaml` defines the four bilingual sidebar groups. Include every primary task and cross-task view exactly once; grouping does not change paper assignments. Venue filtering uses the stored `venue` field: keep main conferences, Workshops, Findings, journals and preprints accurate and distinct. `scripts/site_build.py` normalizes known label variants for multi-selection while preserving the original venue on cards.
