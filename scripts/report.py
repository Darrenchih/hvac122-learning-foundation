"""Public-only quality report; no access to private attachments or source archives."""
import pathlib,json,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
q=load('data/questions.json');k=load('data/knowledge.json');near=load('reports/near_duplicates.json');counts=collections.Counter(x['type'] for x in q)
manifest={'version':'2.0.0','questions':len(q),'knowledge':len(k),'countsByType':dict(counts),'countsByChapter':dict(collections.Counter(x['chapter'] for x in q)),'structuralChecksPassed':300,'calculationChecksPassed':45,'originalSourceVerified':0,'expertReviewed':0,'pendingSourceOrExpertReview':300,'nearDuplicatePairs':len(near),'bankSha256':hashlib.sha256((ROOT/'data/questions.json').read_bytes()).hexdigest(),'distribution':'MIT project review; private originals excluded'}
(ROOT/'data/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
text=f'''# 公開版題庫品質與來源

300 題、74 知識點。記憶 60（20%）、理解 105（35%）、應用 90（30%）、計算 45（15%）。全部通過欄位及結構檢查；45 題計算以獨立測試重算答案與單位。

**原始課程對照 0 題，獨立專家核對 0 題，300 題仍待人工核對。**作者依原理檢查、程式驗證、第三方核對是不同層次。

公開版以專案編寫的 `content/knowledge.seed.json`、`scripts/enrich.py`、`scripts/understanding.txt`、`scripts/application.txt` 及計算模型重建。最初參考過私人摘要，但原始 ZIP、Blackboard 講義、Lab 原稿、老師試卷與私人學習紀錄均不在公開版。沒有假稱取得或核對原始課程。MIT 不授予使用者其他第三方教材的權利。

安全內容區分美國 NEC 與加拿大／省級要求，不猜特定條文；不採固定致命電流或通用放電電阻；非接觸驗電筆不能單獨證明無電。電阻量測處理隔離、儲能、並聯路徑及量程；Relay／Contactor 以用途與額定判斷，接觸器不自動含完整過載保護。這些是限定的教學原理，不是未受訓者的現場帶電工作指引。

計算為 15 模型各三組數值，不是 45 個獨立概念。近似字詞偵測列出 {len(near)} 對候選，45 對為參數變體、9 對為串聯與並聯公式不同但題幹相似；詳見 `near_duplicates.json`。偵測不保證所有語意重複均已排除。部分干擾選項與逐項解析仍待教學專家改善。

Question ID 不依清單排序；改評分相關內容須新 ID。所有知識點至少三題且含應用／計算證據。詳細範圍與備份界線見 FOUNDATION.md、NOTICE.md 與 LIMITATIONS.md。

題庫 SHA-256：`{manifest['bankSha256']}`。
'''
(ROOT/'reports/QUALITY_AND_SOURCES.md').write_text(text,encoding='utf-8')
print('Public report written')
