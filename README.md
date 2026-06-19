# Acaflow Review Generator

基于 **acaflow** 文献地图 + **氢离子** 深搜 + **nature-writing** 撰写的零幻觉中文综述生成工作流。

> ⚠️ 使用前提：acaflow 和 氢离子 两个外部平台必须在 Chrome 中可访问。

## 触发词

在 Codex 中说以下任意关键词即可触发：`acaflow`、`写综述`、`综述生成`、`写review`、`用acaflow`、`acaflow综述`

## 工作流

```
acaflow 文献地图 → 汇总大纲 → 氢离子逐分支深搜 → 去重验证DOI → nature-writing撰写 → pandoc→docx
```

## 适用场景

- 中文综述撰写（任意生命科学/医学主题）
- 需要系统文献检索、零引用幻觉的学术写作
- 目标输出为排版整齐的 `.docx` 文件

## 依赖工具

| 工具 | 用途 | 类型 |
|------|------|------|
| acaflow | 文献地图构建与自动聚类 | Chrome 浏览器 |
| 氢离子 (QingHydrogen) | 逐分支多轮深搜 | Chrome 浏览器 |
| nature-writing (Codex Skill) | 学术写作质量管控 | Codex Skill |
| pandoc | Markdown → docx 转换 | 命令行 |
| fix_docx_fonts.py | 字体/行距/对齐后处理 | Python 脚本 |

## 文件结构

```
acaflow-review-generator/
├── SKILL.md                     # 完整工作流指令
├── agents/openai.yaml           # UI 元数据
├── scripts/
│   └── fix_docx_fonts.py        # docx 格式后处理脚本
├── .gitignore
└── README.md
```

## 安装

```bash
# 将整个文件夹复制到 Codex skills 目录
cp -r acaflow-review-generator ~/.codex/skills/
```

## 常见问题

**Q: 说"acaflow的综述生成skill"没触发？**
A: 直接说 `acaflow` 或 `写综述` 即可。如果仍不触发，确认 skill 在 `~/.codex/skills/acaflow-review-generator/` 路径下。

**Q: acaflow/氢离子打不开？**
A: 这是硬性前提。两个平台不可用时，skill 会主动停止而非编造内容。
