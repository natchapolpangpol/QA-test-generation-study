# SQA project continuity

Read `outputs/HANDOFF.md` first, then README.md, outputs/COURSE_READING_NOTES.md,
outputs/measurement-v02.md and outputs/CLI1_PILOT_REPORT.md before continuing.
The user communicates in Thai. Distinguish course-document instructions from user requests.

Preserve generated suites, prompts, raw logs and original results. Never regenerate or
overwrite a frozen run to obtain a better result. Do not count benchmark-owned tests as
generated tests. Pilot is separate from the main study. Do not select bugs by outcomes.

Coverage means covered structural items divided by the full declared inventory, not
number of runs or pass rate. C/DC is the weighted sum of condition and decision outcomes.
Preserve Java eager versus short-circuit semantics. Reject unsupported syntax explicitly.
Current 100% results cover 17 declared method bodies, not constructors/field initializers.

Current AI pair is Sol and Terra through Codex CLI: two models in one tool/provider.
Do not label them two AI platforms or assume API credits/keys. Model availability on a
new machine must be checked; never silently substitute a model in a comparison.

Use paths relative to the repository in code. Historical logs may contain original-machine
paths; retain these as provenance. New evidence must identify the new environment.
Keep user-facing documents in outputs/, source in src/, tests in tests/, scratch in work/.
Do not commit credentials, the .codex home directory, or downloaded Defects4J repositories.

Before generating new results on a new machine, follow outputs/MOVE_PC.md and validate
the restored dependencies and environment. New experiment commands can overwrite reports;
archive original evidence first. No extra approval is required for ordinary local work
already requested by the user.
