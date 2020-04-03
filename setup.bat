@echo off

set curDir=%~dp0
set target='%curDir%Ruk-Streaming.pyc'
set shortcut='%userprofile%\desktop\Ruk-Streaming.lnk'
set pws=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%pws% -Command "$ws = New-Object -ComObject WScript.Shell; $S = $ws.CreateShortcut(%shortcut%); $S.TargetPath = %target%; $S.WorkingDirectory = '%curDir%'; $S.IconLocation = '%curDir%Ruk_Streaming_icon.ico'; $S.Save()"

echo.
echo Create "Ruk-Streaming" shortcut to Desktop: Success
echo.

assoc .pyc=Python.NoConFile

pause

