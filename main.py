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
        signin(current_user)

def signin(currentUserType):
    if currentUserType == 'P':
        #print('current patient!')
        print("Log in or sign up as patient?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            print("Running sign up!")

            #get required info
            patient_id = input("Enter patient ID: ")
            #check if it already exists in patients table.
            c.execute('select * FROM patients')
            patients_data = c.fetchall()
            ''' for patient_data in patients_data:
                if patient_data[0] == patient_id:
                    print(f"{patient_id} already exists, with name {patient_data[1]}")
                    return'''
            if zampy.check_record_exists(patient_id, 0, patients_data):
                print("User already exists!\nRunning login...")
            else:
                print("User doesnt exist! making new record...")
            #doesnt exist, make a new record.
        elif useridentify == 2:
            print("Running log in!")
    elif currentUserType == 'D':
        print('current doctor!')



start_program()