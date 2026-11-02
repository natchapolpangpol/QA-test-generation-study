# แผนโครงการ SQA ฉบับปรับใหม่

วันที่: 2 พฤศจิกายน 2569 — สถานะ: แผนก่อนลงมือพัฒนาระบบและทดลองจริง

อัปเดตการลงมือ: ผู้ใช้อนุญาตให้เริ่มด้วยเครื่องมือที่ทำงานอัตโนมัติได้แล้ว ดู [สถานะ implementation](IMPLEMENTATION_STATUS.md) สำหรับหลักฐานจริง ขณะนี้ทดสอบ DynaMOSA/MIO และ Codex สองโมเดลผ่านสิทธิ์สมาชิกได้บน teaching fixture; คู่แชตที่เสนอด้านล่างเป็นประวัติแผน ยังไม่ใช่ main protocol ที่ freeze

หมายเหตุล่าสุด: ผู้ใช้แจ้งว่ามี ChatGPT Plus และกำลังพิจารณารันอัตโนมัติ/API ฟรี คู่แชตในเอกสารนี้จึงยังไม่ freeze โดย Plus ไม่รวม OpenAI API usage; ตัวเลือกที่ต้องทดสอบเพิ่มเติมคือ Codex CLI ผ่านสิทธิ์สมาชิก และ Gemini API free tier หรือ Groq Free หากเปลี่ยนไปใช้ agent/CLI ต้องปรับกติกา tool access และ generation budget ก่อนทดลองหลัก ยังไม่ได้ตรวจ API key หรือโควตาบัญชีจริง

## 1. เป้าหมายและขอบเขต

หัวข้อ: **การเปรียบเทียบ DynaMOSA, MIO, ChatGPT และ Claude ในการสร้าง Unit Tests สำหรับ Java โดยประเมิน Structural Coverage และการตรวจพบ Regression บน Defects4J**

เป็นโครงการส่วนตัวของผู้ใช้ ใช้นิยามการทดสอบจากเอกสารวิชา ไม่ผูกกับบริการ AI มหาวิทยาลัย การจองหัวข้อกลุ่ม หรือสิทธิ์การศึกษาของรายวิชา อัปเดตตามข้อมูลล่าสุด: ผู้ใช้แจ้งว่าสิทธิ์ Gemini ไม่ผ่าน จึงไม่ถือว่ามี Plus แล้ว คู่ AI ที่แนะนำใหม่คือ ChatGPT Free + Claude Free โดยต้องตรวจสิทธิ์และโควตาจริงใน pilot ก่อนตรึงการทดลอง

เป้าหมายคือสร้างหลักฐานที่ตอบได้ว่าเทสต์ครอบคลุมส่วนใดของโค้ด เพราะอะไร และตรวจพบความต่างที่เกิดจาก bug ได้หรือไม่ ไม่ตั้งสมมติฐานล่วงหน้าว่าต้องได้ coverage 100% หรือวิธีใดจะชนะ

คำถามหลัก:

1. DynaMOSA กับ MIO ให้ source-decision coverage ต่างกันอย่างไรภายใต้งบค้นหาเดียวกัน?
2. ทั้งสี่วิธีให้ line, statement, block, decision, condition และ C/DC เท่าใดบนขอบเขตเดียวกัน?
3. เทสต์ที่ผ่าน fixed revision ตรวจพบ regression ใน buggy revision ได้กี่ bug และผลคงที่เพียงใด?
4. ต้องใช้เวลาเครื่อง เวลาแรงงาน รอบแก้ และโควตาเท่าใดจึงได้เทสต์ที่ใช้งานได้?

นี่เป็นการสร้าง regression tests โดยมี fixed implementation เป็น reference จึงไม่อ้างว่าเป็นการค้นหา bug ที่ยังไม่เคยทราบโดยไม่มีคำตอบอ้างอิง และ benchmark สาธารณะอาจอยู่ในข้อมูลฝึกของ LLM ได้

## 2. วิธีสร้างเทสต์ที่เลือก

