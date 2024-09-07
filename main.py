import mysql.connector
from datetime import datetime
import zampy
from prettytable import PrettyTable, from_db_cursor
import pickle
import bcrypt
import pyfiglet
import os
from pathlib import Path

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()

current_user_type = None
current_user_data = None

# Define the path to the local directory
directory = Path.home() / "HospitalManagement-PythonSQL"  # This creates a folder in the user's home directory

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define the login file path
login_file = directory / "creds.dat"

def start_program():
    global current_user_type
    global current_user_data

    try:
        bfile = open(login_file, "rb")
    except Exception as e:
        print("Some error occured while trying to find existing login-file:", e)
        print("Proceeding to normal login...")
        try:
            print("Using as patient/doctor?\n")
            user = int(input(zampy.make_menu_from_options(['Patient', 'Doctor'])))
            if user == 1:
                #logging in as patient
                current_user_type = 'P'
            elif user == 2:
                #logging in as doctor
                current_user_type = 'D'
            else:
                print("Something went wrong. Try again...\n")
                start_program()
        except ValueError:
            print("Input was of incorrect datatype. Try again...\n")
            start_program()
        else:
            attain_creds(current_user_type)
    else:
        bfilecontents = pickle.load(bfile)
        print("Found an existing login file:", bfilecontents, "\nConfirm login with these credentials?")
        confirmLogin = int(input(zampy.make_menu_from_options()))
        if confirmLogin == 1:
            current_user_type = bfilecontents[0]
            current_user_data = bfilecontents[1]
            print("Succesfully logged in as", current_user_data[1])
        else:
            #attain_creds(current_user_type)
            try:
                print("Using as patient/doctor?\n")
                user = int(input(zampy.make_menu_from_options(['Patient', 'Doctor'])))
                if user == 1:
                    #logging in as patient
                    current_user_type = 'P'
                elif user == 2:
                    #logging in as doctor
                    current_user_type = 'D'
                else:
                    print("Something went wrong. Try again...\n")
                    start_program()
            except ValueError:
                print("Input was of incorrect datatype. Try again...\n")
                start_program()
            else:
                attain_creds(current_user_type)



def make_new_record(ordered_table, name, usertype):
        global current_user_data
        global current_user_type
        if usertype == "P":
            new_patient_data = (f"{usertype}{int(ordered_table[-1][0][1]) + 1}", name)

            c.execute("INSERT into patients (PatientID, Name) values (%s, %s)", new_patient_data)
            database.commit()

            c.execute("select * from patients")
            confirm_data = c.fetchall()
            print("Updated patients table\n", confirm_data)

            c.execute(f"select * from patients where PatientID = '{new_patient_data[0]}'")
            current_user_data = c.fetchone()
            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data], bfile)
        elif usertype == "D":
            new_doctor_data = (f"{usertype}{int(ordered_table[-1][0][1]) + 1}".upper(), name)

            c.execute("INSERT into doctors (doctorID, Name) values (%s, %s)", new_doctor_data)
            database.commit()

            c.execute("select * from doctors")
            confirm_data = c.fetchall()
            print("Updated doctors table\n", confirm_data)

            c.execute(f"select * from doctors where doctorID = '{new_doctor_data[0]}'")
            current_user_data = c.fetchone()
            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data], bfile)

def signup(user_type):
    global current_user_data
    #get required info
    if user_type == "P":
        patient_name = input("Enter patient name: ")
        #check if it already exists in patients table.
        c.execute('select * FROM patients ORDER BY PatientID')
        ordered_patient_table = c.fetchall()
        (pExists, patient_record) = zampy.check_record_exists(patient_name, 1, ordered_patient_table)
        if pExists:
            print(f"Username already exists with patient data: {patient_record}!") #add column names - !!
            confirm = input("Do you confirm this is your data? (Y/N): ")
            if confirm in 'Yy':
                current_user_data = patient_record
            else:
                make_new_record(ordered_patient_table, patient_name, user_type)
        else:
            print("Patient record doesn't exist! Making new record...")
            #doesnt exist, make a new record.
            make_new_record(ordered_patient_table, patient_name, user_type)
    elif user_type == "D":
        doctor_name = input("Enter doctor name: ")
        #check if it already exists in doctors table.
        c.execute('select * FROM doctors ORDER BY DoctorID')
        ordered_doctor_table = c.fetchall()
        (dExists, doctor_record) = zampy.check_record_exists(doctor_name, 1, ordered_doctor_table)
        if dExists:
            print(f"Username already exists with doctor data: {doctor_record}!") #add column names - !!
            confirm = input("Do you confirm this is your data? (Y/N): ")
            if confirm in 'Yy':
                current_user_data = doctor_record
            else:
                make_new_record(ordered_doctor_table, doctor_name, user_type)
        else:
            print("Doctor record doesn't exist! Making new record...")
            #doesnt exist, make a new record.
            make_new_record(ordered_doctor_table, doctor_name, user_type)

def login(user_type):
    global current_user_data
    global current_user_type
    if user_type == "P":
        requested_id = (input("Enter patient ID: "))
        c.execute(f"select * from patients where patientid = '{requested_id}'")
        record = c.fetchone()
        if record is None:
            requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup()
        else:
            print(f"Succesfully retrieved patient data: {record}")
            current_user_data = record

            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data], bfile)

    elif user_type == "D":
        requested_id = (input("Enter doctor ID: "))
        c.execute(f"select * from doctors where doctorid = '{requested_id}'")
        record = c.fetchone()
        if record is None:
            requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup()
        else:
            print(f"Succesfully retrieved doctor data: {record}")
            current_user_data = record

            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data], bfile)


