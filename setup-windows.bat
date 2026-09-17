@echo off
setlocal
cd /d "%~dp0"

echo [1/2] Setting up FastAPI backend...
cd backend
if not exist .env copy .env.example .env >nul
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Error installing backend requirements.
  pause
  exit /b 1
)

echo [2/2] Setting up React frontend...
cd ..\frontend
if not exist .env copy .env.example .env >nul
call npm install
if errorlevel 1 (
  echo Error installing frontend dependencies.
  pause
  exit /b 1
)

echo.
echo Setup complete. Run run-windows-fixed.bat
endlocal