| วิธี | บทบาทและเหตุผล | วิธีใช้งาน |
|---|---|---|
| DynaMOSA | Search-based many-objective algorithm ที่จัดการเป้าหมายแบบ dynamic เป็นตัวหลักที่มีงานเปรียบเทียบรองรับ | ใช้ implementation ใน EvoSuite และตรึง commit/build |
| MIO | Many Independent Objective เป็นตัวเปรียบเทียบเชิงอัลกอริทึมที่จัดการหลายเป้าหมายต่างจาก DynaMOSA | ใช้ EvoSuite build เดียวกัน และตรวจเส้นทางเรียก algorithm จริง |
| ChatGPT Free | ตัวเลือกฟรีแทน Gemini แพ็กเกจเดิม ไม่พึ่งการอนุมัติสิทธิ์นักศึกษา | ใช้แชตบัญชี Free เก็บชื่อโมเดลหรือป้ายโหมดตามที่แสดงจริง ไม่สมมติว่าได้รุ่นเดียวกับบัญชีเสียเงิน |
| Claude Free | LLM อีกผู้ให้บริการที่ไม่ต้องเพิ่มค่าสมาชิก และใช้แชตในรูปแบบใกล้เคียงกัน | ใช้บัญชี Free; ไม่สมมติว่ารวม API หรือ Claude Code |

เลือกอัลกอริทึมที่เฉพาะกับ test generation แทนการเริ่มจาก GA/PSO ทั่วไป การใช้ implementation เดิมช่วยให้ส่วนที่ศึกษาเป็นวิธีค้นหาและวิธีวัด ไม่ใช่ความต่างของคุณภาพโค้ดที่เขียนเอง ทั้งสองเป็น search-based จึงไม่ได้ตอบคำถาม search เทียบกับ random; หากต้องการคำถามนั้นค่อยเพิ่ม Random Search เป็น baseline เสริมหลังจบงานหลัก

