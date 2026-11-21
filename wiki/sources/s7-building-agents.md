---
title: S7 · Building effective agents（Anthropic）
type: source
sources: [S7]
updated: 2026-11-21
---
# S7 · Building effective agents

**一句話**：AI Agent 會自己規劃、執行多步驟任務，因此需要「檢查點」讓人介入，以及「停止條件」防止失控。 [S7]

- 出處：Schluntz & Zhang, Anthropic Engineering, 2024-12。原始卡片：`raw/s7-anthropic-agents.md`
- 類型：業界實務文章

## 重點
- 工作流程（固定路徑）vs. 代理（LLM 自己決定流程）。 [S7]
- 先用最簡單的解法，必要時才加複雜度。 [S7]
- Agent 每一步要從環境取得真實回饋；可在檢查點或卡住時暫停等人。 [S7]
- 加上停止條件，例如最大迭代次數。 [S7]

## 用在哪些頁面
- [AI Agent 的人類檢查點](../concepts/agent-checkpoints.md)
- [Human-in-the-loop 是什麼](../concepts/human-in-the-loop.md)
