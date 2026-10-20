# 以現有題庫建立考試

```text
請沿用 hvac122 底座，在內容包的 examProfiles 新增一份考試，不重寫考試程式。

現有內容包：［檔名］
考試名稱：［名稱］
範圍：［Ch 1–5 內的章節／Topic／題型］
題數：［1–300］
時間：［分鐘；不計時填 null］
抽題方式：［條件隨機抽題／固定 Question ID 題池］

先讀 FOUNDATION.md、templates/content-pack.schema.json。
若 questionIds 非空，依其清單作題池；否則用 chapters 及 types 篩選。
只引用已存在且 eligible=true 的題目，題數不可超過可用題池。若不足，列出缺口，不擅自啟用未核對題目。
考試中維持隱藏答案解析，交卷後由現有引擎計分；不要把正解放入考試說明文字。
保存清楚的 description，版號更新；新考試先 enabled=false，供我核對後啟用。
執行 CLI 驗證，交付完整內容包、範圍／數量／時間摘要及待處理問題。
```
