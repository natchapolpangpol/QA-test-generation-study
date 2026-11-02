# บันทึกการอ่านเอกสาร SQA และข้อกำหนดการวัด Coverage

วันที่ตรวจเอกสาร: 2 พฤศจิกายน 2569

บันทึกนี้ใช้เป็นฐานความเข้าใจร่วมสำหรับงานเปรียบเทียบ DynaMOSA, MIO, Gemini และ Claude บน Defects4J โดยยึดนิยามในเอกสารของวิชาและตรวจพฤติกรรม Java จริงประกอบ เป้าหมายคือแยกความครอบคลุมของโครงสร้างโค้ดออกจากจำนวนรอบทดลอง จำนวนเทสต์ และอัตราผ่านอย่างชัดเจน

เอกสารเป็นแหล่งข้อมูลของรายวิชา ไม่ใช่คำสั่งให้ดำเนินการทุกกิจกรรมในแลบ ไม่ได้นำข้อกำหนดเรื่องกลุ่ม กำหนดส่ง บริการ AI ของมหาวิทยาลัย หรือการอนุมัติในแม่แบบรายงานกลับมาบังคับโปรเจกต์ส่วนตัวนี้

## ขอบเขตการอ่าน

พบเอกสาร 25 ฉบับ ประกอบด้วย PDF 23 ฉบับ รวม 841 หน้า และ DOCX 2 ฉบับ พร้อมไฟล์ทางลัดงานเก่า 1 ไฟล์ อ่านเนื้อหาแกนหลักเรื่อง coverage, CFG, Lab 7 และหัวข้อ search-based testing/oracle โดยละเอียด ตรวจภาพตัวอย่างที่มีสูตรหรือโค้ดซึ่งการดึงข้อความอย่างเดียวอ่านไม่ครบ ส่วนหมวดเสริมตรวจโครงสร้างเนื้อหาและหน้าที่เกี่ยวข้องกับการออกแบบงาน ไม่ได้ตรวจทุกภาพหน้าจอการติดตั้งเครื่องมือทั้ง 841 หน้า

ไฟล์ต้นฉบับยังอยู่ใน `inputs` และไม่ถูกแก้ไข ข้อความที่สกัดและภาพตรวจอยู่ใน `work/course-reading` ไม่ใช่ผลทดลอง Defects4J

