@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3.12+ and try again.
  pause
  exit /b 1
)

python -m pip install --upgrade pip pyinstaller
if errorlevel 1 (
  echo Failed to install PyInstaller.
  pause
  exit /b 1
)

pyinstaller --onefile --noconsole --name USALB-Radio-24-Broadcaster usalb_broadcaster.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo.
echo Build complete:
echo %~dp0dist\USALB-Radio-24-Broadcaster.exe
pause
