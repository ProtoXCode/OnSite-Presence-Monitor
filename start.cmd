@echo off

echo ==================================
echo  Starting OnSite Presence Monitor
echo ==================================
echo.

if not exist logs/setup.log (
    echo [-] Setup has not been completed...
    echo [!] Run setup.cmd first!
    exit /b 1
)

echo [!] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [-] Failed activating virtual environment
    exit /b 1
)

echo [+] Virtual environment activated...

echo [!] Launching OnSite Presence Monitor (Production Mode)
python.exe runproduction.py
