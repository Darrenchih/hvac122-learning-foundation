# 開始使用：可直接貼給 AI 的提示詞

複製下方內容，補上方括號即可。請只提供你有權交給該 AI 處理的教材。

```text
請沿用這個已存在的複習工具底座，不要從頭重寫程式。

GitHub：https://github.com/Darrenchih/hvac122-learning-foundation
工具路徑：儲存庫根目錄
我的工作：［整理教材／新增題目／建立考試／修正內容］
範圍：［章節、Topic、題數、題型比例］
可用資料：［我提供且有權使用的內容包、筆記及教材］

請先讀取：
1. README.md
2. FOUNDATION.md
3. AI_HANDOFF.md
4. templates/content-pack.schema.json
5. templates/content-pack.example.json

接著：
- 搜尋實際可用檔案，不假設已讀過未提供的教材。
- 有現有內容包就以它為基礎；沒有時，使用範例或 CLI 匯出內建資料。
- 只改教材、knowledge、questions、examProfiles、resources，不重寫 app 引擎。
- 新題保持 eligible=false、verification_status=draft，交由我核對後啟用。
- 每題有英文四選一、繁體中文翻譯、唯一最佳答案、英中解析及逐項理由。
- 已發布題目改題幹、英文選項、正解、章節、題型或知識連結時另建 ID，不改舊紀錄。
- 計算題提供支援模型及明確數值／單位，執行驗證；不生成執行時 AI 答案。
- 不上傳教材、學習紀錄或機密資訊到公開儲存庫；開源權限不涵蓋第三方教材。
- 無法確認的來源、答案或安全規則維持待核對，不冒稱老師原題或技術認證。

交付：可匯入的完整內容包 JSON、改動摘要、驗證結果、人工待核對清單。
先完成可獨立進行的工作，僅在必要資料缺失時提出具體問題。
```
