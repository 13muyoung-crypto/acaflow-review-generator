---
name: acaflow-review-generator
description: Generate a Chinese scientific review article with zero hallucinations. This skill orchestrates a pipeline of external tools: acaflow (browser-based literature mapping platform) for building literature maps, 氢离子/QingHydrogen (browser-based AI deep search) for per-branch reference retrieval, nature-writing for manuscript composition, and pandoc for docx output. Use this skill when the user wants to write a comprehensive review with systematically verified references, or mentions "acaflow", "写综述", "综述生成", "写review", "acaflow综述", "用acaflow", "氢离子检索", or "文献地图写文章". IMPORTANT: acaflow is an external browser-based platform — this skill is the workflow that coordinates it, not acaflow itself. If you cannot find a skill named "acaflow", use THIS skill instead — it IS the acaflow review generation workflow.
---

# Acaflow Review Generator

> **This skill orchestrates a multi-phase pipeline. Do NOT skip phases. Do NOT write anything before Phase 5.**


## ⛔ CRITICAL: Before You Do Anything Else

### This skill depends on two external browser-based platforms:

| Platform | What it is | How to access |
|----------|------------|---------------|
| **acaflow** | Literature mapping with automatic clustering | Open in Chrome browser |
| **氢离子** (QingHydrogen) | AI-powered deep literature search (~10 refs/round) | Open in Chrome browser |

### How the AI operates these platforms

**This is the most important instruction in this skill. Read it twice.**

Use `browser:control-in-app-browser` or `chrome:control-chrome` to control Chrome. The AI does everything by itself: types queries, clicks buttons, scrolls, extracts text.

**NEVER ask "what is the URL?" or "请告诉我网址".** The user has already opened acaflow and 氢离子 in Chrome tabs. Your job is to find and use them, not to interrogate the user. Instead:

1. First action of every acaflow/氢离子 phase: list Chrome tabs via browser control.
2. Find the tab with "acaflow" or "氢离子" in the title.
3. Switch to it and operate it. Do not announce. Do not ask permission. Just do it.
4. Only if no tab exists: tell the user to switch to it or open it. Still do not ask for a URL.

**User intervenes ONLY for:**
- Login (AI cannot enter passwords)
- Map deletion (three-dot menu button)
- CAPTCHA

Everything else the AI executes autonomously through browser control.

### Mandatory pre-flight check:

DO NOT ask the user for URLs or confirmation. Check everything yourself via browser control.

1. Use browser-control skill to list open Chrome tabs.
2. Look for tabs with "acaflow" or "氢离子" in the title/URL.
3. If found: switch to the tab, verify the page is loaded and logged in. Done.
4. If NOT found: tell user "请在 Chrome 中打开 acaflow 和氢离子页面，然后告诉我。" Do not ask for URLs.
5. Run \pandoc --version\.
6. Run \python --version\.

