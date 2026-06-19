---
name: acaflow-review-generator
description: >
  Generate a Chinese scientific review article with zero hallucinations by coordinating acaflow literature mapping, 氢离子 (QingHydrogen) deep reference retrieval, nature-writing composition, and pandoc-based docx formatting. Use when the user wants to write a comprehensive review with systematically verified references. Triggers: "写综述", "写review", "acaflow 综述", "氢离子 检索", "文献地图 写文章", or any request combining acaflow + 氢离子 for literature-to-manuscript generation.
---

# Acaflow Review Generator

## Workflow Overview

```
acaflow 文献地图 → 汇总大纲 → 氢离子逐分支深搜 → 大纲修正 → 去重验证DOI → nature-writing撰写 → pandoc→docx
```

## Before You Begin: Prerequisites

Confirm the following are available before starting:

| Dependency | Check | Notes |
|------------|-------|-------|
| acaflow | Open in Chrome, confirm logged in | Browser-based literature mapping platform |
| 氢离子 | Open in Chrome, confirm logged in | Browser-based AI literature search; returns ~10 refs per response |
| pandoc | `pandoc --version` | v2.0+ recommended |
| Python 3 | `python --version` | For docx post-processing script |
| SimSun (宋体) | Installed on system | Required for Chinese font in docx |
| Times New Roman | Installed on system | Required for Latin font in docx |
| nature.csl | Download once | See Phase 6 for source |

If the user's machine cannot access acaflow or 氢离子 (network restrictions, account issues), ask the user to resolve connectivity before proceeding. Do not attempt to substitute with general web search — the zero-hallucination guarantee depends on these tools' curated databases.

---

## Phase 1: Literature Mapping with acaflow

### Map Architecture — Derive from Title

Read the article title and extract its conceptual dimensions. The standard decomposition template:

```
文章标题
├── ① 核心关联：该领域最直接的流行病学/观察性/组学证据
├── ② 发病机制：开放检索，由acaflow自动聚簇（不预设子分类）
├── ③ 生物标志物/临床转化：诊断、预后、疗效预测等
├── ④ 干预/治疗（天然）：已有的临床前与临床干预证据
└── ⑤ 干预/治疗（工程）：合成生物学、递送系统、改造策略
```

**Adapt, don't copy.** Number of maps depends on the topic:
- A basic science topic with no therapy angle → 3–4 maps (core evidence + mechanism + biomarkers)
- A translational topic → 4–5 maps (add therapy maps)
- A mechanism-heavy topic → split mechanism into two maps
- A topic with only one therapeutic modality → merge maps ④+⑤

**Map titles should be in the same language as the target article.** For Chinese reviews, write map titles in Chinese. acaflow clusters literature based on the semantic space of the title, and language consistency produces better clustering.

### Map Naming Guidelines

- **Broad enough** for acaflow to generate meaningful clusters, **narrow enough** to stay on topic.
- **Map ② (mechanism) is always open-ended.** Do not predefine subcategories like "免疫机制/代谢机制/微生态". Let acaflow's clustering algorithm determine the branch structure. The title should be simply "发病机制" or equivalent — no qualifiers.
- For therapy-oriented topics, separate natural/endogenous approaches from engineered/synthetic approaches.

### acaflow Operational Rules

1. **Maximum 3 saved maps at a time.** acaflow's platform limits concurrent saved maps.
2. **Save every map immediately.** There is no undo for unsaved maps. After generation completes, click save before doing anything else.
3. **Screenshot each map after saving.** The clustering visualization (branch structure, key papers in each cluster) is the primary deliverable. The screenshot is your permanent record.
4. **Delete maps to make room.** Each map card has a three-dot menu in the corner — click it, select delete. Delete the oldest/least-needed map before creating a new one.
5. **Double-check before deleting.** If you accidentally delete a map without a screenshot, you must regenerate it from scratch — there is no trash recovery.

### Map Rotation Pattern

```
Create Map 1 → Save + Screenshot
Create Map 2 → Save + Screenshot
Delete Map 1 → Create Map 3 → Save + Screenshot
Delete Map 2 → Create Map 4 → Save + Screenshot
Delete Map 3 → Create Map 5 → Save + Screenshot
```

Always keep the newest map saved until its successor is safely saved and screenshotted.

---

