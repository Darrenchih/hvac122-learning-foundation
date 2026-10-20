"""Reproducible offline authoring pipeline. Source files are read-only inputs."""
import json, pathlib, hashlib, math, collections, random
from enrich import enrich, EXTRA
ROOT=pathlib.Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
knowledge=load('content/knowledge.seed.json')
# These are educational principles reviewed during authoring, not evidence of source inspection.
applications={1:'Recognize hazards before troubleshooting HVAC equipment. / HVAC 故障排除前辨識危害。',2:'Interpret HVAC electrical ratings and energy use. / 解讀 HVAC 電氣額定值及耗能。',3:'Trace the load and control paths in HVAC circuits. / 追蹤 HVAC 負載與控制通路。',4:'Select and interpret the appropriate HVAC electrical measurement. / 選擇及判讀 HVAC 電氣量測。',5:'Identify the role of a device in an HVAC control schematic. / 辨識 HVAC 控制圖中的元件功能。'}
formula_map={'CH02-008':['I = V/R','V = IR','R = V/I'],'CH02-009':['P = VI','P = I²R','P = V²/R'],'CH02-010':['P = Vrms × Irms × PF'],'CH02-012':['E(Wh) = P(W) × t(h)'],'CH02-013':['1 hp ≈ 746 W','1 W ≈ 3.412 Btu/h'],'CH03-004':['Rt = ΣRi'],'CH03-005':['Vs = ΣVi','Vi = Vs × Ri/Rt'],'CH03-007':['It = ΣIi'],'CH03-008':['1/Rt = Σ(1/Ri)'],'CH04-006':['Iactual = Idisplay / N']}
mis={
'CH01-001':'不存在保證安全的固定電流門檻；接觸時間與路徑同樣重要。',
'CH01-005':'NEC 並非加拿大普遍適用法規；須向所在地主管機關確認採用版本。',
'CH01-012':'不可用固定 20 kΩ / 4 W 當作所有電容的通用放電方法，也不可任意以螺絲起子短路。',
'CH04-003':'通電電路不可使用電阻模式；斷電不代表儲能已消失，並聯支路也會改變讀值。',
'CH04-009':'非接觸驗電筆無反應不能證明無電。',
'CH04-010':'蜂鳴不代表零電阻，也不保證接點能帶負載正常工作。',
'CH05-004':'繼電器不是只能用於低壓；必須依接點額定值、負載種類及設計用途選用。',
'CH05-005':'接觸器與繼電器不能僅以電壓大小區分；馬達額定值及使用類別很重要。',
'CH05-011':'這是簡單通斷恆溫器模型；電子式、多段及熱泵控制必須依原廠邏輯。',
'CH05-015':'不能把所有磁性過流元件視為完整的馬達過載或短路保護；要查設備額定與曲線。'}
for k in knowledge:
 k['hvac_application']=applications[k['chapter']]
 k['related_formulas']=formula_map.get(k['id'],[])
 k['common_misconceptions']=[mis.get(k['id'],'不要把本知識點的功能、單位或適用條件與相似元件混淆。請依本頁定義及題目條件判斷。')]
 k['content_class']='safety_principle' if k['chapter']==1 or k['id'] in ['CH04-003','CH04-009'] else 'classroom_model' if k['id'] in ['CH05-011','CH03-012'] else 'technical_principle'
 k['verification_status']='principle_reviewed_original_source_pending'
 k['source_reference']={'file':'content/knowledge.seed.json','record':k['id'],'original_verified':False,'note':'Project-authored review material derived from a private summary; original course files are not included or verified.'}
 k['source_limitations']='未取得 Blackboard 原始簡報／Lab，未核對課程措辭、版本及法規條文。'
 if k['id']=='CH01-011':
  k['definition_en']='Identify and isolate all hazardous energy, apply the applicable lockout/tagout procedure, and verify absence of voltage before work. For qualified personnel, the applicable verification procedure includes a suitable rated contact instrument whose operation is checked on a known live reference before and after the absence test; a non-contact detector alone is insufficient.'
  k['explanation_zh']='辨識並隔離全部危險能源、依適用程序上鎖掛牌，工作前驗證無電。合資格人員依適用驗證程序使用額定合適的接觸式儀器，並在無電測試前後以已知帶電參考確認儀器有效；單靠非接觸驗電筆不夠。此為程序原理，不是未受訓者帶電操作指南。'
 if k['id']=='CH04-003':
  k['definition_en']='A resistance meter supplies its own test signal. Isolate all energy sources, verify absence of voltage using an appropriate procedure, discharge stored energy according to the manufacturer, and isolate the component as needed before resistance measurement.'
  k['explanation_zh']='電阻表自行供應測試訊號。量測前須隔離所有能源、依合適程序驗證無電、按原廠方法處理儲能，並視需要隔離元件，避免並聯通路影響結果。'
 if k['id']=='CH05-015':
  k['definition_en']='Magnetic current-operated protection responds to current according to a specified trip characteristic. Its role as overload or short-circuit protection depends on the device design and rating.'
  k['explanation_zh']='磁性電流保護依指定跳脫特性動作；是否具過載或短路保護功能，須看裝置設計與額定，不能一概而論。'
 if k['id']=='CH02-010':
  k['definition_en']='For single-phase AC, real input power P = Vrms × Irms × true PF. PF is real power divided by apparent power; for sinusoidal waveforms it equals the cosine of the phase angle.'
  k['explanation_zh']='單相交流實功率 P=Vrms×Irms×真實功率因數；PF=實功率/視在功率。只有正弦波條件才能用相位角餘弦表示。'
