@echo off
cd /d "%~dp0"

set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo [*] Virtual environment not found. Creating one...
    py -3 -m venv "%~dp0.venv"
    if errorlevel 1 (
        echo [!] Failed to create virtual environment. Please install Python 3 first.
        pause
        exit /b 1
    )
)

if not exist "%VENV_PYTHON%" (
    echo [!] Python environment is missing after setup.
    pause
    exit /b 1
)

echo [*] Installing project requirements...
"%VENV_PYTHON%" -m pip install --upgrade pip
"%VENV_PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo [!] Failed to install dependencies.
    pause
    exit /b 1
)

echo [*] Starting Neural Master X...
"%VENV_PYTHON%" "%~dp0mouse.py"

if errorlevel 1 (
    echo [!] mouse.py exited with an error.
    pause
    exit /b 1
)
