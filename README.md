# SQA test generation and coverage study

Moving PCs: read `outputs/MOVE_PC.md` and `outputs/HANDOFF.md`. Git preserves code and frozen experimental evidence; teaching inputs and dependency JARs travel separately in the supplemental ZIP. `AGENTS.md` provides continuity for a new Codex chat.

This workspace contains the user's personal study comparing automatic test generation algorithms and AI-assisted tests on Defects4J.

The user authorized starting autonomously with available tools. Working smoke-test generators: EvoSuite 1.2.0 DynaMOSA and MIO, plus Codex CLI using gpt-6.1-sol and gpt-6.1-terra through the existing ChatGPT subscription. The latter are TWO MODELS IN ONE TOOL/PROVIDER, not two AI platforms. No external API credentials have been verified. ChatGPT Free + Claude Free in plan V2 is an older proposal, not a frozen pair.

## Project knowledge

Latest user clarification: the user has ChatGPT Plus and is exploring free API access/automation. Plus does not itself include OpenAI API billing credits. Codex CLI with ChatGPT sign-in is a subscription-backed automation candidate; Gemini API free tier and Groq Free are candidates subject to account eligibility and model quotas. The ChatGPT Free + Claude Free chat protocol in plan V2 remains a proposal under review, not a locked experimental pair. Do not assume any API key or account quota has been verified.

The revised implementation and experiment plan is `outputs/SQA_PROJECT_PLAN_V2.md`. It proposes a separate 3-bug pilot and 15-bug main study, source-level measurement validation before benchmarking, and fixed-reference regression evaluation. This is a plan, not a completed implementation. Freeze target classes, protocols and budgets after the pilot and before main results.

Read `outputs/COURSE_READING_NOTES.md` for the reviewed course definitions, source pages, corrected coverage methodology, verified teaching examples, limitations of the old project, and pending decisions. This replaces earlier informal assumptions about the course's C/DC calculation.

Structural coverage is not run count or pass rate. Course C/DC uses `(covered condition outcomes + covered decision outcomes) / (total condition outcomes + total decision outcomes)`. Source-level decisions and atomic conditions must remain distinct, and Java `&` must not be confused with `&&`.

## Files

- `inputs`: original teaching materials, project specification and old-work link; preserve originals.
- `src`: measurement prototype, generator adapters and environment fingerprint.
- `tests`: golden Java fixtures and generator smoke validation.
- `work`: extracted text, inspected page images, read-only copies of selected old-project sources, and scratch verification.
- `outputs`: user-facing deliverables.

Read `outputs/IMPLEMENTATION_STATUS.md`, `outputs/measurement-spec.md` and `outputs/reproduce.md` before continuing implementation. Golden checks and generated JUnit suites have been run on teaching fixtures. Results are in `outputs/golden-validation.json` and `outputs/generator-smoke-results.json`; these are NOT Defects4J generator results. The AST prototype fails closed on unsupported syntax and is not ready to claim class-wide benchmark coverage.

Defects4J setup and Cli-1 baseline now PASS: fixed has 0 failing tests; buggy has the expected BugCLI13Test failure. See `outputs/defects4j-baseline.json`. Initial WSL download/extraction needed a native Windows resume; setup logs are in `work/environments/defects4j-init*.log` and helper scripts in `src/environment`. Do not rerun destructive init steps unnecessarily.

Latest completed milestone: measurement 0.2 supports exact syntactic signatures for overloads, direct/non-nested return ternaries without changing arm types, and a class selector that measures DECLARED METHOD BODIES ONLY. All 17 CommandLine method bodies are included; constructors and field initializers are explicitly excluded. See `outputs/measurement-v02.md`. Original and instrumented Cli-1 pass the same 94 benchmark-owned tests. Golden 15 cases plus flow 10 executions/6 rejections pass.

One exploratory Cli-1 pilot is complete (`outputs/CLI1_PILOT_REPORT.md` and `cli1-pilot-results.json`): DynaMOSA/MIO each seed 101, max search 60s; Codex Sol/Terra each one fresh response using identical fixed-only context, no tool use or repairs. All four suites reach 100% of the DEFINED 17-method scope and pass fixed 3 times. DynaMOSA/MIO do not detect this bug in this run; Sol/Terra have reproducible buggy failures, and primary long-name alias assertions were checked against fixed/buggy source and the benchmark trigger AFTER generation (`cli1-cause-review.json`). This is not a ranking, not main-study data, and not full-class executable coverage. Preserve all generated suites and logs.

Next work: per-test/invocation trace and explicit NE; constructor/initializer scope; broader syntax and two more pilot bugs; then freeze main protocol. Current unsupported forms still fail closed. The v0.1 audit TSV is historical; do not use its ternary/overload limitations as current status. Do not hide unsupported code from denominators or change cohort based on pilot winners.
