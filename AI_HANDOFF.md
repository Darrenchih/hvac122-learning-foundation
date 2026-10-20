# 給下一個 AI：沿用這個底座，不要重做

請先讀 `FOUNDATION.md`、`templates/content-pack.schema.json` 及使用者匯出的內容 JSON。

你的預設工作是補充教材、知識點、題目與考試設定，輸出可直接匯入的完整內容包，**不要重新生成另一套 UI／練習引擎**。

1. `app/core.js` 處理學習規則；`app/app.js` 處理練習；`app/content.js` 是內容契約與驗證；`app/manage.js` 是管理入口。只有需求涉及新行為才修改程式。
2. 沿用未實質改動題目的 ID。改已發布題的題幹、正解、英文選項、章節、題型或知識連結時，建立新 ID，保留舊題並停用。不要移除 publishedOnce 來繞過保護。
3. 新生成題預設 `eligible:false`、`verification_status:draft`。不能假裝是老師原題、已查原始簡報或已確認法規。原始來源不在工作區就明確標待核對。
4. 每題恰四個合理干擾選項、唯一最佳答案、英中題幹及選項、英中整題解析及 A–D 各自理由。每個 Knowledge ID 必須存在且章節一致。
5. 計算題用支援的 calculation 模型、正值 inputs、answer 與 unit。新模型必須另加實作及獨立測試，不能透過 eval 或任意程式字串執行。
6. 教材文字放 resources，考試抽題／題數／時間放 examProfiles；不要把考試設定寫死在 UI。原始 PDF/PPTX 只作本機附件，不聲稱已自動解析或轉成正確答案。
7. 只在使用者授權的範圍存取教材，不自動上傳、發信、改系統設定或改其他專案。
8. 保護學習紀錄；不要刪 localStorage／IndexedDB，不要改掉既有學習儲存鍵。備份及還原不得混淆內容包與學習備份。
9. 先用 `node scripts/content_cli.cjs validate pack.json` 檢查。新增功能請跑 `python scripts/run_tests.py`；真實瀏覽器測試用 `--browser`。BLOCKED／NOT RUN 不得標 PASS。
10. 交付內容包、變更摘要、驗證結果及未核對清單。需要可攜程式時用 CLI build 到新資料夾，不覆蓋原專案。

內建題庫仍是 300 題／74 知識點，全部原始 Blackboard 及外部專家核對尚待完成。程式驗證不能替代這個缺口。
