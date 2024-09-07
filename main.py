import mysql.connector
from datetime import datetime

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()

current_user = None



def start_program():
    global current_user
    try:
        user = int(input("Using as patient/doctor?\n1. Patient\n2. Doctor:\n"))
        if user == 1:
            #logging in as patient
            current_user = 'P'
        elif user == 2:
            #logging in as doctor
            current_user = 'D'
        else:
            print("Something went wrong. Try again...\n")
            start_program()
    except ValueError:
        print("Input was of incorrect datatype. Try again...\n")
        start_program()
    else:
        login(current_user)
def login(currentUserType):
    if currentUserType == 'P':
        #print('current patient!')
    elif currentUserType == 'D':
        #print('current doctor!')



start_program()