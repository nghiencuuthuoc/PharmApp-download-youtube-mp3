
@echo off
Title ytpl
set /p url=Please url playlist:
set /p path=Please enter the folder path:
@REM "C:\Users\NCT\AppData\Local\Programs\Python\Python312\python.exe" 1_get_url_yt_input_pl.py -p %url% -i %path%
"C:\Users\NCT\AppData\Local\Programs\Python\Python312\python.exe" 1_get_url_yt_input_pl_v1.py -p %url% -i %path%
REM python 1_get_url_yt_input_pl.py -u %url% -i %path%

pause
cls
1_get_url_yt_input_pl.bat

