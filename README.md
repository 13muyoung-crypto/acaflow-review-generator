# Acaflow Review Generator

基于 **acaflow** 文献地图 + **氢离子** 深搜 + **nature-writing** 撰写的零幻觉中文综述生成工作流。

## 工作流

```
acaflow 文献地图 → 汇总大纲 → 氢离子逐分支深搜 → 去重验证DOI → nature-writing撰写 → pandoc+csl→docx
```

## 适用场景

- 生物医学综述撰写
- 需要系统文献检索、零引用幻觉的学术写作
- 目标输出为排版整齐的 `.docx` 文件

## 依赖工具

| 工具 | 用途 |
|------|------|
| acaflow | 文献地图构建与自动聚类 |
| 氢离子 | 逐分支多轮深搜 |
| nature-writing (Codex Skill) | 学术写作质量管控 |
| pandoc + nature.csl | Markdown → docx 转换 |
| fix_docx_fonts.py | 字体/行距/对齐后处理 |

## 文件结构

```
acaflow-review-generator/
├── SKILL.md                     # 完整工作流指令
├── agents/openai.yaml           # UI 元数据
└── scripts/
    └── fix_docx_fonts.py        # docx 格式后处理脚本
```

## 安装

```bash
# 将整个文件夹复制到 Codex skills 目录
cp -r acaflow-review-generator ~/.codex/skills/
```

然后在 Codex 中说"用 acaflow review generator 写综述"即可触发。
