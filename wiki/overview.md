---
title: 總覽：Human-in-the-loop AI
type: overview
sources: [S1, S2, S3, S4, S5, S6, S7, S8]
updated: 2026-11-21
---
# 總覽：Human-in-the-loop AI

**核心問題**：AI 越來越強，人還要不要、該在哪裡、怎麼參與？（綜合）

## 一張圖看懂（綜合）
```
訓練 AI 時 ──── 人提供示範與排名（RLHF） ─────────────── S2
使用 AI 時 ──── 人檢查、推翻 ── 但會有自動化偏誤 ──────── S4 S5
              └─ 介面要幫人介入（18 條準則） ─────────── [S3]
              └─ 法律要求能理解、推翻、停止 ───────────── S6
AI 自己做事時 ─ 檢查點 + 停止條件 ──────────────────────── S7
怎麼分配人的注意力 ─ 看信心、看後果、看人力 ──────────── S8
```

## 主要結論
1. HITL 不是只有一種：依「誰掌控」可分成主動學習、互動式學習、機器教學。 [S1] → [HITL 是什麼](concepts/human-in-the-loop.md)
2. 你每天用的聊天機器人，就是靠人類排名訓練出來的。 [S2] → [RLHF](concepts/rlhf.md)
3. 有人在迴圈裡 ≠ 安全：人會過度相信 AI，而且訓練擋不住。 [S4] [S5] → [自動化偏誤](concepts/automation-bias.md)
4. 好的設計讓人「看得懂、關得掉、改得動」。 [S3] → [設計準則](concepts/design-guidelines.md)
5. 法律開始要求有效監督，不只是形式上有人。 [S6] → [法律中的人類監督](concepts/human-oversight-law.md)
6. Agent 時代要設計檢查點與停止條件。 [S7] → [Agent 檢查點](concepts/agent-checkpoints.md)
7. 人的注意力有限，應該花在 AI 沒把握、後果嚴重的地方。 [S8] → [什麼時候該檢查](concepts/when-to-review.md)

## 尚待補充
- 真實（非合成）資料的 HITL 成效研究。
- 對話式 AI（如 ChatGPT）使用者端的自動化偏誤研究。
