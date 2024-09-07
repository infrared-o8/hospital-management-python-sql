import mysql.connector
from datetime import datetime
import zampy

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()

current_user_type = None
current_user_data = None


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
        attain_creds(current_user_type)

def make_new_record(ordered_patient_table, patient_name):
        new_patient_data = (int(ordered_patient_table[-1][0]) + 1, patient_name)

        c.execute("INSERT into patients (PatientID, Name) values (%s, %s)", new_patient_data)
        database.commit()

        c.execute("select * from patients")
        confirm_data = c.fetchall()
        print("Updated patients table\n", confirm_data)

        c.execute(f"select * from patients where PatientID = {new_patient_data[0]}")
        current_user_data = c.fetchone()
        print(current_user_data)

def signup():
    global current_user_data
    #get required info
    patient_name = input("Enter patient name: ")
    #check if it already exists in patients table.
    c.execute('select * FROM patients ORDER BY PatientID')
    ordered_patient_table = c.fetchall()
    (pExists, patient_record) = zampy.check_record_exists(patient_name, 1, ordered_patient_table)
    if pExists:
        print(f"Username already exists with patient data: {patient_record}!\nLogging in...")
        confirm = input("Do you confirm this is your data? (Y/N): ")
        if confirm in 'Yy':
            current_user_data = patient_record
        else:
            make_new_record(ordered_patient_table, patient_name)
    else:
        print("User doesnt exist! Making new record...")
        #doesnt exist, make a new record.
        make_new_record(ordered_patient_table, patient_name)


def login():
    global current_user_data
    requested_id = int(input("Enter patient ID: "))
    c.execute(f"select * from patients where patientid = {requested_id}")
    record = c.fetchone()
    if record is None:
        requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
        if requSignUp in 'Yy':
            signup()
    else:
        print(f"Succesfully retrieved patient data: {record}")
        current_user_data = record

def attain_creds(currentUserType):
    global current_user_data
    if currentUserType == 'P':
        #print('current patient!')
        print("Log in or sign up as patient?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            print("Running sign up!")
            signup()
            
        elif useridentify == 2:
            print("Running login!")
            login()
    elif currentUserType == 'D':
        print('current doctor!')



start_program()