@echo off
cls

:: ==============================================================================
:: Editable Values, Verbose Settings are caps sensitive
set "PYTHON_CMD=py -m whisper --model base.en --task transcribe --language en"
set EXT=mp4
set VERBOSE_WHISPER=True
set VERBOSE_SCRIPT=True
:: ==============================================================================

echo Powered By...
echo   ____                                 _____  _       __          __ _      _                         
echo  / __ \                         /\    ^|_   _^|( )      \ \        / /^| ^|    (_)                        
echo ^| ^|  ^| ^| _ __    ___  _ __     /  \     ^| ^|  ^|/  ___   \ \  /\  / / ^| ^|__   _  ___  _ __    ___  _ __ 
echo ^| ^|  ^| ^|^| '_ \  / _ \^| '_ \   / /\ \    ^| ^|     / __^|   \ \/  \/ /  ^| '_ \ ^| ^|/ __^|^| '_ \  / _ \^| '__^|
echo ^| ^|__^| ^|^| ^|_) ^|^|  __/^| ^| ^| ^| / ____ \  _^| ^|_    \__ \    \  /\  /   ^| ^| ^| ^|^| ^|\__ \^| ^|_) ^|^|  __/^| ^|   
echo  \____/ ^| .__/  \___^|^|_^| ^|_^|/_/    \_\^|_____^|   ^|___/     \/  \/    ^|_^| ^|_^|^|_^|^|___/^| .__/  \___^|^|_^|   
echo         ^| ^|                                                                        ^| ^|                
echo         ^|_^|                                                                        ^|_^|  
echo.
echo Script by Seall.DEV 
FOR /F %%i IN ('cd') DO set ADDRESS=%%~nxi
set CWD=%~dp0
title Subtitling %EXT%'s in %ADDRESS%
echo.
echo.
if %VERBOSE_SCRIPT%==True (
echo PYTHON_CMD set to "%PYTHON_CMD%"
echo VERBOSE_WHISPER set to "%VERBOSE_WHISPER%"
)
echo Searching for files with extension %EXT%...             
set /a FILECOUNT = 0
set /a COUNT = 1
echo Counting files...
for %%f in (*.%EXT%) do set /a FILECOUNT += 1
echo Found %FILECOUNT% files with extension %EXT%!
IF %FILECOUNT%==0 (
pause
exit
)
echo Subtitling %FILimage.pngECOUNT% files...
for %%f in (*.%EXT%) do (
IF EXIST "%%f.srt" (
title Skipping %%f ^(%COUNT%/%FILECOUNT%^) ^- Subtitling %EXT%'s in %ADDRESS% ^(%CWD:~0,-1%^) ^- OpenAI's Whisper ^& Seall^.DEV
echo Subtitles already made for "%%f"...
set /a COUNT += 1
) ELSE (
title Working on %%f ^(%COUNT%/%FILECOUNT%^) ^- Subtitling %EXT%'s in %ADDRESS% ^(%CWD:~0,-1%^) ^- OpenAI's Whisper ^& Seall^.DEV
%PYTHON_CMD% --verbose %VERBOSE_WHISPER% "%%f"
echo Subtitles for "%%f" completed!
set /a COUNT += 1
)
)