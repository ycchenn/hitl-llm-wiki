---
title: 紀錄
type: log
sources: []
updated: 2026-11-21
---
# 紀錄（只能往下新增）

> 回到 [索引](index.md)

## [2026-11-21 15:44] discuss | 決定主題與聽眾（先討論）
- 人類選擇主題：**Human-in-the-loop AI**（其他候選：RAG、LLM-as-a-Judge）。理由：與自己的 HCI 研究和急診分流專案相關。
- 目標聽眾：**會用 ChatGPT 但不懂原理的人**。
- 成果放置：新的 GitHub repo。

## [2026-11-21 15:45] discuss | LLM 提出資料清單與簡報大綱
- LLM 搜尋後提出 7 份資料（S1–S7）與 12 張投影片大綱，並說明每份資料負責回答哪個問題。
- 搜尋時發現第一個**矛盾**：業界文章寫 EU AI Act 人類監督 2026-08 生效，但 Digital Omnibus 修正後延至 2027-12-02。→ 待 ingest S6 時處理。

## [2026-11-21 15:47] discuss | 人類決定
- 語言：**中文，專有名詞附英文**（理由：聽眾是台灣一般使用者；評分重教學可理解性）。
- 加入 **S8：自己的急診分流模擬專案** 作為在地案例。
- 大綱確認，開始生成。

## [2026-11-21] ingest | S1 HITL 機器學習綜述
- 新建 concepts/human-in-the-loop.md（定義、三種模式）。

## [2026-11-21] ingest | S2 InstructGPT
- 新建 concepts/rlhf.md；更新 human-in-the-loop.md（訓練階段）。
- 註記：S2 沒提到 ChatGPT 的 👍👎，rlhf.md 中的類比標為（綜合）。

## [2026-11-21] ingest | S3 微軟 18 條準則
- 新建 concepts/design-guidelines.md（挑 6 條與介入最相關者）。

## [2026-11-21] ingest | S4 自動化自滿與偏誤
- 新建 concepts/automation-bias.md。

## [2026-11-21] ingest | S5 不完美自動化實驗
- 更新 automation-bias.md（給錯 vs. 沒給）、design-guidelines.md（與 G2/G10 連結）。

## [2026-11-21] ingest | S6 EU AI Act 第 14 條
- 新建 concepts/human-oversight-law.md；更新 automation-bias.md。
- **矛盾處理**：施行日期採 Digital Omnibus 修正後版本（2027-12-02／2028-08-02），在頁面加 ⚠️ 區塊。

## [2026-11-21] ingest | S7 Building effective agents
- 新建 concepts/agent-checkpoints.md；更新 human-in-the-loop.md（執行任務階段）。

## [2026-11-21] ingest | S8 急診 AI 分流模擬
- 新建 concepts/when-to-review.md（案例 + 三原則綜合）。
- 更新 overview.md、index.md。

## [2026-11-21] lint | 第 1 次執行（lint v1）
- `python3 pipeline/lint_wiki.py` → ✓ 通過（18 頁、8 份來源）。
- 註：v1 只檢查結構（連結、孤兒頁、index、frontmatter、來源代號），**不檢查內容**。

## [2026-11-21] slides | 依 slides/outline.md 生成 13 張投影片

## [2026-11-21] check | 第 1 次執行 check_slides（v1）→ ✗ 3 張失敗
- 只偵測到 12 張投影片（實際 13 張）→ **檢查器本身的 bug**：封面是 `class="slide cover"`，正規式只比對 `class="slide"`，封面完全沒被檢查，且所有編號差 1。
- 修正：改用 `\bslide\b` 比對（check_slides v1.1）。

## [2026-11-21] check | 第 2 次執行 check_slides（v1.1）→ ✗ 4 / 13 張失敗
| 張 | 問題 | 出錯的節點 |
|---|---|---|
| 1 | 「約 15 分鐘」不在 Wiki | 生成：加了 Wiki 以外的內容 |
| 5 | 13 億、1750 億 不在 Wiki（Wiki 只有 1.3B、175B） | 生成：自行換算單位 |
| 11 | 「40 次、12 小時」不在 concepts/when-to-review.md | **Wiki 整理**：concept 頁只搬了結果、漏了條件，而且該行沒有 [S8] |
| 13 | 參考資料年份不在 index.md | **Wiki 整理**：index 沒有作者／年份 |
- 判斷：4 個裡有 2 個的根源在 Wiki 整理節點，卻要到簡報才被發現 → **把數字檢查往前移到 lint**。

## [2026-11-21] lint | 第 3 次執行（lint v2：新增數字引用與可追溯性檢查）→ ✗ 3 個錯誤
- overview.md:9 「18 條準則」沒有 [S3]（圖示中只寫了 S3 字樣）
- concepts/when-to-review.md:10 「31%、27%」沒有 [S8] ← 正是第 11 張失敗的根源
- concepts/human-oversight-law.md:18 矛盾說明中的 2026 沒有 [S6]
- 發現 v2 的限制：抓得到「沒來源的數字」，抓不到「被漏掉的細節」（40 次、12 小時）。

## [2026-11-21] fix | 修正 Wiki（回到 Wiki 補資料，而非硬改投影片）
- when-to-review.md：結果行補上實驗條件與 [S8]。
- rlhf.md：新增單位換算行，標（綜合：單位換算）。
- index.md：來源表新增「作者／年份」欄。
- overview.md、human-oversight-law.md：補 [S3]、[S6]。
- 投影片第 1 張：重新生成，刪除「約 15 分鐘」。

## [2026-11-21] lint | 第 4 次執行 → ✗ 1 個錯誤
- rlhf.md 換算行標的是「（綜合：單位換算）」，但 lint 只認得完全相同的「（綜合）」。
- 修正：lint 接受「（綜合」開頭的標記，並寫入 CLAUDE.md。

## [2026-11-21] lint + check | 第 5 次執行 → ✓ 全部通過
- lint：✓ 18 頁、8 份來源。
- check_slides：✓ 13 張，皆可追溯到 Wiki。
- 更新 CLAUDE.md（schema v2）：數字引用規則、（綜合：…）標記、整理時連同條件一起搬、index 需有作者／年份。

## [2026-11-21] review | 👤 人類檢查點：13 張投影片截圖檢視
- 問題 1：`.grid` 使用 `flex:1` 撐滿高度，導致卡片下方的文字被推到投影片底部、中間大片空白（第 2、6、7、9、11 張）。
- 問題 2：左下角操作說明文字與來源頁腳重疊。
- 修正：取消 `flex:1`、投影片內容垂直置中、操作說明移到右上角；重新截圖確認。
- 備註：這類版面問題 check_slides.py 抓不到，必須靠人看。
