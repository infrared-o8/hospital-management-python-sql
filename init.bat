@echo off
setlocal

:: Installing Python dependencies from requirements.txt
echo Installing Python dependencies...
pip install -r requirements.txt

:: Check if the dependencies installed successfully
if %ERRORLEVEL% equ 0 (
    echo Dependencies successfully installed!
) else (
    echo There was an error installing dependencies.
    pause
    exit /b
)

echo Running install_database.py...
python install_database.py

if %ERRORLEVEL% equ 0 (
    echo Database successfully installed!
) else (
    echo There was an error installing the database.
    pause
    exit /b
)

pause
exit /b