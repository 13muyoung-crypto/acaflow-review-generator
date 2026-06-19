---
name: acaflow-review-generator
description: >
  Generate a Chinese scientific review article with zero hallucinations. This skill orchestrates a pipeline of external tools: acaflow (browser-based literature mapping platform) for building literature maps, 氢离子/QingHydrogen (browser-based AI deep search) for per-branch reference retrieval, nature-writing for manuscript composition, and pandoc for docx output. Use this skill when the user wants to write a comprehensive review with systematically verified references, or mentions "acaflow", "写综述", "综述生成", "写review", "acaflow综述", "用acaflow", "氢离子检索", or "文献地图写文章". IMPORTANT: acaflow is an external browser-based platform — this skill is the workflow that coordinates it, not acaflow itself. If you cannot find a skill named "acaflow", use THIS skill instead — it IS the acaflow review generation workflow.
---

# Acaflow Review Generator

> **This skill orchestrates a multi-phase pipeline. Do NOT skip phases. Do NOT write anything before Phase 5.**

## ⛔ CRITICAL: Before You Do Anything Else

### This skill depends on two external browser-based platforms:

| Platform | What it is | How to access |
|----------|------------|---------------|
| **acaflow** | Literature mapping with automatic clustering | Open in Chrome browser |
| **氢离子** (QingHydrogen) | AI-powered deep literature search (~10 refs/round) | Open in Chrome browser |

### Mandatory pre-flight check:

Before doing anything else, ask the user:

> "请确认以下三项：① Chrome 浏览器中已安装 Codex 插件；② acaflow 已在 Chrome 中登录；③ 氢离子 已在 Chrome 中登录。都准备好了吗？"

If the user says NO or is unsure, provide step-by-step setup instructions:

---

**Setup guide (provide to user if needed):**

```
Step 1: 打开 Chrome 浏览器
Step 2: 安装 Codex 浏览器插件（如未安装）
        → 在 Chrome 插件商店搜索 "Codex" 并安装
Step 3: 打开 acaflow 并登录
        → 网址由用户或机构提供，确保页面正常加载且已登录
Step 4: 打开 氢离子 (QingHydrogen) 并登录  
        → 网址由用户或机构提供，确保聊天界面可用
Step 5: 回到 Codex，重新发送综述写作指令
```

After the user confirms all three are ready, proceed to verify:
- Run `pandoc --version` to confirm pandoc is installed
- Run `python --version` or locate Python 3 for post-processing

---

**If any of the three platforms is still inaccessible after setup attempts — STOP.** Tell the user which platform is blocking progress and wait for resolution. Never fall back to writing from training data. A review without systematic literature retrieval is worse than no review at all.

---

## Workflow Overview

```
Phase 0: 前置检查 (acaflow + 氢离子 可用性)
    ↓
Phase 1: acaflow 文献地图构建 (3-5张地图)
    ↓
Phase 2: 汇总大纲
    ↓
Phase 3: 氢离子 逐分支多轮深搜
    ↓
Phase 4: 去重 → DOI验证 → 大纲修正 → 用户确认
    ↓
Phase 5: nature-writing 撰写 (nature-writing 是本阶段的子组件，不是整个流程的替代品)
    ↓
Phase 6: pandoc → docx + 格式后处理
```

**Each phase depends on the output of the previous one.** You cannot write (Phase 5) before searching (Phase 3). You cannot search before mapping (Phase 1).

---

## Phase 0: Pre-flight Check (MANDATORY)

Before any other action, verify accessibility:

1. Confirm the user has acaflow open in Chrome and is logged in.
2. Confirm the user has 氢离子 open in Chrome and is logged in.
3. Confirm pandoc is installed: run `pandoc --version`.
4. Confirm Python 3 is available for the post-processing script.

If acaflow or 氢离子 are inaccessible due to network issues (common with GitHub/git protocol being blocked in some regions), note that the browser-based platforms may still work even when git push fails — they use different network paths.

**If you cannot confirm all four, report the specific blockers to the user and stop. Do not proceed.**

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
- A basic science topic with no therapy angle → 3–4 maps
- A translational topic → 4–5 maps
- A mechanism-heavy topic → split mechanism into two maps
- A topic with only one therapeutic modality → merge maps ④+⑤

**Map titles should be in the same language as the target article.** For Chinese reviews, write map titles in Chinese.

### Map Naming Guidelines

- **Broad enough** for acaflow to generate meaningful clusters, **narrow enough** to stay on topic.
- **Map ② (mechanism) is always open-ended.** Do not predefine subcategories. Let acaflow's clustering determine the branch structure. The title should be simply "发病机制" or equivalent — no qualifiers.

### acaflow Operational Rules

1. **Maximum 3 saved maps at a time.**
2. **Save every map immediately** after generation completes.
3. **Screenshot each map after saving.**
4. **Delete maps to make room** via the three-dot menu on each map card.
5. **Double-check before deleting** — there is no trash recovery.

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
4. **Ask the user** for target length. Assign proportional allocation.
5. **Review with the user** before proceeding.

**This outline is preliminary.** It will be refined after literature search (Phase 4.5).

---

## Phase 3: Deep Search with 氢离子

### What 氢离子 Is

氢离子 is a browser-based AI literature search tool with its own curated database:
- **Access:** Chrome browser, chat-style interface
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

### Coverage Audit

