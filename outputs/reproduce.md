# การรันต้นแบบที่เริ่มทำแล้ว

รุ่นปัจจุบัน: measurement 0.2 และ exploratory Cli-1 pilot ดู [รายงานล่าสุด](CLI1_PILOT_REPORT.md)

Workspace Windows: `C:\Users\NATCHAPOL\Documents\Codex\2026-11-02\86`

รันคำสั่ง Linux ด้านล่างจาก workspace เดียวกันใน Ubuntu/WSL ที่มี Java 11, javac และ Python 3 การเรียกจาก PowerShell ใช้ `wsl -d Ubuntu -- bash -lc 'คำสั่ง'`

## ระบบวัดและ golden cases

```bash
python3 tests/run_golden.py
```

ตรวจ SHA-256 ของ JavaParser ก่อนใช้ แล้ว compile engine และรัน original/instrumented comparisons ผลรวมเขียน `outputs/golden-validation.json`; รายละเอียดอยู่ `work/golden/<case>/` พร้อม source, inventory, trace, summary และ CFG `.dot`

## สร้างเทสต์ด้วย EvoSuite

```bash
mkdir -p work/smoke-target
javac --release 11 -d work/smoke-target tests/golden/AiTarget.java
python3 src/generators/evosuite_runner.py --algorithm DYNAMOSA --target AiTarget --project-cp work/smoke-target --output work/runs/dynamosa-new --budget 10 --seed 101
python3 src/generators/evosuite_runner.py --algorithm MIO --target AiTarget --project-cp work/smoke-target --output work/runs/mio-new --budget 10 --seed 101
```

ใช้ output directory ใหม่ทุกครั้ง adapter ปฏิเสธการเขียนทับผลเดิม ตัวอย่างนี้ใช้ no-runtime-dependency กับโค้ดสอนที่ควบคุมได้ ยังไม่ใช่ policy ที่ freeze สำหรับ arbitrary Defects4J classes

## สร้างเทสต์ด้วย Codex ที่ล็อกอินแล้ว

รันใน PowerShell ผ่าน Python ที่ใช้งานได้บนเครื่องนี้:

```powershell
& 'C:/Users/NATCHAPOL/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' src/generators/codex_runner.py --model gpt-6.1-sol --prompt tests/golden/ai-smoke-prompt.txt --output work/runs/codex-sol-new
```

เปลี่ยน model เป็น `gpt-6.1-terra` เพื่อทดสอบอีกโมเดล ใช้สิทธิ์ Codex ผ่าน ChatGPT ที่ CLI ล็อกอินอยู่ ไม่ใส่ API key ในไฟล์โครงการ ทั้งสองเป็นโมเดลในเครื่องมือเดียวกัน ไม่ใช่ AI คนละผู้ให้บริการ

Adapter ใช้ prompt เดียว, isolated working directory, fresh ephemeral invocation, read-only sandbox, disabled web search และ ignore user config; เก็บ JSONL events และปฏิเสธผลที่มี tool-use event ก่อนรับเป็นเทสต์ การตรวจ event หลังรันเป็น protocol validation ไม่ใช่การรับประกันว่าทุกรุ่น CLI ปิด tools ทางเทคนิคทั้งหมดได้ การตั้งค่า system context ของ Codex ยังเป็นส่วนหนึ่งของ workflow

อย่ารันคำสั่ง generate ซ้ำเพียงเพื่อให้ได้คำตอบที่ชอบ เก็บ failed attempts และ metadata ทั้งหมด การรันซ้ำใช้โควตาสมาชิก

## ตรวจ generated tests ที่มีอยู่แล้ว

```bash
python3 tests/validate_smoke.py
```

ตรวจ test suites ที่สร้างไว้ 4 ชุดใน `work/runs/`: compile, ผ่าน original 3 fresh JVM runs, coverage replay และ fail ด้วย assertion บน synthetic mutation `&&` → `||` อีก 3 runs โดยไม่แก้เทสต์หลังเห็น mutant

