# CLAUDE.md — Human-in-the-loop AI 的 LLM Wiki

> 本專案依照 Andrej Karpathy 的 LLM Wiki 模式（2026-04 gist）建立。
> 你（LLM）是這個 Wiki 的維護者：**人類負責挑資料、提問、做決定；你負責整理、交叉引用、檢查與記錄。**
> 任何操作前先讀完本文件。

---

## 1. 主題與範圍

- **主題**：Human-in-the-loop（HITL）AI：人在 AI 系統的哪裡、為什麼、怎麼參與。
- **用途**：作為知識庫，產生一份給「**會用 ChatGPT 但不懂原理的人**」看的中文教學簡報。
- **範圍內**：HITL 定義與類型、RLHF、自動化偏誤、人機互動設計準則、法規中的人類監督、AI Agent 的人類檢查點、真實案例。
- **範圍外**：數學推導、特定框架的程式碼教學。遇到時只留一句話並標 `#out-of-scope`。

## 2. 三層架構

```
raw/            ① 原始資料層（不可修改）
wiki/           ② Wiki 層（LLM 撰寫與維護）
  index.md        全部頁面的目錄，查詢時第一個讀
  log.md          時間序紀錄，只能往下新增
  overview.md     主題總覽（綜合所有來源）
  sources/        每份資料一頁摘要  s<N>-<slug>.md
  concepts/       每個概念一頁      <kebab-case>.md
CLAUDE.md       ③ Schema 層（本文件，人與 LLM 共同演進）
```

- `index.md` 的來源表要有「作者／年份」，簡報的參考資料頁從這裡取。（v2）
- `raw/` 存放 **source card**：書目、網址、閱讀筆記（重點萃取）。因為著作權，不存全文；引文每份最多一句、15 字（英文 words）以內。
- `raw/` 建立後**不再修改**；若發現錯誤，在 `log.md` 記錄並於 Wiki 層修正。

## 3. 頁面格式

每個 Wiki 頁面開頭都要有 frontmatter：

```yaml
---
title: 自動化偏誤（Automation bias）
type: concept        # concept | source | overview | index | log
sources: [S4, S5, S6]  # 這頁用到的來源（source 頁填自己）
updated: 2026-11-21
---
```

**引用規則（最重要）**
- 來源代號 `S1`–`S8`，對應 `wiki/sources/s<N>-*.md`。
- 每一個**事實性**段落或條列項，句尾都要有 `[S#]`。
- **含有兩位數以上數字的那一行，同一行一定要有 `[S#]`，且該數字必須出現在被引用的來源頁中**（v2，lint 自動檢查；見 log「lint 第 3 次執行」）。
- 單位換算、自己的推論等不在來源中的內容，標 `（綜合）` 或 `（綜合：說明）`，lint 會略過，但簡報使用時仍需在講者備註說明。
- 整理 concept 頁時，**數字要連同它的條件一起搬**（例如「40 次模擬、每次 12 小時」），不要只搬結果。（v2）
- 頁面之間用相對連結：`[RLHF](rlhf.md)`、`[S2](../sources/s2-instructgpt.md)`。
- 自己的綜合推論要標 `（綜合）`，不可假裝成來源的話。

**語言**：繁體中文；專有名詞第一次出現附英文，例如「自動化偏誤（automation bias）」。

## 4. 操作

### 4.1 Ingest（一次一份資料）
1. 讀資料 → 寫 `raw/s<N>-<slug>.md` source card。
2. **先討論**：向人類報告 3–5 個重點與「它跟現有 Wiki 哪裡衝突／補充」，等人類確認方向（或依已確認的大綱進行）。
3. **後生成**：寫 `wiki/sources/s<N>-*.md`。
4. 更新所有受影響的 `concepts/` 頁（一份資料通常會動到 2–5 頁）；沒有對應頁就新建。
5. 更新 `index.md`、`overview.md`。
6. 在 `log.md` 新增一筆：`## [日期] ingest | S<N> 標題`。
7. 執行 `python3 pipeline/lint_wiki.py`，有 ✗ 就修到通過。

### 4.2 Query（查詢）
1. 先讀 `index.md` 找相關頁面，再讀頁面內容。
2. 回答要附 Wiki 頁面連結與 `[S#]`。
3. 有價值的答案可以存回 Wiki 成為新頁面，並記 log。

### 4.3 Lint（健康檢查）
`python3 pipeline/lint_wiki.py` 會檢查：斷掉的連結、孤兒頁（沒有任何頁面連過來）、index 漏列、frontmatter 缺欄位、引用不存在的來源；
v2 起另外檢查：含數字的行是否有 `[S#]`、數字能否在被引用的來源頁（concept → sources/）或原始卡片（sources/ → raw/）中找到。
限制：lint 抓得到「寫錯、沒來源」的數字，抓不到「整理時漏掉的細節」，這類問題仍靠簡報檢查往回追。
另外人工／LLM 需檢查：**來源之間互相矛盾**、**過時的說法**（例如法規日期）。發現時在相關頁面加 `> ⚠️ 矛盾：…` 區塊並記 log。

## 5. 從 Wiki 產生簡報（slides/）

1. **規劃**：寫 `slides/outline.md`，每張投影片列出：教學目標、要講的重點、引用的 Wiki 頁面。
2. **查詢**：每張投影片只能使用其 `wiki:` 欄位列出頁面中的內容（不可直接讀 raw/、不可用模型自己的記憶補內容）。
3. **生成**：產生 `slides/index.html`。每張投影片是
   `<section class="slide" data-wiki="concepts/rlhf.md sources/s2-instructgpt.md">`，
   並在頁腳顯示來源 `[S#]`。
4. **檢查**：`python3 pipeline/check_slides.py`
   - 每個 `data-wiki` 頁面都存在；
   - 投影片上出現的每個數字，都能在它引用的 Wiki 頁面中找到（防止編造數字）；
   - 每張投影片內文不超過 120 個中文字（教學可讀性）；
   - 頁腳列出的 `[S#]` 必須是所引用 Wiki 頁面的 `sources` 之一。
5. 檢查失敗 → **只重新生成失敗的那張**；同一張重試 3 次仍失敗 → 回到 Wiki 補資料（重新 ingest 或修正 concept 頁），並記 log。
6. 最後由人類檢視整份簡報（人類檢查點）。

教學結構固定為：**引起動機 → 定義 → 機制 → 陷阱 → 怎麼做好 → 規範 → 新趨勢 → 案例 → 帶走的習慣 → 總結**，中間至少一個互動問題。

## 6. 不可以做的事

- 不可在 Wiki 寫沒有來源的事實；不可在簡報放 Wiki 裡沒有的內容。
- 不可修改 `raw/`、不可刪除 `log.md` 的舊紀錄。
- 不可為了通過檢查而刪掉檢查規則；要改規則先更新本文件並記 log。
