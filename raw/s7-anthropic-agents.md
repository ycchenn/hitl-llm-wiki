# S7 · Building effective agents

- **作者**：Erik Schluntz, Barry Zhang（Anthropic）
- **出處**：Anthropic Engineering 部落格，2024-12-19（頁面註明工具生態已有變化）
- **網址**：https://www.anthropic.com/engineering/building-effective-agents
- **類型**：業界實務文章
- **取得日期**：2026-11-21

## 閱讀筆記（萃取，非原文）
- 區分兩種 agentic 系統：
  - **工作流程（workflows）**：LLM 與工具依照預先寫好的路徑串接；
  - **代理（agents）**：LLM 自己決定流程與要用哪些工具。
- 建議先找最簡單的解法，只有在需要時才增加複雜度。
- Agent 從人類的指令或討論開始；任務清楚後自主規劃與執行，必要時回頭找人要資訊或判斷。
- 執行中每一步都要從環境取得「真實回饋」（ground truth，例如工具結果、程式執行結果）來評估進度。
- 可以在**檢查點（checkpoints）**或遇到阻礙時暫停，等待人類回饋。
- 常加上**停止條件**（例如最大迭代次數）以保持控制。