Setup guide (only if user doesn't know how):
- Install Codex browser extension from Chrome Web Store if not already installed
- Open acaflow and log in
- Open 氢离子 (QingHydrogen) and log in

If platforms are still inaccessible after this: STOP. Never write from training data.

---

## Phase 0: Pre-flight Check (MANDATORY)

Before any other action, verify accessibility:

1. Confirm the user has acaflow open in Chrome and is logged in.
2. Confirm the user has 氢离子 open in Chrome and is logged in.
3. Confirm pandoc is installed: run `pandoc --version`.
4. Confirm Python 3 is available.
5. Optionally, check if Zotero is available: `python3 <zotero-plugin-root>/skills/zotero/scripts/zotero.py status --json`. This determines PATH A vs PATH B in Phase 4.7 — but does NOT block progress if unavailable.

If acaflow or 氢离子 are inaccessible due to network issues (common with GitHub/git protocol being blocked in some regions), note that the browser-based platforms may still work even when git push fails — they use different network paths.

**If you cannot confirm all four, report the specific blockers to the user and stop. Do not proceed.**

---

## Phase 1a: Core Association Map (Map ①)

**Start with only ONE map.** Build the map that captures the core association between the subject and the disease — the most direct epidemiological/observational/omics evidence.

Use the user's raw topic description as the starting point. Example: "肠道菌群与孤独症关联的队列与组学研究".

1. **Use browser control to open acaflow in Chrome.** Navigate to the map creation interface.
2. **Type the search query yourself** (e.g., "肠道菌群与孤独症关联的队列与组学研究") and create the map.
3. **Save immediately** (click the save button via browser control). Then take a screenshot.
4. **Review the clustering results** — what major themes emerged? What subtopics cluster together?

## Phase 1b: Title Refinement

**Now that you have real literature clusters, refine the title.**

Users often provide broad, informal topic descriptions (e.g., "肠道菌群与孤独症的关系"). A good review title should be specific, informed by the actual literature landscape, and reflect the article's conceptual structure.

### Title refinement steps:

1. **Examine Map ① clustering results.** What are the dominant subtopics? Are there clear mechanistic themes? Biomarker angles? Therapeutic directions?

2. **Propose 3 title candidates** in Chinese, each grounded in what the literature actually contains. The `"X与Y：A、B与C"` format (colon + comma-separated dimensions) is acceptable for article titles — it differs from the banned colon format for section headings.

3. **Present candidates to the user:**

> "基于 Map ① 的文献聚类，该领域主要围绕 [主题A]、[主题B]、[主题C] 展开。我建议以下三个标题方向：
> 1. [侧重全景式] — 覆盖机制、标志物、治疗三方面
> 2. [侧重机制] — 深挖分子通路
> 3. [侧重临床转化] — 聚焦诊断与治疗应用
> 你倾向哪个？或者想融合调整？"

4. **Once the title is locked**, use it to derive the remaining maps in Phase 1c. A refined title makes the map branching logic much more precise.

**Do NOT build Maps ②-⑤ with a vague user-supplied topic.** The title must be finalized before the remaining maps are created.

## Phase 1c: Remaining Maps (Map ②-⑤)

### Map Architecture — Derive from the Finalized Title

Read the finalized article title (from Phase 1b) and extract its conceptual dimensions. The standard decomposition template:

```
文章标题
├── ① 核心关联：该领域最直接的流行病学/观察性/组学证据
├── ② 发病机制：开放检索，由acaflow自动聚簇（不预设子分类）
├── ③ 生物标志物/临床转化：诊断、预后、疗效预测等
├── ④ 干预/治疗（天然）：已有的临床前与临床干预证据
└── ⑤ 干预/治疗（工程）：合成生物学、递送系统、改造策略
```

**Adapt, don't copy.** Number of maps depends on the topic:
- A basic science topic with no therapy angle → 3–4 maps
- A translational topic → 4–5 maps
- A mechanism-heavy topic → split mechanism into two maps
- A topic with only one therapeutic modality → merge maps ④+⑤

**Map titles should be in the same language as the target article.** For Chinese reviews, write map titles in Chinese.

### Map Naming Guidelines

- **Broad enough** for acaflow to generate meaningful clusters, **narrow enough** to stay on topic.
- **Map ② (mechanism) is always open-ended.** Do not predefine subcategories. Let acaflow's clustering determine the branch structure. The title should be simply "发病机制" or equivalent — no qualifiers.

### acaflow Operational Rules

1. **Maximum 3 saved maps at a time.** acaflow will refuse to create a new map when the limit is reached.
2. **Save every map immediately** after generation completes. Before attempting to create a new map, double-check that the current one is saved — look for a confirmation indicator in the UI.
3. **Screenshot each map after saving.** This is your permanent record of the clustering structure.
4. **Delete maps to make room** via the three-dot menu on each map card. Only the user can perform this action — the AI cannot click UI elements.
5. **Double-check before asking user to delete** — there is no trash recovery.

### When acaflow Refuses to Create a New Map

If acaflow shows an error or the "new map" button is unresponsive, the 3-map limit is likely reached. In this case:

1. **Immediately verify which maps are currently saved.** List them out for the user.
2. **Confirm the most recently generated map is saved.** If unsure, ask the user to verify.
3. **Prompt the user to delete an old map:**

> "acaflow 已达到 3 张地图上限，无法创建新地图。请手动删除一张已不需要的地图：在左侧地图列表中找到要删除的地图，点击卡片右上角三个点的按钮 → 选择删除。当前已保存的地图有：[列出地图名称]。建议删除最早的那张。删除后告诉我，我继续创建新地图。"

4. **Wait for user confirmation** that the deletion is done before attempting to create the next map.
5. **Never assume deletion succeeded** — always verify with the user.

### Extracting References from acaflow Maps

Each acaflow map includes a built-in literature list ("文献" tab) showing the papers that form the clusters. These references should be collected — they complement the later 氢离子 search and provide a baseline reference pool.

1. **After saving a map, switch to the "文献" tab** (usually next to the cluster visualization).
2. **Scroll to the bottom** of the browser page to trigger lazy loading.
3. **Click "查看更多"** (or equivalent load-more button) repeatedly until all references are visible.
4. **Record every reference** into the master log. At minimum capture: title, authors, journal, year, DOI (if shown).
5. **Note which map each reference came from** — this helps with Phase 4 deduplication and section grouping.

If the reference list is very long (50+ papers), prioritize papers that appear in the core clusters (largest nodes or most central in the map). Papers in peripheral clusters are lower priority but should still be scanned for relevance.

### Map Rotation Pattern

```
Create Map 1 → Save + Screenshot
Create Map 2 → Save + Screenshot
Delete Map 1 → Create Map 3 → Save + Screenshot
Delete Map 2 → Create Map 4 → Save + Screenshot
Delete Map 3 → Create Map 5 → Save + Screenshot
```

---

## Phase 2: Outline Generation

After all maps are complete:

1. **Aggregate** clustering results from all maps into one document.
2. **Identify major themes** — these become sections.
3. **Draft a preliminary outline.** Flow: background → core evidence → mechanisms → translational applications → outlook.

### Determining Target Length and Reference Count

**If the user has not explicitly specified word count and reference count, the AI must determine reasonable targets from the literature landscape — not default to minimal values.**

1. **Assess literature volume:** Count papers already collected from acaflow maps. More literature → longer review.
2. **Apply field norms:** Chinese biomedical reviews typically range 12,000–20,000 characters with 100–180 references. A 5-map review inherently targets the upper end.
3. **Calculate from structure:** Allocate proportionally — introduction ~10%, background ~15%, core evidence ~20%, mechanisms ~25%, biomarkers ~15%, therapy ~10%, outlook ~5%.
4. **Propose to user:** "基于 acaflow 地图规模（已收录约 N 篇），建议正文 ~15,000 字、参考文献 ~140 篇。有偏好吗？"
5. **Do NOT silently set low targets.** A 5-map review is a major undertaking.

**This outline is preliminary.** It will be refined after literature search (Phase 4.5).

---

## Phase 3: Deep Search with 氢离子

### What 氢离子 Is

氢离子 is a browser-based AI literature search tool with its own curated database. **The AI operates it through browser control — typing queries, reading responses, and scrolling to load more.**
- **Access:** Chrome browser, chat-style interface (AI navigates and controls it)
- **Capacity:** ~8–12 references per response
- **Context:** Maintains conversation context within a session
- **Saturation signal:** After several rounds, it recycles previously shown references → sub-branch exhausted
- **Language:** Queries work best in Chinese for biomedical topics

### Strategy: Per-Branch, Multi-Round

**This is the most important phase. Do not rush it. Do not use broad queries.**

For each sub-branch from the acaflow maps:

1. **First query** — narrow and specific. NOT "噬菌体与结直肠癌" but "CRC患者粪便噬菌体组多样性变化队列研究".
2. **Record all references** in a structured log file (`hydrogen-refs-log.md`).
3. **Follow up** with distinct angles (3–5 rounds per sub-branch).
4. **Stop when saturated** — fewer than 3 new refs per round or clear recycling.
5. **Log discipline:** Tag each entry with the branch it supports.

### Coverage Audit (MANDATORY — do not skip)

**Before declaring Phase 3 complete, you MUST pass this audit. The audit is not optional.**

1. **List every sub-branch from every acaflow map.** This includes small/peripheral branches, not just the largest clusters. A 5-map acaflow run typically produces 12–25 sub-branches total.

2. **Verify each sub-branch has been searched.** Mark each as ✓ (done) or ✗ (missed). If any sub-branch is marked ✗, go back and search it now.

3. **Verify minimum rounds per sub-branch:**
   - Large/central clusters: **minimum 4 rounds** from distinct angles
   - Medium clusters: **minimum 3 rounds**
   - Small/peripheral clusters: **minimum 2 rounds**
   - If a sub-branch has fewer rounds than required, continue searching.

4. **Verify reference yield:**
   - Large clusters should yield 25+ unique references each
   - Medium clusters: 15+ unique references
   - Small clusters: 5+ unique references
   - If any cluster is below threshold, reformulate queries and search more.

5. **Red flag — do NOT do this:**
   - ❌ Searching only the top 2–3 largest branches and calling it done
   - ❌ One round per branch and moving on
   - ❌ Accepting "no results found" after one query without trying reformulations
   - ❌ Skipping maps ④ and ⑤ because "therapy isn't the main focus"

6. **Present audit results to user** before moving to Phase 4:

> "Phase 3 搜索覆盖审计：
> - Map ①: 4/4 分支完成 (共 N 篇)
> - Map ②: 6/6 分支完成 (共 N 篇)
> - Map ③: 3/3 分支完成 (共 N 篇)
> - Map ④: 2/2 分支完成 (共 N 篇)
> - Map ⑤: 2/2 分支完成 (共 N 篇)
> - 总计: 17 分支, XX 篇文献
> 是否继续进入去重验证阶段？"

If the total reference count is significantly below the Phase 2 target, go back and search more before proceeding.

---

## Phase 4: Reference Assembly

### 4.1 Deduplicate
Cross-reference all entries in the master log — this includes both acaflow-extracted references (Phase 1) and 氢离子 search results (Phase 3). Merging these two sources typically yields the most comprehensive reference pool. Remove duplicates.

### 4.2 Verify DOIs
Every reference must have a verified DOI:
1. Check DOI via `https://api.crossref.org/works/DOI_HERE`
2. Or search via PubMed E-utility: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TITLE[title]`
3. If unverifiable → remove the reference. Do not guess.

### 4.3 Group by Section
Tag each reference with its supporting section(s). Many references support multiple sections.

### 4.4 Recency Audit (MANDATORY)

**A review is only as current as its references.**

| Requirement | Threshold |
|-------------|-----------|
| Published within last 2 years | **≥ 40%** of total |
| Published within last 1 year | **≥ 20%** of total |

If thresholds not met → go back to Phase 3 with time-bounded queries. Do not pad with old references.

### 4.5 Citation Quality Requirements

1. **Primary over secondary.** Cite original research, not other reviews (max 10% reviews).
2. **Peer-reviewed only.** No preprints, no conference abstracts without full text.
3. **Human data over animal/cell-line** when both exist.
4. **Large-N over small-N.** Do not rest broad claims on N=20 studies alone.
5. **No predatory journals.** Verify indexing in PubMed/SCI.
6. **DOI required.** Zero exceptions.

### 4.6 Generate Importable Reference Files (MANDATORY)

**Always generate structured reference files. Even if Zotero isn't used for citation, the user needs importable files.**

1. **Generate `references.bib`** — BibTeX with all verified refs. Each entry: BibTeX key, full authors, title, journal, year, volume, pages, DOI.
2. **Generate `references.ris`** — RIS format fallback.
3. **Save both** in the working directory.

### 4.7 Detect Zotero and Choose Citation Path

```bash
python3 <zotero-plugin-root>/skills/zotero/scripts/zotero.py status --json
```

**PATH A — Zotero available:**
1. Import: `zotero.py import-bibtex --file references.bib --yes`
2. Phase 5: cite with `[@bibtex_key]` in Markdown
3. Phase 6: `pandoc ... --csl=nature.csl --bibliography=references.bib`

**PATH B — No Zotero:**
1. Phase 5: use manual `[1]`, `[2]` numbering
2. Phase 6: append formatted reference list, plain pandoc
3. Tell user: "未检测到 Zotero，使用手动编号。`references.bib` 和 `references.ris` 已生成，可随时导入任意文献管理软件。"

### 4.8 Confirm with User

Present: total count, per-section count, recency breakdown, citation path chosen, under-referenced sections, removed refs. Get approval.

---

## Phase 5: Manuscript Writing

**Only begin after Phase 4 is complete and approved.**

Use `nature-writing` as a sub-component for composition — it is NOT a replacement for the full pipeline.

### 5.1 Required Manuscript Elements (Nature-Level)

A complete review manuscript must include ALL of the following. Do not skip any.

**① Abstract (摘要)**
- 200–300 Chinese characters
- Structured: background (1–2 sentences), scope (what this review covers), key findings (3–5 major conclusions), outlook (1 sentence)
- Self-contained — a reader should understand the review's contribution from the abstract alone
- Place at the very beginning of the manuscript, before the introduction

**② Introduction (引言)**
- Opens with the broad significance of the field
- Narrows to the specific gap this review addresses
- Ends with a clear statement of scope: "本文系统综述了……重点探讨了……"
- No sub-headings within the introduction

**③ Key Points box (要点)**
- 3–5 bullet points summarizing the review's most important messages
- Each bullet: one finding/conclusion, not a topic description
- Place after the abstract in a callout box format:
  ```
  > **要点**
  > - 关键发现1……
  > - 关键发现2……
  ```



**⑥ Outstanding Questions (待解决问题)**

End the review with a dedicated section listing 4–7 explicitly stated unanswered questions:
```
## 待解决问题

1. ……的具体分子机制仍不清楚。
2. ……在……中的作用缺乏直接证据。
3. ……的长期安全性和有效性有待验证。
4. ……的因果关系尚未通过前瞻性研究建立。
```
Each question must be grounded in a specific gap identified in the literature — not generic "more research is needed."

### 5.2 Dynamic Adjustment During Writing

Writing rarely follows the outline rigidly. The AI should exercise judgment within these boundaries:

**Supplemental search (自主补搜):**
- If a paragraph lacks supporting evidence → pause writing, go back to 氢离子 for 1–3 targeted rounds on the specific gap.
- Verify new DOIs and add to the reference pool. Do not restart Phase 3 — this is a surgical fix, not a full re-search.
- After supplementing, resume writing from where you left off.

**Outline adjustment (动态调纲):**
- Sub-section level: merge, split, or reallocate word count → AI decides autonomously. No need to ask.
- Major section level: add, remove, or significantly restructure → ask the user first.

**Trust the maps (信地图):**
- If acaflow clustered a branch, the literature exists. Struggle to write it usually means Phase 3 didn't search deeply enough — not that the branch should be cut.
- Default action: go back and search more. Do not silently delete sections from the outline.

### 5.3 Citation Method

| PATH A (Zotero) | PATH B (Manual) |
|---|---|
| `[@smith2025]` in Markdown | `[1]`, `[2]` inline |
| Use `zotero.py cite` to insert | Number by first appearance |
| Pandoc formats bibliography | Manual reference list at end |

### 5.4 Prohibited Patterns

| Pattern | Fix |
|---------|-----|
| Section titles with colons ("名词：描述") | Concise noun phrases |
| Journal names in body text | Citation only |
| Parenthetical years "（2019）" | Remove entirely |
| Reference stacking (5+ per sentence) | Synthesize across sentences |
| One ref per statement listing | Synthesize across refs |
| Citing unverified references | Only from verified collection |
| Writing from training data | **NEVER** |
| No abstract | **Required — see 5.1-①** |


### 5.5 Writing Quality Standards

- **Paragraph unity:** One idea per paragraph. Topic sentence → evidence → transition.
- **Verb calibration:** demonstrate > reveal > show > suggest > correlate.
- **Synthesis over inventory:** What do papers collectively teach us?
- **Audience awareness:** Write for a broad scientific audience — scientists outside your subfield should understand every paragraph.
- **Abbreviation discipline:** Expand ALL abbreviations on first use. Do not assume readers know field-specific acronyms. Example: "结直肠癌（colorectal cancer, CRC）" on first mention, then "CRC" thereafter.

---

## Phase 6: Formatting and docx Output

### PATH A — Zotero + Pandoc-citeproc

```markdown
# 文章标题

> **要点**
> - 关键发现1……
> - 关键发现2……

**摘要：** 200–300字中文摘要……

## 引言

正文。引用 [@smith2025]。多项引用 [@smith2025; @jones2026]。

*图1. 概述图说明……*

## 大节标题

### 小节标题

## 待解决问题

1. ……
2. ……

## 参考文献
```

```bash
pandoc manuscript.md -o manuscript.docx --csl=nature.csl --bibliography=references.bib --from=markdown --to=docx
```

### PATH B — Manual Numbering

```markdown
# 文章标题

> **要点**
> - 关键发现1……

**摘要：** ……

## 参考文献

[1] Author A, et al. Title. Journal, Year, Volume: Pages. DOI: xxx

[2] Author B, et al. Title. Journal, Year, Volume: Pages. DOI: xxx
```

- **Blank line between each `[N]` entry** — critical for pandoc paragraph separation.
- Pandoc: `pandoc manuscript.md -o manuscript.docx --from=markdown --to=docx`

### Obtaining nature.csl (PATH A)

```bash
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl" -OutFile "nature.csl"
```

### Post-Processing (Both Paths)

`scripts/fix_docx_fonts.py`:

| Property | Value |
|----------|-------|
| Chinese font | SimSun (宋体) |
| Latin font | Times New Roman |
| Line spacing | 1.5× |
| Alignment | Justified |
| H1 | 22pt bold |
| H2 | 16pt bold |
| H3 | 14pt bold |
| Body | 12pt |

### Windows Caveats
- Chinese paths → copy to `$env:TEMP` before Python
- PowerShell: use `if/else`, no ternary


---

## Common Problems

| Phase | Problem | Action |
|-------|---------|--------|
| 0 | acaflow/氢离子 inaccessible | Guide user: Chrome → Codex 插件 → acaflow 登录 → 氢离子 登录 |
| 0 | "acaflow" skill not found | Use THIS skill — it IS the acaflow workflow |
| 1 | Map limit reached | Prompt user to manually delete an old map |
| 1 | Unsaved map lost | Regenerate; always save immediately |
| 1 | acaflow CAPTCHA | Tell user to complete in Chrome; cannot auto-solve |
| 3 | 氢离子 CAPTCHA | Tell user to complete in Chrome; review existing refs while waiting |
| 3 | Too few refs per round | Continue multi-round (~10/round) |
| 3 | 氢离子 recycles refs | Branch saturated → move on |
| 3 | Skipping small branches | Run coverage audit; 2–4 rounds per branch |
| 4 | .bib generation fails | Verify all DOIs; fix malformed fields |
| 4 | Zotero import fails | Check Zotero running with local API (port 23119) |
| 5 | Reference/word count too low | Go back to Phase 2/3 |
| 5 | Citation key not in .bib | Search Zotero; add to .bib if missing |
| 5 | Reference hallucination | Only cite from verified collection |
| 5 | Writing from training data | **NEVER** |
| 5 | Missing abstract / figures / key points | See Phase 5.1 — these are mandatory |
| 6 | References run together | Blank line between each `[N]` entry |
| 6 | Pandoc citation errors | Check `[@key]` matches .bib keys exactly |
| 6 | Font not applying | Modify both styles.xml AND theme1.xml |
| 6 | Chinese path errors | Copy to `$env:TEMP` first |


---

## Key Principles

1. **Literature first, writing second.**
2. **Let acaflow cluster mechanisms.**
3. **Multi-round narrow search beats single broad search.**
4. **Verify DOIs before citing.**
5. **Revise the outline after search.**
6. **Always generate `references.bib` + `references.ris`.** Zotero-available → use it. No Zotero → manual numbering + deliver files.
7. **Format at the end.**
8. **Synthesize, don't list.**
9. **If acaflow or 氢离子 are unavailable, STOP.**
10. **This skill is the orchestrator.** nature-writing is a sub-component.
11. **Targets from literature, not laziness.**
12. **Every sub-branch, every time.** 12–25 branches, all covered.
13. **≥20% refs from last 1 year, ≥40% from last 2 years.**
14. **Quality beats quantity.**
15. **Mandatory manuscript elements.** Abstract, key points, and outstanding questions — always include these. Define all abbreviations on first use.

---

## Reference Management: File Inventory

```
project-dir/
├── refined-title.md           # Phase 1b output
├── acaflow-maps-summary.md    # Clustering from all maps
├── preliminary-outline.md     # Phase 2 output
├── hydrogen-refs-log.md       # Reference log (Phase 3)
├── hydrogen-answers.md        # 氢离子 narrative answers by branch
├── references-by-section.md   # Grouped refs (Phase 4)
├── verified-dois.md           # DOI verification results
├── references.bib             # BibTeX for import
├── references.ris             # RIS for import
├── manuscript.md              # Final markdown
├── manuscript.docx            # Final docx
└── nature.csl                 # Citation style (PATH A)
```






