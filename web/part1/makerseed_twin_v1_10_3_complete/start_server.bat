@echo off
setlocal
cd /d "%~dp0"
set URL=http://127.0.0.1:8080/standalone.html
where py >nul 2>nul
if %errorlevel%==0 (
  start "" "%URL%"
  py -3 -m http.server 8080 --bind 127.0.0.1
  goto :eof
)
where python >nul 2>nul
if %errorlevel%==0 (
  start "" "%URL%"
  python -m http.server 8080 --bind 127.0.0.1
  goto :eof
)
echo [ERROR] Python 3 not found. Please install Python 3 or run another local HTTP server.
pause
