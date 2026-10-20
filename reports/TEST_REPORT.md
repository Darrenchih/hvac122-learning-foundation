# 開源版測試結果

本機實際執行：`python scripts/run_tests.py --browser`。

| 套件 | 檢查數 | 結果 |
|---|---:|---|
| 資料／Schema／計算／公開檔案範圍 | 12 | PASS |
| 練習與間隔複習領域邏輯 | 14 | PASS |
| 練習 VM 介面模擬 | 9 | PASS |
| 內容契約／發布／版本保護 | 17 | PASS |
| 管理 VM 介面模擬與練習整合 | 9 | PASS |
| 內容 Schema／CLI／可攜建置 | 6 | PASS |
| 真實瀏覽器練習驗收 | 未開始流程 | BLOCKED：本機沙箱限制 |
| 真實瀏覽器管理與附件驗收 | 未開始流程 | BLOCKED：本機 socket 限制 |
| Windows CMD／PowerShell | 0 | NOT RUN |

合計 **67 項通過**。包含 BLOCKED 的總命令回傳 2，不代表全部驗收通過。單元／模擬測試不等於真實瀏覽器、IndexedDB 或 Windows 實測。

公開版以「不包含私人原始教材／壓縮檔」檢查取代私用交付的原壓縮檔逐位元比較；公開儲存庫不需取得私人附件即可重建與跑測試。

CI 已提供 Linux 單元及真實 Chromium 流程，線上結果應以 GitHub Actions 實際狀態為準。重跑會產生 reports/*.log 與 test-results.json（不納入公開版本）。
