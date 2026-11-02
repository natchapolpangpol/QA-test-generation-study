# CFG ตัวอย่าง countWords

ขอบเขต: source-level decisions ของเมธอดใน tests/golden/TeachingExamples.java

```mermaid
flowchart TD
  N0["TeachingExamples#countWords(String)@11:EXIT / exit"]
  N1["TeachingExamples#countWords(String)@11:block1 / process / lines 19"]
  N2["TeachingExamples#countWords(String)@11:block2 / decision / lines 18"]
  N3["TeachingExamples#countWords(String)@11:block3 / process / lines 18"]
  N4["TeachingExamples#countWords(String)@11:block4 / decision / lines 14"]
  N5["TeachingExamples#countWords(String)@11:block5 / for-update / lines 14"]
  N6["TeachingExamples#countWords(String)@11:block6 / process / lines 16"]
  N7["TeachingExamples#countWords(String)@11:block7 / decision / lines 15"]
  N8["TeachingExamples#countWords(String)@11:block8 / process / lines 15"]
  N9["TeachingExamples#countWords(String)@11:block9 / for-init / lines 14"]
  N10["TeachingExamples#countWords(String)@11:block10 / process / lines 12,13"]
  N1 -->|next| N0
  N3 -->|next| N1
  N2 -->|T| N3
  N2 -->|F| N1
  N5 -->|next| N4
  N6 -->|next| N5
  N8 -->|next| N6
  N7 -->|T| N8
  N7 -->|F| N6
  N4 -->|T| N7
  N4 -->|F| N2
  N9 -->|next| N4
  N10 -->|next| N9
```

กราฟนี้มี 10 counted blocks และ synthetic exit ที่ไม่นับ ตัวเลข decision coverage มาจาก 3 decisions × 2 outcomes ไม่ใช่จำนวน edges ทั้งกราฟ

สำหรับ input `cats|dogs` ได้ block 10/10 และ decision 5/6; outcome ที่ยังไม่เกิด:

- `TeachingExamples#countWords(String)@11:decision3:F`