ผล: `outputs/generator-smoke-results.json` เป็น teaching-fixture infrastructure test ไม่ใช่ Defects4J fault detection result ไม่รวมเป็น main dataset

## Dependencies

- JavaParser 3.26.3 จาก Maven Central
- JUnit 4.13.2 และ Hamcrest Core 1.3 จาก Maven Central
- EvoSuite 1.2.0 และ standalone runtime จาก GitHub release ทางการ
- Defects4J clone ใน `work/environments/defects4j`; init/checkout status ต้องตรวจจากบันทึกสถานะล่าสุด

Defects4J init ดาวน์โหลด EvoSuite 1.1.0 ของ framework เองด้วย แต่ adapters ของโครงการนี้เรียก `work/dependencies/evosuite-1.2.0.jar` แบบ explicit อย่ารวมผลคนละเวอร์ชันหรือใช้คำสั่ง wrapper ของ Defects4J แล้วสมมติว่าเป็น 1.2.0

ขั้นแตก project repository archive ใช้ `src/environment/extract_repos_windows.py` หลังหยุด unzip เดิม เพราะ WSL-to-Windows extraction ช้า ตรวจ CRC ของไฟล์เดิมและ path confinement ก่อนเขียนไฟล์ แล้วจัดวางด้วย PowerShell ภายใน workspace ไม่แก้ source ของ Defects4J ขั้นติดตั้งที่ดำเนินต่อมี log ใน `work/environments/defects4j-init-resume.log`

ไฟล์ Gradle dependencies ดาวน์โหลดต่อด้วย native curl แบบ resume แล้วใช้ `src/environment/finish_setup_windows.py` ทำขั้นแตก Gradle archives และติดตั้ง analyzer ตาม init.sh จนครบ การยืนยันการติดตั้งใช้ baseline จริง ไม่ใช้เพียงข้อความจบจาก installer

## ตรวจ baseline ของ Defects4J

เมื่อติดตั้งเสร็จ:

```bash
python3 src/environment/pilot_baseline.py --project Cli --bug 1
```

ใช้ tests เดิมของ benchmark เพื่อตรวจ environment เท่านั้น ผลอยู่ `outputs/defects4j-baseline.json` และ logs ใน `work/baseline/Cli-1` ไม่รวม tests เหล่านี้ใน generated-test coverage

## Overload / ternary / declared-method scope รุ่น 0.2

```bash
python3 tests/run_flow.py
python3 tests/run_golden.py
python3 src/evaluation/class_replay.py
```

Flow checks ทดสอบ original/instrumented semantics, manual counts, CFG edges, method-scope inventory และ fail-closed rejections ส่วน class replay ใช้ original checkout ที่ไม่แก้ไขและ instrumented class overlay เพื่อเทียบ benchmark-owned tests 94 เทสต์

## ตรวจ pilot suites ที่ตรึงแล้ว

```bash
python3 src/evaluation/evaluate_cli_pilot.py
python3 src/evaluation/report_cli_pilot.py
python3 src/environment/build_progress_report.py
```

คำสั่งนี้รัน generated suites ที่มีอยู่ ไม่เรียก AI ใหม่ ไม่แก้เทสต์ และไม่ใช้ benchmark tests ใน generated-test coverage รายงาน cause review เป็นการตรวจ source/log โดยผู้ช่วยหลังตรึง generation แล้ว ไม่ใช่ independent human review

การสร้าง pilot ชุดใหม่จะใช้ `prepare_cli_pilot.py` และ adapters โดยต้องใช้ run ID ใหม่และเก็บ metadata แยก อย่ารัน generation ใหม่แล้วเขียนทับ run IDs เดิมเพื่อเลือกผลที่ชอบ

Raw prompts/logs ใน `work` ไม่ควรเผยแพร่ credentials; adapter ไม่อ่านหรือบันทึก authentication tokens ของ Codex