enrich(knowledge)
K={k['id']:k for k in knowledge}
questions=[]
def pair(s):
 a=s.split('~'); assert len(a)==2,s
 return a

def add(kid,typ,q,opts,ex=None,calc=None):
 k=K[kid]; en,zh=pair(q); oid='HV2-'+hashlib.sha256((kid+'|'+en+'|'+'|'.join(sorted(opts))+'|'+opts[0]).encode()).hexdigest()[:12]
 if not ex:
  ex=next((value for key,value in EXTRA.items() if en.startswith(key)),None)
 choices=[]; reasons={}
 correct=pair(opts[0])
 for i,s in enumerate(opts):
  oe,oz=pair(s); ci='ABCD'[i]; choices.append({'id':ci,'text_en':oe,'text_zh':oz})
  if i==0: re,rz=pair(ex) if ex else (k['definition_en'],k['explanation_zh'])
  else:
   re=f'“{oe}” does not satisfy the stated conditions. '+(pair(ex)[0] if ex else k['definition_en'])
   rz=f'「{oz}」不符合題目條件。'+(pair(ex)[1] if ex else k['explanation_zh'])
  reasons[ci]={'en':re,'zh':rz}
 re,rz=pair(ex) if ex else (correct[0]+'. '+k['definition_en'],correct[1]+'。'+k['explanation_zh'])
 for ci in 'BCD':
  reasons[ci]['en']+=' Under the stated conditions the supported conclusion is: '+correct[0]+'.'
  reasons[ci]['zh']+=' 題目條件下支持的結論是：'+correct[1]+'。'
 item={'id':oid,'knowledge_ids':[kid],'chapter':k['chapter'],'topic':k['topic_key'],'difficulty':'basic' if typ=='recall' else 'intermediate' if typ=='understanding' else 'applied','type':typ,'question_en':en,'question_zh':zh,'choices':choices,'correct_choice':'A','explanation_en':re,'explanation_zh':rz,'choice_explanations':reasons,'source_reference':k['source_reference'],'verification_status':'calculation_verified_source_pending' if calc else 'principle_reviewed_source_pending','eligible':True,'original_teacher_question':False}
 if calc:item['calculation']=calc
 questions.append(item)

