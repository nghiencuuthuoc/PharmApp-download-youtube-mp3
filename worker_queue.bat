@echo off
:: Worker that pulls ONE URL at a time from url_yt_queue.txt using url_queue_pop.py
:: and downloads it via 2_down_mp3_url_yt_v2.py
:: Place this .bat in the same folder as url_queue_pop.py and 2_down_mp3_url_yt_v2.py

REM set "OUT_DIR=.\out"
set "OUT_DIR=E:\PhatHoc\DAO-TRANG-PHAP-HOA\_TAT-CA-VIDEO"
set "CODEC=mp3"
set "QUALITY=192"
:: Optional extra args for your downloader (leave blank if not needed)
:: set "EXTRA=--tor" 
set "EXTRA="

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

:loop
for /f "usebackq delims=" %%U in (`python url_queue_pop.py`) do (
  echo [%%DATE%% %%TIME%%] Processing: %%U
  python 2_down_mp3_url_yt_v2.py "%%U" -o "%OUT_DIR%" --codec "%CODEC%" --quality "%QUALITY%" %EXTRA%
  echo [%%DATE%% %%TIME%%] Done: %%U
  goto loop
)
echo [INFO] Queue empty. Worker exiting.
exit /b 0

pause