Before declaring search complete:
- Has every sub-branch from every acaflow map been queried with at least 2–3 rounds?
- Are earlier maps (core evidence, mechanisms) searched more thoroughly?
- Any obvious gaps?

---

## Phase 4: Reference Assembly

### 4.1 Deduplicate
Cross-reference all entries in the master log. Merge duplicates.

### 4.2 Verify DOIs
Every reference must have a verified DOI:
1. Check DOI via `https://api.crossref.org/works/DOI_HERE`
2. Or search via PubMed E-utility
3. If unverifiable → remove the reference

### 4.3 Group by Section
Tag each reference with its supporting section(s).

### 4.4 Confirm with User
Present: total count, count per section, under-referenced sections, removed references.

### 4.5 Adapt the Outline
Based on what was actually found:
- Sections with abundant literature → split
- Sparse sections → merge or trim
- New themes → new sections
- Adjust character allocation

---

## Phase 5: Manuscript Writing

**Only begin writing after Phase 4 is complete and approved by the user.**

Use the `nature-writing` skill for composition. Note: nature-writing is a **sub-component** invoked during this phase — it is NOT a substitute for the entire workflow. Phases 1–4 (literature retrieval and verification) must be completed before nature-writing is used.

### Reference Format

Manual inline numbering: `[1]`, `[2]`, `[3]`. Numbered sequentially by first appearance. Reference list at end uses `[N]` format, one entry per line, blank lines between entries.

### Prohibited Patterns

| Pattern | Fix |
|---------|-----|
| Section titles with colons ("名词：描述") | Concise noun phrases |
| Journal names in body text | Reference numbers only |
| Parenthetical years "（2019）" | Remove entirely |
| Reference stacking (5+ per sentence) | Break into synthesis across sentences |
| One ref per statement listing | Synthesize across multiple refs |
| Citing unread/unverified references | Only cite from the verified collection |
| **Writing from training data instead of retrieved literature** | **NEVER do this** |

### Writing Quality Standards

- **Paragraph unity:** One controlling idea per paragraph.
- **Verb calibration:** demonstrate > reveal > show > suggest > correlate with.
- **Synthesis over inventory:** Explain what papers collectively teach us, not what each paper individually found.

---

## Phase 6: Formatting and docx Output

### Markdown Structure

```markdown
# 文章标题

## 大节标题

正文。引用用 [1]、[2,3] 格式……

### 小节标题

更多正文……

## 参考文献

[1] Author A, et al. Title. Journal, Year, Volume: Pages. DOI: xxx

[2] Author B, et al. Title. Journal, Year, Volume: Pages. DOI: xxx
```

- `#` title, `##` major sections, `###` sub-sections
- Blank line between each `[N]` reference entry (critical for pandoc)
- Superscript: `10^12^`

### Pandoc Command

```bash
pandoc manuscript.md -o manuscript.docx --from=markdown --to=docx
```

No `--csl` or `--bibliography` — references are manually formatted.

### Post-Processing

Use `scripts/fix_docx_fonts.py`:

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

- Chinese paths → copy to `$env:TEMP` before Python processing
- PowerShell: no ternary operators, use `if/else`

---

## Common Problems

| Phase | Problem | Action |
|-------|---------|--------|
| 0 | acaflow/氢离子 inaccessible | Guide user through setup: Chrome → Codex 插件 → acaflow 登录 → 氢离子 登录 → 重试 |
| 0 | "acaflow" skill not found | Use THIS skill (acaflow-review-generator) — it IS the acaflow workflow |
| 1 | Map limit reached | Delete oldest map via three-dot menu |
| 1 | Unsaved map lost | Regenerate; always save immediately |
| 3 | Too few refs per round | Normal — continue multi-round (~10/round) |
| 3 | 氢离子 recycles refs | Sub-branch saturated → move on |
| 3 | Missing DOIs | Flag for Phase 4 verification |
| 5 | Reference hallucination | Only cite from verified collection |
| 5 | Writing from training data | **NEVER** — if literature isn't ready, go back to Phase 3 |
| 6 | References run together | Blank line between each `[N]` entry |
| 6 | Font not applying | Modify both styles.xml AND theme1.xml |
| 6 | Chinese path errors | Copy to `$env:TEMP` first |

---

## Key Principles

1. **Literature first, writing second.** Complete all retrieval and verification before opening the manuscript.
2. **Let acaflow cluster mechanisms.** Do not impose a preset framework.
3. **Multi-round narrow search beats single broad search.**
4. **Verify DOIs before citing.** Remove, don't guess.
5. **Revise the outline after search.**
6. **Format at the end.**
7. **Synthesize, don't list.**
8. **If acaflow or 氢离子 are unavailable, STOP.** Never substitute with training data.
9. **This skill is the orchestrator.** nature-writing is a sub-component used in Phase 5, not a replacement for the full pipeline.

---

## Reference Management: File Inventory

```
project-dir/
├── acaflow-maps-summary.md    # Clustering results from all maps
├── preliminary-outline.md     # Phase 2 output
├── hydrogen-refs-log.md       # Master reference log (Phase 3)
├── references-by-section.md   # Grouped references (Phase 4)
├── verified-dois.md           # DOI verification results
├── manuscript.md              # Final markdown (Phase 5)
├── manuscript.docx            # Final output (Phase 6)
└── nature.csl                 # Citation style (downloaded once)
```


