# PowerShell wrapper for process-staging.py
param (
    [switch]$DryRun
)

$scriptPath = Join-Path $PSScriptRoot "process-staging.py"
if ($DryRun) {
    python $scriptPath --dry-run
} else {
    python $scriptPath
}