## Phase 2: Outline Generation

After all maps are complete and screenshotted:

1. **Aggregate** clustering results from all maps into one document. For each map, record:
   - The major clusters acaflow identified and their labels
   - Key representative papers in each cluster
   - Cross-map themes (clusters from different maps that overlap)
2. **Identify major themes** that emerge — these become sections.
3. **Draft a preliminary outline.** Logical flow: background → core evidence → mechanisms → translational applications → outlook.
4. **Ask the user** for target length (character or word count). Assign proportional allocation to each section.
5. **Review with the user** and adjust before proceeding to Phase 3.

**This outline is preliminary.** It will be refined in Phase 4.5 based on what the literature search actually finds.

---

## Phase 3: Deep Search with 氢离子

### What 氢离子 Is (and Isn't)

氢离子 is a browser-based AI literature search tool with its own curated database. Key operational facts:

- **Access:** Open in Chrome at its web address. It presents a chat-style interface.
- **Capacity:** Each response returns approximately 8–12 references.
- **Context:** It maintains conversation context within a session, so follow-up questions can build on previous results.
- **Limitation:** After several rounds on the same topic, it may begin recycling previously shown references. When this happens, the sub-branch is saturated — move on.
- **Language:** Queries work best in Chinese for biomedical topics.

### Strategy: Per-Branch, Multi-Round

**This is the most important phase for reference completeness. Do not rush it.**

For each sub-branch identified in the acaflow maps:

1. **Formulate the first query** — narrow and specific, capturing exactly that sub-topic. Example: not "噬菌体与结直肠癌", but "CRC患者粪便噬菌体组多样性变化队列研究".
2. **Record all references** from the response in a structured log file. Minimum fields: authors, title, journal, year, volume, pages, DOI (if provided), which map branch this supports.
3. **Follow up** with related but distinct angles. Example sequence for one sub-branch:
   - Round 1: "CRC患者粪便噬菌体组多样性变化队列研究"
   - Round 2: "腺瘤与CRC噬菌体组差异比较"
   - Round 3: "噬菌体组与CRC分期/预后的关联"
   - Round 4: "不同地域人群CRC噬菌体组特征"
4. **Stop when saturated** — 氢离子 starts repeating references or returns fewer than 3 new refs per round.
5. **Log file discipline:** Maintain a single master log (e.g., `hydrogen-refs-log.md`) throughout all searches. Tag each entry with the branch it came from. This is your source of truth for Phase 4.

### Coverage Audit

Before declaring search complete, audit:
- Has every sub-branch from every acaflow map been queried with at least 2–3 rounds?
- Are the earlier maps (core evidence, mechanisms) searched as thoroughly as later maps? They should receive **more** rounds — they form the evidentiary backbone.
- Are there obvious gaps? If a topic that should have literature returns nothing, try reformulating the query before giving up.

### Common 氢离子 Pitfalls

| Pitfall | Fix |
|---------|-----|
| Using the broad map title as query | Narrow to specific sub-branch terms |
| Stopping after 1 round per branch | Multiple angles needed for saturation |
| Not logging refs in real time | Log as you go; batch-logging leads to loss |
| Accepting refs without DOIs | Flag for verification in Phase 4 |
| Treating all returned refs as equally relevant | Skim titles; not every result is on-topic |

---

## Phase 4: Reference Assembly

### 4.1 Deduplicate

References often appear in multiple search rounds (especially high-impact papers). Cross-reference all entries in the master log and merge duplicates. A paper cited in both Map 1 and Map 2 should appear once with both tags.

### 4.2 Verify DOIs

Every reference in the final manuscript must have a verified DOI. Methods, in order of preference:

1. **If 氢离子 provided a DOI** — verify it resolves:
   - Open `https://api.crossref.org/works/DOI_HERE` in browser or via curl
   - A 200 response with author/title matching your record → verified
   - A 404 → the DOI is wrong; proceed to method 2

2. **If 氢离子 did not provide a DOI** — search for it:
   - PubMed E-utility: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TITLE_HERE[title]`
   - Crossref search: `https://api.crossref.org/works?query.title=TITLE_HERE&rows=3`
   - Web search: paste the exact title in quotes

3. **If no DOI can be found** — remove the reference. An unverifiable reference is worse than no reference.