# 60 recall questions: curated homogeneous alternatives rather than unrelated definitions.
# Format: Knowledge suffix | question | correct | three plausible alternatives.
RECALL='''
02-001|Which particle carries negative charge?~哪種粒子帶負電？|Electron~電子|Proton~質子|Neutron~中子|A positive ion~正離子
02-002|Which material is normally chosen as an electrical insulator?~哪種材料通常用作電絕緣體？|Ceramic~陶瓷|Copper~銅|Aluminum~鋁|Silver~銀
02-003|Which conversion supplies a battery's electrical output?~哪種轉換供應電池輸出的電能？|Chemical to electrical~化學能轉電能|Mechanical to electrical by induction~機械能經感應轉電能|Electrical to mechanical~電能轉機械能|Electrical to radiant~電能轉輻射能
02-004|Which unit expresses potential difference?~電位差使用哪個單位？|Volt~伏特|Ampere~安培|Ohm~歐姆|Watt~瓦特
02-005|Which quantity is measured in amperes?~安培是什麼量的單位？|Current~電流|Potential difference~電位差|Resistance~電阻|Energy~能量
02-006|What defines alternating current?~什麼是交流電的定義特徵？|Periodic reversal of current direction~電流方向週期性反轉|Constant current direction~電流方向固定|Constant current magnitude at all times~電流大小永遠固定|Zero average heating in a resistor~在電阻中平均不發熱
02-007|What is the SI unit of resistance?~電阻的 SI 單位為何？|Ohm~歐姆|Siemens~西門子|Farad~法拉|Henry~亨利
01-004|Which response avoids making a rescuer another shock victim?~哪種反應可避免救援者也成為觸電傷者？|Avoid direct contact with an energized casualty~避免直接碰仍帶電傷者|Pull with bare hands immediately~立刻徒手拉開|Touch the conductor to check its warmth~碰導體測溫|Start chest compressions before isolation~未隔離先胸外按壓
01-007|What is the purpose of a grounding plug pin on a grounded tool?~接地式工具插頭的接地腳有何用途？|Maintain the intended protective grounding connection~維持預定保護接地連接|Carry all normal return current~承載全部正常回流|Set the motor speed~設定馬達速度|Reduce supply frequency~降低電源頻率
01-009|What happens to a conventional single-use fuse after it opens by melting?~一般一次性保險絲熔斷後如何？|It requires the specified replacement after the cause is addressed~處理原因後須用指定替換件|It is reset with a handle~用把手重置|It restores itself after cooling~冷卻後自行恢復|It becomes a calibrated resistor~變校準電阻
02-011|Which ideal load has current in phase with voltage?~哪種理想負載的電流與電壓同相？|Pure resistor~純電阻|Pure inductor~純電感|Pure capacitor~純電容|An open circuit carrying no current~無電流的開路
02-012|Which expression gives electrical energy for constant power?~功率固定時，哪個式子表示電能？|Power multiplied by time~功率乘時間|Power divided by time~功率除時間|Voltage divided by time~電壓除時間|Current multiplied by resistance~電流乘電阻
02-013|One mechanical horsepower is approximately how many watts?~一機械馬力約等於幾瓦？|746 W~746 W|1000 W~1000 W|3412 W~3412 W|2545 W~2545 W
02-014|Which ratio is used for SEER?~SEER 使用哪種比值？|Seasonal cooling Btu / electrical Wh~季節冷量 Btu / 用電 Wh|Electrical Wh / seasonal cooling Btu~用電 Wh / 季節冷量 Btu|Instantaneous current / voltage~瞬間電流 / 電壓|Heating watts / motor horsepower~暖氣瓦數 / 馬達馬力
02-015|What multiplier does the prefix kilo mean?~kilo 前綴代表何倍率？|1000~1000|1000000~1000000|0.001~0.001|0.000001~0.000001
03-001|Which item is essential to sustain current in a simple load circuit?~簡單負載電路要維持電流，哪項不可缺？|A continuous conducting path~完整導電通路|A thermostat specifically~一定要有恆溫器|A relay specifically~一定要有繼電器|A second load in parallel~另一個並聯負載
03-002|What does an open circuit mean?~開路的意思為何？|A path is interrupted~通路中斷|All resistances are zero~所有電阻為零|The supply voltage is always zero~電源電壓一定為零|Two points are shorted together~兩點被短接
03-003|Which quantity is equal through all elements of one series path?~同一串聯通路的所有元件哪個量相同？|Current~電流|Voltage drop~壓降|Resistance~電阻|Power dissipation~耗散功率
03-004|How do ideal series resistances combine?~理想串聯電阻如何合成？|Add the resistances~電阻相加|Add their reciprocals to obtain resistance~倒數相加直接當電阻|Use only the largest resistance~只用最大電阻|Use only the smallest resistance~只用最小電阻
03-005|In an ideal series resistor divider, voltage drops are proportional to what?~理想串聯分壓器的壓降與什麼成正比？|Each resistance~各電阻值|The reciprocal of each resistance~各電阻倒數|The number of supply terminals~電源端子數|Each wire's color~各導線顏色
03-006|What is equal across branches connected to the same two ideal nodes?~跨接同兩理想節點的各支路什麼量相同？|Voltage~電壓|Current~電流|Power~功率|Resistance~電阻
01-010|Which protective device may be reset after its trip cause is corrected?~哪種保護裝置排除跳脫原因後可重置？|A suitable resettable circuit breaker~合適可重置斷路器|A melted single-use fuse~已熔斷一次性保險絲|A broken conductor~已斷導線|A removed grounding pin~已剪接地腳
03-008|For two positive resistors in parallel, equivalent resistance is what?~兩個正電阻並聯，等效電阻如何？|Less than either resistor~小於任一電阻|Greater than both resistors~大於兩電阻|Their arithmetic mean~兩者算術平均|Their sum~兩者總和
03-009|Which arrangement commonly permits HVAC loads to share supply voltage while safeties control a coil?~哪種接法常讓 HVAC 負載共用電壓而保護接點控制線圈？|Parallel loads and series safety contacts~負載並聯、保護接點串聯|Series loads and parallel bypasses around safeties~負載串聯、保護接點以旁路並聯|All loads and contacts in one parallel group~所有負載及接點全部並聯|All motors in one series path~所有馬達串聯
03-010|What happens when a required series safety contact opens?~必要的串聯保護接點斷開會怎樣？|The controlled coil path is interrupted~受控線圈通路中斷|The coil receives twice its voltage~線圈電壓加倍|The coil becomes a power source~線圈成為電源|The other contacts automatically bypass it~其他接點自動旁路
03-011|Why are correctly rated fan and compressor loads often parallel?~額定合適的風扇與壓縮機為何常並聯？|Each can receive the intended supply voltage~各自可取得預定電源電壓|Each must draw identical current~各自必須取相同電流|Their winding resistances must add~繞組電阻必須相加|One motor must carry the other's current~一馬達必須承載另一馬達電流
03-012|Two identical rated lamps in series on one lamp's rated supply generally appear how?~兩相同額定燈泡串聯接在單顆額定電源上通常如何？|Dimmer than when each is at rated voltage~比各得額定電壓時暗|Brighter than rated~比額定時亮|Exactly rated brightness~剛好額定亮度|One rated and the other always dark~一顆額定亮、一顆永遠不亮
03-013|In a typical PSC motor model, where is the run capacitor?~典型 PSC 馬達模型中運轉電容接在哪裡？|In series with the auxiliary winding branch~與輔助繞組支路串聯|In series with the entire equipment supply~與整台設備電源串聯|Across the disconnect as a bypass~跨隔離開關作旁路|In place of the overload device~取代過載裝置
04-001|How is a voltmeter connected to measure a component's voltage?~量元件電壓時電壓表如何接？|Across the two component terminals~跨元件兩端|In place of the load as a short~以短路方式取代負載|Only around the outside insulation~只環抱絕緣外皮|In series as the sole load~串聯成唯一負載
04-002|How is a conventional inline ammeter connected?~一般串入式電流表如何接？|In series with the measured path~與待測通路串聯|Across the voltage source~跨電源兩端|Across a closed switch~跨閉合開關|Across the load in voltage mode~以電壓模式跨負載
05-019|Which reference normally identifies model-specific field-wiring terminals?~何種參考通常識別型號專用現場配線端子？|Installation wiring diagram~安裝接線圖|Generic power-factor chart~通用功率因數圖|Motor efficiency trend graph~馬達效率趨勢圖|Atomic charge table~原子電荷表
04-004|What does a clamp ammeter sense to infer current?~鉤表感測什麼以推知電流？|Magnetic field around the conductor~導體周圍磁場|Resistance of the insulation~絕緣皮電阻|Wire color~導線顏色|Voltage at a single unconnected probe~單支未接表筆電壓
04-005|Balanced line and return conductors inside one clamp tend to produce what?~鉤口同時包住平衡的去回導線通常讀到什麼？|Approximately zero net current~淨電流近零|Twice the load current~兩倍負載電流|Exactly the line voltage~剛好線電壓|The load resistance~負載電阻
04-006|A conductor makes N same-direction turns through a clamp. How is actual current found?~同一導線同方向穿鉤口 N 次，實際電流如何求？|Indication divided by N~讀數除以 N|Indication multiplied by N~讀數乘 N|Indication plus N~讀數加 N|Indication minus N~讀數減 N
04-007|Which two items determine an analog meter reading?~判讀指針表需哪兩項？|Selected scale and range multiplier~選用刻度及檔位倍率|Case size and wire length~外殼大小與線長|Battery color and display angle~電池顏色與顯示角度|Only the pointer's raw number~只看指針原始數字
04-008|A DMM shows kΩ. What quantity and prefix are indicated?~數位表顯示 kΩ，代表何量及前綴？|Resistance in thousands of ohms~以千歐姆表示的電阻|Current in thousands of amperes~以千安培表示的電流|Voltage in thousandths of a volt~以毫伏表示的電壓|Resistance in millionths of an ohm~以微歐姆表示的電阻
04-009|What can a non-contact voltage detector alone establish?~單靠非接觸驗電筆能確定什麼？|An electric field may be present when it indicates~有指示時可能存在電場|All conductors are safe when silent~無聲表示所有導體安全|Exact line current~精確線電流|Verified absence of all hazardous voltage~已驗證無任何危險電壓
04-010|A continuity buzzer primarily indicates what?~導通蜂鳴主要表示什麼？|A path below the meter's continuity threshold~通路低於該表蜂鳴門檻|An exact resistance of zero~電阻精確為零|A contact proven good at full load~已證明接點滿載正常|A conductor proven de-energized~已證明導線無電
04-011|An isolated open path usually gives which resistance indication?~隔離的開路通常顯示何電阻讀值？|OL or very high resistance~OL 或極高電阻|Exactly zero ohms~精確零歐姆|Rated supply volts~額定電源伏特|Rated running amperes~額定運轉安培
04-012|What is the purpose of meter calibration?~電表校驗目的為何？|Compare readings with known references~與已知標準比較讀值|Increase every reading by a fixed amount~把所有讀值固定增加|Prove every circuit is safe~證明所有電路安全|Make voltage and resistance ranges identical~使電壓與電阻檔相同
04-013|On a meter, what does the function setting select?~電表 function 選擇什麼？|The measured quantity such as V, A or Ω~V、A、Ω 等待測物理量|Only the decimal-place count~只有小數位數|The conductor's ampacity~導線容許電流|The equipment supply frequency~設備供電頻率
04-014|What tolerance does a gold resistor tolerance band usually denote?~電阻金色容差環通常表示何容差？|±5%~±5%|±1%~±1%|±10%~±10%|±20%~±20%
05-001|Which item normally serves as an electrical source?~哪個通常是電源？|Battery~電池|Heater element~加熱元件|Motor winding~馬達繞組|Energized solenoid~通電電磁線圈
05-002|A fan motor primarily converts electrical energy into what useful output?~風扇馬達主要將電能轉成何種有效輸出？|Mechanical shaft work~機械軸功|Stored chemical energy~儲存化學能|Electrical isolation~電氣隔離|Purely capacitive energy~純電容儲能
05-003|What directly actuates an ordinary solenoid plunger?~一般電磁閥柱塞由什麼直接驅動？|Magnetic field from coil current~線圈電流產生的磁場|The coil's paint color~線圈漆色|The open contact air gap alone~只有開接點氣隙|The thermostat display~恆溫器顯示器
05-004|What does energizing a conventional relay coil do?~一般繼電器線圈通電會做什麼？|Change its associated contact states~改變所屬接點狀態|Guarantee overload protection~保證過載保護|Guarantee every contact is closed~保證每個接點都閉合|Set all load voltages equal to coil voltage~使所有負載電壓等於線圈電壓
05-005|Which rating is especially relevant when choosing a contactor for a compressor?~替壓縮機選接觸器時哪個額定特別相關？|Motor-load switching rating at the actual voltage~實際電壓下馬達負載切換額定|Only its physical width~只有外殼寬度|Only its coil wire color~只有線圈線色|Only its enclosure label language~只有外殼標籤語言
05-006|What does NO mean for a defined unactuated contact?~在定義的未動作狀態，NO 表示什麼？|Normally open~常開|Normally overloaded~正常過載|Neutral only~僅中性線|No overload protection~無過載保護
05-007|What is an NC contact's state before actuation in its defined normal condition?~NC 接點在定義的正常未動作狀態如何？|Closed~閉合|Open~斷開|Always shorted to ground~永遠接地短路|Dependent only on load amperage~僅由負載安培決定
05-008|What does a basic magnetic motor starter combine?~基本電磁馬達啟動器結合什麼？|Contactor and motor overload protection~接觸器與馬達過載保護|Transformer and voltmeter only~只有變壓器及電壓表|Thermostat and capacitor only~只有恆溫器及電容|Disconnect handle and lamp only~只有隔離把手與燈
05-009|What does pole count describe in a switch?~開關 pole 數表示什麼？|Independently switched circuits~獨立切換的迴路組數|Number of selectable throws per pole~每極可選擇的位置數|Coil supply frequency~線圈供電頻率|Contact resistance in ohms~接點歐姆電阻
05-010|What is the primary role of a disconnect?~隔離開關主要功能為何？|Provide a means of supply isolation~提供電源隔離手段|Regulate room temperature~調節室溫|Improve motor power factor~改善馬達功率因數|Measure branch current~量支路電流
05-011|In a simple on/off cooling-call model, what occurs as temperature rises above the call threshold?~簡單通斷冷房模型中溫度超過啟動點時如何？|The cooling-call contact closes~冷房需求接點閉合|The cooling-call contact opens~冷房需求接點斷開|The contact always changes to heating~接點總改為暖房|The compressor reverses its winding polarity~壓縮機繞組反轉極性
05-012|How is a pressure switch's action determined?~壓力開關動作如何判定？|By specified function and pressure setpoints~依指定功能及壓力設定點|By assuming every switch opens on pressure rise~假設全部壓升斷開|By assuming every switch closes on pressure rise~假設全部壓升閉合|Only by wire insulation color~只看絕緣皮顏色
05-013|Which contact is commonly used for a simple momentary start command?~簡單瞬時啟動指令常使用何接點？|Normally open momentary contact~瞬時常開接點|Permanently open contact~永久斷開接點|Welded closed contact~熔焊閉合接點|A disconnected coil~斷線線圈
05-014|A thermal overload device principally responds to what?~熱過載裝置主要回應什麼？|Heating associated with excessive motor current~馬達過電流相關的發熱|Room illumination~室內照度|Only supply conductor color~只看電源線色|Only refrigerant type~只看冷媒種類
05-015|What determines a magnetic protective device's actual trip behavior?~磁性保護裝置實際跳脫行為依什麼決定？|Its rated design and trip characteristic~其額定設計及跳脫特性|The word magnetic alone~只靠 magnetic 名稱|Any relay coil voltage~任意繼電器線圈電壓|A universal fixed time for all devices~所有裝置通用固定時間
05-016|An ordinary control transformer operates using what principle?~一般控制變壓器利用何原理？|Magnetic coupling with changing flux~變動磁通的磁耦合|Chemical reaction~化學反應|Steady DC resistive division only~僅穩態直流電阻分壓|Mechanical contact friction~機械接點摩擦
05-017|Which drawing best emphasizes circuit logic rather than physical placement?~哪種圖主要呈現電路邏輯而非實際位置？|Schematic diagram~原理圖|Pictorial layout~實體配置圖|Site floor plan~現場平面圖|Equipment photograph~設備照片
05-018|Which drawing emphasizes recognizable component appearance?~哪種圖著重可辨識的元件外觀？|Pictorial diagram~實體圖|Ladder logic schematic~梯形邏輯原理圖|Truth table~真值表|Power-versus-time graph~功率時間圖
'''
for line in RECALL.strip().splitlines():
 kid,q,*opts=line.split('|');add('CH'+kid,'recall',q,opts)
