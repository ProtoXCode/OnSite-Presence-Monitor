@echo off

echo ====================================
echo  Setting up OnSite Presence Monitor
echo ====================================
echo.

REM --- Check for flags ---
set FORCE_RECREATE=false

if "%~1"=="--force" (
    set FORCE_RECREATE=true
    echo [!] FORCE mode: Virtual environment will be recreated...
)

REM --- Python minimum version ---
set MIN_MAJOR=3
set MIN_MINOR=10

echo [!] Checking for installed Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [-] Python not installed...
    exit /b 1
)

for /f "usebackq tokens=2 delims= " %%a in (`python --version 2^>^&1`) do set PYVER=%%a
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set CUR_MAJOR=%%a
    set CUR_MINOR=%%b
)

if %CUR_MAJOR% LSS %MIN_MAJOR% (
    echo [-] Python is too old: %PYVER%
    exit /b 1
)

if %CUR_MAJOR%==%MIN_MAJOR% if %CUR_MINOR% LSS %MIN_MINOR% (
    echo [-] Python doesn't meet minimum version: %PYVER%
    echo [!] Should be at least: %MIN_MAJOR%.%MIN_MINOR%
    exit /b 1
)

echo [+] Python version OK: %PYVER%
echo.

REM --- Virtual Environment handling ---
if exist .venv (
    if "%FORCE_RECREATE%"=="true" (
        echo [!] Nuking existing virtual environment...
        rmdir /s /q .venv
        if errorlevel 1 (
            echo [-] Could not remove old venv
            exit /b 1
        )
    ) else (
        echo [+] Using existing virtual environment...
        goto ACTIVATE
    )
)

echo [!] Creating fresh virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo [-] Failed creating virtual environment
    exit /b 1
)
echo [+] Virtual environment created!

:ACTIVATE
echo [!] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [-] Failed activating virtual environment
    exit /b 1
)

echo [+] Virtual environment activated!

REM --- Installing dependencies ---
echo [!] Installing dependencies...
if not exist requirements.txt (
    echo [-] Cannot locate requirements.txt
    exit /b 1
)

pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [-] Error installing dependencies...
    exit /b 1
)

echo [+] Dependencies successfully installed!
echo SETUP_OK > logs\setup.log
