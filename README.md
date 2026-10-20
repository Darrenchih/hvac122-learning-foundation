# HVAC-122 離線複習與內容管理底座

MIT 開源。繁體中文介面、英文四選一、隨時切換中文翻譯。程式引擎與題庫／教材／考試設定分開，後續可以由人或 AI 補內容，不必重寫工具。

這是獨立的公開專案，不依賴或修改其他考試模板儲存庫。

## Windows 雙擊啟動

1. 在 GitHub 按 **Code → Download ZIP**，完整解壓縮。
2. 進入 `hvac122-learning-foundation-main/`。
3. 雙擊 **「開始練習.cmd」**，會啟動本機伺服器並開啟 `http://127.0.0.1:8122/`。
4. 學習期間保留啟動視窗，用完關閉即可。不需管理員、Node、Python、帳號或付費 API。

也可以在本資料夾執行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start.ps1
```

只對該程序設定執行政策，不改永久系統設定。若已有一份在執行，直接開啟原網址；換連接埠會是另一個瀏覽器儲存區。直接開啟 `app/index.html` 可作備用，但 `file://` 不保證管理頁與練習頁共用儲存，管理功能應使用 CMD 的固定本機網址。

## 功能

- 按章節／知識點、隨機、錯題、未作答、弱點與計算練習。
- 英文題目與選項，中文翻譯可顯示／隱藏；提交後提供雙語及各選項理由。
- 模擬考、計時、自訂題數、標記回看與交卷後解析。
- 知識庫、中英搜尋、錯題追蹤、間隔複習、首次與重複成績分析。
- localStorage 保存學習紀錄；JSON 學習備份／還原。
- **內容管理**：新增／編輯知識點與題目，草稿與啟用分開，檢查後發布。
- 文字教材／考試範圍及本機原始附件（IndexedDB，不上傳）。
- 考試設定按章節／題型抽題，或使用固定 Question ID 題池。
- 完整內容包匯入／匯出、上一發布版本恢復、固定 Schema 與離線 CLI。

鍵盤：`1`–`4` 選答案、`Enter` 提交／下一題、`Alt+T` 切換翻譯。

## 讓 AI 接手：直接複製

```text
請沿用 https://github.com/Darrenchih/hvac122-learning-foundation 的既有底座，
先讀 FOUNDATION.md、AI_HANDOFF.md、prompts/START_HERE_ZH.md，
以及 templates/content-pack.schema.json。

我的工作是：[整理教材／新增題目／建立考試／修改功能]
範圍與檔案：[填入實際需求及已授權資料]

不要重新寫整套程式。內容工作請修改可匯入的內容包，沿用穩定 ID。
新題保持草稿、不能假稱已核對來源；計算題驗證答案與單位。
保留既有學習紀錄，不上傳第三方教材或私人資料。
交付內容包、改動摘要、實際測試結果與待核對清單。
```

完整提示詞：[開始使用](prompts/START_HERE_ZH.md)、[補題](prompts/ADD_QUESTIONS_ZH.md)、[建立考試](prompts/CREATE_EXAM_ZH.md)、[英文開發交接](prompts/DEVELOPER_HANDOFF_EN.md)。

## 加入內容

左側 **內容管理** → 新增／編輯 → 儲存草稿 → 更新內容版本 → 檢查並發布 → 回到練習。

完整說明：[FOUNDATION.md](FOUNDATION.md)、[AI_HANDOFF.md](AI_HANDOFF.md)。

- 範例：`templates/content-pack.example.json`。
- 契約：`templates/content-pack.schema.json`（格式版本 1）。
- 新題預設 `eligible:false`，核對後才啟用。
- 修改已發布題目的評分相關內容需新 ID，管理頁會保留並停用舊題。
- 本版仍限 HVAC Ch 1–5；不是已支援任意學科章節數的通用平台。

## 資料與開源範圍

內建 **300 題、74 知識點**。記憶 60（20%）、理解 105（35%）、應用 90（30%）、計算 45（15%）。45 題計算是 15 模型各 3 組參數。

題庫是專案編寫的教學練習，不是學校／老師原始考題。結構驗證與程式重算不代表教學專家認證；**300 題全部仍待原始課程及獨立專家核對**。

公開版含自主編寫內容、可重建的事實種子及腳本；**不含使用者原 ZIP、Blackboard 講義、Lab 原稿、老師試卷、私人學習備份或瀏覽器檔案**。詳見 [NOTICE.md](NOTICE.md)。MIT 不會替你取得第三方教材的公開散布權。

學習紀錄、內容包與原始附件是三份不同資料：學習備份不含內容包，內容包不含附件。請分別備份並保留原始文件。沒有雲端同步；清除瀏覽器資料會影響保存。

## 開發與測試

執行端零套件依賴。開發端需 Node 18+、Python 3.10+：

```powershell
python -m pip install -r requirements-dev.txt
python scripts/build_data.py
python scripts/run_tests.py
python scripts/run_tests.py --browser
```

CLI：

```powershell
node scripts/content_cli.cjs export my-content.json
node scripts/content_cli.cjs validate my-content.json
node scripts/content_cli.cjs merge my-content.json incoming.json merged.json
node scripts/content_cli.cjs build merged.json C:\HVAC122_CustomBuild
```

匯出／合併輸出檔及 build 目錄需為新路徑，避免覆蓋既有檔案。

本次本機可執行檢查 **67 項通過**。真實瀏覽器受開發沙箱限制為 **BLOCKED**，Windows CMD／PowerShell **未實機驗證**；VM 管理頁模擬不等於瀏覽器或附件 IndexedDB 實測。CI 的實際狀態請看 GitHub Actions，不預先宣稱通過。

## 目錄

```text
app/          練習引擎、內容管理與固定題庫
content/      公開、可重建的專案知識種子
data/        題庫、知識庫、章節、Schema
scripts/      重建、內容 CLI、測試、報告及打包
tests/       資料／邏輯／模擬／真實瀏覽器測試
templates/   內容包格式與範例
prompts/     可直接給 AI 的提示詞
reports/     品質、測試與已知限制說明
```

[貢獻指南](CONTRIBUTING.md) · [已知限制](reports/LIMITATIONS.md) · [品質與來源](reports/QUALITY_AND_SOURCES.md) · [MIT License](LICENSE)
