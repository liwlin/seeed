$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$url = 'http://127.0.0.1:8080/standalone.html'
$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) {
  Start-Process $url
  & py -3 -m http.server 8080 --bind 127.0.0.1
  exit
}
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
  Start-Process $url
  & python -m http.server 8080 --bind 127.0.0.1
  exit
}
Write-Error 'Python 3 not found. Please install Python 3 or run another local HTTP server.'
