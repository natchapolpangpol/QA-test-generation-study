param(
    [ValidateSet('golden','flow','smoke','baseline','class-replay','pilot-evaluate','pilot-report','report')]
    [string]$Task = 'golden'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    switch ($Task) {
        'golden' { wsl -d Ubuntu -- python3 tests/run_golden.py }
        'flow' { wsl -d Ubuntu -- python3 tests/run_flow.py }
        'class-replay' { wsl -d Ubuntu -- python3 src/evaluation/class_replay.py }
        'pilot-evaluate' { wsl -d Ubuntu -- python3 src/evaluation/evaluate_cli_pilot.py }
        'pilot-report' { wsl -d Ubuntu -- python3 src/evaluation/report_cli_pilot.py }
        'smoke' { wsl -d Ubuntu -- python3 tests/validate_smoke.py }
        'baseline' { wsl -d Ubuntu -- python3 src/environment/pilot_baseline.py --project Cli --bug 1 }
        'report' { wsl -d Ubuntu -- python3 src/environment/build_progress_report.py }
    }
    if ($LASTEXITCODE -ne 0) { throw "Task $Task failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
