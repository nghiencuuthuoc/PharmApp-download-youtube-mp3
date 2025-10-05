@echo off
:: Launch N workers in parallel. Adjust N below.
set "N=4"

for /l %%i in (1,1,%N%) do (
  start "YT Worker %%i" cmd /c worker_queue.bat
  ping -n 2 127.0.0.1 >nul
)
echo Launched %N% workers.
