# Classification audit · 2026-11-05

[English](classification-2026-11-05.md) · [简体中文](classification-2026-11-05.zh-CN.md)

The library contains **417 unique publications**, **206 with public code**, **133 with weights (132 official, one third-party)**, and **29 datasets**. The previous 419 entries included two challenge implementations pointing to the same publications as their challenge reports. MW-ISPNet and MWRCANet are now implementation resources under those reports; their descriptions, code and all weight links are preserved.

## Primary tasks and overlapping collections

Each publication has one primary task. This audit assigns all 417 publications and changes **123 primary assignments**. The evidence is the official title, the source-grounded summary and, for boundary cases, the primary-source abstract. This is a taxonomy review, not a new exhaustive literature search or a claim to have reproduced the methods.

The complete decisions and source links are available as [English CSV](classification-audit-2026-11-05.csv) and [Chinese CSV](classification-audit-2026-11-05.zh-CN.csv). Category ids are stable source identifiers, not alternative paper titles.

| Primary category | Boundary |
|:--|:--|
| End-to-end RAW-to-sRGB | Full learned rendering when a more specific imaging objective is not central. |
| RAW denoising / noise modeling | Noise removal, calibration and synthesis; low illumination alone does not make it an exposure-enhancement method. |
| Low-light / exposure | Brightness and exposure recovery with rendering, including documented conventional baselines. |
| Demosaicing / remosaicing | CFA reconstruction or pattern conversion, including joint denoising. |
| Other RAW restoration | Deblurring, deraining, reflections, moiré, under-display and mixed degradation. |
| RAW SR / resampling | Single-image resolution scaling and its degradation models. |
| Burst / HDR | Multi-frame still reconstruction and sensor-domain HDR, including single-shot HDR. |
| RAW video | Temporally evaluated sequence output; video input for machine perception remains under machine vision. |
| White balance | Illuminant estimation, color constancy and post-capture white-balance editing. |
| Color / tone / retouching | General color correction, LUTs and photographic finishing, including RGB-only context. |
| Inverse ISP / synthesis | RGB-to-RAW/linear-color inversion, generated RAW and sensor-domain translation. |
| RAW compression | Learned coding, entropy modeling, rate–distortion or storage is central. |
| Machine vision | A downstream perception or action objective is central. |
| Parameter / pipeline optimization | General-purpose search, proxies, parameter prediction and multi-objective tuning. |
| Reports / evaluation | Challenge reports, surveys, evaluation protocols and position papers. |

These rules describe the main evaluated contribution, not a keyword hierarchy. Dataset publications stay with their imaging task. Bidirectional models can have both signal tags but still receive one primary task. A general-purpose optimizer supporting both viewing and detection stays under tuning; a method designed around a specific detection reward stays under machine vision.

**Controllable Neural ISP** is retained as a dedicated collection with **9 publications**, crossing end-to-end, low-light, burst and tuning. Its membership requires documented learned rendering with user parameters, reference/style adjustment, replaceable learned stages or camera/capture conditioning. These interfaces are labeled separately:

- CtrlISP, Modular Neural ISP, DRIFT and Neural Photo-Finishing expose user parameters.
- Deep-FlexISP explicitly discusses preference-based style adjustment.
- ParamISP, MetaISP, Uni-ISP and CRISPnet use camera or capture conditioning. This does not establish an interactive editing interface.
- Color-only editors such as NILUT remain under color/tone and are found through their control tags. Edit-aware inverse reconstruction remains inverse. Automatic tuning does not by itself qualify for this collection.

**Mobile & Efficient ISP** is a deployment collection with **32 publications** across tasks. Membership requires an explicit mobile, edge or sensor-efficiency design/evaluation. A small parameter count alone is not evidence of latency on every phone. Collection counts overlap and are never added to the publication total.

## Boundary corrections

- DPED operates on processed photographs, so it is color/retouching rather than a complete RAW-to-RGB ISP.
- DiR learns representations for ISP-related degradations; it is general restoration, not a full renderer.
- StereoISP is joint stereo-assisted demosaicing/denoising. It is not temporal burst capture.
- A single-frame HDR ISP belongs to the HDR task; multi-frame training targets do not imply burst inference.
- HDR methods producing continuous video sequences move to video.
- Burst-specific training/fine-tuning alone does not move a demosaicing method into burst fusion.
- RawNIND's main contribution is denoising data and methods; joint compression is an additional capability.
- JPEG-plus-learned-entropy/metadata coding is separated from inversion methods that merely use sparse reconstruction samples.

## Tags, reading notes and citations

The independent facets are model/mechanism, training/optimization, signal/capture and control interface. Evidence excerpts live in `data/research.yaml`; the linked publication supplies their source context. Tags can describe components, such as a Transformer discriminator, rather than implying that the entire backbone is a Transformer. Missing tags mean **not annotated**, never proof that a method lacks that property. Supervision labels describe documented training stages and may overlap.

This revision adds **15 bilingual reading notes** covering challenge, concrete method, contribution and editorial reading cautions, plus **30 explicit paper-to-dataset associations**. The cautions are editor guidance, not unverified claims of author-reported failures. Numerical rankings are not invented or compared across incompatible protocols.

Annotation coverage at this revision: 112 publications have model/mechanism labels, 22 have training labels, 88 have signal/capture labels and 25 have control labels. These are conservative annotations, not an exhaustive method-family census of all 417 publications.

**242 BibTeX records** were obtained from arXiv's citation export, CVF pages, DOI/Crossref export or official project/repository citations, checked for title correspondence and author/editor metadata. Whitespace and source-provided author-list separators may be normalized. Records retain the source's publication type and version; an arXiv citation is not silently rewritten as a conference citation. Verified citation records remain in the source data for maintenance. The website omits citation blocks and citation/BibTeX copy controls; paper, code and download links remain visible.

Three broad/repository-only paper links were resolved to verified publisher identities: [AIM 2019 RAW-to-RGB report](https://doi.org/10.1109/ICCVW.2019.00443), [EEMEFN](https://doi.org/10.1609/aaai.v34i07.7013), and [ISP-Teacher](https://doi.org/10.1609/aaai.v38i7.28569). Their code links remain separate.

## Maintenance

`data/categories.yaml` defines primary tasks; `data/collections.yaml` defines overlapping collections. Publication records remain under `data/papers/`. `data/facets.yaml` contains bilingual facet labels, while `data/research.yaml` contains evidence, collection memberships, reading notes, citations and dataset associations. Challenge implementations are nested under `implementations` on their single report publication.

The literature-addition date remains **2026-10-28** and the last complete code/weight audit remains **2026-10-11**. Summary and classification revisions are dated **2026-11-05**. Fetching citations or reorganizing records does not imply a new full link audit.

Run `python scripts/build.py`, `python scripts/check_research.py`, `python scripts/build.py --check`, and the optional Playwright check `node scripts/check_site.cjs`. The build validates unique publication identities, references, translation completeness and the source evidence required by tags.
