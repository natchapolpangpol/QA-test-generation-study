# Measurement specification — prototype 0.1

บันทึกประวัติรุ่น 0.1 — สถานะปัจจุบันและส่วนที่รองรับเพิ่มดู [measurement-v02.md](measurement-v02.md)

สถานะ: ใช้ตรวจระบบกับตัวอย่างสอน ยังไม่อนุมัติให้ใช้รายงาน coverage ของคลาส Defects4J ทั้งคลาส

## หน่วยและขอบเขต

หนึ่ง inventory ผูกกับ source SHA-256 และเมธอดชื่อเดียวที่ระบุชัดในไฟล์ต้นฉบับ ปฏิเสธชื่อที่กำกวมจาก overload หรือหลายคลาส ไม่รวม helper methods, constructors, dependencies และ tests ใน scope นี้ ต้องขยายเป็น class inventory ก่อนทดลองหลัก

ใช้ JavaParser 3.26.3 parse AST, source-level CFG และ runtime recorder ที่เพิ่มในสำเนาโค้ดเท่านั้น เก็บ original source แยกไว้ ค่า fitness ของ EvoSuite เป็นอีก metric หนึ่ง ไม่ถูกใช้แทนผลจาก recorder

## กฎการนับที่ implementation ใช้จริง

| Metric | Inventory | Runtime evidence |
|---|---|---|
| Line | unique source lines ของ executable items ที่รองรับ | probe ก่อนเริ่ม statement/predicate/init/update |
| Statement | simple statement, predicate evaluation, for-init expression และ update expression | probe เมื่อเริ่มประเมิน item นั้น |
| Block | maximal straight-line groups, predicate, for-init, for-update | block entry; synthetic exit ไม่นับ |
| Decision | T/F ของ if, while และ for comparison | boolean result เมื่อประเมิน expression รวมสำเร็จ |
| Condition | T/F ของ atomic occurrence ภายใต้ decision | boolean result ของ occurrence ที่ประเมินสำเร็จจริง |
| C/DC | union ที่มีชนิด condition และ decision แยกกัน | `(Ccovered+Dcovered)/(Ctotal+Dtotal)` |

Prototype ปฏิเสธ multiline executable items เพื่อไม่อ้างว่า start-line probe วัดทุกบรรทัดใน multiline expression ได้ถูกต้อง นโยบาย statement ที่ระบุข้างต้นเป็นหน่วยที่ประกาศเพื่อทดสอบ engine ยังต้องตรวจ mapping กับโค้ดจริงก่อน main study

`&&`, `||`, Boolean `&`, `|` และ `^` คง operator และลำดับประเมินเดิม แยก atoms ตามโครงสร้าง AST โดย occurrence คนละตำแหน่งเป็นคนละรายการ Negated atom เช่น `!isLetter(x)` วัดผลของ expression ตามที่เขียน; negated compound ยังปฏิเสธเพื่อรอ policy/implementation เพิ่ม

เงื่อนไขที่ short-circuit ไม่เกิด condition event; ไม่สมมติผลจากค่าของ argument ถ้าเกิด exception ก่อน expression คืน boolean จะไม่มี T/F ของ expression นั้น อย่างไรก็ตาม block/statement ที่เริ่มทำงานแล้วนับ reached ได้ Prototype ยังไม่มีตาราง NE ราย invocation หรือ MC/DC-pair extractor จึงไม่อ้างว่ารองรับ MC/DC แล้ว

ตัวหารเป็นรายการ structural outcomes ที่กำหนดไว้ก่อนรัน ไม่ตัดรายการที่ยังหาเทสต์ไม่พบออก การรันเทสต์ซ้ำไม่เพิ่มจำนวน covered items; suite coverage เป็น set union ภายใน run

ตัวหาร 0 เป็น null/N/A, trace ว่างที่มีไฟล์จริงคือไม่มี events, trace หายหรือมี unknown IDs เป็น error ไม่ใช่ coverage 0

## โครงสร้างที่รองรับในต้นแบบ

- method bodies ที่มี block, expression statement, return, if/else, while และ for ที่มี comparison
- source-decision CFG มี labeled T/F edges และ non-counted synthetic exit
- selected method เดียวต่อการ instrument; ภายใน scope มีเงื่อนไขและ executable leaf items บรรทัดเดียว
- trace เก็บ sequence, thread ID, item kind และ item ID แบบ TSV

ยังไม่รองรับ switch, do/while, break/continue, try/catch/finally, throw statement, synchronized statement, enhanced for, lambda, method reference, ternary, anonymous-class expression, negated compound conditions และ multiline executable items; ปฏิเสธแทนการละออกจากตัวหาร

AST instrumentation ยังไม่ผ่านการรับรองสำหรับ arbitrary Java programs: compile gate และ original-versus-instrumented semantic checks เป็นข้อบังคับ เส้นทางที่มี compile-time constants, name shadowing และ construct combinations ยังต้องเพิ่ม validation ก่อนขยาย scope

## หลักฐานการตรวจ

`tests/run_golden.py` คอมไพล์ Java 11-compatible bytecode แล้วรัน original และ instrumented ใน JVM แยกกัน ตรวจ output/exception-handling behavior และ side-effect counts พร้อม expected counts ที่กำหนดไว้ใน test harness

ตัวอย่างสำคัญ: `cats|dogs` มี block 10/10, decision 5/6; เพิ่ม `cats|dog` เป็น decision 6/6; `&` ตัวอย่างสองเทสต์ให้ C/DC 5/6 ส่วน `&&` ให้ 4/6 และกรณี 3 conditions ตรวจ C/DC แบบถ่วงด้วยจำนวนรายการเป็น 7/8 ไม่เฉลี่ยเปอร์เซ็นต์ condition กับ branch

ไฟล์ผลจริง: [golden-validation.json](golden-validation.json)

## Gate ก่อนใช้กับ Defects4J main study

1. ขยาย scope เป็น target class พร้อม source mapping ครบทุก supported method และแยก constructor/synthetic policy
2. ตรวจ syntax ของ candidate classes และเพิ่ม implementation/tests; ไม่คัด cohort จากผล generator
3. ตรวจ CFG, denominator และ trace ด้วยมือบน pilot จริงทั้ง fixed และ buggy
4. เก็บ test/invocation boundaries, explicit NE และ per-test provenance ก่อนอ้าง MC/DC หรือ path evidence
5. ตรวจ recorder ไม่รบกวน framework classloader, filesystem mocking, threads และ exception behavior
6. Freeze measurement version/hash และ protocol หลัง pilot ผ่านแล้ว