### 4.3 Group by Section

Tag each verified reference with the outline section(s) it supports. Some references will support multiple sections — note all applicable sections.

### 4.4 Confirm with User

Present the user with:
- Total verified reference count
- Count per section
- Any sections that appear under-referenced
- Any references that were removed due to unverifiable DOIs

Get user approval before writing.

### 4.5 Adapt the Outline

**This is a critical feedback loop.** Based on what was actually found:
- Sections with abundant literature may need to be split
- Sections with sparse literature may need to be merged or trimmed
- New themes that emerged during search may warrant new sections
- The character allocation per section should be adjusted

Revise the outline with the user before writing begins.

---

## Phase 5: Manuscript Writing

Use the `nature-writing` skill for composition.

### Reference Format

This workflow uses **manual inline numbering**: `[1]`, `[2]`, `[3]` in the text, with a corresponding numbered reference list at the end.

- References are numbered sequentially by first appearance in the text.
- The same reference re-cited later uses its original number.
- The reference list at the end of the manuscript uses `[N]` format with one entry per line, blank lines between entries.

This means the pandoc command does NOT use `--csl` or `--bibliography` flags — those require `[@key]` syntax and a `.bib` file, which is a different workflow. Our manual approach is simpler and sufficient for most Chinese review articles.

### Prohibited Patterns

| Pattern | Why | Fix |
|---------|-----|-----|
| Section titles with colons ("名词：描述") | Sounds machine-translated | Use concise noun phrases or declarative statements |
| Journal names in body text | Clutters narrative flow | Cite by reference number only |
| Parenthetical years "（2019）" | Breaks reading flow | Remove entirely; reference numbers suffice |
| Reference stacking (5+ per sentence) | Unreadable | Break into multiple sentences, synthesize across refs |
| One ref per statement listing | Reads like an annotated bibliography | Synthesize findings across multiple refs into coherent paragraphs |
| Citing unread references | Hallucination risk | Only cite refs you have read the abstract (at minimum) of |

### Writing Quality Standards

- **Paragraph unity:** One controlling idea per paragraph. Topic sentence → evidence synthesis → transition.
- **Verb calibration:** Use precise verbs reflecting strength of evidence. Hierarchy: demonstrate/prove → reveal/uncover → show/indicate → suggest/imply → correlate with/associate with.
- **Synthesis over inventory:** A paragraph listing 8 papers' individual findings is poor. A paragraph explaining what those 8 papers collectively teach us is good.
- **Logical flow within paragraphs:** Don't jump between unrelated findings. Group by theme, not by paper.

---

## Phase 6: Formatting and docx Output

### Markdown Structure

The manuscript markdown should follow this pattern:

```markdown
# 一级标题（文章标题）

## 二级标题（大节）

正文内容。引用用 [1]、[2,3] 格式……

### 三级标题（小节）

更多正文……

## 参考文献

[1] Author A, Author B, et al. Title. Journal, Year, Volume: Pages. DOI: xxx

[2] Author C, Author D, et al. Title. Journal, Year, Volume: Pages. DOI: xxx
```

Key rules:
- `#` for title, `##` for major sections, `###` for sub-sections
- Inline citations: `[1]` for single, `[1,2]` or `[1-3]` for multiple
- Reference list: one `[N]` entry per line, **blank line between entries** (critical for pandoc paragraph separation)
- Superscript: `10^12^` (pandoc syntax)

### Obtaining nature.csl

Download once from the official CSL repository:
```
https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl
```
Save it in the working directory as `nature.csl`. This file is used by the fix_docx_fonts.py script as a formatting reference, though manual numbering means CSL processing is not applied. Keep it for consistency and potential future use with .bib workflows.

### Pandoc Command

```bash
pandoc manuscript.md -o manuscript.docx --from=markdown --to=docx
```

No `--csl` or `--bibliography` flags — references are manually formatted in the markdown.

### Post-Processing

The bundled `scripts/fix_docx_fonts.py` applies the final formatting. It modifies the docx XML internals (styles.xml + theme1.xml) and repacks the ZIP.

| Property | Value |
|----------|-------|
| Chinese font | SimSun (宋体) |
| Latin font | Times New Roman |
| Line spacing | 1.5× (`w:line="360"`) |
| Alignment | Justified (两端对齐) |
| H1 | 22pt bold |
| H2 | 16pt bold |
| H3 | 14pt bold |
| Body | 12pt |

