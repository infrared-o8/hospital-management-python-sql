import mysql.connector
from datetime import datetime
import zampy

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()

current_user = None



def start_program():
    global current_user
    try:
        print("Using as patient/doctor?\n")
        user = int(input(zampy.make_menu_from_options(['Patient', 'Doctor'])))
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
        print("Log in or sign up as patient?")
        useridentify = input(zampy.make_menu_from_options(['Sign up', 'Log in']))
    elif currentUserType == 'D':
        print('current doctor!')



start_program()