| เอกสาร | หน้า | ประเด็นที่นำมาใช้ / ระดับการตรวจ |
|---|---:|---|
| CourseSyllabus_SQA2026.pdf | 5 | อ่านข้อกำหนดและตารางวิชา แยก lecture กับ lab |
| SQA_Project_2026.docx | — | อ่านข้อกำหนดโครงงาน การวัด การทำซ้ำ และการส่งหลักฐาน |
| 2026_Lecture6_Whitebox.pdf | 57 | อ่านละเอียดทุกหน้าข้อความ ตรวจภาพสำคัญ 29 หน้า: CFG, DD-path, coverage, C/DC, path, MC/DC |
| Lab7_Strcutural.pdf | 15 | อ่านละเอียดทุกหน้าข้อความ: ลำดับ CFG → line → block → branch → condition → C/DC |
| 2026_Lecture11_AdvIntelligentTesting (3).pdf | 71 | อ่านเนื้อหา static/mutation/fuzz/search และ AI testing; เน้นหน้า 16–18, 34–43, 52–55 |
| 2026_Lecture2_PrincipleSWTesting.pdf | 36 | ทบทวน black/white/gray-box ระดับการทดสอบ และข้อจำกัด exhaustive testing |
| 2026_Lecture3_Blackbox_BVT.pdf | 44 | ทบทวน normal/robust/worst-case BVT และจำนวนเทสต์ ไม่ใช้จำนวนดังกล่าวแทน structural coverage |
| 2026_Lecture5_Blackbox_DT.pdf | 45 | ทบทวน decision table, rule combinations, infeasible combinations และ state transitions |
| 2026_Lecture7_ModelBaseTesting.pdf | 45 | ทบทวน state/transition coverage, transition trees และเส้นทางที่มีลูป |
| 2026_Lecture8_SelfTestingSystems (2).pdf | 62 | ทบทวน oracle, assertions, pre/postconditions, invariants และ design by contract; ไม่ได้ตรวจทุกภาพโค้ด |
| 2026_Lecture9_PragmaticTesting (2).pdf | 62 | ทบทวน unit/integration/system levels, test doubles, testability, FIRST |
| 2026_Lecture10_NonfunctionalTesting (2).pdf | 37 | สำรวจ performance/load/stress/usability; แยก checklist coverage จาก code coverage |
| 2026_Lecture12_DefectManagement (1).pdf | 38 | อ่านประเด็น defect evidence, severity/priority, reporting และความต่างระหว่าง metrics |
| 2026_Lecture13_ImprovingSoftwareQualityAndSoftwareProcess (1).pdf | 63 | อ่านประเด็น metric validity, reliability, process/product และ quality planning |
| Lab3_JUnit.pdf | 53 | สำรวจ setup/Git และข้อกำหนด JUnit test design; ไม่ตรวจทุกภาพหน้าจอติดตั้ง |
| Lab4_BVT.pdf | 38 | ทบทวน AAA, assertions, parameterized/repeated tests และงาน BVT |
| Lab5_EC.pdf | 16 | ทบทวน MethodSource, input/output EC และงานท้ายแลบ |
| Lab6_DT.pdf | 7 | อ่าน LEDT/EEDT และข้อกำหนดออกแบบ/รันเทสต์ |
| Lab8_IntegrationTesting (1).pdf | 30 | ทบทวน top-down/bottom-up, driver/stub และ test doubles |
| Lab9_TestDouble (1).pdf | 24 | ทบทวน dummy/fake/stub/spy/mock, Mockito และงานท้ายแลบ |
| Lab10_APITesting_Postman (1).pdf | 25 | สำรวจ API tests, response assertions และ schema validation |
| Lab11_UAT.pdf | 20 | สำรวจ Robot Framework และขอบเขต UAT |
| Lab12_JMeter (2).pdf | 32 | สำรวจ load configuration, loop count, listeners และ performance metrics |
| Lab13_Metrics (1).pdf | 16 | อ่านวัตถุประสงค์ static analysis/PMD/Checkstyle; ไม่ถือจำนวน warnings เป็น coverage |
| Test_Summary_Report_Template (1).docx | — | อ่านทุกหัวข้อ; แยก execution progress/pass rate ออกจาก structural coverage |

ไม่พบไฟล์เฉลย Lab 7 ที่ตรวจแล้วหรือข้อความคอมเมนต์อาจารย์โดยตรงในชุดเอกสารนี้ ไฟล์ `งานเก่า.url` ชี้ไป repository ของงานเก่า จึงไม่สามารถระบุเหตุผลการหักคะแนนแทนอาจารย์ได้

## ข้อค้นพบที่เปลี่ยนแผนเดิม

1. วิชาใช้ branch/decision coverage ระดับผลของ decision รวม ไม่ควรใช้ทุก edge ใน CFG หรือทุก bytecode jump แทนโดยไม่มี mapping (Lecture 6 หน้า 35–37; Lab 7 หน้า 5–6)
2. Basic condition coverage แยก compound condition เป็นเงื่อนไขย่อยและต้องได้ทั้ง True/False (Lecture 6 หน้า 38–40; Lab 7 หน้า 7–8)
3. C/DC มีสูตรรวมจำนวนรายการโดยตรงใน Lecture 6 หน้า 41 และ Lab 7 หน้า 9 ต้องเพิ่มค่านี้ในแผน ไม่ใช่รายงานแค่ branch และ condition แยกกัน
4. Lab 7 ต้องมี CFG, block numbers, edge names และ test cases ที่อ้างอิงกราฟ ใช้ DD-path เมื่อเหมาะสม ไม่ใช่มีเพียงเปอร์เซ็นต์สรุปจากเครื่องมือ
5. ตัวอย่างหน้า 42 ใช้ Boolean `&` ไม่ใช่ `&&` ความต่างนี้เปลี่ยนจำนวน condition outcomes ที่ประเมินจริง
6. บท Advanced Testing หน้า 17–18 ยกตัวอย่าง coverage สูงแต่ไม่มี assertion จึงต้องวัด fault detection และตรวจ oracle ควบคู่
7. จำนวนการค้นหา จำนวน generation runs จำนวน fixed-validation repetitions และจำนวน bugs เป็นคนละหน่วย ไม่ใช้แทนกัน
8. แม่แบบ Test Summary เป็นรายงานหลายระดับ ไม่ใช่พจนานุกรม structural coverage ช่องตัวอย่างและค่า threshold ในแม่แบบไม่ใช่ผลจริงหรือข้อบังคับอัตโนมัติของโครงงานนี้

