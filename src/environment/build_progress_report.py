"""Build user-facing progress from recorded outputs; no invented benchmark results."""
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]

def load(path): return json.loads(path.read_text(encoding="utf-8"))

def main():
    golden=load(ROOT/"outputs/golden-validation.json")
    smoke=load(ROOT/"outputs/generator-smoke-results.json")
    baseline_path=ROOT/"outputs/defects4j-baseline.json"
    baseline=load(baseline_path) if baseline_path.exists() else None
    cfg=load(ROOT/"work/golden/countOne/inventory.json")
    coverage=load(ROOT/"work/golden/countOne/summary.json")
    folder=ROOT/"outputs/cfg"
    folder.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/"work/golden/countOne/cfg.dot",folder/"countWords.dot")
    aliases={n["id"]:f"N{i}" for i,n in enumerate(cfg["cfg_nodes"])}
    graph=["# CFG ตัวอย่าง countWords", "", "ขอบเขต: source-level decisions ของเมธอดใน tests/golden/TeachingExamples.java", "", "```mermaid", "flowchart TD"]
    for n in cfg["cfg_nodes"]:
        name=n["id"]+" / "+n["type"]
        if n.get("lines"): name+=" / lines "+",".join(map(str,n["lines"]))
        graph.append(f'  {aliases[n["id"]]}["{name}"]')
    for e in cfg["cfg_edges"]:
        graph.append(f'  {aliases[e["from"]]} -->|{e["label"]}| {aliases[e["to"]]}')
    graph += ["```", "", "กราฟนี้มี 10 counted blocks และ synthetic exit ที่ไม่นับ ตัวเลข decision coverage มาจาก 3 decisions × 2 outcomes ไม่ใช่จำนวน edges ทั้งกราฟ", "", "สำหรับ input `cats|dogs` ได้ block 10/10 และ decision 5/6; outcome ที่ยังไม่เกิด:", ""]
    graph.extend("- `"+x+"`" for x in coverage["metrics"]["decision"]["uncovered_ids"])
    (folder/"countWords.md").write_text("\n".join(graph)+"\n",encoding="utf-8")
    text=["# สถานะการเริ่มพัฒนาโครงการ SQA", "", "เริ่มลงมือแล้ว: มีโค้ดที่รันได้และหลักฐานทดสอบ ไม่ใช่เพียงแผน", "", "## สิ่งที่ผ่านจริง", "",
          f"- Golden executions {len(golden['cases'])} กรณี: original/instrumented ให้ผลตรงกันและตัวนับตรง expected counts",
          "- ปฏิเสธ syntax ที่ยังไม่รองรับ 2 กรณี พร้อมตรวจ repeat-union, unknown trace, denominator 0, weighted C/DC, empty trace และ missing trace",
          "- DynaMOSA และ MIO เลือก algorithm ได้จริงตาม log ของ EvoSuite 1.2.0",
          "- Codex CLI ผ่านสิทธิ์ ChatGPT สร้างเทสต์อัตโนมัติได้ด้วย Sol และ Terra; ไม่พบ tool-use events ในสอง smoke runs",
          "- เทสต์ทั้ง 4 ชุด compile และผ่าน original ใน 3 fresh JVM runs; ตรวจพบ synthetic mutation ด้วย assertion ใน 3 runs",
          "", "## ผล smoke test บน AiTarget.classify", "", "| Generator | Decision | Condition | C/DC | Original passes | Synthetic mutation failures |", "|---|---:|---:|---:|---:|---:|"]
    for r in smoke["runs"]:
        m=r["coverage"]["metrics"]
        counts=lambda k:f"{m[k]['covered']}/{m[k]['total']}"
        text.append(f"| {r['run']} | {counts('decision')} | {counts('condition')} | {counts('condition_decision')} | {r['original_passes']}/3 | {r['synthetic_mutant_assertion_failures']}/3 |")
    text += ["", "ผลนี้เป็นตัวอย่างเล็กสำหรับตรวจ pipeline เท่านั้น ไม่ใช่หลักฐานจัดอันดับ AI/algorithms และไม่ใช่ผล Defects4J", "",
             "EvoSuite BRANCH goals ของคลาสตัวอย่างนับ 5 รายการ แต่ source decision ของเมธอดเป้าหมายนับ 2 outcomes จึงเก็บ native fitness metrics แยกจาก course coverage", "",
             "## คู่ AI ที่ใช้เริ่มงาน", "", "ใช้ Codex ผ่านสิทธิ์ Plus ที่มีอยู่จริง ไม่เพิ่ม API bill ใน smoke tests นี้ Sol และ Terra เป็นสองโมเดลของเครื่องมือและผู้ให้บริการเดียวกัน จึงต้องเรียกการเปรียบเทียบตามนั้น หากจะรักษาโจทย์สองแพลตฟอร์ม ต้องมีช่องทางที่สองและแก้ protocol ก่อน freeze งานหลัก", "",
             "## สิ่งที่ยังต้องทำ", "", "- ตรวจสถานะ Defects4J initialization และรัน fixed/buggy baseline ของ Cli-1",
             "- ขยาย measurement จาก selected-method prototype เป็น class scope และรองรับ syntax ที่พบใน pilot",
             "- เพิ่ม test/invocation boundaries, explicit NE, CFG audit และ stability checks บนโครงการจริง",
             "- ตรึง main cohort, AI protocol และ budgets หลัง pilot ไม่รวม smoke tests เป็นผลหลัก", "",
             "## ไฟล์อ้างอิง", "", "- [Measurement specification](measurement-spec.md)", "- [วิธีรันซ้ำ](reproduce.md)", "- [Golden results](golden-validation.json)", "- [Generator smoke results](generator-smoke-results.json)", "- [Environment and artifact hashes](environment-manifest.json)", "- [CFG ตัวอย่าง](cfg/countWords.md)"]
    if baseline and baseline["status"]=="passed":
        text.remove("- ตรวจสถานะ Defects4J initialization และรัน fixed/buggy baseline ของ Cli-1")
        f=baseline["revisions"]["f"]["failing_tests"]
        b=baseline["revisions"]["b"]["failing_tests"]
        text += ["", "## Defects4J baseline ที่รันแล้ว", "", f"Cli-1 fixed: failing tests {f}; buggy: failing tests {b} บน Java 11 / America/Los_Angeles ใช้ tests เดิมของ benchmark เพื่อยืนยัน environment ไม่ใช่เทสต์จาก AI หรือ algorithms", "", "- [รายละเอียด baseline](defects4j-baseline.json)", "- [Syntax readiness audit ของ CommandLine](pilot-syntax-audit.tsv)"]
    if (ROOT/"outputs/cli1-pilot-results.json").exists():
        text[2:2]=["**อัปเดตล่าสุด: ทำ exploratory pilot บน Cli-1 จริงแล้ว ดู [รายงาน Cli-1](CLI1_PILOT_REPORT.md)**", "", "ระบบวัด 0.2 รองรับ overload, direct return ternary และรวม 17 declared method bodies ของ CommandLine แล้ว ตรวจ original/instrumented ผ่าน 94 เทสต์ ขอบเขตยังไม่รวม constructor/field initializers; ตาราง smoke ด้านล่างเป็นหลักฐานระยะแรก ไม่ใช่ผลนำร่องล่าสุด", ""]
        text=[line for line in text if line!="- ขยาย measurement จาก selected-method prototype เป็น class scope และรองรับ syntax ที่พบใน pilot"]
        text += ["", "- [Counting policy รุ่น 0.2](measurement-v02.md)", "- [Flow validation](flow-validation.json)", "- [ผล pilot](cli1-pilot-results.json)"]
    (ROOT/"outputs/IMPLEMENTATION_STATUS.md").write_text("\n".join(text)+"\n",encoding="utf-8")
    print("Generated IMPLEMENTATION_STATUS.md and CFG evidence")

if __name__=="__main__": main()
