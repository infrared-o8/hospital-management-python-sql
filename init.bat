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

echo Running main.py
python main.py
pause
exit /b