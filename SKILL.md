---
name: review-generator
description: >
  Generate a Chinese scientific review article with zero hallucinations by coordinating acaflow literature mapping, 氢离子 (QingHydrogen) deep reference retrieval, nature-writing composition, and pandoc-based docx formatting. Use when the user wants to write a comprehensive review with systematically verified references. Triggers: "写综述", "写review", "acaflow 综述", "氢离子 检索", "文献地图 写文章", or any request combining acaflow + 氢离子 for literature-to-manuscript generation.
---

# Review Generator: acaflow + 氢离子 + nature-writing

## Workflow Overview

```
acaflow 文献地图 → 汇总大纲 → 氢离子逐分支深搜 → 去重验证DOI → nature-writing撰写 → pandoc+csl→docx
```

## Phase 1: Literature Mapping with acaflow

### Map Architecture — Derive from Title

Read the article title and extract its conceptual dimensions. The standard decomposition:

```
文章标题
├── ① 核心关联：该领域最直接的流行病学/观察性/组学证据
├── ② 发病机制：开放检索，由acaflow自动聚簇（不预设子分类）
├── ③ 生物标志物：诊断、预后、疗效预测等临床转化维度
├── ④ 干预/治疗（天然）：已有的临床前与临床干预证据
└── ⑤ 干预/治疗（工程）：合成生物学、递送系统、改造策略
```

Adjust the number and naming of maps to the topic. A topic without a therapeutic dimension may need only 3-4 maps. A topic with rich mechanistic literature may benefit from splitting mechanism into two maps.

### Map Naming Guidelines

- Map titles should be broad enough for acaflow to cluster meaningfully, narrow enough to stay on topic.
- **Map ② (mechanism) is always open-ended.** Do not predefine subcategories. Let acaflow's clustering determine the branch structure.
- For therapy-oriented topics, separate "natural/endogenous" approaches from "engineered/synthetic" approaches.

### acaflow Operational Rules

1. **Maximum 3 saved maps at a time** on the acaflow platform.
2. **Save every map immediately** after generation completes — there is no undo for unsaved maps.
3. **Delete maps to make room**: click the three-dot menu on each map card, select delete.
4. **Screenshot completed maps** before deleting, to preserve the clustering structure.

### Map Rotation Pattern

```
Save Map 1 + Map 2 → delete Map 1 → create Map 3 → delete Map 2 → create Map 4 → delete Map 3 → create Map 5
```

Always keep the newest map saved until the next one is generated and saved.

## Phase 2: Outline Generation

After all maps are complete and screenshotted:

1. Aggregate clustering results from all maps into one document.
2. Identify the major themes that emerge across maps — these become sections.
3. Draft a preliminary outline. Sections should flow logically: background → core evidence → mechanisms → translational applications → outlook.
4. Ask the user for target length (character or word count). Assign proportional allocation to each section.
5. Review and adjust with the user before proceeding.

## Phase 3: Deep Search with 氢离子

### Strategy: Per-Branch, Multi-Round

**Do NOT use the broad map title as a search query.** For each sub-branch identified in the acaflow maps, conduct narrow, targeted searches.

For each sub-branch:
1. Formulate specific Chinese queries that capture the sub-topic precisely.
2. Engage in multi-round dialog. 氢离子 returns a limited number of references per response — continue until the sub-branch stops yielding new, relevant results.
3. Log every reference with: authors, title, journal, year, volume, pages, DOI, and which outline section it supports.

### Coverage Discipline

Before declaring search complete, audit each sub-branch:
- Has every sub-branch from every acaflow map been queried?
- Are the early maps (core evidence, mechanisms) searched as thoroughly as later maps?
- Are there obvious gaps where a known paper should have appeared but didn't?

## Phase 4: Reference Assembly

1. **Deduplicate** across all search logs. Many references appear in multiple branches.
2. **Verify DOIs** via web search or Crossref API. Flag any reference lacking a verifiable DOI — either find it or remove the reference.
3. **Group by section** — tag each reference with the outline section(s) it supports.
4. **Confirm count with user** before writing begins.

## Phase 5: Manuscript Writing

Use the `nature-writing` skill for composition. Key writing rules:

### Prohibited Patterns