## นิยามการวัดที่จะใช้

ให้กำหนดขอบเขตเป็น project + bug ID + revision + รายการคลาส/เมธอด + source hash + เวอร์ชันรายการ coverage items ก่อนรัน แล้วใช้รายการเดียวกันเมื่อเปรียบเทียบวิธีต่าง ๆ ภายในเป้าหมายนั้น

| Metric | ตัวตั้ง | ตัวหาร | หลักฐาน |
|---|---|---|---|
| Line | source lines ที่ถูก execute แบบไม่ซ้ำ | executable source lines ตามนโยบายที่ประกาศ | source locations และ execution records |
| Statement | executable statements ที่ถูก execute แบบไม่ซ้ำ | executable statements ในขอบเขต | AST statement IDs และ trace |
| Block | blocks ที่ถูก execute แบบไม่ซ้ำ | blocks ของ CFG ที่กำหนด | block inventory และ trace |
| Branch/Decision | ผลของ source decisions ที่เกิดขึ้นจริง | ผล decision ทั้งหมด เช่น D1:T, D1:F | decision inventory และผลประเมินจริง |
| Basic condition | True/False outcomes ของ atomic condition occurrences ที่ถูกประเมินจริง | outcomes ทั้งหมดของเงื่อนไขย่อย | C1:T, C1:F ฯลฯ พร้อมตำแหน่งและ trace |
| C/DC | covered condition outcomes + covered decision outcomes | total condition outcomes + total decision outcomes | tagged inventories ทั้งสองชุดและผล union ของเทสต์ |

ทุกเปอร์เซ็นต์คำนวณจากจำนวนรายการที่ครอบคลุมหารจำนวนทั้งหมด แล้วคูณ 100 ตัวหารศูนย์เป็น N/A; ไม่พบเครื่องมือวัดหรือวัดไม่สำเร็จเป็น unavailable ไม่ใช่ศูนย์

สูตร C/DC ที่ถอดเป็นหน่วยชัดเจนจากสไลด์:

`C/DC = (C_covered + D_covered) / (C_total + D_total) × 100`

โดย C เป็น atomic-condition outcomes และ D เป็น source-decision outcomes ทั้งสองชุดมีชนิดรายการแยกกัน แม้ decision ที่มีเงื่อนไขเดียวจะสัมพันธ์กับ condition เดียวกันก็ตาม เก็บ subcounts ทั้งสองไว้เสมอ ไม่ใช้ค่าเฉลี่ยเปอร์เซ็นต์แบบไม่ถ่วงน้ำหนักแทนสูตรนี้

เมื่อมี m atomic condition occurrences โดยทั่วไปมี 2m outcomes ก่อนพิจารณาความเป็นไปได้ ห้ามนับเฉพาะผล True หรือนับจำนวน expressions แล้วอ้างว่าครบทั้ง True/False

Lecture 6 หน้า 9–12 ใช้ตัวอย่างจำนวนบรรทัดที่ขึ้นกับการจัดรูปแบบ ในโค้ดจริงต้องประกาศการนับ blank/comment/declaration/braces/synthetic code ให้ชัด ไม่อ้างว่า line counter ของ JaCoCo จะให้ตัวหารตรงสไลด์โดยอัตโนมัติ และไม่ใช้ instruction coverage แทน source-statement coverage

## CFG และตัวอย่างที่ตรวจแล้ว

แนวทางใน Lecture 6 หน้า 13–31 และ Lab 7 หน้า 10–15:

