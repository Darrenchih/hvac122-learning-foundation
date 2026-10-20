# 新增／改善題庫

```text
請依 hvac122-learning-foundation 的內容契約，補充現有內容包，不要改 UI 或練習引擎。
先讀 FOUNDATION.md、AI_HANDOFF.md、templates/content-pack.schema.json。

現有內容包：［檔名］
資料來源：［實際檔案／經授權的筆記］
範圍：［Chapter／Knowledge ID／Topic］
新增題數：［數量］
預期題型：［記憶、理解、應用診斷、計算比例］

要求：
1. 保留未改題目的 ID，為新題建立永久唯一 ID，不以陣列排序作 ID。
2. 同概念要有不同情境，避免只換詞序；干擾選項須有合理誤解依據。
3. 每題英文四選一，雙語欄位及 A–D 逐項解析完整，只有一個最佳答案。
4. 題目 Knowledge ID 必須存在，章節一致；需要新知識點時一併建立完整欄位。
5. 明確限定電路模型、設備及法規適用範圍，不把固定電容放電規格、驗電筆無反應等當通用安全答案。
6. 計算用支援的 calculation.model、正值 inputs、answer、unit，獨立重算後檢查選項。
7. 新題 eligible=false、verification_status=draft；不把未核對來源標成已驗證。
8. 保留原始教材，不擅自上傳，不把老師原始題目冒充自主創作或擅自 MIT 授權。

執行 node scripts/content_cli.cjs validate output.json；若無執行環境，明確列 NOT RUN。
交付完整可匯入內容包、各題型數量、重複題檢查、數值驗證及待人工核對清單。
```