def attain_creds(currentUserType):
    if currentUserType == 'P':
        print("Log in or sign up as patient?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)
    elif currentUserType == 'D':
        print("Log in or sign up as doctor?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)

def viewPatientDetails(patientID):
    c.execute(f"select * from patients where PatientID = '{patientID}'")
    return c.fetchone()

def viewDoctorDetails(doctorID):
    c.execute(f"select * from doctors where doctorID = '{doctorID}'")
    return c.fetchone()

def viewPrescriptions(pID, all = True):
    if all:
        c.execute("select * from prescriptions")
        return c.fetchall()
    else:
        if pID:
            c.execute(f"select * from prescriptions where prescriptionID = '{pID}'")

def viewRecordDetails(patientID ,recordID = None, doctorID = None, all = False):
    if recordID:
        c.execute(f"select * from medicalhistory where recordID = '{recordID}' AND patientID = '{patientID}'")
        return c.fetchone()
    if doctorID:
        c.execute(f"select * from medicalhistory where doctor = '{doctorID}' AND patientID = '{patientID}'")
        return c.fetchall()
    if all:
        c.execute(f"select * from medicalhistory where patientID = '{patientID}'")
        return c.fetchall()

def add_value_to_table(tableName, columnNames, values):
    c.execute(f"insert into {tableName} {columnNames} values ({(('%s,'*(len(values) - 1)) + '%s')})", values)
    database.commit()



def makeAppointment(patientID, doctorID, appointmentDate, appointmentReason):
    if patientID and doctorID and appointmentDate and appointmentReason:
        appointmentID = ""
        #fetch existing appointments
        c.execute("select * from appointments")
        data = c.fetchall()
        
        if zampy.checkEmpty(data):
            appointmentID = "A1"
        else:
            appointmentID = f"A{int(data[-1][0][1]) + 1}"
        
        #c.execute(f"insert into appointments (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, status) values (%s, %s, %s, %s, %s, %s)", (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, "Scheduled"))
        add_value_to_table('appointments', "(appointmentID, patientID, doctorID, appointmentDate, appointmentReason, status)", (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, "Scheduled"))



start_program()


all_options = ['View a patient\'s details', 'View a doctor\'s details', 'Make an appointment', 'Access medical history', 'View prescriptions', 'Access medical history of a patient', 'Access appointments history'] #also update own info, group doctors by specialization, view pending appointments
options = ['View a patient\'s details' if current_user_type == "D" else None, 'View a doctor\'s details', 'Make an appointment' if current_user_type == "P" else None, 'Access medical history' if current_user_type == "P" else None, 'Access medical history of a patient' if current_user_type == "D" else None, 'View all prescriptions', 'Access appointments history' if current_user_type == "D" else None]
options_menu_str, options_dict = zampy.make_menu_from_options(options, True)
#Doctor's/Patients Panel
while True:
    print("Enter action: ")
    tempIndex = int(input(options_menu_str))
    action = options_dict[tempIndex]
    try:
        index = all_options.index(action)
    except Exception as e:
        print(f"Error occured:", e)
    else:
        if index == 0:
            patientID = (input("Enter patient ID: "))
            data = viewPatientDetails(patientID)
            print("Requested data:", data)
        elif index == 1:
            doctorID = (input("Enter doctor ID: "))
            data = viewDoctorDetails(doctorID)
            print("Requested data:", data)
        elif index == 2:
            #Make an appointment
            doctorID = input("Enter doctor ID to make appointment to: ")
            #appointmentDate = input("Enter date of appointment (Format: YYYY-MM-DD): ")
            appointmentDate = zampy.choose_date()
            appointmentReasonIndex = int(input(zampy.make_menu_from_options(['Check-up', 'Surgery'])))
            if appointmentReasonIndex == 1:
                appointmentReason = "Check-up"
            elif appointmentReasonIndex == 2:
                appointmentReason = "Surgery"
            
            makeAppointment(current_user_data[0], doctorID, appointmentDate, appointmentReason)
        elif index == 3:
            historyOptions = ['Access using recordID', 'Access your records by specific doctor (doctorID)', 'Access your history'] #add more options here
            historyIndex = int(input(zampy.make_menu_from_options(historyOptions)))
            if historyIndex == 1:
                recordID = (input("Enter recordID: "))
                data = viewRecordDetails(recordID=recordID)
                print(data)
            elif historyIndex == 2:
                doctorID = (input("Enter doctor ID: "))
                data = viewRecordDetails(doctorID=doctorID)
                print(data)
            elif historyIndex == 3:
                data = viewRecordDetails(current_user_data[0], all=True)
                print(data)
        elif index == 4:
            data = viewPrescriptions(all=True) #expand to finding by name, and id
            print(data)
        elif index == 5:
            #Access medical history of a patient
            patientID = input("Enter patient ID: ").upper()
            data = viewRecordDetails(patientID=patientID)
            print(data)
        elif index == 6:
            #Access appointments history
            options = ['Upcoming appointments', 'Completed appointments']
            index = int(input(zampy.make_menu_from_options(options)))
            if index == 1:
                c.execute("SELECT * FROM appointments WHERE doctorID = %s AND status = %s", (current_user_data[0], 'Scheduled'))
                data = c.fetchall()
                print(data)
                # print(from_db_cursor(c))
            elif index == 2:
                c.execute("SELECT * FROM appointments WHERE doctorID = %s AND status = %s", (current_user_data[0], 'Completed'))
                data = c.fetchall()
                print(data)
                # print(from_db_cursor(c))
        else:
            print("Something went wrong.")