- ใส่หมายเลขบรรทัดหรือ statement และระบุ source-to-node mapping
- ใช้ process blocks เป็น maximal sequences ที่ทำงานต่อกันโดยไม่มีแขนงภายใน
- แสดง decision, junction, loop และกรณี switch ตามโครงสร้างจริง
- มี source และ sink; หากมีหลาย return ให้รวมไปยัง synthetic sink สำหรับการวาด แต่ไม่เพิ่ม synthetic sink เป็น executed statement โดยอัตโนมัติ
- ใช้ DD-path เป็นการย่อกราฟโดยเก็บ mapping กลับไปยังโค้ดไว้
- แยกกราฟ compound decisions สำหรับ branch coverage ออกจากกราฟ atomic conditions สำหรับ condition coverage
- Block ในตัวอย่างสอนนับรวม predicate blocks ด้วย ไม่จำกัดเฉพาะกล่อง assignment; junction/entry/exit ที่เพิ่มเพื่อการวาดต้องประกาศว่าจะนับหรือไม่
- ทุก test case ต้องเชื่อมกับ input, expected result, actual result, node path/edge path และรายการที่ครอบคลุมจริง
- รูป CFG และเส้นทางที่คาดหมายยังไม่ใช่หลักฐาน execution ต้องมี trace จากการรัน

ตัวอย่าง CountLetters ใน Lecture 6 หน้า 34, 36–37:

| Test suite | ผลลัพธ์ | Block | Source-decision branch |
|---|---|---:|---:|
| `cats\|dogs` | 2 | 10/10 = 100% | 5/6 = 83.33% |
| เพิ่ม `cats\|dog` | 1 สำหรับเทสต์ใหม่ | 10/10 = 100% | 6/6 = 100% |

อาจารย์ปัดเปอร์เซ็นต์ 5/6 เป็น 83% ตัวนับประกอบด้วย loop decision, decision ในลูป และ decision หลังลูป จึงรวม 6 outcomes การรัน input เดิมซ้ำไม่เพิ่มจำนวนรายการที่ครอบคลุม

## ความต่างของ & และ && ที่ต้องรักษา

Lecture 6 หน้า 42 แสดง `if (a > 10 & b > 20)` ซึ่งประเมินทั้งสอง operands ส่วน `&&` ประเมินขวาเฉพาะเมื่อซ้ายเป็น True ห้ามแก้ operator เพื่อให้ได้ coverage ตามต้องการ

ให้ T1=(20,10), T2=(5,30), T3=(20,30)

| Expression / suite | Condition outcomes | Decision outcomes | C/DC |
|---|---:|---:|---:|
| `&`, T1 + T2 | 4/4 = 100% | 1/2 = 50% | 5/6 = 83.33% |
| `&&`, T1 + T2 | 3/4 = 75% | 1/2 = 50% | 4/6 = 66.67% |
| `&` หรือ `&&`, T1 + T2 + T3 | 4/4 = 100% | 2/2 = 100% | 6/6 = 100% |

สำหรับ `&&` ใน T2 เงื่อนไข `b > 20` ไม่ถูกประเมิน จึงบันทึก NE (Not evaluated) ไม่บันทึกว่าเป็น True แม้ค่าที่ส่งเข้ามาจะทำให้ expression นั้นเป็น True หากประเมินแยก

ภาพกราฟหน้า 42 เป็นภาพอธิบายแนวคิดที่ดูคล้าย short-circuit ขณะโค้ดใช้ `&` ดังนั้นสำหรับการสร้าง trace และ instrumentation ต้องอ้างอิง semantics ของโค้ดจริง ไม่สร้างเส้นทางรันจากภาพอย่างเดียว

ได้สร้างโปรแกรมตรวจตัวอย่างขนาดเล็ก `work/course-reading/CoverageExampleCheck.java` และรันด้วย Java 17 ที่มีอยู่บนเครื่อง ผลตัวนับข้างต้นผ่าน checks ทั้งหมด โปรแกรมนี้เป็นการตรวจความเข้าใจตัวอย่าง ไม่ใช่ระบบ coverage ทั่วไป และไม่ใช่ผลทดลอง Defects4J ซึ่งจะต้องใช้ runtime ที่กำหนดแยกต่างหาก

## Path และ MC/DC

Lecture 6 หน้า 43–49 อธิบาย path และ coverage table; หน้า 50–55 อธิบาย combinations และ independence pairs

