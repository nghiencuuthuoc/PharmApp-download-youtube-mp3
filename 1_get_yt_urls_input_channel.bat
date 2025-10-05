
@echo off
Title yld-pl-1st
set /p url=Please url channel:
set /p path=Please enter the folder path:
"C:\Users\NCT\AppData\Local\Programs\Python\Python312\python.exe" 1_get_yt_urls_input_channel.py -u %url% -i "%path%"
REM python 1_get_yt_urls_input_channel.py -u %url% -i %path%

pause
cls
1_get_yt_urls_input_channel.bat

