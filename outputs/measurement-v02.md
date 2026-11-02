# ระบบวัดรุ่น 0.2: overload, return ternary และขอบเขต declared methods

เอกสารนี้ปรับปรุงสถานะจาก measurement-spec.md รุ่น 0.1 โดยใช้หลักการนับเดิม เวอร์ชัน 0.2 ยังเป็นต้นแบบสำหรับขอบเขตที่ตรวจแล้ว ไม่ใช่เครื่องมือวัด Java ทุก syntax

## สิ่งที่เพิ่มและตรวจแล้ว

- เลือกเมธอดด้วย `method(Type,...)` หรือ `Owner#method(Type,...)` ชื่อชนิดเป็นรูปสะกดใน source ไม่ใช่ผล resolve ชื่อเต็มจาก compiler; ชื่อสั้นที่กำกวมยังถูกปฏิเสธ
- เลือก `class:CommandLine` เพื่อรวม bodies ของ declared methods ทุกเมธอดในคลาสเดียวกัน โดย validate ทุกเมธอดก่อนสร้างผล หากเมธอดใดไม่รองรับให้ล้มทั้ง scope ไม่ตัดเมธอดนั้นออกจากตัวหาร
- มีรายการ excluded_members แสดง fields, constructors, initializer blocks และ nested types ที่อยู่นอก declared-method scope ชัดเจน ไม่เรียกผลนี้ว่า coverage ของทุก executable construct ในคลาส
- รองรับ ternary ที่เป็น expression ของ return โดยตรงและไม่มี ternary ซ้อน เช่น `return condition ? a : b;` รวมถึง parentheses รอบ expression; ternary ใน assignment, argument, predicate หรือแบบซ้อนยังถูกปฏิเสธ

## ทำไมรักษา ?: ไว้ใน source

การเปลี่ยน ternary เป็น if แล้ว return แยกอาจเปลี่ยน type conversion หรือ null unboxing จึงคง operands ของ `?:` ไว้และ instrument เฉพาะ predicate ตัวบันทึกคืนค่า boolean เดิมและบันทึก arm ที่ถูกเลือกก่อนประเมิน arm นั้น การตรวจรวมถึงตัวอย่าง numeric promotion, generic reference, null unboxing, side effects และ exception [Java Language Specification §15.25](https://docs.oracle.com/javase/specs/jls/se11/html/jls-15.html#jls-15.25)

CFG ของ direct return ternary ใช้ predicate block และ true/false arm blocks จากนั้นไปยัง synthetic method exit ซึ่งไม่นับเป็น executable block ไม่มี probe wrapper รอบค่าของ arms ที่อาจทำให้ compiler infer type ต่างออกไป Statement policy นับการเริ่ม return และ predicate evaluation เป็นคนละ item ตามนิยามของ engine

เส้น CFG ที่ไป exit เป็นเส้นการคืนค่าตามปกติ หาก arm โยน exception trace จะไม่รับประกันว่าทำ return สำเร็จ จึงใช้ block-entry coverage และ decision-outcome coverage ตามที่ระบุ ไม่อ้าง exception-edge/path coverage จากกราฟนี้

## ผลตรวจด้วยตัวอย่าง

ชุดเดิม 15 executions ยังผ่าน และชุดใหม่ตรวจ 10 executions พร้อม 6 rejection cases ดู [flow-validation.json](flow-validation.json)

- `a && b ? 7 : 9` เมื่อ a=false: condition 1/4, decision 1/2, block 2/3
- เมื่อทดสอบ a=false, a=true/b=false และทั้งคู่ true: condition 4/4, decision 2/2, block 3/3
- predicate โยน exception ก่อนคืน boolean: decision 0/2 และ condition 0/2 แต่ predicate block ถูกเข้าแล้ว
- class scope เก็บเมธอดที่ไม่ได้เรียกไว้ใน denominator; overloaded methods มี IDs แยกกัน

## การตรวจ source จริงของ Cli-1

ขอบเขตคือ **17 declared method bodies ของ CommandLine fixed revision** ไม่รวม 2 field initializers และ constructor ข้อมูลนี้แสดงอยู่ใน inventory ทุกครั้ง

ตรวจตัวหารจาก source ด้วยมือก่อนรับผล:

| หน่วย | ตัวหาร | เหตุผล |
|---|---:|---|
| Line | 38 | executable source lines ตามนโยบายบรรทัดเดียว |
| Statement | 42 | 38 line items + for initializer ที่อยู่ร่วมบรรทัด comparison 1 + ternary predicates 3 |
| Block | 40 | straight-line groups, predicates, for-init และ ternary arms |
| Decision outcomes | 16 | 8 decisions × T/F |
| Atomic condition outcomes | 16 | 8 atomic occurrences × T/F; decision แต่ละตัวในคลาสนี้มี atom เดียว |
| C/DC items | 32 | 16 condition outcomes + 16 decision outcomes |

ทั้งนี้ line ไม่เท่ากับ statement โดยทั่วไป ความสัมพันธ์ด้านบนเป็นการตรวจเฉพาะ source นี้ตาม counting policy ไม่ใช่สูตรทั่วไป

เทสต์เดิม 94 เทสต์ผ่านทั้ง original และ instrumented โดยใช้ overlay classpath ไม่แก้ checkout ดู [class-replay-validation.json](class-replay-validation.json) ผลนี้ใช้ตรวจระบบวัดเท่านั้น ไม่ใช้แทนผล generated tests

## ข้อจำกัดที่ยังคงอยู่

ยังไม่รองรับ multiline executable items, switch, do/while, enhanced for, break/continue, try/catch/finally, throw statement, synchronized statement, lambda, method reference, anonymous-class expressions และ negated compound conditions

ยังไม่มี explicit NE table ราย invocation, test-boundary trace หรือ MC/DC/path evaluator ไม่แปลงการไม่มี event เป็นค่า True/False และยังไม่อ้างว่า coverage 100% แปลว่าทดสอบพฤติกรรมครบ

ก่อนรวมผลหลาย source inventories ต้อง qualify IDs ด้วย scope/source hash ไม่รวม ID ที่เหมือนกันข้ามไฟล์โดยตรง Main cohort และนโยบาย constructor/initializer ต้องตรึงหลัง pilot
