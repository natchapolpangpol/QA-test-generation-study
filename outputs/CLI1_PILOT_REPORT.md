# ผลนำร่อง Cli-1 และความคืบหน้าระบบวัด 0.2

ทดลองกับ bug จริงตัวแรกแล้ว ใช้ fixed reference สร้างเทสต์ จากนั้นตรึงเทสต์ไปตรวจ buggy ไม่มีการส่ง buggy failures หรือ benchmark tests ให้ generator และไม่มีการแก้เทสต์ด้วยมือ

**ผลนี้เป็น pilot 1 bug / 1 generation ต่อวิธี ใช้ประเมินระบบและหาข้อจำกัด ไม่เพียงพอจัดอันดับวิธีสร้างเทสต์**

## ขอบเขตการวัด

วัด 17 declared method bodies ของ org.apache.commons.cli.CommandLine บน fixed revision เท่านั้น ไม่รวม 2 field initializers และ constructor จึงไม่เรียกว่า coverage ของ executable code ทั้งคลาสหรือทั้งโครงการ

ตัวหารที่ตรวจจาก source: line 38, statement 42, block 40, decision outcomes 16, condition outcomes 16 และ C/DC items 32 ทุกวิธีใช้ inventory/source hash เดียวกัน

## ผล generated tests

| วิธี | จำนวนเทสต์ | Line | Statement | Block | Decision | Condition | C/DC | ตรวจพบ Cli-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| DynaMOSA | 15 | 38/38 | 42/42 | 40/40 | 16/16 | 16/16 | 32/32 | ไม่พบในรอบนี้ |
| MIO | 15 | 38/38 | 42/42 | 40/40 | 16/16 | 16/16 | 32/32 | ไม่พบในรอบนี้ |
| Codex / Sol | 7 | 38/38 | 42/42 | 40/40 | 16/16 | 16/16 | 32/32 | พบ — ตรวจสาเหตุแล้ว |
| Codex / Terra | 6 | 38/38 | 42/42 | 40/40 | 16/16 | 16/16 | 32/32 | พบ — ตรวจสาเหตุแล้ว |

ทั้งสี่ชุดผ่าน fixed 3 fresh JVM runs และผ่าน instrumented replay โดยไม่แก้เทสต์ เทสต์จาก Sol และ Terra ล้มบน buggy ด้วย failure ชุดเดิมทั้ง 3 runs; การรันซ้ำเหล่านี้เป็น stability checks ไม่ใช่ independent generations

## เหตุผลที่ยืนยันการตรวจพบ

เลือกตรวจ assertion เรื่อง hasOption(longName) จากทั้งสองโมเดล: เมื่อสร้าง option ที่ชื่อสั้นต่างจากชื่อยาว fixed จะ resolve alias ก่อนตรวจ membership แต่ buggy ใช้ key ที่รับมาโดยตรง จึงคืน false สำหรับชื่อยาวบางแบบ ตรงกับพฤติกรรมที่ benchmark trigger ของ CLI-13 ตรวจอยู่แล้ว

Sol ตรวจชื่อ --verbose (short v) และ Terra ตรวจชื่อ flag (short f) ทั้งคู่ผ่าน fixed และ fail ด้วย assertion บน buggy ไม่ใช่ compile error หรือ timeout ส่วน failures อื่นที่เกิดใน suite เดียวกันไม่ได้ถูกนับเป็น bugs เพิ่ม

## สิ่งที่ผลนี้บอกได้

ในกรณีนี้ทุกวิธีครอบคลุมโครงสร้างตาม inventory ครบ แต่สองชุดจาก search algorithms ยังตรวจไม่พบ regression จึงเห็นโดยตรงว่า structural coverage 100% ไม่ได้แปลว่าเลือกค่าข้อมูลและ assertions ที่ตรวจ bug นี้ได้ครบ

ยังบอกไม่ได้ว่า AI ดีกว่า search algorithms โดยทั่วไป: มีเพียงหนึ่ง bug/หนึ่ง seed, oracle-generation workflows ต่างกัน และ compute budget ของ search ไม่เท่ากับ model response budget

## งบและ provenance

DynaMOSA/MIO ใช้ EvoSuite 1.2.0, seed 101, search budget สูงสุด 60 วินาที และ config ร่วมกัน DynaMOSA หยุดก่อนหมดงบเมื่อ native goals ครบ ส่วน MIO ใช้งบตามรอบค้นหา; ต้องดู elapsed/search time จาก logs ไม่ตีความจำนวน runs เป็น coverage

Sol/Terra ใช้ Codex CLI ผ่านสิทธิ์สมาชิก รุ่นละหนึ่ง invocation, reasoning effort low, prompt/context SHA-256 เดียวกัน, ไม่พบ tool-use events, ไม่ใช้ repair responses ทั้งสองเป็นคนละโมเดลในผู้ให้บริการเดียวกัน ไม่ใช่สองแพลตฟอร์ม

## หลักฐานและงานถัดไป

- [ผลดิบทั้งสี่วิธี](cli1-pilot-results.json)
- [หลักฐานตรวจสาเหตุ](cli1-cause-review.json)
- [ระบบวัดรุ่น 0.2 และข้อจำกัด](measurement-v02.md)
- [การตรวจ original/instrumented ด้วยเทสต์เดิม 94 เทสต์](class-replay-validation.json)
- [ตัวอย่างทดสอบ overload/ternary](flow-validation.json)
- [ตัวอย่าง CFG ของ 3 เมธอดจาก source จริง](cfg/CommandLine_methods.md)

ขั้นถัดไป: เพิ่ม per-test/invocation trace และ NE, กำหนด constructor/initializer scope ให้จบ และขยาย pilot ไปอีก 2 bugs ก่อน freeze main study ห้ามนำผล pilot นี้ไปนับรวม main study หรือเปลี่ยนการเลือก cohort ตามผู้ชนะ
