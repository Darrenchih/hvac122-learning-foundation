# Contributing

這是獨立的 HVAC-122 複習與內容管理專案。請沿用固定引擎與內容契約。

## 開始前

讀取 README.md、FOUNDATION.md、AI_HANDOFF.md 及內容 Schema。一般補題使用內容包，不必重寫 UI。

## 資料貢獻

- 提交自己有權開源的內容，不提交學校講義、老師原卷、商用題庫、學習備份或機密。
- 新題設 eligible=false、verification_status=draft，附可追溯來源與待核對項目。
- 四個合理選項、單一最佳答案、雙語與逐項解析完整；計算需可重算模型及單位。
- 不重用已發布／曾發布題目的 ID 改變評分相關內容。
- 不冒稱教師核可、原始來源已查證或適用所有法規／設備。

## 程式貢獻

保留離線功能、穩定儲存鍵與既有紀錄，不加入帳號、雲端上傳或執行時 AI 相依。變更行為需具體回歸測試。

在儲存庫根目錄：

```sh
python -m pip install -r requirements-dev.txt
python scripts/run_tests.py
python scripts/run_tests.py --browser
```

使用公開種子重建資料：`python scripts/build_data.py`。提交必要的生成結果；不可把個人 localStorage／IndexedDB 匯出納入版本。

PR 說明交代問題、變更及實際測試。BLOCKED、NOT RUN 與 PASS 分開；不可把 VM 介面測試說成 Windows／真實瀏覽器通過。UI 變更若有真實截圖可附，沒有就不要偽造。

提交表示你有權依本專案 MIT 授權提供該貢獻；第三方教材權利不會因本專案開源而改變。
