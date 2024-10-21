@echo off
setlocal

:: Ask for SQL user, password, and host
set /p db_user="Enter SQL username: "
set /p db_password="Enter SQL password: "
set /p db_host="Enter SQL host (localhost in most cases): "

:: Set database and SQL file paths
set db_name=hospital_main
set sql_file=hospital_main.sql

:: Check if SQL file exists
if not exist %sql_file% (
    echo SQL file "%sql_file%" not found!
    pause
    exit /b
)

:: Execute MySQL command to create the database and import the SQL file
echo Importing database...
mysql -h %db_host% -u %db_user% -p%db_password% -e "CREATE DATABASE IF NOT EXISTS %db_name%;"
mysql -h %db_host% -u %db_user% -p%db_password% %db_name% < %sql_file%

:: Check if the command succeeded
if %ERRORLEVEL% equ 0 (
    echo Database successfully installed!
) else (
    echo There was an error installing the database.
    pause
    exit /b
)

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

:: Run the main Python script
echo Running the main Python script...
python main.py

:: Check if the Python script executed successfully
if %ERRORLEVEL% equ 0 (
    echo Program executed successfully!
) else (
    echo There was an error running the program.
)

pause
exit /b
