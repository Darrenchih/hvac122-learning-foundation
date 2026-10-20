# HVAC-122 可延續開發底座 v2.1

目標：固定練習引擎，讓使用者與後續 AI 透過明確的內容契約補充教材、題庫及考試，不必從頭重寫。

## 一般使用者入口

解壓縮後雙擊「開始練習.cmd」，在工具側邊選「內容管理」。請使用這個固定本機網址；直接以 `file://` 開啟不同 HTML 時，部分瀏覽器會把管理頁與練習頁當成不同儲存區。

1. **知識點編輯**：新增 Topic、雙語定義、HVAC 應用、公式、誤解及來源限制。
2. **題庫編輯**：建立雙語題幹、四選項、正解、整題解析及各選項理由。新題預設草稿，不會立即進練習。
3. **教材／考試資料**：貼文字筆記、考試範圍、Lab 摘要；另可保存 PDF、PPTX、DOCX、圖片等原始文件。
4. **考試設定**：填名稱、題數、分鐘，按章節／題型篩選，或指定固定題目 ID 清單。每次考試可在指定題池內隨機抽題。
5. **內容總覽**：更新內容版本，檢查並預覽，再按「確認啟用此內容」。回練習頁即載入新版本。
6. **匯入／匯出與 AI**：匯出完整 JSON；讓 AI 根據格式整理內容，再以合併或取代草稿方式匯入、核對、發布。

管理頁沒有帳號或權限系統，適合本機單人操作。表單需按「儲存草稿」，切頁不保留未儲存文字。這不是多人同步服務。

## 三層邊界

| 層 | 檔案／儲存 | 用途 |
|---|---|---|
| 練習引擎 | `app/core.js`、`app/app.js`、`app/style.css` | 作答、解析、間隔複習、考試及分析 |
| 內容與管理 | `app/content.js`、`manage.html`、`manage.js`、`content-loader.js` | 格式檢查、編輯、草稿、發布與版本 |
| 原始附件 | `app/materials.js` → IndexedDB | 本機保存原始文件，不自動解析／生成答案 |
| 學習紀錄 | `hvac122.learning.v2` localStorage | 作答、錯因、排程及學習備份 |

內建 `bank.js`／`source/` 保留原本資料。內容管理不改寫這些磁碟檔案，也不覆寫學習紀錄。

## 固定內容契約

完整 JSON Schema：`templates/content-pack.schema.json`。可匯入範例：`templates/content-pack.example.json`。計算模型欄位範例：`templates/calculation.example.json`。

頂層：

```json
{
  "format": "hvac122-content-pack",
  "schemaVersion": 1,
  "version": "my-content-1",
  "title": "HVAC-122 自訂內容",
  "chapters": [],
  "knowledge": [],
  "questions": [],
  "examProfiles": [],
  "resources": []
}
```

- `chapters`：本版底座支援現有 HVAC Ch 1–5。可改章節名稱；擴展到其他章節數或其他科目需調整章節限制與學習備份驗證，不能只任意換數字。
- `knowledge`：沿用現有欄位，需唯一安全 ID、chapter、雙語術語／定義、Topic、應用、公式、誤解、課堂提示、來源及核對狀態。`related_question_ids` 會在發布成練習題庫時重建。
- `questions`：沿用現有欄位；選項 ID 固定 A–D，正解以 `correct_choice` 指向選項 ID，不依畫面位置評分。支援 recall／understanding／application／calculation。
- `eligible:false` 代表草稿／停用。`verification_status:draft`、`unverified`、`generated_unreviewed` 的題目不得啟用。勾選作者核對不等於原始來源或獨立專家認證。
- `source_reference.original_verified` 只在實際對照原始來源後設 true；`original_teacher_question` 不能由 AI 無憑據設 true。
- `publishedOnce` 由發布流程保留，用來阻止已發布／曾發布題目改答案卻沿用原 ID。不要手動移除此標記以繞過版本保護。
- `resources` 為文字教材：id、title、text、source、kind（lecture／lab／exam／other）、chapter（可 null）、verified。

