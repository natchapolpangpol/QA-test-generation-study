# ส่งต่องาน SQA ไปเครื่องใหม่

สถานะ ณ 2026-11-02: ระบบวัด 0.2 และ exploratory pilot Cli-1 เสร็จแล้ว ยังไม่เริ่ม main study

## เป้าหมายและสิ่งที่ตกลง

เปรียบเทียบ DynaMOSA และ MIO ผ่าน EvoSuite 1.2.0 กับ AI สองโมเดล Sol/Terra ผ่าน Codex CLI ที่ล็อกอิน ChatGPT ผู้ใช้ต้องการไม่จ่าย API เพิ่ม คู่ AI นี้ใช้ได้จริงบนเครื่องเดิม แต่เป็นสองโมเดลในเครื่องมือเดียวกัน ไม่ใช่สองแพลตฟอร์ม แผน Gemini/Claude ในเอกสารเก่าไม่ใช่คู่ปัจจุบัน

ผู้ใช้ย้ำให้วัด coverage ตามหลักวิชา เคยวัดผิดด้วยจำนวนรอบ งานนี้วัด white-box structural coverage: line, statement, block, decision, condition และ C/DC พร้อม CFG การส่ง source ให้ generator ไม่ใช่ black-box-only workflow

สูตรรายวิชา: C/DC = (covered condition outcomes + covered decision outcomes) / (total condition outcomes + total decision outcomes) ต้องไม่เฉลี่ยเปอร์เซ็นต์สองตัวตรง ๆ และต้องรักษาความต่างระหว่าง `&` กับ `&&`

## ผลที่มีจริง

- Golden 15 cases และ flow 10 executions ผ่าน; fail-closed checks ผ่าน
- original และ instrumented CommandLine ผ่าน benchmark-owned tests 94 เทสต์
- Cli-1 fixed baseline ผ่าน ส่วน buggy ล้มที่ BugCLI13Test ตามคาด
- Pilot สร้างเทสต์ DynaMOSA 15, MIO 15, Sol 7, Terra 6 เทสต์; แต่ละชุดผ่าน fixed 3 fresh JVM runs
- ทุกชุด coverage 100% เฉพาะ 17 declared method bodies: line 38, statement 42, block 40, decision 16, condition 16, C/DC 32 ไม่รวม constructor และ field initializers
- DynaMOSA/MIO รอบนี้ไม่ตรวจพบ bug; Sol/Terra ตรวจพบ long-name alias regression ทำซ้ำได้ 3 ครั้ง ตรวจ source และ log หลังตรึง generation แล้ว
- หนึ่ง bug/หนึ่ง generation ต่อวิธี ยังจัดอันดับไม่ได้ และไม่ใช่ main-study data

ดู CLI1_PILOT_REPORT.md, cli1-pilot-results.json, cli1-cause-review.json และ measurement-v02.md ในโฟลเดอร์นี้ รายงานผลดิบเก็บแยกจากการ review สาเหตุโดยผู้ช่วย ไม่ใช่ independent human review

## สภาพแวดล้อมเดิม

Windows + WSL Ubuntu, Java 11, Python 3, TZ=America/Los_Angeles
Defects4J commit `8c16da8230843cdc918eaf4ddb449637f02b83c6` ที่ work/environments/defects4j
JavaParser 3.26.3, EvoSuite 1.2.0 + standalone runtime, JUnit 4.13.2, Hamcrest 1.3
Codex CLI 0.162.0; models `gpt-6.1-sol` และ `gpt-6.1-terra`, reasoning low
รายละเอียดและ SHA-256: environment-manifest.json และ metadata ของแต่ละ run

ต้นทางเดิม C:/Users/NATCHAPOL/Documents/Codex/2026-11-02/86 เป็นเพียง provenance ไม่ใช่ path ที่เครื่องใหม่ต้องใช้
Frozen pilot run IDs: cli1-dynamosa-001, cli1-mio-001, cli1-sol-001, cli1-terra-001 ใน work/runs

## ข้อจำกัดและงานต่อไป

1. ย้ายไฟล์/ตรวจ hashes/ตั้ง environment ตาม MOVE_PC.md ก่อนทำการทดลองใหม่
2. เพิ่ม trace ต่อ test/invocation และสถานะ NE (condition ไม่ได้ถูกประเมิน)
3. กำหนด constructor/initializer scope และเพิ่ม syntax support; ห้ามตัด unsupported code ออกจากตัวหารแบบเงียบ ๆ
4. เพิ่ม pilot อีก 2 bugs; freeze cohort, budget, seeds และ protocol ก่อน main study ที่เสนอไว้ 15 bugs

ต้นแบบยังไม่รองรับ Java ทุกรูปแบบ เช่น try/throw, switch, enhanced-for และ ternary ซ้อน รองรับ direct non-nested return ternary และ exact syntactic signatures สำหรับ overloads CFG เป็น normal control flow ไม่ใช่ exception/path coverage หรือ MC/DC

อย่ารัน init Defects4J ซ้ำบน installation ที่พร้อมแล้วโดยไม่จำเป็น อย่ารัน generator เพื่อสร้างผลเดิมซ้ำหรือเปลี่ยนผลที่ไม่ชอบ เก็บ original reports ไว้ก่อน replay เพราะ scripts บางตัวเขียนผลทับที่เดิม

เอกสารรายวิชาเคยอ่าน 25 ไฟล์แล้ว สรุปอยู่ COURSE_READING_NOTES.md; ต้นฉบับอยู่ inputs ใน migration ZIP ไฟล์อ่านประกอบอยู่ work/course-reading
