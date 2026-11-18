# Weekly Job Radar run for Windows. Used by Task Scheduler (see README). Test it once by hand first:
#   powershell -ExecutionPolicy Bypass -File run-weekly.ps1
Set-Location -Path $PSScriptRoot
New-Item -ItemType Directory -Force -Path logs | Out-Null
$log = "logs\run-$(Get-Date -Format yyyy-MM-dd).log"

claude -p "/job-radar" --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Agent,Bash(python *),Bash(py *)" *> $log
$ok = ($LASTEXITCODE -eq 0)

$msg = if ($ok) { "Job Radar finished. Open tracker.html." } else { "Job Radar failed. See $log" }
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show($msg, "Job Radar") | Out-Null
