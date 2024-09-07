import mysql.connector
from datetime import datetime
import zampy

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()

current_user_type = None
current_user_id = None


def start_program():
    global current_user_type
    try:
        print("Using as patient/doctor?\n")
        user = int(input(zampy.make_menu_from_options(['Patient', 'Doctor'])))
        if user == 1:
            #logging in as patient
            current_user_type = 'P'
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
        signin(current_user_type)

def signin(currentUserType):
    global current_user_id
    if currentUserType == 'P':
        #print('current patient!')
        print("Log in or sign up as patient?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            print("Running sign up!")

            #get required info
            patient_name = input("Enter patient name: ")
            #check if it already exists in patients table.
            c.execute('select * FROM patients ORDER BY PatientID')
            ordered_patient_table = c.fetchall()
            (pExists, patient_record) = zampy.check_record_exists(patient_name, 1, ordered_patient_table)
            if pExists:
                print("Username already exists!\nRunning login...")
                #confirm if all details are correct, if not, sign up.
                current_user_id = patient_record[0]
            else:
                print("User doesnt exist! Making new record...")
                #doesnt exist, make a new record.
                
                new_patient_data = (int(ordered_patient_table[-1][0]) + 1, input("Enter patient name: "))

                c.execute("INSERT into patients (PatientID, Name) values (%s, %s)", new_patient_data)
                database.commit()

                c.execute("select * from patients")
                confirm_data = c.fetchall()
                print("Updated patients table\n", confirm_data)
        elif useridentify == 2:
            print("Running log in!")

    elif currentUserType == 'D':
        print('current doctor!')



start_program()