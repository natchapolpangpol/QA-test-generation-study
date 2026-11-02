# CFG จาก source จริงของ Cli-1

กราฟระดับ source decisions ภายในแต่ละเมธอด แสดง normal control flow; ไม่ใช่ exception/path coverage และไม่ขยาย call edges ไปยังเมธอดอื่น Synthetic exit ไม่นับเป็น block

Source SHA-256: `4000f382a138b952dbfc784318dbff32d21219c6b04ca5f22ee37396da944d35`

## CommandLine#getOptionObject(String)

```mermaid
flowchart TD
  N0["EXIT / exit"]
  N1["block1 / ternary-decision / L99"]
  N2["block2 / ternary-arm / L99"]
  N3["block3 / ternary-arm / L99"]
  N4["block4 / process / L97"]
  N5["block5 / decision / L92"]
  N6["block6 / process / L94"]
  N7["block7 / process / L89,91"]
  N1 -->|T| N2
  N1 -->|F| N3
  N2 -->|return| N0
  N3 -->|return| N0
  N4 -->|next| N1
  N6 -->|next| N0
  N5 -->|T| N6
  N5 -->|F| N4
  N7 -->|next| N5
```

| Node | Source lines | Counted |
|---|---|---|
| EXIT |  | False |
| block1 | 99 | True |
| block2 | 99 | True |
| block3 | 99 | True |
| block4 | 97 | True |
| block5 | 92 | True |
| block6 | 94 | True |
| block7 | 89,91 | True |

## CommandLine#resolveOption(String)

```mermaid
flowchart TD
  N0["EXIT / exit"]
  N1["block1 / process / L179"]
  N2["block2 / decision / L166"]
  N3["block3 / decision / L173"]
  N4["block4 / process / L175"]
  N5["block5 / decision / L169"]
  N6["block6 / process / L171"]
  N7["block7 / process / L168"]
  N8["block8 / for-init / L166"]
  N9["block9 / process / L165"]
  N1 -->|next| N0
  N4 -->|next| N0
  N3 -->|T| N4
  N3 -->|F| N2
  N6 -->|next| N0
  N5 -->|T| N6
  N5 -->|F| N3
  N7 -->|next| N5
  N2 -->|T| N7
  N2 -->|F| N1
  N8 -->|next| N2
  N9 -->|next| N8
```

| Node | Source lines | Counted |
|---|---|---|
| EXIT |  | False |
| block1 | 179 | True |
| block2 | 166 | True |
| block3 | 173 | True |
| block4 | 175 | True |
| block5 | 169 | True |
| block6 | 171 | True |
| block7 | 168 | True |
| block8 | 166 | True |
| block9 | 165 | True |

## CommandLine#getOptionValue(String,String)

```mermaid
flowchart TD
  N0["EXIT / exit"]
  N1["block1 / ternary-decision / L207"]
  N2["block2 / ternary-arm / L207"]
  N3["block3 / ternary-arm / L207"]
  N4["block4 / process / L205"]
  N1 -->|T| N2
  N1 -->|F| N3
  N2 -->|return| N0
  N3 -->|return| N0
  N4 -->|next| N1
```

| Node | Source lines | Counted |
|---|---|---|
| EXIT |  | False |
| block1 | 207 | True |
| block2 | 207 | True |
| block3 | 207 | True |
| block4 | 205 | True |

