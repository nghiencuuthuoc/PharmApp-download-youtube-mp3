# PowerShell script to prepare the queue file from url_yt.txt
# 1) Clean empty lines and comments
# 2) De-duplicate
# 3) (Optional) Shuffle for load balancing

Param(
  [string]$InputFile = ".\url_yt.txt",
  [string]$QueueFile = ".\url_yt_queue.txt",
  [switch]$Shuffle
)

if (-not (Test-Path $InputFile)) {
  Write-Error "Input file not found: $InputFile"
  exit 1
}

# Read, clean, dedupe
$lines = Get-Content $InputFile -Encoding UTF8 |
  Where-Object { $_.Trim() -ne "" -and $_ -notmatch '^\s*#' } |
  ForEach-Object { $_.Trim() } |
  Select-Object -Unique

if ($Shuffle) {
  # Simple shuffle
  $rand = New-Object System.Random
  $lines = $lines | Sort-Object { $rand.Next() }
}

$lines | Set-Content $QueueFile -Encoding UTF8
Write-Host "Queue prepared:" (Get-Item $QueueFile).FullName
Write-Host "Total:" $lines.Count
