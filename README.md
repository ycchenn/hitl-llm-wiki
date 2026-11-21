# Human-in-the-loop AI · LLM Wiki + 教學 HTML 簡報

🌐 **網站**：<https://ycchenn.github.io/hitl-llm-wiki/>
🎞️ **簡報**：<https://ycchenn.github.io/hitl-llm-wiki/slides/>

依 Andrej Karpathy 的 **LLM Wiki** 模式，先用 8 份資料建立一個由 LLM 維護的知識庫，
再**只從這個 Wiki** 產生一份給「會用 ChatGPT、但不懂原理的人」看的中文教學簡報。

## 結構

```
CLAUDE.md          Schema：LLM 維護 Wiki、產生簡報時要遵守的規則（v2）
raw/               ① 原始資料卡片（S1–S8，書目 + 網址 + 閱讀筆記）
wiki/              ② LLM 維護的 Wiki
  index.md           目錄（查詢時第一個讀）
  log.md             討論、ingest、檢查的完整時間序紀錄
  overview.md        總覽
  sources/           每份資料一頁
  concepts/          每個概念一頁
slides/
  outline.md         簡報大綱（每張投影片 ↔ Wiki 頁面）
  index.html         教學簡報
pipeline/
  lint_wiki.py       Wiki 健康檢查（結構 + 數字可追溯）
  check_slides.py    簡報檢查（數字、字數、來源頁腳）
  build_site.py      把 Markdown 轉成網頁
docs/
  workflow.md        Loop / Graph 設計（含流程圖）
  run-log.md         實際執行與檢查紀錄
  reflection.md      反思
```

## 執行

```bash
python3 pipeline/lint_wiki.py      # ✓ lint 通過：18 頁、8 份來源
python3 pipeline/check_slides.py   # ✓ 簡報檢查通過：13 張投影片，皆可追溯到 Wiki
pip install markdown && python3 pipeline/build_site.py
```

## 來源

| 代號 | 資料 |
|---|---|
| S1 | Mosqueira-Rey et al. (2023). Human-in-the-loop machine learning: a state of the art. *Artif Intell Rev* 56. |
| S2 | Ouyang et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. |
| S3 | Amershi et al. (2019). Guidelines for Human-AI Interaction. CHI. |
| S4 | Parasuraman & Manzey (2010). Complacency and Bias in Human Use of Automation. *Human Factors* 52(3). |
| S5 | Wickens, Clegg, Vieane & Sebok (2015). Complacency and Automation Bias in the Use of Imperfect Automation. *Human Factors* 57(5). |
| S6 | EU AI Act (Regulation 2024/1689) Article 14; Digital Omnibus on AI (2026). |
| S7 | Schluntz & Zhang (2024). Building effective agents. Anthropic. |
| S8 | 陳宥錡. AI-Assisted Emergency Department Triage Simulation. GitHub. |
