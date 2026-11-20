# Windows: theme Windows Terminal + lệnh `ide` + skill cho Claude Code / Codex / agy
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw "cần uv: winget install astral-sh.uv" }

$frag = "$env:LOCALAPPDATA\Microsoft\Windows Terminal\Fragments\agent-ide"
New-Item -ItemType Directory -Force $frag | Out-Null
Copy-Item themes\windows-terminal\claude-ide.json $frag -Force

$bin = "$env:USERPROFILE\.local\bin"
New-Item -ItemType Directory -Force $bin | Out-Null
Copy-Item bin\ide, bin\ide.cmd $bin -Force
if (($env:PATH -split ";") -notcontains $bin) {
  [Environment]::SetEnvironmentVariable("PATH", "$bin;" + [Environment]::GetEnvironmentVariable("PATH", "User"), "User")
}

# đặt Claude IDE làm profile mặc định của Windows Terminal
$wt = Get-ChildItem "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal*\LocalState\settings.json" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($wt) {
  Copy-Item $wt.FullName "$($wt.FullName).bak-agent-ide" -Force
  (Get-Content $wt.FullName -Raw) -replace '"defaultProfile":\s*"[^"]*"', '"defaultProfile": "{c1a0de1d-0000-4000-8000-000000000001}"' |
    Set-Content $wt.FullName -Encoding utf8
}

if (Get-Command npx -ErrorAction SilentlyContinue) {
  npx --yes skills add "$PSScriptRoot" --skill ide --agent claude-code codex antigravity-cli -g -y
}
"xong: mở tab Windows Terminal mới rồi gõ  ide claude"
