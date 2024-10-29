import subprocess
import mysql.connector
import pickle
from pathlib import Path #sql_file destination
import sys
import os
import time
import zampy

def vanilla_sql_login():
    userinp = input('Enter SQL username: ')
    userpassword = input("Enter SQL password: ")
    colorify('Store SQL credentials?')
    storeInFile = int(input(zampy.make_menu_from_options()))

    if storeInFile == 1:
        file = open(sql_creds, 'wb')
        data = [userinp, userpassword]
        pickle.dump(data, file)
        file.close()
    return userinp, userpassword

directory = Path.home() / "HospitalManagement-PythonSQL"
sql_creds = directory / 'sqlcreds.dat'


try:
    file = open(sql_creds, 'rb')
except FileNotFoundError:
    print('Error: SQL creds file not found.')
    userinp, userpassword = vanilla_sql_login()
else:
    data = pickle.load(file)
    userinp, userpassword = data[0], data[1]

database = mysql.connector.connect(host="localhost", user = userinp, password=userpassword)
c = database.cursor()

def execute_sql_file(userinp, userpassword):

    try:
        database.database='hospital_main'
    except:
        c.execute("CREATE DATABASE hospital_main")

        mysql_executable = r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
        command = [mysql_executable, "-u", userinp, "-p" + userpassword, 'hospital_main']

        with open(r'hospital_main.sql', 'r') as sql_file:
            subprocess.run(command, stdin=sql_file)

        database.database='hospital_main'

flag_file = '.first_run'

# Check if the flag file exists
if not os.path.exists(flag_file):
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    with open(flag_file, 'w') as f:
        f.write("This file marks the first run completion.")

execute_sql_file(userinp,userpassword)