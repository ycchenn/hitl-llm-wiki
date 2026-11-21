---
title: Human-in-the-loop（HITL）是什麼
type: concept
sources: [S1, S2, S7]
updated: 2026-11-21
---
# Human-in-the-loop（HITL）是什麼

## 定義
讓人類在 AI 系統的建立或運作過程中持續參與，而不是「模型做完就放手」。 [S1]
目標有兩個：讓 AI 更好，也讓人更有效率。 [S1]

## 三種模式：誰說了算？
| 模式 | 誰掌控 | 例子（綜合） |
|---|---|---|
| 主動學習（active learning） | 系統：挑出最沒把握的資料請人標註 | 系統只把看不懂的照片丟給人標 |
| 互動式機器學習（interactive ML） | 人機頻繁來回 | 使用者一邊修正、模型一邊更新 |
| 機器教學（machine teaching） | 領域專家：決定教什麼 | 醫師挑選教學案例 |

分類依據見 [S1](../sources/s1-hitl-ml-survey.md)。 [S1]

## 人可以出現在三個階段（綜合）
1. **訓練時**：人提供示範與評分，例如 [RLHF](rlhf.md)。 [S2]
2. **使用時**：人檢查、推翻 AI 的輸出，見 [自動化偏誤](automation-bias.md) 與 [法律中的人類監督](human-oversight-law.md)。
3. **執行任務時**：AI Agent 在檢查點停下來等人，見 [AI Agent 的人類檢查點](agent-checkpoints.md)。 [S7]

## 相關
- [什麼時候該讓人檢查 AI？](when-to-review.md)
- [好的 HITL 設計準則](design-guidelines.md)
