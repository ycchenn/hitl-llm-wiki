---
title: S2 · InstructGPT 與 RLHF（Ouyang et al.）
type: source
sources: [S2]
updated: 2026-11-21
---
# S2 · Training language models to follow instructions with human feedback

**一句話**：ChatGPT 的前身之所以「聽得懂人話」，關鍵是讓**人類替答案排名**，再用這些排名訓練模型。 [S2]

- 出處：Ouyang et al., NeurIPS 2022（arXiv:2203.02155）；OpenAI 部落格 2022-01-27。原始卡片：`raw/s2-instructgpt.md`
- 類型：學術論文 + 官方說明

## 重點
- 模型變大不等於更符合使用者意圖；GPT-3 的訓練目標是預測下一個字，不是幫助使用者。 [S2]
- RLHF 三步驟：人寫示範 → 人替輸出排名、訓練獎勵模型 → 用獎勵模型做強化學習。 [S2]
- 1.3B 參數的 InstructGPT 在人類評估中勝過 175B 的 GPT-3，參數少 100 倍。 [S2]
- 較少編造事實、毒性略降，但仍會犯簡單錯誤。 [S2]
- 選人類偏好當獎勵，是因為「好不好、安不安全」很主觀，難用自動指標衡量。 [S2]

## 用在哪些頁面
- [RLHF](../concepts/rlhf.md)
- [Human-in-the-loop 是什麼](../concepts/human-in-the-loop.md)
