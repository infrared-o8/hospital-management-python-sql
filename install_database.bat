@echo off
setlocal

:: Ask for SQL user, password, and host
set /p db_user="Enter SQL username: "
set /p db_password="Enter SQL password: "
set db_host="localhost"

:: Set database and SQL file paths
set db_name=hospital_main
set sql_file=hospital_main.sql
set sql_file_compatible=hospital_main_compatible.sql

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

:: Check if SQL file exists
if not exist %sql_file% (
    echo SQL file "%sql_file%" not found!
    pause
    exit /b
)
if not exist %sql_file_compatible% (
    echo SQL file "%sql_file_compatible%" not found!
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
    echo Trying to install compatible version...
    mysql -h %db_host% -u %db_user% -p%db_password% -e "CREATE DATABASE IF NOT EXISTS %db_name%;"
    mysql -h %db_host% -u %db_user% -p%db_password% %db_name% < %sql_file_compatible%
        if %ERRORLEVEL% equ 0 (
        echo Database successfully installed!
    ) else (
        echo Error in installing compatible version.
        pause
        exit /b
    )
)

pause
exit /b