| Pattern | Why | Fix |
|---------|-----|-----|
| Section titles with colons ("名词：描述") | Sounds machine-translated | Use concise noun phrases or declarative statements |
| Journal names in body text | Clutters narrative flow | Cite by reference number only |
| Parenthetical years "（2019）" | Breaks reading flow | Remove entirely; reference numbers suffice |
| Reference stacking (5+ per sentence) | Unreadable | Break into multiple sentences, synthesize across refs |
| One ref per statement listing | Reads like an annotated bibliography | Synthesize findings across multiple refs into coherent paragraphs |

### Writing Quality Standards

- **Paragraph unity**: One controlling idea per paragraph. Topic sentence → evidence synthesis → transition.
- **Verb calibration**: Use precise verbs that reflect strength of evidence (demonstrate > reveal > suggest > correlate with).
- **Synthesis over inventory**: A paragraph describing 8 papers' findings is poor. A paragraph explaining what those 8 papers collectively teach us is good.

### Citation Format

Use `[@ref]` format for pandoc citation processing. Number references sequentially by first appearance. Cite only references you have read and understand — never pad with unread references.

## Phase 6: Formatting and docx Output

### Markdown Preparation

- References must be separated by blank lines (pandoc treats adjacent lines as one paragraph).
- Use pandoc superscript syntax: `10^12^` for superscript.
- Each `[N]` reference entry on its own line with a blank line before the next.

### Pandoc Command

```bash
pandoc manuscript.md -o manuscript.docx --csl=nature.csl --from=markdown --to=docx
```

### Post-Processing (Python)

Pandoc's docx output needs font and spacing fixes. The bundled `scripts/fix_docx_fonts.py` handles:

| Property | Value |
|----------|-------|
| Chinese font | SimSun (宋体) |
| Latin font | Times New Roman |
| Line spacing | 1.5× |
| Alignment | Justified (两端对齐) |
| H1 | 22pt bold |
| H2 | 16pt bold |
| H3 | 14pt bold |
| Body | 12pt |

```bash
python scripts/fix_docx_fonts.py input.docx output.docx
```

### Windows Caveats

- Python may fail on paths containing Chinese characters. Copy files to `$env:TEMP` before running Python.
- PowerShell lacks ternary operators — use `if/else` blocks.

## Common Problems

### acaflow Phase

| Problem | Action |
|---------|--------|
| Map limit reached | Delete oldest saved map via three-dot menu before creating new |
| Map clustering unfocused | Narrow the map title; for mechanism map, trust auto-clustering |
| Unsaved map lost | Regenerate; always save immediately after each generation |

### 氢离子 Phase

| Problem | Action |
|---------|--------|
| Too few refs per round | Continue multi-round dialog; each round yields ~10 refs |
| Broad search returns noise | Search specific sub-branch terms, not map titles |
| Missing DOIs | Flag for later verification; check Crossref or PubMed |

### Writing Phase

| Problem | Action |
|---------|--------|
| Reference hallucination | Only cite refs from the verified collection |
| Colon titles | Rewrite as concise noun phrases |
| Reference stacking | Break into synthesis across multiple sentences |
| Journal names in body | Remove all journal mentions |

### Formatting Phase

| Problem | Action |
|---------|--------|
| References run together | Ensure blank line between each `[N]` entry in markdown |
| Font not applying | Modify both `styles.xml` and `theme1.xml` in docx ZIP |
| Chinese path errors | Copy to `$env:TEMP` before Python post-processing |

## Key Principles

1. **Literature first, writing second.** Complete all retrieval and verification before opening the manuscript.
2. **Let acaflow cluster mechanisms.** Do not impose a preset framework on the mechanism map.
3. **Multi-round narrow search > single broad search.** Ten rounds on one sub-branch finds more than one round on the whole field.
4. **Verify DOIs before citing.** No unverifiable references in the final manuscript.
5. **Format at the end.** Apply fonts, spacing, alignment via post-processing — not during drafting.
6. **Synthesize, don't list.** The nature-writing skill rewards integrated understanding over annotated bibliographies.
7. **Adapt map count and depth to the topic.** Not every review needs 5 maps; adjust based on the field's maturity and the user's scope.

