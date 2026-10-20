"""Explicit, authored teaching notes, applied by build_data.py."""
NOTES='''
01-001|Assess shock hazards during condenser service, not just nominal supply voltage.~冷凝機維修要評估電擊危害，不能只看標稱電壓。|A voltage label alone does not predict injury.~只看電壓標籤不能預測傷害。
01-002|Identify potential differences between exposed HVAC terminals.~辨識 HVAC 裸端子間電位差。|Earth contact is not required for every shock path.~不是所有觸電路徑都必須接觸大地。
01-003|Include arc energy when evaluating work on motor power panels.~評估馬達動力盤作業時也須考量電弧能量。|Low voltage does not mean no arc-flash hazard.~低壓不代表沒有電弧閃絡危害。
01-004|Recognize safe emergency response boundaries in a service area.~辨識維修區緊急救援的安全界線。|Directly grabbing an energized casualty can injure the rescuer.~直接拉仍帶電傷者可能傷及救援者。
01-005|Confirm the adopted local requirements before installing HVAC branch wiring.~安裝 HVAC 分路配線前核對當地採用要求。|NEC is not automatically the applicable Canadian installation code.~NEC 不自動成為加拿大適用安裝規範。
01-006|Understand how bonding a metal air-handler cabinet supports fault clearing.~了解空調箱金屬機殼搭接如何協助清故障。|A protective conductor is not a general substitute for neutral.~保護導體不是可任意替代的中性線。
01-007|Preserve the intended grounding connection on service tools.~保留維修工具預定的接地連接。|Removing the pin does not make a tool double insulated.~剪接地腳不會使工具變雙重絕緣。
01-008|Interpret imbalance trips on portable service supplies.~解讀可攜式維修供電的失衡跳脫。|GFCI does not prevent all line-to-neutral shocks or balanced overloads.~GFCI 不防止全部火線中性線觸電或平衡過載。
01-009|Check fuse type, current rating and interrupting capacity against equipment requirements.~依設備要求核對保險絲種類、電流額定及分斷能力。|A physically fitting fuse is not necessarily a suitable replacement.~裝得進去不代表替換件合適。
01-010|Treat repeated compressor breaker trips as a fault investigation signal.~把壓縮機反覆跳斷路器視為調查故障訊號。|Repeated resets do not repair an overload or short.~反覆重置不會修復過載或短路。
01-011|Identify all sources feeding indoor and outdoor HVAC sections before service.~維修前辨識室內外 HVAC 部分的全部供電。|Thermostat off does not isolate all energy.~關恆溫器不會隔離全部能源。
01-012|Account for run-capacitor stored energy after disconnecting a condenser.~冷凝機斷電後仍須考慮運轉電容儲能。|A fixed discharge resistor and waiting time are not universal.~固定放電電阻及等待時間不能通用。
01-013|Reject damaged leads and match PPE and instruments to the task.~停用損壞表筆並使 PPE 及儀器適合作業。|PPE does not replace qualification or isolation.~PPE 不取代資格或隔離。
02-001|Use charge polarity to understand electrical potential in controls.~用電荷極性理解控制電路電位。|Losing a negative electron makes an initially neutral atom positive.~中性原子失去負電子會帶正電。
02-002|Distinguish copper conductors from ceramic insulating supports.~區分銅導線與陶瓷絕緣支座。|Insulation can fail; no material choice alone proves a circuit safe.~絕緣可能失效，僅材質不能證明電路安全。
02-003|Distinguish backup batteries from generator supplies.~區分備用電池與發電機供電。|A generator converts energy rather than creating it from nothing.~發電機轉換能量而非無中生有。
02-004|Interpret the voltage across open thermostat contacts.~解讀開路恆溫接點兩端電壓。|Voltage can exist when load current is zero.~負載電流為零仍可有電壓。
02-005|Read coil and motor current specifications in amperes.~用安培解讀線圈及馬達電流規格。|Current is not used up as it passes through series loads.~電流不會經串聯負載就被用掉。
02-006|Identify AC transformer supplies and DC control electronics.~辨識交流變壓器供電與直流控制電子電路。|Varying DC need not reverse direction.~大小變化的直流不必反向。
02-007|Predict a fixed-voltage heater's current when resistance changes.~預測固定電壓加熱器在電阻改變時的電流。|Higher resistance does not mean more current at fixed voltage.~固定電壓下阻值較高不表示電流較大。
02-008|Solve ideal resistive control-board training circuits.~求解理想電阻控制板訓練電路。|Motor AC impedance is not always its DC winding resistance.~馬達交流阻抗不一定等於直流繞組電阻。
02-009|Estimate resistive strip-heater electrical input.~估算電阻式電熱條輸入。|Half voltage gives quarter power only for a fixed resistor.~電壓減半功率四分之一限固定電阻模型。
02-010|Distinguish compressor input W from apparent VA.~區分壓縮機輸入 W 與視在 VA。|V times I equals VA; multiplying by true PF gives single-phase real W.~V 乘 I 得 VA，乘真實 PF 才得單相實 W。
02-011|Recognize lagging current in inductive fan-motor models.~辨識電感性風扇馬達模型的落後電流。|A real motor is not a pure ideal inductor or pure resistor.~真實馬達不是純理想電感或純電阻。
02-012|Estimate heater energy from operating power and runtime.~由加熱功率及運轉時間估耗能。|kW and kWh measure different quantities.~kW 與 kWh 是不同物理量。
02-013|Convert motor shaft hp before applying efficiency to find input watts.~先換算馬達軸 hp，再用效率求輸入瓦數。|746 W per mechanical hp describes mechanical power, not automatic electrical input.~每機械 hp 的 746 W 不自動等於電輸入。
02-014|Compare seasonal cooling ratings under the same test method.~比較相同測試方法的季節冷房評等。|SEER is not an instantaneous current measurement.~SEER 不是瞬間電流量測。
02-015|Read kΩ, MΩ and mA accurately on component lists and meters.~正確讀取零件表及電表的 kΩ、MΩ、mA。|Uppercase M and lowercase m are not interchangeable.~大寫 M 與小寫 m 不可互換。
03-001|Trace source, load and return in a 24 VAC control schematic.~追蹤 24 VAC 控制圖中的電源、負載及回路。|A switch is useful but not essential in the simplest circuit model.~開關有用但非最簡電路必需。
03-002|Distinguish an open coil feed from a shorted load.~區分線圈供電開路與負載短路。|An open path can still have voltage across it.~開路兩端仍可有電壓。
03-003|Follow the same current through series permissive contacts.~追蹤流過串聯允許接點的相同電流。|Different series resistances do not imply different series currents.~不同串聯阻值不表示串聯電流不同。
03-004|Predict current reduction after adding series test resistance.~預測增加串聯測試電阻後的電流降低。|Series resistance adds; it does not combine like parallel resistance.~串聯電阻相加，不用並聯合成方式。
03-005|Explain reduced coil voltage due to a resistive contact.~解釋高阻接點造成線圈電壓降低。|A nearly closed mechanical contact can still develop significant voltage drop under load.~機械上接近閉合的接點在負載下仍可有明顯壓降。
03-006|Recognize fan and compressor branches connected across the same supply nodes.~辨識風扇及壓縮機跨相同供電節點的支路。|Equal branch voltage does not require equal branch current.~支路等電壓不要求等電流。
03-007|Estimate total current from DC or in-phase training branches.~由直流或同相訓練支路估總電流。|Different-phase AC currents require phase-aware addition of waveforms or phasors.~不同相位交流電流須依波形或相量相加。
03-008|Recognize why an in-circuit resistance reading may be too low.~辨識在電路內量阻為何可能偏低。|Parallel equivalent resistance is below the smallest positive branch resistance.~正電阻並聯等效值小於最小支路。
03-009|Separate motor load branches from the contactor control path.~分開理解馬達負載支路與接觸器控制通路。|Power and control circuits need not have the same topology.~動力與控制電路不必同拓撲。
03-010|Interpret a thermostat and pressure-safety series chain.~解讀恆溫器與壓力保護串聯鏈。|One open required series contact prevents coil energization; do not bypass it.~必要串聯接點任一開路就阻止線圈通電，不可旁路。
03-011|Analyze a fan branch opening without assuming compressor voltage vanishes.~分析風扇支路開路，不假設壓縮機電壓消失。|Independent electrical branches can still have interacting mechanical and protective behavior.~電氣獨立支路的機械與保護行為仍可能互相影響。
03-012|Compare training-lamp brightness in series and parallel.~比較訓練燈串並聯亮度。|Cold filament resistance is not a constant operating resistance.~冷態燈絲電阻不是固定工作電阻。
03-013|Use the manufacturer PSC motor diagram to locate the auxiliary capacitor branch.~用原廠 PSC 馬達圖找輔助電容支路。|Do not assume one capacitor topology fits all motor types.~不可假設所有馬達用同電容拓撲。
04-001|Choose the two nodes whose potential difference is needed.~選出欲量電位差的兩個節點。|High input impedance reduces loading but can permit coupled ghost-voltage indications.~高輸入阻抗減負載效應但可能顯示耦合虛電壓。
04-002|Understand the series path of an inline current test setup.~理解串入式電流測試的串聯通路。|A current input across a source can create a dangerous short.~電流輸入跨電源可能造成危險短路。
04-003|Interpret isolated heater and coil resistance without parallel-path errors.~解讀隔離加熱器及線圈電阻，避免並聯通路誤差。|Power off alone does not address stored energy or alternative paths.~只關電源未處理儲能及其他通路。
04-004|Select an AC- or DC-capable clamp appropriate to the HVAC conductor.~選適合 HVAC 導體的交流或直流鉤表。|Not every AC clamp can measure steady DC.~不是所有交流鉤表都能量穩態直流。
04-005|Explain near-zero current when a balanced whole cord is clamped.~解釋鉤整條平衡電纜時近零讀值。|Near-zero net clamp reading does not mean no load current.~淨鉤值近零不代表沒有負載電流。
04-006|Improve low-current training resolution with a known number of passes.~以已知穿過圈數提高低電流訓練解析度。|The display is multiplied, not the actual circuit current.~放大的是顯示值，不是實際電路電流。
04-007|Read the correct voltage scale during analog-meter labs.~指針表實驗讀正確電壓刻度。|The same pointer position can mean different values on different ranges.~同指針位置在不同檔位可代表不同值。
04-008|Avoid a thousand-fold prefix error when reading a control meter.~讀控制電表時避免千倍前綴錯誤。|0.024 A equals 24 mA, not 0.024 mA.~0.024 A 等於 24 mA，不是 0.024 mA。
04-009|Treat non-contact detection as a preliminary indication, not proof of isolation.~將非接觸偵測視初步指示，不當隔離證據。|Absence of indication is not verified absence of voltage.~無指示不等於已驗證無電壓。
04-010|Distinguish a contact's low-current continuity from its loaded condition.~區分接點低電流導通與負載工作狀態。|A beep does not prove a zero-ohm or full-load-quality contact.~蜂鳴不證明零歐姆或可正常滿載。
04-011|Check range and isolation before diagnosing an open winding from OL.~由 OL 判斷繞組開路前核對量程及隔離。|OL can be overrange rather than physical discontinuity.~OL 可能超量程而非實際斷路。
04-012|Compare instruments to known references before relying on unusual lab readings.~相信異常實驗讀值前，將儀表與已知標準比較。|Agreement between unverified meters does not establish traceable accuracy.~未校驗表一致不建立可追溯準確度。
04-013|Check quantity, AC/DC mode, jacks, range and CAT suitability before use.~使用前核對物理量、交直流、插孔、檔位及 CAT 適用性。|Display range is not a substitute for transient-category rating.~顯示量程不能取代暫態類別額定。
04-014|Judge an isolated replacement resistor against its stated tolerance.~依指定容差判斷隔離替換電阻。|Nominal resistance need not equal measured resistance exactly.~標稱阻值不必精確等於量測值。
05-001|Identify coils, motors and heaters as loads on an HVAC wiring diagram.~在 HVAC 接線圖辨識線圈、馬達及加熱器負載。|An energized coil consumes input; it is not the circuit's normal supply.~通電線圈消耗輸入，不是電路正常電源。
05-002|Connect fan and pump shaft work to electrical input and losses.~把風扇及泵軸功與電輸入及損失連結。|Current alone does not prove rotation or airflow.~只有電流不證明旋轉或風量。
05-003|Relate solenoid current to magnetic valve actuation.~將電磁閥電流與磁驅動連結。|Voltage across an open coil does not produce normal coil current.~開路線圈兩端有電壓不會產生正常線圈電流。
05-004|Use a control coil to operate separately rated load contacts.~以控制線圈操作獨立額定負載接點。|A coil click does not prove all contacts can carry load.~線圈吸合聲不證明所有接點能帶負載。
05-005|Match compressor switching contacts to motor duty and starting demand.~依馬達使用類別及起動需求匹配壓縮機切換接點。|Coil voltage alone does not determine contact suitability.~只有線圈電壓不能決定接點適用性。
05-006|Read NO auxiliary contacts in the unactuated diagram state.~以未動作圖示狀態讀 NO 輔助接點。|Normal does not mean the machine is currently running.~正常不代表機器目前運轉中。
05-007|Trace NC stop and interlock contacts before and after actuation.~追蹤 NC 停止與互鎖接點動作前後狀態。|NC is not a promise that the contact is always closed.~NC 不保證接點永遠閉合。
05-008|Separate contactor switching from overload protection in a starter.~在啟動器中區分接觸器切換與過載保護。|A starter may still require separate branch short-circuit protection.~啟動器仍可能需要獨立分路短路保護。
05-009|Choose SPDT for one circuit selection or DPST for two on/off poles.~一路選擇用 SPDT，兩極通斷可用 DPST。|Poles count independent circuits; throws count selections, not amperes.~極數計獨立迴路，投數計選擇，不是安培數。
05-010|Identify line-side and load-side boundaries of an HVAC disconnect.~辨識 HVAC 隔離開關電源側及負載側界線。|An open handle does not prove upstream terminals dead.~開把手不證明上游端子無電。
05-011|Use a simple on/off model before learning model-specific heat-pump sequences.~先用簡單通斷模型再學專用熱泵流程。|Thermostat logic varies with equipment and mode.~恆溫器邏輯依設備及模式變化。
05-012|Interpret pressure-safety action from its cut-in and cut-out specification.~依切入切出規格解讀壓力保護動作。|Not every pressure switch opens on pressure rise.~不是所有壓力開關都壓升斷開。
05-013|Trace a momentary start circuit with and without a holding contact.~追蹤有無自保持接點的瞬時啟動電路。|A momentary start button alone does not latch a coil.~瞬時啟動鈕本身不使線圈保持。
05-014|Interpret delayed overload trips without defeating motor protection.~解讀延遲過載跳脫而不破壞馬達保護。|A trip is a reason to investigate, not to bypass protection.~跳脫是調查原因，不是旁路保護的理由。
05-015|Read device trip curves before identifying magnetic protection functions.~辨識磁性保護功能前先讀跳脫曲線。|Magnetic does not by itself specify overload versus short-circuit duty.~magnetic 一詞本身不指定過載或短路用途。
05-016|Respect secondary VA and coil inrush when sizing 24 VAC controls.~設計 24 VAC 控制須尊重次級 VA 及線圈湧入需求。|Low secondary voltage does not mean unlimited capacity or no hazards.~次級低壓不代表容量無限或無危害。
05-017|Use K1 labels to link a coil and distributed contacts in ladder diagrams.~用 K1 標號連結梯形圖中分散的線圈接點。|Schematic spacing does not establish physical spacing.~原理圖間距不代表實體間距。
05-018|Recognize component appearance while cross-checking the circuit logic diagram.~辨識元件外觀，同時交叉核對電路邏輯圖。|A pictorial layout is not always the clearest representation of logic.~實體配置不一定最清楚呈現邏輯。
05-019|Find model-specific field terminals and conductor identification.~查找該型號現場端子與導線識別。|A generic sketch does not replace the model installation instructions.~通用草圖不取代該型號安裝指示。
'''
EXTRA={
'Why does a low-voltage label':'Available fault current and clearing time can still yield hazardous arc energy.~可用故障電流及清除時間仍可能造成危險電弧能量。',
'Why is a low-impedance':'A suitable fault path helps protective devices operate; it does not guarantee zero touch voltage at every instant.~合適故障通路有助保護動作，但不保證每瞬間接觸電壓為零。',
'Why must a replacement fuse':'A replacement must match specified current, voltage, interrupting and time-current requirements; size alone is not enough.~替換件須符合指定電流、電壓、分斷及時間電流要求，僅尺寸不夠。',
'Why is V × I':'V × I is apparent power in VA. For a single-phase motor, real input W = VA × true PF; shaft output also depends on efficiency.~V×I 是視在功率 VA；單相馬達實輸入 W=VA×真實 PF，軸輸出另看效率。',
'At fixed real input power':'From I = P/(V PF), lowering PF raises RMS current if P and V stay fixed.~由 I=P/(V×PF)，P、V 固定時 PF 降會升高有效值電流。',
'In an ideal sinusoidal inductive':'Inductance opposes changes in current, producing lagging current in sinusoidal steady state.~電感阻礙電流變化，因此正弦穩態電流落後。',
'Why is exact filament':'A filament heats up and its resistance changes; fixed-resistance lamp models give only qualitative brightness guidance.~燈絲發熱會改變阻值，固定電阻燈泡模型只適合定性亮度比較。',
'Why can a contact pass':'A buzzer uses a meter-specific threshold and small current. Under load, even modest contact resistance can cause IR drop and I²R heating.~蜂鳴依該表門檻及小電流；負載下即使不大接點阻值仍可有 IR 壓降及 I²R 發熱。',
'Why must OL':'OL can mean the selected range is exceeded. Use a suitable range and valid isolated setup before diagnosing an open circuit.~OL 可代表超出選定量程，須以適當檔位及有效隔離接法再診斷開路。',
'Why does selecting a higher':'Range describes measurable magnitude; CAT and voltage ratings address transient exposure suitability. Both meter and leads must suit the task.~檔位描述可量大小，CAT 及電壓額定描述暫態適用性；儀表及表筆皆須適合作業。',
'Can every clamp':'Some AC clamps use transformer sensing and cannot read steady DC; a suitable DC-capable design is required.~部分交流鉤表用變壓器感測而不能讀穩態直流，須有直流能力設計。',
'Why can a high-impedance':'A nearby live wire can couple through capacitance. The high meter impedance permits a voltage indication despite little available current; the reading is not proof of safety.~鄰近帶電線可經電容耦合，高表阻抗讓很小供電能力也顯示電壓，讀值不構成安全證據。',
'Why is comparing a meter':'Agreement between instruments with unknown errors is not a traceable reference comparison.~未知誤差儀表互相一致，不等於可追溯標準比較。',
'Why must the lead jack':'A current input is a low-resistance path. Leaving a lead there while connecting across a source can create a short even if the selector seems appropriate.~電流輸入是低阻通路，表筆留此孔跨電源可能短路，即使旋鈕看似適當。',
'Why does an ordinary AC':'Steady DC cannot sustain ordinary transformer action and may cause saturation and excessive primary current. Use only the specified supply.~穩態直流不能維持一般變壓作用，可能飽和及一次側過流，須用指定供電。',
'A student assumes a GFCI':'A line-to-neutral body path may have equal outgoing and returning current. A GFCI does not make intentional contact safe.~人體火線至中性線通路可能去回相等，GFCI 不使直接接觸變安全。',
'At fixed ideal branch':'At the common voltage, I = V/R. Lower R means higher branch current; equal voltage does not imply equal current.~共同電壓下 I=V/R，R 較低支路電流較大；同電壓不代表同電流。',
'Why should scalar':'Kirchhoff current balance applies instantaneously to AC, but different phases require waveform or phasor addition rather than adding RMS magnitudes directly.~克希荷夫電流平衡瞬時仍適用交流，但不同相位須用波形或相量相加，不能直接加有效值大小。',
'Can R = V/I':'V/I for an AC motor describes an impedance magnitude at that operating point; phase and true PF must also be considered.~交流馬達的 V/I 是該工作點阻抗大小，還須考慮相位及真實 PF。',
'A momentary NO start':'Without a holding path, releasing the NO button opens the only coil-current path. Latching requires additional circuitry or a different device.~沒有自保持通路時，放開 NO 鈕中斷唯一線圈通路；保持須額外電路或不同裝置。',
}
def enrich(knowledge):
 for line in NOTES.strip().splitlines():
  suffix,app,mis=line.split('|');k=next(x for x in knowledge if x['id']=='CH'+suffix)
  k['hvac_application']=app.replace('~',' / ');k['common_misconceptions']=[mis.replace('~',' / ')]
