(function(){
'use strict';
window.HVAC_BUILTIN=window.HVAC_BANK;
try{
 const raw=localStorage.getItem(HVAC_CONTENT.KEYS.active);
 if(raw){const base=HVAC_CONTENT.fromBank(HVAC_BUILTIN),pack=HVAC_CONTENT.read(localStorage,HVAC_CONTENT.KEYS.active,base);window.HVAC_BANK=HVAC_CONTENT.toBank(pack);}
}catch(err){window.HVAC_CONTENT_ERROR='自訂內容未能載入，暫用內建題庫；原內容已保留。請到內容管理匯出／修復：'+err.message;}
})();
