"""Publish pilot findings and an explicitly reviewed causal link, preserving raw results."""
import hashlib
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def main():
    data=json.loads((ROOT/"outputs/cli1-pilot-results.json").read_text())
    review={"review_type":"assistant source-and-log review after frozen generation; not independent human review",
        "project":"Cli","bug_id":1,"benchmark_trigger_used_only_after_generation_for_cause_review":True,
        "fixed_behavior":"hasOption(String) resolves short/long names and strips leading hyphens before membership lookup",
        "buggy_behavior":"hasOption(String) performs options.containsKey(opt), using the supplied string directly",
        "benchmark_behavior":"BugCLI13Test checks hasOption(longName) after adding an option with different short and long names",
        "sources":[],"runs":[]}
    for relative in ["work/checkouts/Cli-1f/src/java/org/apache/commons/cli/CommandLine.java",
                     "work/checkouts/Cli-1b/src/java/org/apache/commons/cli/CommandLine.java",
                     "work/checkouts/Cli-1f/src/test/org/apache/commons/cli/bug/BugCLI13Test.java"]:
        review["sources"].append({"path":relative,"sha256":hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()})
    checks={"cli1-sol-001":("presentOptionsWithoutValuesReturnNullAndUseDefaults","assertTrue(line.hasOption(\"--verbose\"));","short v / long verbose"),
            "cli1-terra-001":("presentOptionWithoutValueUsesDefaults","assertTrue(line.hasOption(\"flag\"));","short f / long flag")}
    for r in data["runs"]:
        if r["run"] not in checks: continue
        name,assertion,setup=checks[r["run"]]
        source=ROOT/"work/runs"/r["run"]/"GeneratedTest.java"
        if assertion not in source.read_text(): raise RuntimeError("Reviewed assertion changed")
        frozen_hash=r["suite_files"][0]["sha256"]
        if hashlib.sha256(source.read_bytes()).hexdigest()!=frozen_hash: raise RuntimeError("Suite hash changed")
        if not all(any(x.startswith(name+"(") for x in b["failures"]) for b in r["buggy_runs"]):
            raise RuntimeError("Reviewed failure not reproduced")
        if not all(f["status"]=="passed" for f in r["fixed_runs"]): raise RuntimeError("Invalid fixed oracle")
        review["runs"].append({"run":r["run"],"confirmed_bug_detection":True,"test_method":name,
            "assertion":assertion,"setup":setup,"suite_sha256":frozen_hash,
            "cause":"Distinct long-name lookup is true on fixed and false on buggy, matching the CLI-13 alias-resolution regression",
            "not_all_additional_failures_individually_reviewed":True})
    (ROOT/"outputs/cli1-cause-review.json").write_text(json.dumps(review,indent=2))
    confirmed={r["run"] for r in review["runs"]}
    labels={"cli1-dynamosa-001":"DynaMOSA","cli1-mio-001":"MIO","cli1-sol-001":"Codex / Sol","cli1-terra-001":"Codex / Terra"}
    report=["# ผลนำร่อง Cli-1 และความคืบหน้าระบบวัด 0.2", "",
        "ทดลองกับ bug จริงตัวแรกแล้ว ใช้ fixed reference สร้างเทสต์ จากนั้นตรึงเทสต์ไปตรวจ buggy ไม่มีการส่ง buggy failures หรือ benchmark tests ให้ generator และไม่มีการแก้เทสต์ด้วยมือ", "",
        "**ผลนี้เป็น pilot 1 bug / 1 generation ต่อวิธี ใช้ประเมินระบบและหาข้อจำกัด ไม่เพียงพอจัดอันดับวิธีสร้างเทสต์**", "",
        "## ขอบเขตการวัด", "",
        "วัด 17 declared method bodies ของ org.apache.commons.cli.CommandLine บน fixed revision เท่านั้น ไม่รวม 2 field initializers และ constructor จึงไม่เรียกว่า coverage ของ executable code ทั้งคลาสหรือทั้งโครงการ",
        "", "ตัวหารที่ตรวจจาก source: line 38, statement 42, block 40, decision outcomes 16, condition outcomes 16 และ C/DC items 32 ทุกวิธีใช้ inventory/source hash เดียวกัน", "",
        "## ผล generated tests", "", "| วิธี | จำนวนเทสต์ | Line | Statement | Block | Decision | Condition | C/DC | ตรวจพบ Cli-1 |", "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in data["runs"]:
        label=labels[r["run"]]
        if r["status"]!="evaluated":
            report.append(f"| {label} | — | — | — | — | — | — | — | {r['status']} |")
            continue
        m=r["coverage"]["metrics"]
        counts=[f"{m[k]['covered']}/{m[k]['total']}" for k in ["line","statement","block","decision","condition","condition_decision"]]
        found="พบ — ตรวจสาเหตุแล้ว" if r["run"] in confirmed else "ไม่พบในรอบนี้"
        report.append(f"| {label} | {r['fixed_runs'][0]['test_count']} | "+" | ".join(counts)+f" | {found} |")
    report += ["", "ทั้งสี่ชุดผ่าน fixed 3 fresh JVM runs และผ่าน instrumented replay โดยไม่แก้เทสต์ เทสต์จาก Sol และ Terra ล้มบน buggy ด้วย failure ชุดเดิมทั้ง 3 runs; การรันซ้ำเหล่านี้เป็น stability checks ไม่ใช่ independent generations", "",
        "## เหตุผลที่ยืนยันการตรวจพบ", "",
        "เลือกตรวจ assertion เรื่อง hasOption(longName) จากทั้งสองโมเดล: เมื่อสร้าง option ที่ชื่อสั้นต่างจากชื่อยาว fixed จะ resolve alias ก่อนตรวจ membership แต่ buggy ใช้ key ที่รับมาโดยตรง จึงคืน false สำหรับชื่อยาวบางแบบ ตรงกับพฤติกรรมที่ benchmark trigger ของ CLI-13 ตรวจอยู่แล้ว", "",
        "Sol ตรวจชื่อ --verbose (short v) และ Terra ตรวจชื่อ flag (short f) ทั้งคู่ผ่าน fixed และ fail ด้วย assertion บน buggy ไม่ใช่ compile error หรือ timeout ส่วน failures อื่นที่เกิดใน suite เดียวกันไม่ได้ถูกนับเป็น bugs เพิ่ม", "",
        "## สิ่งที่ผลนี้บอกได้", "",
        "ในกรณีนี้ทุกวิธีครอบคลุมโครงสร้างตาม inventory ครบ แต่สองชุดจาก search algorithms ยังตรวจไม่พบ regression จึงเห็นโดยตรงว่า structural coverage 100% ไม่ได้แปลว่าเลือกค่าข้อมูลและ assertions ที่ตรวจ bug นี้ได้ครบ", "",
        "ยังบอกไม่ได้ว่า AI ดีกว่า search algorithms โดยทั่วไป: มีเพียงหนึ่ง bug/หนึ่ง seed, oracle-generation workflows ต่างกัน และ compute budget ของ search ไม่เท่ากับ model response budget", "",
        "## งบและ provenance", "",
        "DynaMOSA/MIO ใช้ EvoSuite 1.2.0, seed 101, search budget สูงสุด 60 วินาที และ config ร่วมกัน DynaMOSA หยุดก่อนหมดงบเมื่อ native goals ครบ ส่วน MIO ใช้งบตามรอบค้นหา; ต้องดู elapsed/search time จาก logs ไม่ตีความจำนวน runs เป็น coverage",
        "",
        "Sol/Terra ใช้ Codex CLI ผ่านสิทธิ์สมาชิก รุ่นละหนึ่ง invocation, reasoning effort low, prompt/context SHA-256 เดียวกัน, ไม่พบ tool-use events, ไม่ใช้ repair responses ทั้งสองเป็นคนละโมเดลในผู้ให้บริการเดียวกัน ไม่ใช่สองแพลตฟอร์ม",
        "",
        "## หลักฐานและงานถัดไป", "",
        "- [ผลดิบทั้งสี่วิธี](cli1-pilot-results.json)",
        "- [หลักฐานตรวจสาเหตุ](cli1-cause-review.json)",
        "- [ระบบวัดรุ่น 0.2 และข้อจำกัด](measurement-v02.md)",
        "- [การตรวจ original/instrumented ด้วยเทสต์เดิม 94 เทสต์](class-replay-validation.json)",
        "- [ตัวอย่างทดสอบ overload/ternary](flow-validation.json)",
        "- [ตัวอย่าง CFG ของ 3 เมธอดจาก source จริง](cfg/CommandLine_methods.md)",
        "", "ขั้นถัดไป: เพิ่ม per-test/invocation trace และ NE, กำหนด constructor/initializer scope ให้จบ และขยาย pilot ไปอีก 2 bugs ก่อน freeze main study ห้ามนำผล pilot นี้ไปนับรวม main study หรือเปลี่ยนการเลือก cohort ตามผู้ชนะ"]
    (ROOT/"outputs/CLI1_PILOT_REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    inventory=json.loads((ROOT/"work/class-replay/Cli-1f-v02/inventory.json").read_text())
    graph=["# CFG จาก source จริงของ Cli-1", "", "กราฟระดับ source decisions ภายในแต่ละเมธอด แสดง normal control flow; ไม่ใช่ exception/path coverage และไม่ขยาย call edges ไปยังเมธอดอื่น Synthetic exit ไม่นับเป็น block", "",
           "Source SHA-256: `"+inventory["source_sha256"]+"`", ""]
    selected={"CommandLine#resolveOption(String)","CommandLine#getOptionObject(String)","CommandLine#getOptionValue(String,String)"}
    for method in inventory["methods"]:
        if method["method"] not in selected: continue
        prefix=method["method"]+"@"+str(method["line"])+":"
        nodes=[n for n in inventory["cfg_nodes"] if n["id"].startswith(prefix)]
        aliases={n["id"]:f"N{i}" for i,n in enumerate(nodes)}
        graph += ["## "+method["method"],"", "```mermaid", "flowchart TD"]
        for node in nodes:
            label=node["id"].split(":")[-1]+" / "+node["type"]
            if node.get("lines"): label+=" / L"+",".join(map(str,node["lines"]))
            graph.append(f'  {aliases[node["id"]]}["{html.escape(label,quote=True)}"]')
        for edge in inventory["cfg_edges"]:
            if edge["from"] in aliases:
                graph.append(f'  {aliases[edge["from"]]} -->|{edge["label"]}| {aliases[edge["to"]]}')
        graph += ["```","", "| Node | Source lines | Counted |", "|---|---|---|"]
        graph += [f"| {n['id'].split(':')[-1]} | {','.join(map(str,n.get('lines',[])))} | {n['counted']} |" for n in nodes]
        graph.append("")
    (ROOT/"outputs/cfg/CommandLine_methods.md").write_text("\n".join(graph)+"\n",encoding="utf-8")
    print("Saved CLI1_PILOT_REPORT.md and source-checked cause review")

if __name__=="__main__": main()
