# ย้ายโครงการไป PC ใหม่

ใช้ Git repo + supplemental ZIP คู่กัน บัญชีเดียวช่วยให้เข้าใช้บริการเดิมได้ แต่ไม่ถือว่าไฟล์และ environment จาก PC เดิมถูกย้ายแล้ว การ sync แชตแยกจากการเข้าถึงไฟล์: [เอกสาร OpenAI](https://learn.chatgpt.com/docs/projects)

## เครื่องเดิม

1. สร้าง repo แบบ Private ว่าง ๆ (ไม่เพิ่ม README/license/gitignore ที่เว็บ) แล้วเชื่อม remote กับโฟลเดอร์งานนี้
2. `.gitignore` เตรียมให้แล้ว: เก็บ src, tests, outputs, README, AGENTS, frozen runs/prompts และหลักฐานการวัด แต่ไม่เอา inputs, dependency JARs, Defects4J/download caches หรือ credentials ขึ้น Git
3. ตรวจ `git status --short` แล้ว commit/push เอกสารและโค้ด หลังเพิ่ม URL ของ repo จริง คำสั่งด้านล่างเป็นตัวอย่าง ยังไม่ได้ push ให้

```powershell
git add .
git diff --cached --stat
git commit -m "Preserve SQA measurement v0.2 and Cli-1 pilot"
git remote add origin <REPO_URL>
git push -u origin main
```

ถ้า Git ขอชื่อ/email ให้กำหนดตัวตนของคุณสำหรับ repo นี้ก่อน commit; ไม่จำเป็นต้องตั้ง global

4. เก็บ `outputs/migration/sqa-transfer-supplement.zip` แยกผ่าน USB/ที่เก็บไฟล์ส่วนตัว ZIP นี้ไม่อยู่ใน Git มี inputs ต้นฉบับ, dependency JARs และเอกสารอ่านประกอบ พร้อมรายการ SHA-256 ใน `outputs/migration-files.json` อย่าแนบ ZIP นี้กับ public repository
5. เก็บเครื่องเดิม/โฟลเดอร์เดิมไว้จนเครื่องใหม่ verify และรัน golden ผ่าน

## เครื่องใหม่

ติดตั้ง Git, Codex desktop และล็อกอินบัญชีเดิม สำหรับเส้นทางที่ใกล้กับเครื่องเดิมใช้ Windows + WSL Ubuntu, Java 11, Python 3 ติดตั้ง Codex CLI และล็อกอินใหม่เมื่อต้องสร้างเทสต์ AI; ไม่ต้องย้าย `.codex/auth.json` หรือ credentials จากเครื่องเดิม

```powershell
git clone <REPO_URL> sqa-project
cd sqa-project
Expand-Archive -LiteralPath 'D:\Transfer\sqa-transfer-supplement.zip' -DestinationPath .
```

เปลี่ยน path ของ ZIP ตามที่เก็บจริง สร้างโฟลเดอร์ใหม่สำหรับ clone; ZIP เสริมไม่ใช่สำเนา repo และไม่มี src/tests รายการ `TRANSFER_CONTENTS.json` ที่แตกออกมาเป็น manifest สำหรับตรวจไฟล์เท่านั้น

จาก root ของ repo ใช้ Python 3 ตรวจ hashes ก่อนทำงานต่อ:

```bash
python3 src/environment/migration_bundle.py --verify
```

บน Windows ที่ใช้ Python launcher สามารถใช้ `py -3` แทน `python3` ได้ ส่วนคำสั่งทดสอบ Java ให้รันใน WSL จาก root เดียวกัน

## เตรียม Defects4J ใหม่

ZIP ไม่รวม WSL, Java installation, Defects4J repository/cache หรือ benchmark checkouts จึงต้องติดตั้งใหม่ก่อน replay bug จริง ใช้ Java 11 และ dependencies ตาม README ของ Defects4J commit ที่ตรึงไว้ (Git, SVN, Perl, cpanm และ Perl modules ใน cpanfile) ไม่ใช้ installation helpers ของเครื่องเดิมโดยไม่อ่านก่อน เพราะ helpers บางตัวออกแบบสำหรับกู้ download ที่ค้าง

ตัวอย่างคำสั่งใน Ubuntu หลังติดตั้ง prerequisites แล้ว:

```bash
mkdir -p work/environments
git clone https://github.com/rjust/defects4j.git work/environments/defects4j
git -C work/environments/defects4j checkout 8c16da8230843cdc918eaf4ddb449637f02b83c6
cd work/environments/defects4j
cpanm --installdeps .
./init.sh
cd ../../..
java -version
javac -version
```

ต้องให้ทั้ง java และ javac เป็นรุ่น 11 และตรวจ installation exit codes ก่อนเดินต่อ การดาวน์โหลด benchmark อาจใช้เวลานาน ไม่ได้ทดสอบขั้นตอนติดตั้งทั้งหมดบน PC ใหม่แล้ว

## ตรวจ environment โดยรักษาหลักฐานเดิม

ก่อน replay ให้สำรอง outputs และ work/runs เพราะ scripts เขียน validation results ลงตำแหน่งเดิม โดยใช้ Python จาก root ของ repo (ปลายทางต้องยังไม่มี):

```bash
python3 -c "import shutil; shutil.copytree('outputs','work/pre-replay-evidence/outputs',ignore=shutil.ignore_patterns('migration')); shutil.copytree('work/runs','work/pre-replay-evidence/runs')"
python3 tests/run_golden.py
python3 tests/run_flow.py
python3 src/environment/pilot_baseline.py --project Cli --bug 1
python3 src/evaluation/class_replay.py
python3 src/evaluation/evaluate_cli_pilot.py
python3 src/evaluation/report_cli_pilot.py
```

รันทีละคำสั่งและตรวจผลก่อนคำสั่งถัดไป baseline จะ checkout Cli-1f/Cli-1b ใหม่และสร้าง paths ของเครื่องใหม่ ไม่ใช้ cp.test ในบันทึกเก่าโดยตรง เก็บ logs เก่าที่มี absolute paths ไว้เป็น provenance ห้าม replace path ทั้ง repo

การตรวจนี้ใช้เทสต์เดิม ไม่สร้าง AI responses ใหม่ หากผลต่างจากเครื่องเดิม ให้ตรวจ environment ก่อน อย่าแก้ suite เพื่อให้ผ่าน ห้ามแทนรุ่น AI แบบเงียบ ๆ ถ้าเครื่องใหม่ไม่มีโมเดลเดิม

## เปิด Codex ทำต่อ

เปิดโฟลเดอร์ repo ที่ clone เป็น local project ใน Codex แล้วส่งข้อความนี้ในแชตเดิมหรือแชตใหม่:

> นี่คือโครงการ SQA ที่ย้ายเครื่องมา อ่าน AGENTS.md และ outputs/HANDOFF.md รวมถึงเอกสารที่อ้างถึงก่อน ตรวจไฟล์จาก migration ZIP และ environment แล้วทำต่อจากงานค้าง รักษาผล pilot เดิม ห้ามสร้างเทสต์เดิมซ้ำหรือสรุปผู้ชนะจาก bug เดียว

AGENTS.md และ HANDOFF ทำให้เริ่มต่อได้แม้แชตเก่าไม่ปรากฏบนเครื่องใหม่ งานต่อไปคือ trace ต่อ test/invocation + NE, scope constructor/initializer และ pilot อีก 2 bugs
