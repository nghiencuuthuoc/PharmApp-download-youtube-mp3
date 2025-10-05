@echo off


echo Select mode:
echo [1] Extract URLs from YouTube PLAYLIST
echo [2] Extract URLs from YouTube CHANNEL
echo.
set /p mode="Enter your choice (1/2): "

if "%mode%"=="1" (
    echo Running: Playlist URL Extractor...
    call 1_get_url_yt_input_pl.bat
    goto :eof
)

if "%mode%"=="2" (
    echo Running: Channel URL Extractor...
    call 1_get_yt_urls_input_channel.bat
    goto :eof
)

echo Invalid option. Please run again.
REM pause
exit /b

pause
cls

1_get_yt_urls_option.bat