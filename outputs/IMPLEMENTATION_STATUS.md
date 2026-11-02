# สถานะการเริ่มพัฒนาโครงการ SQA

**อัปเดตล่าสุด: ทำ exploratory pilot บน Cli-1 จริงแล้ว ดู [รายงาน Cli-1](CLI1_PILOT_REPORT.md)**

ระบบวัด 0.2 รองรับ overload, direct return ternary และรวม 17 declared method bodies ของ CommandLine แล้ว ตรวจ original/instrumented ผ่าน 94 เทสต์ ขอบเขตยังไม่รวม constructor/field initializers; ตาราง smoke ด้านล่างเป็นหลักฐานระยะแรก ไม่ใช่ผลนำร่องล่าสุด

เริ่มลงมือแล้ว: มีโค้ดที่รันได้และหลักฐานทดสอบ ไม่ใช่เพียงแผน

## สิ่งที่ผ่านจริง

- Golden executions 15 กรณี: original/instrumented ให้ผลตรงกันและตัวนับตรง expected counts
- ปฏิเสธ syntax ที่ยังไม่รองรับ 2 กรณี พร้อมตรวจ repeat-union, unknown trace, denominator 0, weighted C/DC, empty trace และ missing trace
- DynaMOSA และ MIO เลือก algorithm ได้จริงตาม log ของ EvoSuite 1.2.0
- Codex CLI ผ่านสิทธิ์ ChatGPT สร้างเทสต์อัตโนมัติได้ด้วย Sol และ Terra; ไม่พบ tool-use events ในสอง smoke runs
- เทสต์ทั้ง 4 ชุด compile และผ่าน original ใน 3 fresh JVM runs; ตรวจพบ synthetic mutation ด้วย assertion ใน 3 runs

## ผล smoke test บน AiTarget.classify

| Generator | Decision | Condition | C/DC | Original passes | Synthetic mutation failures |
|---|---:|---:|---:|---:|---:|
| codex-sol-smoke-001 | 2/2 | 4/4 | 6/6 | 3/3 | 3/3 |
| codex-terra-smoke-001 | 2/2 | 4/4 | 6/6 | 3/3 | 3/3 |
| dynamosa-smoke-002 | 2/2 | 4/4 | 6/6 | 3/3 | 3/3 |
| mio-smoke-002 | 2/2 | 4/4 | 6/6 | 3/3 | 3/3 |

ผลนี้เป็นตัวอย่างเล็กสำหรับตรวจ pipeline เท่านั้น ไม่ใช่หลักฐานจัดอันดับ AI/algorithms และไม่ใช่ผล Defects4J

EvoSuite BRANCH goals ของคลาสตัวอย่างนับ 5 รายการ แต่ source decision ของเมธอดเป้าหมายนับ 2 outcomes จึงเก็บ native fitness metrics แยกจาก course coverage

## คู่ AI ที่ใช้เริ่มงาน

ใช้ Codex ผ่านสิทธิ์ Plus ที่มีอยู่จริง ไม่เพิ่ม API bill ใน smoke tests นี้ Sol และ Terra เป็นสองโมเดลของเครื่องมือและผู้ให้บริการเดียวกัน จึงต้องเรียกการเปรียบเทียบตามนั้น หากจะรักษาโจทย์สองแพลตฟอร์ม ต้องมีช่องทางที่สองและแก้ protocol ก่อน freeze งานหลัก

## สิ่งที่ยังต้องทำ

- เพิ่ม test/invocation boundaries, explicit NE, CFG audit และ stability checks บนโครงการจริง
- ตรึง main cohort, AI protocol และ budgets หลัง pilot ไม่รวม smoke tests เป็นผลหลัก

## ไฟล์อ้างอิง

- [Measurement specification](measurement-spec.md)
- [วิธีรันซ้ำ](reproduce.md)
- [Golden results](golden-validation.json)
- [Generator smoke results](generator-smoke-results.json)
- [Environment and artifact hashes](environment-manifest.json)
- [CFG ตัวอย่าง](cfg/countWords.md)

## Defects4J baseline ที่รันแล้ว

Cli-1 fixed: failing tests 0; buggy: failing tests 1 บน Java 11 / America/Los_Angeles ใช้ tests เดิมของ benchmark เพื่อยืนยัน environment ไม่ใช่เทสต์จาก AI หรือ algorithms

- [รายละเอียด baseline](defects4j-baseline.json)
- [Syntax readiness audit ของ CommandLine](pilot-syntax-audit.tsv)

- [Counting policy รุ่น 0.2](measurement-v02.md)
- [Flow validation](flow-validation.json)
- [ผล pilot](cli1-pilot-results.json)