- ต้องแยก path ของ CFG ทั้งเมธอดออกจาก truth-table combinations ของ decision เดียว การมี n conditions ไม่ได้ทำให้ทั้งโปรแกรมมีแค่ 2^n execution paths เสมอไป
- ลูปอาจสร้างจำนวนเส้นทางไม่จำกัด ต้องประกาศ bound หรือใช้เกณฑ์อื่นที่ระบุชัด ไม่เรียก bounded-path coverage ว่า full path coverage
- เงื่อนไขบางชุดไม่สามารถเกิดร่วมกันได้ เช่น `last == 's'` และ `last == 'r'` ไม่อาจเป็น True พร้อมกันใน execution เดียว ต้องบันทึก infeasibility ไม่สร้าง input สมมติว่าทำได้
- MC/DC ต้องมี evidence ของคู่เทสต์ที่แสดงผลอย่างเป็นอิสระของแต่ละ condition ไม่ใช่ได้ True/False ครบแล้วถือว่าผ่าน
- จำนวน N+1 ในตัวอย่างไม่ใช่การรับประกันสำหรับทุก expression; ต้องพิจารณา dependencies และ variant ของ MC/DC
- แผนหลักจะวัด line/statement/block/decision/condition/C/DC ส่วน MC/DC และ path ต้องระบุขอบเขตที่รองรับก่อนอ้างว่าทำครบ

## ผลตรวจงานเก่า

ลิงก์ที่ผู้ใช้ให้: https://github.com/TeamburapA/GROUP14_PROJECT_SQA

ตรวจ README, `Report/report-source.md`, `Report/data/summary.json`, headers ของ `Report/data/final_comparison.csv` และ measurement scripts บางส่วนแบบ read-only ไม่มีการรันโค้ดจาก repository และไม่ได้ audit ทุกผลดิบ

Git tree ที่อ่าน: `4e42385f1bd648e3a52d51f566520e46e2cac4ff` (tree SHA ไม่ใช่การยืนยันว่าเป็น commit SHA)

สิ่งที่เห็นจากหลักฐาน:

- รายงานเก่ามี line coverage และ Cobertura branch/condition counters อยู่จริง จึงไม่ถูกต้องที่จะสรุปว่างานเก่าทั้งหมดมีเพียงจำนวนรอบ
- `Experiment/reproduction/runtime/scripts/study/evaluate.py` บรรทัด 129–146 อ่าน `LinesTotal`, `LinesCovered`, `ConditionsTotal`, `ConditionsCovered` และ map Conditions ไปเป็น `branch_total`/`branch_covered`
- CSV สรุปมี `line_covered`, `line_total`, `branch_covered`, `branch_total` แต่ไม่มีตัวนับแยกของ source-decision outcomes, atomic-condition outcomes, block และ C/DC ครบตามสไลด์
- รายงานเรียกผลบางส่วนว่า condition coverage แต่ยังต้องตรวจว่า Cobertura counter ตรงกับ atomic-condition coverage ของวิชาหรือไม่ ชื่อคอลัมน์ไม่ใช่หลักฐาน semantic equivalence
- รายงานระบุ 130 bugs / 17 projects และ 396 recorded jobs เป็นสถานะการดำเนินงาน ไม่ใช่ structural coverage
- AI และ algorithms ใช้บริบท/oracle ต่างกัน และจำนวนผลที่วัดได้ต่างกัน จึงไม่ควรตัดสินผู้ชนะจากค่าเฉลี่ยแยกกลุ่มเพียงอย่างเดียว
- การผ่าน fixed สองครั้งเป็น repeatability check ไม่ใช่ generation สองรอบอิสระ

สิ่งที่ยังสรุปไม่ได้: สาเหตุที่อาจารย์หักคะแนน และงานเก่าฉบับที่อาจารย์ตรวจเป็น snapshot เดียวกับ repository นี้หรือไม่

## การใช้เครื่องมือและรูปแบบผลลัพธ์ของงานใหม่