```bash
python scripts/fix_docx_fonts.py manuscript.docx manuscript.docx
```

The script works in-place (input and output can be the same file). It extracts the docx ZIP to a temp subdirectory, modifies the XML, repacks, and cleans up.

### Windows Caveats

- **Chinese path problem:** Python's zipfile module may fail on paths containing Chinese characters. If the working directory path contains Chinese, copy the docx to `$env:TEMP` first, run the fix there, and copy back.
- **PowerShell limitations:** No ternary operators. Use `if/else` blocks in scripts.

---

## Common Problems and Fixes

### acaflow Phase

| Problem | Action |
|---------|--------|
| Map limit reached (3) | Delete oldest saved map via three-dot menu before creating new |
| Map clustering unfocused or too broad | Narrow the map title; for mechanism map, trust auto-clustering |
| Unsaved map lost | Regenerate from scratch; always save immediately after generation |
| Accidentally deleted wrong map | If screenshotted, you have the structure but not interactive access — regenerate if the map is critical |

### 氢离子 Phase

| Problem | Action |
|---------|--------|
| Too few refs per round | Normal — continue multi-round dialog; each round yields ~10 |
| Broad search returns noise | Search specific sub-branch terms, not map titles |
| 氢离子 recycles previous refs | The sub-branch is saturated — move to next branch |
| Missing DOIs | Flag for Phase 4 verification; check Crossref or PubMed |
| Uneven coverage across maps | Count refs per branch; Maps 1–2 need proportionally more rounds |
| 氢离子 inaccessible (network) | Pause work; ask user to restore connectivity |

### Writing Phase

| Problem | Action |
|---------|--------|
| Reference hallucination | Only cite refs from the verified collection |
| Colon-formatted titles | Rewrite as concise noun phrases |
| Reference stacking (5+ in one sentence) | Break into multiple sentences with thematic synthesis |
| Journal names in body text | Remove all journal mentions; reference numbers suffice |
| Parenthetical years in body | Remove all "(YYYY)" markers |
| Section under/over length | Adjust based on available literature, not the initial plan |

### Formatting Phase

| Problem | Action |
|---------|--------|
| References run together in docx | Ensure blank line between each `[N]` entry in markdown |
| Font not applying | Modify both `styles.xml` AND `theme1.xml` in docx ZIP |
| Chinese path errors in Python | Copy files to `$env:TEMP` before running Python |
| Superscript not rendering | Use `10^12^` syntax (pandoc superscript) |

---

## Reference Management: Complete File Inventory

During a full run, expect to generate these working files:

```
project-dir/
├── acaflow-maps-summary.md    # Clustering results from all 5 maps
├── preliminary-outline.md     # Phase 2 output
├── hydrogen-refs-log.md       # Master reference log (Phase 3)
├── references-by-section.md   # Grouped references (Phase 4)
├── verified-dois.md           # DOI verification results
├── manuscript.md              # Final markdown manuscript (Phase 5)
├── nature.csl                 # Citation style file
├── manuscript.docx            # Final output (Phase 6)
└── _bib_index.csv             # Optional: spreadsheet index of all refs
```

Do not delete the intermediate files after completion — they are the audit trail proving zero hallucination.

---

## Key Principles

1. **Literature first, writing second.** Complete all retrieval and verification before opening the manuscript.
2. **Let acaflow cluster mechanisms.** Do not impose a preset framework on the mechanism map.
3. **Multi-round narrow search beats single broad search.** Ten rounds on one sub-branch finds more than one round on the whole field.
4. **Verify DOIs before citing.** No unverifiable references in the final manuscript. Remove, don't guess.
5. **Revise the outline after search.** The literature you actually find should shape the structure, not the other way around.
6. **Format at the end.** Apply fonts, spacing, alignment via post-processing — not during drafting.
7. **Synthesize, don't list.** The nature-writing skill rewards integrated understanding over annotated bibliographies.
8. **Adapt to the topic.** Map count, search depth, and section structure all depend on the field's maturity and the user's scope — not a fixed template.
9. **Keep the audit trail.** Intermediate files (maps summary, ref log, DOI verification) are proof of systematic retrieval. Save them.