考試設定範例：

```json
{
  "id": "EXAM-CH2-CALC",
  "name": "Ch 2 計算練習考",
  "description": "從已啟用的 Ch 2 計算題抽題",
  "count": 5,
  "minutes": 15,
  "chapters": [2],
  "types": ["calculation"],
  "questionIds": [],
  "enabled": true
}
```

填入 `questionIds` 時以該清單為題池，忽略章節／題型篩選；`count` 可小於池大小。未啟用題不會進考試，可用題數不足會拒絕發布。`minutes:null` 表示不計時。

計算題必須提供 `calculation.model`、`inputs`、`answer`、`unit`。支援 15 個明確模型，程式驗證數值及單位，拒絕任意公式字串／程式碼／eval。新模型才需要修改引擎並補測試；一般新增題目不用。

## ID 與版本規則

- 不同題目需不同 ID。不要把重排序號當永久 ID。
- 已發布的英文題幹、選項、答案、章節、題型或知識連結改變時，建立新 ID；管理表單會自動保留／停用舊題並建立新題。
- 匯入內容包不會替 AI 猜測 ID 修訂；同 ID 的已發布題實質改動會拒絕發布，請 AI 提供新 ID。
- 純解析補充可沿用 ID，但仍應更新內容版本，歷史紀錄保留原作答時版本。
- 全量取代會從練習題庫移除未包含的題目，但不刪作答歷史。不要日後重用已移除題目的舊 ID 作別題；離線工具不是全域 ID 登記服務。
- 未完成練習若題目被移除可能無法接續，更新前先完成或備份。

## 本機保存與備份

內容使用獨立鍵：

- `hvac122.content.draft.v1`：草稿。
- `hvac122.content.active.v1`：已發布內容。
- `hvac122.content.previous.v1`：上一個已發布版本。

為避免重複保存整個內建題庫而浪費 localStorage，內部只存相對內建版本的差異；**匯出時會展開成完整可攜內容包**。內建基底指紋改變時會停止套用舊差異而保留原值，需要從先前完整備份匯入。

學習備份、內容包、原始附件是三種不同資料。學習備份不包含內容包；內容包不包含附件。附件保存在 `hvac122.materials.v1` IndexedDB、每份上限 25 MB，可逐份下載原檔。沒有整批附件打包或跨裝置自動同步；請保留原始文件。

儲存配額不足會明確報錯，不會顯示已保存。發布失敗不會覆寫原啟用內容。只有上一個發布版本自動留存，多版歷史請自行匯出。

## 後續 AI 的工作入口

給 AI：本文件、`templates/` 及匯出的內容包。先整理內容，避免直接修改 `core.js`、`app.js` 或學習紀錄。參見 `AI_HANDOFF.md`。

開發端離線 CLI（需 Node，不是一般使用者執行工具的必要條件）：

```powershell
node .\scripts\content_cli.cjs export .\my-content.json
node .\scripts\content_cli.cjs validate .\my-content.json
node .\scripts\content_cli.cjs merge .\my-content.json .\ai-new-content.json .\merged.json
node .\scripts\content_cli.cjs build .\merged.json C:\HVAC122_CustomBuild
```

CLI 匯出／合併拒絕覆蓋既有輸出 JSON，請使用新檔名。`build` 只允許輸出至尚不存在的新資料夾，複製固定引擎並產生題庫資料及 CMD 啟動器，不覆蓋原專案。輸出內 `content-pack.json` 保留完整草稿與內容；練習端只編入已啟用題目。CLI 的 export 讀磁碟內建內容，**不會讀瀏覽器草稿**；瀏覽器內容請從管理頁匯出。

## 測試界線

提供內容格式／計算驗證、差異存取、發布、ID 修訂保護、考試篩選及管理／練習整合的自動測試。VM 介面模擬不是實際瀏覽器測試。原始附件 IndexedDB、真實雙頁管理／練習及 Windows CMD／PowerShell 仍須在實際瀏覽器／Windows 驗收，不能因程式測試通過而當成已實測。
