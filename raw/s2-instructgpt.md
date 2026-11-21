# S2 · Training language models to follow instructions with human feedback（InstructGPT）

- **作者**：Long Ouyang, Jeff Wu, Xu Jiang 等 20 人（OpenAI）
- **出處**：NeurIPS 2022；arXiv:2203.02155；OpenAI 部落格〈Aligning language models to follow instructions〉（2022-01-27）
- **網址**：https://arxiv.org/abs/2203.02155 、 https://openai.com/index/instruction-following/
- **類型**：學術論文 + 官方說明
- **取得日期**：2026-11-21

## 閱讀筆記（萃取，非原文）
- 問題：把模型變大不會自動讓它更聽得懂使用者要什麼；GPT-3 會產生不實、有毒或沒幫助的內容，因為它的訓練目標是「預測網路上的下一個字」，不是「有幫助又安全地完成指令」。
- 方法（RLHF，reinforcement learning from human feedback）三步驟：
  1. 標註人員針對提示寫出示範答案 → 監督式微調；
  2. 標註人員替模型的多個輸出**排名** → 訓練獎勵模型（reward model）；
  3. 用獎勵模型當作獎勵訊號，以強化學習進一步微調。
- 結果：1.3B 參數的 InstructGPT，在人類評估中比 175B 的 GPT-3 更受偏好（參數少 100 倍）。
- 也較少編造事實、毒性輸出略減；但仍會犯簡單錯誤。
- OpenAI 稱這些模型是「trained with humans in the loop」，並成為其 API 的預設模型。
- 選擇人類偏好當獎勵，是因為安全與對齊問題複雜又主觀，難以用簡單自動指標衡量。