assert len(questions)==60,len(questions)

# Each row below is independently authored; no runtime AI or answer generation.
for typ,file in [('understanding','understanding.txt'),('application','application.txt')]:
 for line in (ROOT/'scripts'/file).read_text(encoding='utf-8').splitlines():
  if not line.strip() or line.startswith('#'):continue
  kid,q,*rest=line.split('|');opts=rest[:4];ex=rest[4] if len(rest)>4 else None
  add('CH'+kid,typ,q,opts,ex)

# 45 explicit calculation models: 15 model families x 3 parameter sets.
for n in range(3):
 def calc(kid,q,ans,unit,vals,model,inputs,work):
  def fmt(v):return f'{v:.6g}'
  add(kid,'calculation',q,[f'{fmt(v)} {unit}~{fmt(v)} {unit}' for v in [ans]+vals],work,{'model':model,'inputs':inputs,'answer':ans,'unit':unit,'tolerance':1e-5})
 v=[24,120,240][n];r=[12,30,60][n];i=v/r
 calc('CH02-008',f'An ideal HVAC training resistor of {r} Ω has {v} V DC across it. What current flows?~理想 HVAC 訓練電阻 {r} Ω 兩端接 {v} V 直流，電流多少？',i,'A',[i/2,i*2,i*4],'ohm_current',{'V':v,'R':r},f'I = V/R = {v}/{r} = {i:g} A.~I=V/R={v}/{r}={i:g} A。')
 i=[2,3,5][n];r=[12,20,30][n];a=i*r
 calc('CH02-008',f'A resistive control-test load carries {i} A and measures {r} Ω. What DC voltage is required?~純電阻控制測試負載 {i} A、{r} Ω，所需直流電壓多少？',a,'V',[a/2,a*2,a*3],'ohm_voltage',{'I':i,'R':r},f'V = IR = {i} × {r} = {a} V.~V=IR={i}×{r}={a} V。')
 v=[24,120,240][n];i=[0.5,4,8][n];a=v/i
 calc('CH02-008',f'A DC heater draws {i} A at {v} V at steady state. What is its resistance?~直流加熱器穩態於 {v} V 取 {i} A，電阻多少？',a,'Ω',[a/2,a*2,a*4],'ohm_resistance',{'V':v,'I':i},f'R = V/I = {v}/{i} = {a:g} Ω.~R=V/I={v}/{i}={a:g} Ω。')
 v=[120,208,240][n];i=[5,10,15][n];a=v*i
 calc('CH02-009',f'A unity-PF heater operates at {v} V RMS and {i} A RMS. What real power does it use?~功率因數 1 加熱器於 {v} V、{i} A 有效值運轉，實功率多少？',a,'W',[a/2,a*2,a/10],'power_vi',{'V':v,'I':i},f'For a resistive load P = VI = {a} W.~純電阻 P=VI={a} W。')
 i=[2,3,4][n];r=[10,20,30][n];a=i*i*r
 calc('CH02-009',f'A heater element of {r} Ω carries {i} A RMS. What is its heating power?~{r} Ω 加熱元件流過 {i} A 有效值，發熱功率多少？',a,'W',[i*r,i*i/r,a*2],'power_i2r',{'I':i,'R':r},f'P = I²R = {i}² × {r} = {a} W.~P=I²R={i}²×{r}={a} W。')
 v=[24,120,240][n];r=[12,24,48][n];a=v*v/r
 calc('CH02-009',f'A fixed {r} Ω heater is connected to {v} V RMS. What power is dissipated?~固定 {r} Ω 加熱器接 {v} V 有效值，耗散功率多少？',a,'W',[a/2,a*2,v/r],'power_v2r',{'V':v,'R':r},f'P = V²/R = {a:g} W.~P=V²/R={a:g} W。')
 v=[120,208,240][n];i=[10,5,8][n];pf=[0.8,0.75,0.9][n];a=v*i*pf
 calc('CH02-010',f'A single-phase motor input is {v} V RMS, {i} A RMS, true PF {pf}. What is real electrical input power?~單相馬達輸入 {v} V、{i} A 有效值、真實 PF {pf}，輸入實功率多少？',a,'W',[v*i,a/2,a*2],'power_pf',{'V':v,'I':i,'PF':pf},f'P = Vrms Irms PF = {a:g} W; shaft output would also require efficiency.~P=Vrms×Irms×PF={a:g} W；軸輸出另需效率。')
 p=[500,1200,2000][n];t=[2,3,1.5][n];a=p*t/1000
 calc('CH02-012',f'A heater draws a constant {p} W for {t} h. What electrical energy is used?~加熱器固定 {p} W 運轉 {t} h，用電多少？',a,'kWh',[a*1000,a/2,a*2],'energy',{'P':p,'h':t},f'E = P × t / 1000 = {a:g} kWh.~E=P×t/1000={a:g} kWh。')
 hp=[0.5,1,2][n];eff=[0.8,0.75,0.9][n];a=hp*746/eff
 calc('CH02-013',f'A motor delivers {hp} mechanical hp at efficiency {eff}. Using 746 W/hp, what electrical input power is required?~馬達輸出 {hp} 機械 hp、效率 {eff}；以 746 W/hp 計，輸入電功率多少？',a,'W',[hp*746,hp*746*eff,a*2],'horsepower',{'hp':hp,'efficiency':eff},f'Input = shaft watts / efficiency = {a:.6g} W. Rounded to 6 significant figures.~輸入=軸瓦數/效率={a:.6g} W，取 6 位有效數字。')
 r1=[10,20,30][n];r2=[20,40,60][n];a=r1+r2
 calc('CH03-004',f'Two ideal resistors {r1} Ω and {r2} Ω are in series. What is equivalent resistance?~{r1} Ω 與 {r2} Ω 理想電阻串聯，等效電阻多少？',a,'Ω',[a/2,r1*r2/a,a*2],'series',{'R1':r1,'R2':r2},f'Rt = R1 + R2 = {a} Ω.~Rt=R1+R2={a} Ω。')
 v=[24,120,240][n];r1=[10,20,30][n];r2=r1*2;a=v*r2/(r1+r2)
 calc('CH03-005',f'A {v} V DC supply feeds series resistors {r1} Ω and {r2} Ω. What is the voltage across the {r2} Ω resistor?~{v} V 直流供應 {r1} Ω、{r2} Ω 串聯電阻；{r2} Ω 上電壓多少？',a,'V',[v/2,v-a,v],'divider',{'V':v,'R1':r1,'R2':r2},f'V2 = Vs × R2/(R1+R2) = {a:g} V.~V2=Vs×R2/(R1+R2)={a:g} V。')
 r1=[12,20,30][n];r2=r1*2;a=r1*r2/(r1+r2)
 calc('CH03-008',f'Ideal {r1} Ω and {r2} Ω resistors are in parallel. What is equivalent resistance?~理想 {r1} Ω 與 {r2} Ω 並聯，等效電阻多少？',a,'Ω',[r1+r2,(r1+r2)/2,r1],'parallel',{'R1':r1,'R2':r2},f'Rt = R1R2/(R1+R2) = {a:g} Ω, less than either branch.~Rt=R1R2/(R1+R2)={a:g} Ω，小於任一支路。')
 i1=[2,3,4][n];i2=[5,6,8][n];a=i1+i2
 calc('CH03-007',f'Two parallel DC branches draw {i1} A and {i2} A. What is their combined supply current?~兩並聯直流支路各取 {i1} A、{i2} A，總供應電流多少？',a,'A',[i2-i1,a/2,i1*i2],'current_sum',{'I1':i1,'I2':i2},f'It = I1 + I2 = {a} A.~It=I1+I2={a} A。')
 turns=[3,4,5][n];shown=[6,12,20][n];a=shown/turns
 calc('CH04-006',f'A suitable clamp shows {shown} A with one insulated test conductor passing through {turns} times in the same direction. What is the conductor current?~合適鉤表顯示 {shown} A，同一絕緣測試導線同方向穿過 {turns} 次，實際電流多少？',a,'A',[shown,shown*turns,a/2],'clamp',{'reading':shown,'turns':turns},f'Actual current = indication / turns = {a:g} A.~實際電流=顯示值/圈數={a:g} A。')
 nominal=[100,200,1000][n];a=nominal*.05
 calc('CH04-014',f'A nominal {nominal} Ω resistor has a gold ±5% tolerance band. What is its allowed deviation from nominal?~標稱 {nominal} Ω 電阻金環 ±5%，允許偏離標稱多少？',a,'Ω',[nominal*.1,nominal*.01,nominal*.5],'tolerance',{'nominal':nominal,'percent':5},f'Deviation = nominal × 0.05 = ±{a:g} Ω.~偏差=標稱×0.05=±{a:g} Ω。')

# Distribute authored answer keys; stable option IDs remain fixed during runtime shuffling.
for q in questions:
 old=q['choices']; random.Random(q['id']).shuffle(old)
 remap={c['id']:'ABCD'[i] for i,c in enumerate(old)}
 q['correct_choice']=remap[q['correct_choice']]
 q['choice_explanations']={remap[c]:v for c,v in q['choice_explanations'].items()}
 for c in old:c['id']=remap[c['id']]

counts=collections.Counter(q['type'] for q in questions)
assert counts=={'recall':60,'understanding':105,'application':90,'calculation':45},counts
assert len({q['id'] for q in questions})==300
for k in knowledge:k['related_question_ids']=[q['id'] for q in questions if k['id'] in q['knowledge_ids']]
(ROOT/'data/knowledge.json').write_text(json.dumps(knowledge,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf-8')
bank={'version':'2.0.0','knowledge':knowledge,'questions':questions,'chapters':load('data/chapters.json'),'provenance':'Derived educational practice; not teacher exam questions. All original slide/lab verification pending.'}
(ROOT/'app/bank.js').write_text('window.HVAC_BANK = '+json.dumps(bank,ensure_ascii=False)+';\n',encoding='utf-8')
print('Built',len(questions),dict(counts))