EvoSuite มี DYNAMOSA และ MIO ในรายการ algorithm แต่ต้องยืนยันด้วย smoke test ว่า build และ command ที่ใช้เลือกได้จริง ไม่ใช่อ่านชื่อ config แล้วถือว่าทำงานแล้ว [EvoSuite source](https://github.com/EvoSuite/evosuite/blob/master/client/src/main/java/org/evosuite/Properties.java)

มีหลักฐานเชิงทดลองสนับสนุน DynaMOSA แต่ไม่มีเหตุผลให้ประกาศว่าดีที่สุดสำหรับทุกโปรแกรมหรือทุก metric ก่อนทดลอง [งานเปรียบเทียบจาก EvoSuite](https://www.evosuite.org/experimental-data/evolutionary-algorithm-study/)

Claude มี Free plan และมีข้อจำกัดการใช้งาน จึงออกแบบการเก็บผลแบบแบ่ง session ไม่ใช้สมมติฐานว่าแชตฟรีเรียก API ได้ฟรี หากโควตาเต็มให้บันทึกและรอ ไม่เปลี่ยนโมเดลกลางชุดโดยไม่แยกผล [Claude pricing](https://claude.com/pricing)

OpenAI มี ChatGPT Free plan; ไม่ใช้สิทธิ์หรือข้อจำกัดของ Work/Codex มาอ้างว่าเป็นโควตาแชตเดียวกัน ให้ตรวจหน้าแชตและบัญชีจริงใน pilot [official OpenAI documentation](https://learn.chatgpt.com/docs/pricing) คู่ใหม่นี้เป็นข้อเสนอด้านความสะดวกและงบ ไม่ใช่ข้อสรุปว่าเขียนเทสต์เก่งกว่า Gemini

ตัวสำรองคือ Gemini แบบไม่มี Google AI plan ซึ่ง Google ระบุว่ามี standard limits จึงยังเป็นตัวเลือกได้หากไม่ผ่านเฉพาะโปรโมชัน/แพ็กเกจ แต่ไม่ได้แปลว่าบัญชีที่ถูกจำกัดการใช้บริการจะเข้าได้แน่นอน [Gemini limits](https://support.google.com/gemini/answer/16275805?hl=en) เปลี่ยนผู้ให้บริการได้ก่อน freeze; หลัง main run เริ่มให้แยก experiment version

## 3. Coverage ที่ต้องวัดและพิสูจน์

นิยามหลักอิง Lecture 6 และ Lab 7 ที่ตรวจไว้ใน `COURSE_READING_NOTES.md` ทุก metric เก็บทั้งจำนวนที่ครอบคลุม จำนวนทั้งหมด และรายการ IDs ไม่เก็บเพียงเปอร์เซ็นต์

| Metric | หน่วยที่นับ | เงื่อนไขสำคัญ |
|---|---|---|
| Line | executable source lines | ตรึงนโยบาย declarations/braces/multiline และ source revision |
| Statement | executable source statements | นับ AST statement ตามนโยบาย ไม่แทนด้วย bytecode instruction |
| Block | blocks ใน CFG ที่ประกาศ | มี source mapping และระบุการนับ predicate/entry/exit |
| Branch / Decision | outcomes ของ source-level decisions | if/loop เป็น T/F; switch กำหนดแขนงตาม successor/case policy ไม่เหมารวมว่าทุก decision มี 2 outcomes |
| Basic Condition | T/F ของ atomic condition แต่ละ occurrence | บันทึก NE เมื่อไม่ได้ประเมินจาก short-circuit; exception ก่อนจบไม่ถือว่ามี boolean outcome |
| Condition/Branch (C/DC) | condition outcomes และ decision outcomes รวมกัน | ใช้สูตรรวมจำนวนรายการ ไม่เฉลี่ยเปอร์เซ็นต์ |

`C/DC = (C_covered + D_covered) / (C_total + D_total) × 100`

Branch เป็นผลของ decision รวม ส่วน condition เป็นผลของเงื่อนไขย่อย แม้ expression จะเหมือนกันแต่คนละตำแหน่งก็เป็นคนละรายการ ตัวหารศูนย์เป็น N/A; ระบบวัดล้มเหลวเป็น unavailable

ต้องมี inventory สำหรับ ternary, switch, loop, short-circuit, boolean operators, return และ exception handling ตามขอบเขตที่รองรับ ไม่แอบตัด syntax ที่วัดไม่ได้ออกจาก denominator หากยังรองรับคลาสใดไม่ครบให้แสดง unsupported และแก้ก่อนนำคลาสนั้นเข้า primary cohort

Uncovered ไม่เท่ากับ infeasible: ไม่ลบรายการเพราะหาเทสต์ไม่เจอ ตัวเลขหลักคง structural denominator ไว้; รายการที่พิสูจน์ว่า infeasible ได้ให้แสดงเหตุผลแยก หากมี adjusted coverage ให้รายงานเป็นผลรองพร้อมสูตร

**MC/DC และ path:** ทำตัวอย่างอธิบายพร้อมหลักฐานคู่เทสต์และเส้นทางบนเมธอดที่เลือก 3–5 เมธอด หลังระบบหลักผ่าน ระบุ MC/DC variant และขอบเขตลูปให้ชัด ไม่ประกาศ full path coverage ของโปรแกรมที่มีลูป และไม่เรียก truth-table coverage ว่า path coverage ทั้งโปรแกรม

## 4. สถาปัตยกรรมระบบวัด

แยก generation ออกจาก measurement:

`fixed source → generator → original suite → compile/validate → frozen admissible suite → coverage replay on fixed + regression replay on buggy → report`

ส่วนประกอบ:

1. **Environment/benchmark manager:** checkout fixed/buggy, export classpath, build, เก็บ hashes และตรวจ triggering test ของ benchmark โดยไม่ส่งให้ generator
2. **Source inventory และ CFG builder:** parse Java, สร้าง IDs, source-to-node mapping และกราฟ; เก็บกราฟ compound decision แยกจากรายละเอียด atomic conditions
3. **Execution recorder:** instrument สำเนาโค้ดสำหรับการวัด เก็บ block/decision/condition events โดยไม่เปลี่ยนลำดับประเมิน จำนวนครั้งเรียก side effects หรือ semantics ของ exception
4. **Generator adapters:** EvoSuite DynaMOSA/MIO และตัวนำเข้าไฟล์ผลจาก ChatGPT/Claude พร้อม provenance
5. **Validator/evaluator:** ตรวจ compile, stability, assertions, coverage และ fixed-versus-buggy outcomes
6. **Aggregator/report:** สร้างตาราง ตัวอย่าง CFG และรายงานจาก raw artifacts ที่เก็บไว้

ใช้ Java AST/CFG tooling ที่เหมาะกับ syntax ของชุดข้อมูล เลือก library/version หลัง compatibility spike ไม่เขียน parser ด้วย regex ต้องตรวจเรื่อง scope, evaluation order, unboxing, constructor calls, try/finally และ short-circuit ก่อนใช้กับจริง

JaCoCo ใช้เป็น counter อ้างอิงเสริม โดยติดป้าย metric ของมันไว้ชัด ไม่ถือว่า instruction เป็น statement หรือ branch counter ตรงกับ source-level decision/condition ของวิชาโดยอัตโนมัติ [นิยาม JaCoCo counters](https://www.jacoco.org/jacoco/trunk/doc/counters.html)

ระหว่าง search ให้ EvoSuite ใช้ fitness/branch distance ของ framework ที่ตรึงเหมือนกันทั้งสอง algorithm; วัด course metrics ด้วยระบบกลางหลัง generation ต้องรายงานชัดว่า optimization target อาจต่างจาก reporting metric ไม่อ้างว่า optimize C/DC ถ้าไม่ได้ทำจริง

## 5. ขั้นตรวจความถูกต้องก่อน benchmark

สร้างชุดตัวอย่างที่นับคำตอบด้วยมือ พร้อมโค้ด CFG ตารางเทสต์และ trace:

- if/else เงื่อนไขเดียว; nested decisions; early return
- `&` เทียบ `&&`, `|` เทียบ `||`, negation และ short-circuit หลายชั้น
- loop แบบ 0/1/หลายรอบ รวม break/continue
- switch หลาย labels/default/fall-through และ ternary ตาม syntax ที่พบจริง
- boolean expressions ที่มี side effects, method calls หรือ exception
- try/catch/finally และ constructs เพิ่มเติมที่พบใน pilot
- โค้ดหลาย statements ในบรรทัดเดียว และ statement หลายบรรทัด
- suite ว่าง, metric ไม่มี items และเทสต์เดิมรันซ้ำ

Golden examples จากวิชา:

| ตัวอย่าง | คำตอบที่ต้องตรง |
|---|---|
| `cats\|dogs` | block 10/10, decision 5/6 |
| เพิ่ม `cats\|dog` | block 10/10, decision 6/6 |
| `a > 10 & b > 20`, inputs (20,10), (5,30) | condition 4/4, decision 1/2, C/DC 5/6 |
| เปลี่ยนเป็น `&&`, inputs เดิม | condition 3/4, decision 1/2, C/DC 4/6 |
| รัน input เดิมซ้ำ | จำนวน distinct covered items ไม่เพิ่ม |

เกณฑ์ผ่าน: ตัวนับตรงกับคำตอบที่ตรวจด้วยมือทุกกรณี; instrumented กับ original ให้ผลและลำดับ side effects ตรงกัน; trace ย้อนกลับหาโค้ดได้; unsupported constructs ถูกตรวจพบ ไม่ถูกละเลย ต้องผ่านก่อนเก็บผลหลัก ตัวอย่างทดสอบให้หลักฐานเฉพาะขอบเขตที่ตรวจ ไม่ใช่การพิสูจน์ว่ารองรับ Java ทุกแบบ

## 6. ชุดข้อมูลและการคัดเลือก

Defects4J README ที่ตรวจ ณ วันที่วางแผนระบุ version 3.0.1 มี 854 active bugs และ 10 deprecated bugs จาก 17 projects; ใช้ Java 11 และ timezone ที่ framework กำหนดสำหรับ reproducibility [Defects4J README](https://github.com/rjust/defects4j/blob/master/README.md)

รอบแรกใช้ **pilot 3 bugs และ main study 15 bugs** โดยไม่นำ pilot มาปะปนกับ main study ตั้งต้นจาก Lang, Math และ Cli อย่างละ 5 bugs ใน main study; รายชื่อจริงเลือกหลังตรวจ build และ measurement compatibility แล้วตรึงก่อนดูผลผู้ชนะ

หน่วยเป้าหมายคือ `(project, bug ID, fixed revision, target class)` เลือก production classes ที่ patch แตะทั้งหมดของแต่ละ bug เป็น scope ไม่เลือกเฉพาะเมธอดที่วิธีใดทำได้ดี กำหนด inner/nested classes และ dependency code ใน inventory ให้ชัด Coverage headline เป็น target scope ไม่ใช่ coverage ทั้งโครงการ

ให้ K เป็นจำนวน target classes รวมของ main study: **15 bugs ไม่จำเป็นต้องเท่ากับ 15 classes** งานหลายคลาสของ bug เดียวต้องรวม suite ภายใน repeat เดียวกันเพื่อประเมินระดับ bug

ขั้นคัดเลือก:

1. อ่าน active bug metadata ตรวจ build และ fixed/buggy baseline ในสภาพแวดล้อมที่ตรึง
2. คัดตาม compatibility, source availability และ constructs ที่ระบบวัดรองรับครบ ไม่คัดจาก generated coverage หรือจำนวน bugs ที่ตรวจพบ
3. แบ่งชั้นตามขนาด/จำนวน decisions แล้วสุ่มด้วย seed ที่ประกาศให้ได้ 5 bugs ต่อ project; เก็บ candidate list และ exclusion reasons
4. ขนาด class/context ต้องพอดีกับการให้ input เดียวกันแก่ AI ทั้งสอง ระบุเพดานตาม pilot ก่อนสุ่ม; หากทำ context แบบแบ่งส่วนให้ใช้ policy เดียวกันและนับ requests ทุกครั้ง
5. Freeze cohort และจำนวน K พร้อม manifest ก่อน main run; generator ล้มเหลวภายหลังเป็นผลการทดลอง ไม่ใช่เหตุผลตัด target ทิ้ง

ชุดนี้เป็น subset ที่เลือกตามขอบเขตเครื่องมือ มี selection bias และขนาดเล็ก จึงไม่ใช้สรุปแทน Defects4J ทั้ง 854 bugs การขยายเป็น 30–50 bugs เป็นระยะถัดไปหลังงานหลักครบ

## 7. Protocol ที่ใช้ร่วมกัน

### 7.1 ข้อมูลและ oracle

ทุกวิธีสร้างเทสต์จาก fixed revision และ scope เดียวกัน อนุญาต API/dependency context ที่กำหนดไว้ ไม่ให้ patch diff, issue description ที่ชี้คำตอบ, triggering tests หรือผลจาก buggy revision ระหว่างสร้าง/แก้เทสต์ AI ไม่ใช้ web search/connectors/memory จากงานก่อน และเริ่มแชตใหม่ต่อ independent generation เท่าที่แพลตฟอร์มรองรับ

การเลือก target จาก patch metadata เป็นการประเมินแบบรู้ตำแหน่งคลาสที่เกี่ยวข้องอยู่แล้ว ต้องเปิดเผยข้อจำกัดนี้ ชื่อ benchmark ที่ซ่อนจาก prompt ช่วยลดคำใบ้ตรง ๆ แต่ไม่รับประกันไม่มี training-data contamination

Fixed implementation เป็น reference oracle เหมือนกันในระดับ protocol แต่ EvoSuite กับ LLM มีวิธีสร้าง assertions ต่างกัน จึงตีความการเปรียบเทียบข้ามกลุ่มว่าเป็นผลของ workflow ทั้งชุด ไม่ใช่ผลบริสุทธิ์จาก algorithm เพียงตัวเดียว

เทสต์ต้องมี assertion ที่ตรวจพฤติกรรมจริง ห้าม unconditional pass, swallow ทุก exception หรือ mock target จนไม่มี execution ตรวจคุณภาพ assertion เพิ่มจาก pass rate ไม่ถือว่า coverage สูงแปลว่าตรวจ bug ได้ดี

### 7.2 Validation

เก็บ original suite เสมอ และใช้กฎคัดเทสต์ที่ประกาศไว้ล่วงหน้าเหมือนกันทุกวิธี: compile ผ่าน, มี oracle ที่อธิบายได้ และผ่าน fixed ใน 3 fresh JVM runs การตรวจซ้ำนี้เป็น stability check ไม่ใช่ generation เพิ่มอีก 3 รอบ

เทสต์ที่ผิด/ไม่เสถียรต้องเก็บสถานะและเหตุผล ไม่ลบทิ้งจากจำนวนที่ผลิต หากแยก runnable subset ได้โดยกฎอัตโนมัติให้เก็บเป็น admissible suite; ไม่ช่วยเขียนเนื้อหาเทสต์ให้วิธีใดเป็นพิเศษ

Coverage หลักวัด union ของ items จาก admissible suite บน fixed revision ถ้ากระบวนการ generation ทำงานแต่ไม่เหลือเทสต์ใช้ได้ ให้ระบุ empty suite และ coverage 0 เมื่อ denominator มากกว่า 0; ถ้าระบบวัด/build infrastructure ใช้งานไม่ได้ให้เป็น unavailable ไม่ปลอมเป็น 0

วัด coverage จาก generated tests เท่านั้น ไม่รวม existing tests หรือ triggering test ของ benchmark ไว้ในตัวเลขหลัก

### 7.3 การตรวจพบ bug

ตรึง suite แล้วรันบน original fixed และ buggy revisions โดยใช้ tests เดียวกัน; การตัดสิน fault detection ใช้โค้ดที่ไม่ผ่าน measurement instrumentation เพื่อลดผลรบกวน

นับ bug ว่าตรวจพบเมื่อมี test ที่ผ่าน fixed และ fail บน buggy ซ้ำได้ 3 fresh runs พร้อมตรวจว่า assertion failure/exception เกิดจากพฤติกรรมของ bug ไม่ใช่ environment error, API incompatibility หรือ timeout ที่ยังไม่ยืนยันเหตุผล Compile failure บน buggy รายงานแยก ไม่ถือเป็น assertion-based detection โดยอัตโนมัติ

ไม่ส่ง buggy failures กลับไปให้ generator ปรับเทสต์หลังเริ่ม evaluation หากต้องศึกษา feedback-directed repair ให้เป็นการทดลองอีกชุด

## 8. จำนวนรอบและงบ

| กลุ่ม | งบต่อ target class | Independent repetitions |
|---|---|---:|
| DynaMOSA | search 60 และ 180 วินาที | 10 seeds ต่อ budget |
| MIO | search 60 และ 180 วินาที | seed set เดียวกัน 10 seeds ต่อ budget |
| ChatGPT Free | prompt แรก + repair ได้ไม่เกิน 2 responses | 3 แชตใหม่ |
| Claude Free | prompt/context/repair policy เดียวกับ ChatGPT | 3 แชตใหม่ |

Algorithm runs รวม `2 × 2 × 10 × K = 40K`; AI generations รวม `2 × 3 × K = 6K`; AI responses สูงสุด `18K` เมื่อหนึ่ง generation ใช้ครบ 3 responses ไม่รวมการแบ่ง context ซึ่งต้องล็อกต่างหากใน pilot

ตัวอย่างถ้า K=15: 600 algorithm runs, 90 AI generations, สูงสุด 270 AI responses และ algorithm search budget รวม 20 ชั่วโมง การ build/startup/assertion generation/validation/coverage replay ไม่รวมอยู่ใน 20 ชั่วโมง ต้องวัดจริงจาก pilot แล้วคำนวณเวลาเครื่องใหม่ หาก K=30 ตัวเลขเหล่านี้เพิ่มเป็นสองเท่า

ใช้ search budget แยกจาก wall-clock timeout; กำหนด CPU/RAM/JVM limits และ concurrency คงที่ ไม่เปิดงานแข่งขันทรัพยากรจนเวลา search เปรียบเทียบไม่ได้ เก็บ generation, postprocessing, evaluation และ queue/quota waiting time แยกกัน

สำหรับ AI ใช้ prompt template/context hash เดียวกัน แต่ไม่อ้างว่าบังคับ sampling seed, temperature หรือ model snapshot ได้ถ้า UI ไม่เปิดเผย เก็บชื่อโมเดลที่แสดงจริง วันที่ เวลา mode และ transcript; ถ้ารุ่นเปลี่ยนให้แบ่ง batch วิเคราะห์ ไม่รวมเงียบ ๆ

Repair ให้เฉพาะ compiler diagnostics หรือ fixed-validation feedback รูปแบบเดียวกัน ไม่ส่ง coverage gaps ในการทดลองหลักและไม่ส่ง buggy outcome ไม่แก้ด้วยมือแบบไม่บันทึก เก็บ first-shot และ after-repair แยก

ไม่อ้างว่า 180 วินาทีของ EvoSuite เท่ากับ 3 responses ของ AI: การเทียบ algorithm-to-algorithm ควบคุม compute budget ส่วน AI-to-AI ควบคุมข้อมูลและ response budget; การเทียบทั้งสี่รายงานคุณภาพและค่าใช้ทรัพยากรควบคู่กัน ไม่มีการประกาศผู้ชนะภายใต้งบเท่ากันข้ามกลุ่ม

## 9. สถิติและการรายงาน

- Primary metric: source-decision coverage บน fixed target scope ที่ algorithm budget 180 วินาที; 60 วินาทีเป็น sensitivity comparison ส่วน AI รายงานตาม response budget ที่กำหนด
- Secondary: line, statement, block, condition, C/DC, valid-suite rate, first-shot compile/pass rate, detected bugs, test count, execution cost และ human effort
- แสดงผลทุก target รวมถึง failures; ตาราง complete comparable targets เป็นผลรองที่ระบุจำนวน ไม่ใช้เฉพาะ successful runs แล้วปกปิดจำนวนที่หาย
- สรุป repeats ภายใน target ก่อน แล้วจับคู่เปรียบเทียบบน targets เดียวกัน ไม่ถือ 10 seeds ของ bug เดียวเป็น 10 bugs อิสระ
- แสดง median/IQR และ paired differences เป็นหลัก พร้อมช่วงความไม่แน่นอนที่ resample ระดับ bug เพื่อเก็บ classes/repeats ที่สัมพันธ์กันไว้ด้วยกัน; 15 bugs ให้ข้อสรุปจำกัด ไม่พึ่ง p-value อย่างเดียว
- DynaMOSA เทียบ MIO เป็น primary contrast; หากทำหลาย pairwise tests ให้ประกาศ family และปรับ multiple comparisons เช่น Holm ภายหลังเลือกรูปแบบสถิติที่ตรง distribution/จำนวนข้อมูลจริง
- แสดง macro average และ pooled counts แยกกันพร้อมสูตร ไม่ให้คลาสใหญ่กลบคลาสเล็กโดยไม่อธิบาย
- Coverage suite เป็น union ภายใน run; หากรวมหลาย repeats เพื่อดู best attainable coverage ให้เป็นผลเสริมและระบุ budget รวม
- Fault detection นับ unique bug IDs; รายงานต่อ repetition และสัดส่วน detection ต่อ bug การนับพบอย่างน้อยหนึ่งครั้งจาก 10 repeats เทียบกับ 3 repeats มีงบต่างกัน ต้องติดป้ายและให้ผลเทียบ 3 repeats แรกเป็นผลรอง

เลือก case studies ทั้งกรณี coverage สูงแต่ไม่พบ bug, coverage ต่ำแต่พบ bug และ short-circuit/condition gaps พร้อม CFG และ execution evidence โดยไม่เลือกเฉพาะตัวอย่างที่สนับสนุนวิธีที่ชอบ

## 10. ลำดับงานและเกณฑ์ส่งต่อ

| ระยะ | งาน | ผลส่งมอบและเกณฑ์ผ่าน |
|---|---|---|
| 1: นิยาม | เขียน counting policy, metric IDs, exception/switch/short-circuit rules, sampling และ oracle protocol | measurement specification ตรวจย้อนถึงสไลด์ได้; ไม่มีชื่อ metric กำกวม |
| 2: สภาพแวดล้อม | ใช้ Linux ผ่าน WSL2/container ตามความพร้อมเครื่อง ตรึง Defects4J/EvoSuite/JDK/dependencies และ export metadata | checkout/build fixed+buggy และ triggering test ใน pilot ใช้ได้; DynaMOSA/MIO smoke test ยืนยัน algorithm |
| 3: ระบบวัด | AST/CFG, instrumentation, trace, aggregation และ golden fixtures | ตัวอย่างนับมือและ differential semantic checks ผ่านทั้งหมดใน scope |
| 4: Pilot | 3 bugs; ทั้งสี่วิธี; วัดต้นทุน โควตา context และ failure modes | pipeline end-to-end, metrics ครบ, ตรวจ CFG/trace ด้วยมือ และปรับแผนเวลา/ขนาดก่อน freeze |
| 5: Freeze | เลือก main 15 bugs, target manifests, seeds, prompt, budgets และ analysis policy | มี run manifest/version hashes; ไม่ปรับตามผลแพ้ชนะ |
| 6: Main run | รันเป็น batches ที่ restart ได้ เก็บทุก attempt และจับคู่ AI ในช่วงวันที่ใกล้กัน | expected jobs ครบหรือมี failure status ชัดเจน; artifacts ไม่ทับกัน |
| 7: วิเคราะห์ | สรุปตาม target/bug, uncertainty, detection audit และ case studies | ทุกเปอร์เซ็นต์ย้อนถึง denominator/trace ได้ |
| 8: ส่งมอบ | รายงาน กราฟ CSV และคำสั่งทำซ้ำ | rerun ตัวอย่างที่เลือกจาก manifest ได้ และสร้างตารางจาก raw data ใหม่ได้ |

หากระบบวัดไม่ผ่านระยะ 3 ให้แก้ก่อน main run หากรองรับ syntax ได้ไม่ครบ ให้ขยาย implementation หรือประกาศ subset ที่รองรับและคัดก่อน freeze ห้ามเปลี่ยน metric เป็นตัวอื่นแล้วใช้ชื่อเดิม หาก AI quota ทำให้เก็บข้อมูลช้าให้ขยาย calendar time; การลด repetitions/cohort ต้องแก้แผนก่อน main study หรือบันทึก deviation ชัดเจน

## 11. เวลาโดยประมาณ

เป็นประมาณการพัฒนาสำหรับคนเดียว ไม่ใช่เวลาที่วัดจากเครื่องนี้แล้ว:

| งาน | ชั่วโมงแรงงาน |
|---|---:|
| นิยามและวาง evidence schema | 15–25 |
| Environment และ generator adapters | 20–35 |
| Source-level measurement, CFG และ semantic verification | 80–130 |
| Pilot และแก้ integration | 25–40 |
| คุม main runs, AI sessions และตรวจผล | 30–50 |
| วิเคราะห์ รายงาน และ reproduction package | 30–40 |
| รวมก่อนเผื่อปัญหา | 200–320 |

เผื่อประมาณ 20% เป็น **240–384 ชั่วโมง** หรือประมาณ **12–20 สัปดาห์ที่ 20 ชั่วโมง/สัปดาห์** งาน AI quota และรันเครื่องอาจซ้อนกับงานอื่นได้ เวลาจริงขึ้นกับ K, ความยาก instrumentation และสภาพแวดล้อม ต้องปรับหลัง pilot ไม่สัญญาว่าทำครบในเวลานี้ได้หากขยาย scope หรือเขียน engine รองรับ Java ทุก syntax

เป้าหมายระยะแรกคือภายในประมาณ 3–5 สัปดาห์ได้ environment, counting specification และ measurement prototype ที่ตรวจได้บางส่วน จากนั้นจึงประเมินวันจบใหม่ การทำครบ 854 bugs ไม่อยู่ในประมาณการนี้

## 12. โครงสร้างไฟล์และหลักฐานที่ต้องมี

โครงสร้างด้านล่างเป็นแผนสำหรับสร้างระหว่าง implementation ไม่ได้หมายความว่าไฟล์เหล่านี้มีแล้ว:

```text
inputs/                       เอกสารต้นฉบับ ไม่แก้ทับ
src/measurement/              inventory, CFG, instrumentation, trace
src/generators/               adapters และ AI import/validation
src/evaluation/               fixed/buggy replay และ aggregation
tests/golden/                 โค้ดตัวอย่าง + expected counts/paths
work/environments/            environment/build logs
work/checkouts/               fixed/buggy working copies
work/runs/<run_id>/            prompts, suites, logs, traces, metadata
outputs/measurement-spec.md
outputs/experiment-protocol.md
outputs/dataset-manifest.csv
outputs/run-manifest.csv
outputs/results-per-run.csv
outputs/results-per-bug.csv
outputs/cfg/                  กราฟ source-linked และ case studies
outputs/final-report.md
outputs/reproduce.md
```

ขั้นต่ำแต่ละ run: project/bug/revision, target scope, source hash, tool/model label/version, seed/repeat, prompt/context hashes, budgets, timestamps, hardware/runtime, original/final test hashes, generation/compile/validation statuses, item inventory/hash, covered IDs, raw traces, repair history และ stdout/stderr

ขั้นต่ำแต่ละ test: input/setup, expected, oracle provenance, actual, result, node/edge path, decision outcomes, atomic outcomes รวม NE และ assertion evidence เก็บรายละเอียดผล trace ตาม invocation/thread เมื่อเกี่ยวข้อง ไม่อาศัยชุด T/F รวมเพื่ออธิบาย MC/DC คู่เทสต์

## 13. เงื่อนไขถือว่างานเสร็จ

1. มี counting specification, CFG mapping และ golden checks ที่ผ่านและตรวจด้วยมือแล้ว
2. Main cohort มีผลทุก planned job หรือระบุ failure/missing พร้อมเหตุผลโดยไม่ปกปิด
3. ทุก metric รายงาน covered/total/percent และย้อนกลับถึงหลักฐานได้
4. ตรวจ bug detection บน fixed/buggy อย่างเป็นระบบ และแยก infrastructure failures
5. รายงานความต่างของ budget, oracle, repetitions, quota/model drift และ subset selection
6. ส่งโค้ด configuration manifests transcripts ที่แชร์ได้ raw results และขั้นตอนสร้างรายงานซ้ำ

ลำดับเริ่มงานที่ชัดเจน: **เขียน measurement specification → ตรวจ environment → สร้าง golden measurement prototype → pilot → freeze → main study**

## 14. แหล่งอ้างอิงและสถานะปัจจุบัน

แหล่งหลักของ course metrics คือ `inputs/05-other-materials/2026_Lecture6_Whitebox.pdf` โดยเฉพาะหน้า 9–42 และ `Lab7_Strcutural.pdf` หน้า 5–15; ประเด็น oracle/coverage ใน `2026_Lecture11_AdvIntelligentTesting (3).pdf` รายละเอียดการอ่านอยู่ใน [บันทึกประกอบ](COURSE_READING_NOTES.md)

ลิงก์ทางการของ EvoSuite, Defects4J, Claude และ JaCoCo อยู่ใกล้ข้ออ้างในเนื้อหา ตรวจวันที่ 2 พฤศจิกายน 2569 ต้องตรึง release/commit ที่ติดตั้งจริงแทนลิงก์ master ใน reproduction manifest

ปัจจุบันอ่านเอกสารและตรวจตัวอย่างเล็กจากสไลด์แล้ว ยังไม่ได้ติดตั้ง/ทดลอง Defects4J ชุดหลัก และยังไม่มีผลที่ตัดสินว่าวิธีใดดีที่สุด เอกสารนี้คือแผนงานฉบับใหม่ ไม่ใช่รายงานผลการทดลอง