1. กำหนด source-level coverage inventory ก่อนสร้างเทสต์ และบันทึก hash/version
2. เก็บ source decision กับ atomic condition แยกกัน มี occurrence IDs; expressions เหมือนกันคนละตำแหน่งไม่รวมเป็นตัวเดียว
3. เก็บ runtime evidence ที่รักษาลำดับประเมิน short-circuit, side effects, exceptions และจำนวนครั้งเรียกเมธอดเดิม
4. เครื่องมือที่ไม่รองรับตัววัดใดต้องรายงาน unavailable ไม่เปลี่ยนชื่อตัววัดอื่นมาแทน
5. เปรียบเทียบผลบน source revision และขอบเขตเดียวกัน ไม่รวม denominator ของ buggy กับ fixed เข้าด้วยกัน
6. แยก generated, compiled, executed, passed, failed, skipped, infrastructure error และ unavailable measurement
7. เพิ่ม explicit C/DC column พร้อม C_covered/C_total และ D_covered/D_total
8. คำนวณ coverage ของ suite จาก union ของ item IDs ภายใน run; การรวมเทสต์ข้าม independent runs เป็นอีกการทดลองหนึ่ง ต้องติดป้ายแยก
9. หากคำนวณทั้ง macro average และ pooled item coverage ให้แสดงวิธีถ่วงน้ำหนักและจำนวนเป้าหมายที่มีผลวัด
10. ใช้ assertions ที่มี oracle อธิบายได้ ไม่แก้ production code เพื่อให้เทสต์ผ่าน ไม่ mock เมธอดเป้าหมายจนไม่ execute โค้ดที่ต้องวัด
11. เลือก JUnit/JDK ให้เข้ากับ Defects4J project จริง เอกสารแลบมีทั้ง JUnit 5 และ 6 จึงไม่ควรนำเลขเวอร์ชันแลบมาครอบทุกโปรเจกต์โดยอัตโนมัติ
12. ก่อนเริ่ม benchmark ตรวจระบบวัดกับตัวอย่างสไลด์และ Java edge cases ไม่เริ่มรันครบชุดเพื่อหวังว่าเปอร์เซ็นต์จากเครื่องมือจะถูกต้องเอง

โครงสร้างข้อมูลขั้นต่ำ:

`project, bug_id, revision, source_hash, method, model_or_algorithm_version, seed_or_repeat, budget, scope_id, metric_definition_version, generated_suite_hash, items_total, items_covered, coverage_percent, trace_path, status`

ตารางรายเทสต์เพิ่ม:

`test_id, input, expected, oracle_source, actual, result, node_path, edge_path, decision_outcomes, condition_outcomes, assertion_evidence`

## สิ่งที่ยังขาดและงานถัดไป

มีเอกสารพอสำหรับปรับนิยามและสร้างต้นแบบระบบวัดแล้ว ไม่จำเป็นต้องรอไฟล์เพิ่มเพื่อทำงานต่อ แต่ยังไม่มีเฉลย/ไฟล์ Excel test-design template ของ Lab 7 และข้อความ feedback อาจารย์โดยตรง หากผู้ใช้เพิ่มภายหลังให้ใช้ตรวจความสอดคล้องอีกครั้ง

ขั้นถัดไปที่เหมาะสมคือทำ measurement specification และ golden examples ให้ผ่านก่อนปรับแผนทดลองหลัก ตัวเลือก DynaMOSA + MIO และ Gemini Plus + Claude Free ยังเป็นแผนที่เสนอ ไม่ใช่ระบบที่ติดตั้งหรือทดลองครบแล้ว

## แหล่งอ้างอิงประกอบ

- แหล่งหลักในเครื่อง: `inputs/05-other-materials/2026_Lecture6_Whitebox.pdf`, `Lab7_Strcutural.pdf`, `2026_Lecture11_AdvIntelligentTesting (3).pdf` และเอกสารตามดัชนีข้างต้น
- งานเก่า: https://github.com/TeamburapA/GROUP14_PROJECT_SQA/blob/main/Report/report-source.md
- Measurement parser งานเก่า: https://github.com/TeamburapA/GROUP14_PROJECT_SQA/blob/main/Experiment/reproduction/runtime/scripts/study/evaluate.py
- Java evaluation semantics: https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.22.2 และ https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.23
- ขอบเขตตัวนับ JaCoCo: https://www.jacoco.org/jacoco/trunk/doc/counters.html
