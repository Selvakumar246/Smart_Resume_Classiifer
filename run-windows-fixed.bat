@echo off
setlocal
cd /d "%~dp0"

if not exist "frontend\node_modules" (
  echo ERROR: Frontend packages are missing.
  echo Run setup-windows.bat first.
  pause
  exit /b 1
)

echo Starting Smart Resume Classification...

if exist "backend\.venv\Scripts\python.exe" (
  start "Smart Resume API" /D "%~dp0backend" cmd.exe /k "call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
) else (
  start "Smart Resume API" /D "%~dp0backend" cmd.exe /k "python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
)

timeout /t 2 /nobreak >nul

start "Smart Resume Web" /D "%~dp0frontend" cmd.exe /k "call npm.cmd run dev -- --host 127.0.0.1 --port 5173"

echo.
echo Two terminal windows should now be open.
echo Keep both windows open while using the website.
echo Wait until the frontend window displays: Local: http://localhost:5173/
echo.
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173

timeout /t 6 /nobreak >nul
start "" "http://localhost:5173"

pause
endlocal
