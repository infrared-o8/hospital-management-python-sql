import subprocess
import mysql.connector
import pickle
from pathlib import Path #sql_file destination
import sys
import os
import zampy

def vanilla_sql_login():
    userinp = input('Enter SQL username: ')
    userpassword = input("Enter SQL password: ")
    print('Store SQL credentials?')
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

def execute_sql_file(filename,cursor):

    cursor.execute("CREATE DATABASE hospital_main")
    database.database='hospital_main'
    cursor.execute("USE hospital_main")    # Switch to the new database

    with open(filename, 'r') as sql_file:
        sql_commands = sql_file.read()
        # Split commands by the semicolon
        sql_commands_list = sql_commands.split(';')
        
        for command in sql_commands_list:
            # Strip and check if the command is not empty
            if command.strip():
                try:
                    cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    return False
            
    return True

flag_file = '.first_run'

# Check if the flag file exists
if not os.path.exists(flag_file):
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    with open(flag_file, 'w') as f:
        f.write("This file marks the first run completion.")

try:
    database.database='hospital_main'
except:
    temp=execute_sql_file('hospital_main.sql',c)
    if temp:
        print("Successfuly installed database.")
    else:
        print("Database installation unsuccessful.")
        
if 'c' in locals():
    c.close()
if 'database' in locals():
    database.close()
