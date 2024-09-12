import mysql.connector
from datetime import datetime, date
import zampy
from prettytable import PrettyTable, from_db_cursor
import pickle
import bcrypt
import pyfiglet
import os
from pathlib import Path
import getpass
import tkinter as tk
from tkinter import ttk

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()
#c = database.cursor(buffered=True)

current_user_type = None
current_user_data = None

request_sign_up = "Request to Sign Up"
request_promotion = 'Request to Promote'
# Define the path to the local directory
directory = Path.home() / "HospitalManagement-PythonSQL"  # This creates a folder in the user's home directory

debug = True
# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define the login file path
login_file = directory / "creds.dat"
log_file = directory / 'log.txt'

def convertTime(rawTime):
    #"""Converts 24-hour formatted time (HH:MM:SS) to 12-hour AM/PM format."""
    # Split the rawTime into components
    time_parts = str(rawTime).split(":")
    hour = int(time_parts[0])
    minutes = time_parts[1]
    #seconds = time_parts[2] if len(time_parts) == 3 else "00"  # Default to "00" if no seconds are provided
    
    # Determine AM/PM and adjust hour
    period = "AM"
    if hour == 0:
        hour = 12
    elif hour >= 12:
        period = "PM"
        if hour > 12:
            hour -= 12
    
    # Return formatted time
    return f"{hour}:{minutes} {period}"

def checkIfNonNull(variable):
    '''If null, returns False.'''
    if variable in [None, 'None', 'NULL', 'Null', (None,), ('NULL',), (), '', [], {}]:
        print(variable, "was null.")
        return False
    else:
        return True

def returnNewID(tableName):
    return incrementNumericPart(getHighestID(retreiveData(tableName)))

def makePrettyTable(tableName, data):
    # Fetch column names for the table
    c.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{tableName}'")
    columnNames = c.fetchall()
    
    # Create PrettyTable with the column names
    table = PrettyTable([columnNames[x][0] for x in range(len(columnNames))])
    
    # Print data for debugging purposes
    print('data in makePrettyTable:', data)
    
    # Check if data is a single row (tuple or list) or multiple rows (list of tuples/lists)
    if data and checkIfNonNull(data) == True:
        if isinstance(data[0], (tuple, list)):  # Multiple rows case (list of lists/tuples)
            table.add_rows([x for x in data])
        else:  # Single row case (tuple or list)
            table.add_row([x for x in data])

    # Display the table
    print(table)
    

def viewPendingRequests():
    global current_user_data, current_user_type
    if current_user_type == 'A': #confirm its an admin
        #all signup requests.
        c.execute(f'select * from admin_requests where requestReason = \'{request_sign_up}\'')
        signUpRequests = c.fetchall()
        if len(signUpRequests) > 0:
            print('Pending signup requests:\n')
            makePrettyTable('admin_requests', signUpRequests)
        '''        c.execute(f'select * from admin_requests where requestReason = \'{request_promotion}\'')
        promotionRequests = c.fetchall()
        if len(promotionRequests) > 0:
            print('Pending promotion requests:', promotionRequests)'''
        return signUpRequests

def dealWithPendingRequests():
    signupReq = viewPendingRequests()
    for req in signupReq:
        name = req[2]
        id = returnNewID('admins')
        print(f"Approve pending sign-up of {name} as admin:")
        choice = int(input(zampy.make_menu_from_options()))
        if choice == 1:
            #delete from admin_requests
            c.execute(f'delete from admin_requests where requestID = "{req[0]}";')
            database.commit()
            #add new user to credentials and admin table
            add_value_to_table('admins', ['adminID', 'adminName'], [id, name])
            add_value_to_table('credentials', ['userID'], [id])
        else:
            continue
    #deal with promotionReq
        '''    for req in promotionReq:
        name = req[2]
        id = returnNewID('admins')
        print(f"Approve pending promotion of {name} as admin:")
        choice = int(input(zampy.make_menu_from_options()))
        if choice == 1:
            #delete from admin_requests
            c.execute(f'delete from admin_requests where requestID = "{req[0]}";')
            database.commit()
            #add new user to credentials and admin table
            add_value_to_table('admins', ['adminID', 'adminName'], [id, name])
            existingPassword = retreiveData('credentials', columnNames=['password'], conditionNames=['userID'], conditionValues=[id])
            if checkIfNonNull(existingPassword):
                add_value_to_table('credentials', ['userID', 'password'], [existingPassword])
        else:
            continue'''
def log(text):
    file = None
    try:
        file = open(log_file, 'a')
    except Exception as e:
        print("Error while trying to open log_file:", e)
        file = open(log_file, "w")
    file.write(f'{str(datetime.now())}: {text}\n')

def askForPassword(name: str = "current user"):
    print(f"Enter password for:\t {name}")
    inpPassword = getpass.getpass()
    return inpPassword

def checkPasswords(correct_password: str, name: str = "current user", usebcrypt = False) -> bool:
    inpPassword = askForPassword(name)
    if usebcrypt:
        if bcrypt.checkpw(inpPassword.encode('utf-8'), correct_password):
            return True
    else:
        if correct_password == inpPassword:
            return True
    return False

def incorrectPassword():
    print("Incorrect password!")
    #do something more here!
def incrementNumericPart(text):
    number = (text[1:])
    x = 0
    while not number.isnumeric():
        x += 1
        number = (text[1+x:])
    number = int(number) + 1
    return text[0:1+x] + str(number)

def getHighestID(ordered_table):
    highestNum = 0
    #highestID = None
    for record in ordered_table:
        currentNum = (record[0][1:])
        x = 0
        while not currentNum.isnumeric():
            x += 1
            currentNum = (record[0][(1 + x):])
        currentNum = int(currentNum)
        if currentNum > highestNum:
            highestNum = currentNum
    return ordered_table[0][0][0:(1+x)] + str(highestNum)  

def makeNewPrescription(returnPCID = True):
    prescription = input("Enter prescription name: ")
    prescriptionID = None
    #check if it already exists
    c.execute(f"select * from prescriptions where medication_name = '{prescription}'")
    existingPrescriptions = c.fetchall()
    if len(existingPrescriptions) > 0:
        #exists already!
        print(f"A prescription already recorded with the same name was found.\n")
        for existingPrescription in existingPrescriptions:
            if existingPrescription[1] == prescription:
                print("Details are:\n")
                makePrettyTable('prescriptions', existingPrescription)
                prescriptionID = existingPrescription[0]
    else:
        prescriptionID = returnNewID('prescriptions')
        dosage = input("Enter general dosage: ")
        add_value_to_table('prescriptions', ['prescriptionID', 'medication_name', 'dosage'], [prescriptionID, prescription, dosage])
        log(f'New prescription added with: {[prescriptionID, prescription, dosage]}')
    if returnPCID:
        return prescriptionID

def requestExistingAdminToSignUp(adminName):
    #c.execute(f"insert into admin_requests values('{}', 'Request to Sign Up', ')")
    c.execute('select * from admin_requests')
    ordered_table = c.fetchall()
    new_request_id = ''
    if len(ordered_table) > 0:
        new_request_id = f"{returnNewID('admin_requests')}" 
    else:
        new_request_id = 'REQ1'
    add_value_to_table('admin_requests', ['requestID', 'requestReason', 'signUpRequestName'], [new_request_id, request_sign_up, adminName])

def updateAppointments(current_user_type):
    global current_user_data
    if current_user_type == "P":
        #appointmentsPending = retreiveData('appointments', conditionNames=['patientID'], conditionValues=[current_user_data[0]])
        c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate")
        appointmentsPendingToday = c.fetchall()
        c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' < appointmentDate")
        appointmentsPendingLater = c.fetchall()

        if len(appointmentsPendingLater) > 0:
            for appointment in appointmentsPendingLater:
                print(f"You have an appointment scheduled with Dr. {viewDoctorDetails(appointment[2])[1]} on {appointment[3]} at {convertTime(appointment[-1])}")
        if len(appointmentsPendingToday) > 0:
            for appointment in appointmentsPendingToday:
                if appointment[6] not in [None, 'None', 'NULL']:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time < appointment_time:
                        print(f"You have an upcoming appointment at {convertTime(appointment_time)} with Dr. {viewDoctorDetails(appointment[2])[1]}")
                    else:
                        #Check for whether the record with same date and time, patientID and doctorID was added to medicalhistory. 
                        #missedRecordConfirm = retreiveData('medicalhistory', conditionNames=['patientID', 'doctorID', 'visitDate', 'time'], conditionValues=[current_user_data[0], appointment[2], str(date.today().isoformat()), appointment_time])
                        c.execute(f"select * from medicalhistory where patientID = '{current_user_data[0]}' and doctorID = '{appointment[2]}' and visitDate = '{date.today().isoformat()}' and time = '{appointment_time}'")
                        missedRecordConfirm = c.fetchall()
                        if checkIfNonNull(missedRecordConfirm) == True:
                            if len(missedRecordConfirm) > 0:
                                print(f"You missed an appointment that was scheduled for {convertTime(appointment_time)}")
                                log(f'{current_user_data[1]} missed an appointment: {missedRecordConfirm}')
                else:
                    print(f"Your appointment scheduled for {date.today()} was found to have no time assigned.\nChoose a time: ")
                    timeInput = zampy.choose_time()
                    timeDateTime = datetime.strptime(timeInput, "%H:%M").time()
                    #check if the patient has another appointment at chosen time
                    #appointDateTimeFormat = datetime.strptime(appointmentTime, "%H:%M").time() 
                    #check if the patient has another appointment at chosen time
                    #todayStr = str(datetime.today().date())
                    #ensure time doesnt overlap.
                    if timeDateTime > datetime.now().time(): #check if its not in the past
                        c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                        potentialPatientAlreadyHasAppointment = c.fetchall()
                        if len(potentialPatientAlreadyHasAppointment) > 0:
                            print("You already have an appointment at that time!")
                        else:
                            #check if doctor has another appointment at chosen time
                            c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}'")
                            potentialDoctorBusy = c.fetchall()
                            if len(potentialDoctorBusy) > 0:
                                print("Sorry! The doctor is busy at that time. Please try another time.")
                            else:
                                add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointment[0], patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                                if debug:
                                    print("Succeeded in making appointment!")
                                    log("Succeeded in making appointment!")
                    else:
                        print("Time cannot be chosen in the past.")
        else:
            print("You have no appointments upcoming today.")
    elif current_user_type == "D":
        if current_user_data:
            doctorID = current_user_data[0]
        c.execute(f"select * from appointments where LOWER(doctorID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate")
        appointmentsPendingToday = c.fetchall()
        c.execute(f"select * from appointments where LOWER(doctorID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' < appointmentDate")
        appointmentsPendingLater = c.fetchall()

        

        #appointmentsPendingToday = c.fetchall()
        if len(appointmentsPendingToday) > 0:
            for appointment in appointmentsPendingToday:
                if checkIfNonNull(appointment[6]) == True:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time < appointment_time:
                        print(f"You have an upcoming appointment at {convertTime(appointment_time)} with {viewPatientDetails(appointment[1])[1]}")
        else:
            print("No upcoming appointments today.")
        #print(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and {date.today().isoformat()} >= appointmentDate")
        c.execute(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and '{date.today().isoformat()}' >= appointmentDate")
        assumedDoneAppointments = c.fetchall()
        doneAppointments = []
        for assumedAppointment in assumedDoneAppointments:
            if checkIfNonNull(assumedAppointment[6]) == True:
                    appointment_time = datetime.strptime(assumedAppointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if date.today() > assumedAppointment[3]:
                            doneAppointments.append(assumedAppointment)
                    else:
                        if current_time > appointment_time:
                            doneAppointments.append(assumedAppointment)
        makePrettyTable('appointments', doneAppointments)
        log(f'doneAppointments requested: {doneAppointments}')
        if len(doneAppointments) > 0:
            if debug:
                print(len(doneAppointments), "completed appointments found in appointments table. attempting to move them to medicalhistory...")
                log(f"{len(doneAppointments), } completed appointments found in appointments table. attempting to move them to medicalhistory...")
            for appointment in doneAppointments:
                patientID = appointment[1]
                patientName = viewPatientDetails(patientID)[1]
                print(f"Has the appointment scheduled with {patientName} been completed?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    diagnosis = input("Enter diagnosis: ")
                    prescriptionID = input("Enter prescriptionID: ")
                    print(f"Is this the prescription: {viewPrescriptions(prescriptionID,False)}?")
                    confirm = int(input(zampy.make_menu_from_options()))
                    if confirm == 1:
                        #log into medical history
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], diagnosis, prescriptionID, 'Completed'])
                        #delete from appointments.

                    else:
                        print("Attempting to make a new prescription...")
                        log(f"Attempting to make a new prescription.")
                        pcID = makeNewPrescription()
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], diagnosis, pcID, 'Completed'])
                        #delete from appointments.

                        #make a new prescription here!
                    c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                    database.commit()
                else:
                    print("Was the appointment cancelled?")
                    choice = int(input(zampy.make_menu_from_options()))
                    if choice == 1:
                        #log into medical history, 
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], 'NULL', 'NULL','Cancelled']) 
                        #delete from appointments.
                        c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                        database.commit()
                    #delay mechanism?
                    
def start_program():
    global current_user_type
    global current_user_data
    #signUpLoginPage()
    try:
        bfile = open(login_file, "rb")
        bfilecontents = pickle.load(bfile)
        found_user_type = bfilecontents[0]
        found_user_data = bfilecontents[1]
        found_user_password = bfilecontents[2]
    except Exception as e:
        print("Some error occured while trying to access existing login-file:", e)
        log(f"Some error occured while trying to access existing login-file: {e}.\nProceeding to normal login.")
        print("Proceeding to normal login...")
        try:
            print("Using as:\n")
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
        name = bfilecontents[1][1]
        print("Found an existing login file for", name, "\nConfirm login with these credentials?")
        confirmLogin = int(input(zampy.make_menu_from_options()))
        if confirmLogin == 1:
            #print("found)user_password", found_user_password)
            if checkPasswords(found_user_password, name, usebcrypt=True):
                current_user_type = bfilecontents[0]
                current_user_data = bfilecontents[1]
                print("Succesfully logged in as", current_user_data[1])
                
            else:
                incorrectPassword()
        else:
            try:
                print("Using as:\n")
                user = int(input(zampy.make_menu_from_options(['Patient', 'Doctor', 'Admin'])))
                if user == 1:
                    #logging in as patient
                    current_user_type = 'P'
                elif user == 2:
                    #logging in as doctor
                    current_user_type = 'D'
                elif user == 3:
                    current_user_type = 'A'
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
            #new_patient_id = f"{usertype}{int(ordered_table[-1][0][1]) + 1}" #update thisss
            new_patient_id = f"{incrementNumericPart(getHighestID(ordered_table))}" 
            new_patient_data = [new_patient_id, name]
            #print(new_patient_id)
            #c.execute("INSERT into patients (PatientID, Name) values (%s, %s)", new_patient_data)
            print("Type a new ", end="")
            new_p = getpass.getpass()
            new_p_bytes = new_p.encode('utf-8')
            add_value_to_table("credentials", ['userid', 'password'], [new_patient_id, new_p])
            add_value_to_table("patients", ['PatientID', 'Name'], new_patient_data)
            #database.commit()

            #c.execute("select * from patients")
            #confirm_data = c.fetchall()

            confirm_data = retreiveData('patients', allColumns=True)

            #print("Updated patients table\n")
            #makePrettyTable('patients', confirm_data)
            log(f"Updated patients table: {confirm_data}")
            #c.execute(f"select * from patients where PatientID = '{new_patient_data[0]}'")
            #current_user_data = c.fetchone()

            current_user_data = retreiveData("patients", allColumns=True, conditionNames=['PatientID'], conditionValues=[new_patient_data[0]], returnAllData=False)

            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)
        elif usertype == "D":
            new_doctor_id = f"{incrementNumericPart(getHighestID(ordered_table))}"
            new_doctor_data = [new_doctor_id, name]

            #c.execute("INSERT into doctors (doctorID, Name) values (%s, %s)", new_doctor_data)
            #database.commit()
            print("Type a new ", end="")
            new_p = getpass.getpass()
            new_p_bytes = new_p.encode('utf-8')
            add_value_to_table("credentials", ['userid', 'password'], [new_doctor_id, new_p])
            add_value_to_table("doctors", ['DoctorID', 'Name'], new_doctor_data)

            #c.execute("select * from doctors")
            #confirm_data = c.fetchall()

            confirm_data = retreiveData('doctors', allColumns=True)
            #print("Updated doctors table\n", confirm_data)
            log(f"Updated doctors table: {confirm_data}")
            #c.execute(f"select * from doctors where doctorID = '{new_doctor_data[0]}'")
            #current_user_data = c.fetchone()

            current_user_data = retreiveData("doctors", allColumns=True, conditionNames=['DoctorID'], conditionValues=[new_doctor_data[0]], returnAllData=False)


            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)
            '''elif usertype == "A":
            new_admin_id = f"{incrementNumericPart(getHighestID(ordered_table))}"
            new_admin_data = [new_admin_id, name]

            #c.execute("INSERT into doctors (doctorID, Name) values (%s, %s)", new_doctor_data)
            #database.commit()
            new_p = askForPassword()
            new_p_bytes = new_p.encode('utf-8')
            add_value_to_table("credentials", ['userid', 'password'], [new_admin_id, new_p])
            add_value_to_table("admins", ['adminID', 'Name'], new_admin_data)

            #c.execute("select * from doctors")
            #confirm_data = c.fetchall()

            confirm_data = retreiveData('admins', allColumns=True)
            print("Updated admins table\n", confirm_data)
            log(f"Updated admins table: {confirm_data}")
            #c.execute(f"select * from doctors where doctorID = '{new_doctor_data[0]}'")
            #current_user_data = c.fetchone()

            current_user_data = retreiveData("admins", allColumns=True, conditionNames=['adminID'], conditionValues=[new_admin_data[0]], returnAllData=False)


            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)'''

def signup(user_type):
    global current_user_data
    #get required info
    if user_type == "P":
        patient_name = input("Enter patient name: ")
        #check if it already exists in patients table.
        c.execute('select * FROM patients ORDER BY PatientID') ##orderby functionality here!
        ordered_patient_table = c.fetchall()

        #ordered_patient_table = retreiveData("patients", )

        (pExists, patient_record) = zampy.check_record_exists(patient_name, 1, ordered_patient_table)
        if pExists:
            print(f"Username already exists with patient data: {patient_record}!") #add column names - !!
            confirm = input("Do you confirm this is your data? (Y/N): ") #add password protection here
            if confirm in 'Yy':
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[patient_record[0]], returnAllData=False)
                password = password[0]
                if checkPasswords(password, patient_record[1]):
                    current_user_data = patient_record
                else:
                    incorrectPassword()
            else:
                print("Would you like to create a new account with this name?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    make_new_record(ordered_patient_table, patient_name, user_type)
        else:
            print("Patient record doesn't exist! Making new record...")
            #doesnt exist, make a new record.
            make_new_record(ordered_patient_table, patient_name, user_type)
    elif user_type == "D":
        doctor_name = input("Enter doctor name: ")
        #check if it already exists in doctors table.
        c.execute('select * FROM doctors ORDER BY DoctorID') ##orderby functionality here!
        ordered_doctor_table = c.fetchall()
        (dExists, doctor_record) = zampy.check_record_exists(doctor_name, 1, ordered_doctor_table)
        if dExists:
            print(f"Username already exists with doctor data: {doctor_record}!") #add column names - !!
            confirm = input("Do you confirm this is your data? (Y/N): ")
            if confirm in 'Yy':
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[doctor_record[0]], returnAllData=False)
                password = password[0]
                if checkPasswords(password, doctor_record[1]):
                    current_user_data = doctor_record
                else:
                    incorrectPassword()
            else:
                print("Would you like to create a new account with this name?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    make_new_record(ordered_doctor_table, doctor_name, user_type)
        else:
            print("Doctor record doesn't exist! Making new record...")
            #doesnt exist, make a new record.
            make_new_record(ordered_doctor_table, doctor_name, user_type)
    elif user_type == 'A':
        admin_name = input("Enter admin name: ")
        #check if it already exists in doctors table.
        c.execute('select * FROM admins ORDER BY adminID') ##orderby functionality here!
        ordered_admin_table = c.fetchall()
        (aExists, admin_record) = zampy.check_record_exists(admin_name, 1, ordered_admin_table)
        if aExists:
            print(f"Username already exists with admin data: {admin_record}!") #add column names - !!
            confirm = input("Do you confirm this is your data? (Y/N): ")
            if confirm in 'Yy':
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[admin_record[0]], returnAllData=False)
                print('password:', password)
                if password and checkIfNonNull(password) == True:
                    password = password[0]
                    if checkPasswords(password, admin_record[1]):
                        current_user_data = admin_record
                    else:
                        incorrectPassword()
                else:
                    print("The user was found with no password. Enter new password?")
                    choice = input(zampy.make_menu_from_options())
                    if choice == 1:
                        print("Enter new",end="")
                        newPassword = askForPassword()
                        while newPassword != None:
                            newPassword = askForPassword()
                        c.execute(f'update credentials set password = "{newPassword}" where userid = "{admin_record[0]}"')
                    else:
                        start_program()
            else:
                print("Would you like to create a new account with this name?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    #make_new_record(ordered_admin_table, admin_name, user_type)
                    requestExistingAdminToSignUp(admin_name)
        else:
            print("Admin record doesn't exist! Making new record...")
            requestExistingAdminToSignUp(admin_name)

            #doesnt exist, make a new record.
            #make_new_record(ordered_doctor_table, doctor_name, user_type)


def login(user_type):
    global current_user_data
    global current_user_type
    if user_type == "P":
        requested_id = (input("Enter patient ID: "))
        #c.execute(f"select * from patients where patientid = '{requested_id}'")
        #record = c.fetchone()

        record = retreiveData("patients", conditionNames=['patientID'], conditionValues=[requested_id], returnAllData=False)
       # if record:
           # password = input(f"Record found. Enter password for {record[1]}:")

        if record is None:
            requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup(user_type)
            else:
                start_program()
        else:
            cpassword = retreiveData('credentials', False, ['password'], ['userid'], [record[0]], returnAllData=False)
            cpassword = cpassword[0]
            cpasswordbytes = cpassword.encode('utf-8')
            #print("cpassword:", cpassword)
            if checkPasswords(cpassword, record[1]):
                current_user_data = record

                bfile = open(login_file, "wb")
                pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
            else:
                incorrectPassword()

    elif user_type == "D":
        requested_id = (input("Enter doctor ID: "))
        #c.execute(f"select * from doctors where doctorid = '{requested_id}'")
        #record = c.fetchone()

        record = retreiveData("doctors", conditionNames=['doctorID'], conditionValues=[requested_id], returnAllData=False)


        if record is None:
            requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup(user_type)
        else:
            cpassword = retreiveData('credentials', False, ['password'], ['userid'], [record[0]], returnAllData=False)
            cpassword = cpassword[0]
            cpasswordbytes = cpassword.encode('utf-8')
            if checkPasswords(cpassword, record[1]):
                current_user_data = record

                bfile = open(login_file, "wb")
                pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
            else:
                incorrectPassword()
    elif user_type == 'A':
        requested_id = (input("Enter admin ID: "))
        record = retreiveData("admins", conditionNames=['adminID'], conditionValues=[requested_id], returnAllData=False)

        if record is None:
            requSignUp = input("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup(user_type)
        else:
            cpassword = retreiveData('credentials', False, ['password'], ['userid'], [record[0]], returnAllData=False)
            #print(cpassword)
            if checkIfNonNull(cpassword) == True:
                cpassword = cpassword[0]
                if checkPasswords(cpassword, record[1]):
                    current_user_data = record
                else:
                    incorrectPassword()
            else:
                print("The user was found with no password. Enter new password?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    #print("Enter new",end="")
                    newPassword = askForPassword()
                    while newPassword == None or newPassword == "":
                        newPassword = askForPassword()
                    c.execute(f'update credentials set password = "{newPassword}" where userid = "{record[0]}"')
                    database.commit()
                else:
                    start_program()

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
    elif current_user_type == 'A':
        print("Log in or sign up as admin?")
        useridentify = int(input(zampy.make_menu_from_options(['Sign up', 'Log in'])))
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)

def viewPatientDetails(patientID):
    #c.execute(f"select * from patients where PatientID = '{patientID}'")
    #return c.fetchone()
    return retreiveData("patients", conditionNames=['patientID'], conditionValues=[patientID], returnAllData=False)

def viewDoctorDetails(doctorID):
    #c.execute(f"select * from doctors where doctorID = '{doctorID}'")
    #return c.fetchone()
    return retreiveData("doctors", conditionNames=['doctorID'], conditionValues=[doctorID], returnAllData=False)
    

def viewPrescriptions(pID = None, all = True):
    if all:
        #c.execute("select * from prescriptions")
        #return c.fetchall()

        return retreiveData("prescriptions", allColumns=True)
    else:
        if pID:
            #c.execute(f"select * from prescriptions where prescriptionID = '{pID}'")
            return retreiveData("prescriptions", allColumns=True, returnAllData=False, conditionNames=['prescriptionID'], conditionValues=[pID])

def viewRecordDetails(patientID ,recordID = None, doctorID = None, all = False):
    if recordID:
        #c.execute(f"select * from medicalhistory where recordID = '{recordID}' AND patientID = '{patientID}'")
        #return c.fetchone()
        return retreiveData("medicalhistory", True, conditionNames=['recordID', 'patientID'], conditionValues=[recordID, patientID])
    if doctorID:
        #c.execute(f"select * from medicalhistory where doctorID = '{doctorID}' AND patientID = '{patientID}'")
        #return c.fetchall()
        return retreiveData("medicalhistory", True, conditionNames=['doctorID', 'patientID'], conditionValues=[doctorID, patientID])
    if all:
        #c.execute(f"select * from medicalhistory where patientID = '{patientID}'")
        #return c.fetchall()
        return retreiveData("medicalhistory", True, conditionNames=['patientID'], conditionValues=[patientID])

def add_value_to_table(tableName, columnNames: list, values: list):
    #c.execute(f"insert into {tableName} {columnNames} values ({(('%s,'*(len(values) - 1)) + '%s')})", values)
    command = "insert into"
    if tableName:
        command += f" {tableName}"
        if columnNames:
            command += f" ({','.join(columnNames)})"
            if values:
                command += f" values ({(('%s,'*(len(values) - 1)) + '%s')})"
    c.execute(command, values)
    database.commit()

def retreiveData(tableName: str, allColumns:bool = False, columnNames: list = None, conditionNames: list = None, conditionValues: list = None, returnAllData:bool = True):
    '''Assumes all conditions to be seperated by AND for now.'''
    command = "select"
    if columnNames == None:
        allColumns = True
    if tableName:
        if not allColumns:
            if columnNames:
                command += f" {','.join(columnNames)}"
        else:
            command += " *"
        command += f" from {tableName}"
        if conditionNames and conditionValues:
            command += " where"
            for conditionIndex in range(1, len(conditionNames) + 1):
                currentValue = conditionValues[conditionIndex - 1]
                if type(currentValue) is str:
                    command += f" {conditionNames[conditionIndex - 1]} = '{currentValue}'"
                elif type(currentValue) is int:
                    command += f" {conditionNames[conditionIndex - 1]} = {currentValue}"
                if conditionIndex == len(conditionNames):
                    continue
                command += " AND"
        command += ";"
    else:
        print("Received no tableName.")
        #return None
    if debug:
        print("Final commmand:", command)
        log(f"Final commmand: {command}")

    try:
        c.execute(command)
    except Exception as e:
        print("Error while trying to retrieve data:", e)
        log(f"Error while trying to retrieve data: {e}")
        return None
    else:
        if returnAllData:
            data = c.fetchall()
        else:
            data = c.fetchone()
        return data

def makeAppointment(patientID, doctorID, appointmentDate, appointmentTime, appointmentReason):
    if patientID and doctorID and appointmentDate and appointmentReason and appointmentTime:
        #fetch existing appointments
        #c.execute("select * from appointments")
        #data = c.fetchall()
        
        data = retreiveData('appointments')

        if zampy.checkEmpty(data):
            appointmentID = "A1"
        else:
            appointmentID = f"{returnNewID('appointments')}"
        
        #c.execute(f"insert into appointments (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, status) values (%s, %s, %s, %s, %s, %s)", (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, "Scheduled"))
        #timeInput = zampy.choose_time()
        appointDateTimeFormat = datetime.strptime(appointmentTime, "%H:%M").time() 
        #check if the patient has another appointment at chosen time
        todayStr = str(datetime.today().date())
        if appointmentDate >= todayStr: #check if the appointmentDate is today. If it is, 
            if appointmentDate == todayStr:
                #print("appointmentdate chosen was today!")
                log("appointmentdate chosen was today!")
                #ensure time doesnt overlap.
                if appointDateTimeFormat > datetime.now().time(): #check if its not in the past of today.
                    c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                    potentialPatientAlreadyHasAppointment = c.fetchall()
                    if len(potentialPatientAlreadyHasAppointment) > 0:
                        print("You already have an appointment at that time!")
                        log(f"You already have an appointment at that time: {potentialPatientAlreadyHasAppointment}")
                    else:
                        #check if doctor has another appointment at chosen time
                        c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and '{date.today().isoformat()}' = appointmentDate")
                        potentialDoctorBusy = c.fetchall()
                        if len(potentialDoctorBusy) > 0:
                            print("Sorry! The doctor is busy at that time. Please try another time.")
                            log(f"Doctor already has appointment at that time: {convertTime(potentialDoctorBusy)}")
                        else:
                            add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                            if debug:
                                print("Succeeded in making appointment!")
                                log('Succeeded in making appointment!')
                else:
                    print("Time cannot be chosen in the past.")
            elif appointmentDate > todayStr:
                print("appointmentdate chosen was after today!")
                #ensure time doesnt overlap.
                c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{appointmentDate}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                potentialPatientAlreadyHasAppointment = c.fetchall()
                if len(potentialPatientAlreadyHasAppointment) > 0:
                    print("You already have an appointment at that time!")
                else:
                    #check if doctor has another appointment at chosen time
                    c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = '{appointmentDate}'")
                    potentialDoctorBusy = c.fetchall()
                    #print("command: ", f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = '{appointmentDate}'")
                    #print("potentialDoctorBusy: ", potentialDoctorBusy)
                    if len(potentialDoctorBusy) > 0:
                        print("Sorry! The doctor is busy at that time. Please try another time.")
                    else:
                        add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                        if debug:
                            print("Succeeded in making appointment!")
                            log("Succeeded in making appointment!")
        else:
            print("Cant choose a date in the past!")
            
start_program()

def resetMenuOptions(current_user_type):
    all_options = ['View a patient\'s details',
                   'View a doctor\'s details', 
                   'Make an appointment', 
                   'Access medical history', 
                   'View prescriptions', 
                   'Access medical history of a patient',
                    'Access appointments panel', 
                    'View pending requests', 
                    'View table',
                    'Execute custom SQL command',
                    'Log out',
                    'Log in',
                    #'Edit data',
                    'Exit'] #also update own info, group doctors by specialization, view pending appointments
    options = ['View a patient\'s details' if current_user_type == "D" else None, 
               'View a doctor\'s details', 
               'Make an appointment' if current_user_type == "P" else None, 
               'Access medical history' if current_user_type == "P" else None, 
               'Access medical history of a patient' if current_user_type == "D" else None, 
               'View prescriptions', 
               'Access appointments panel' if current_user_type == "D" else None, 
               'View pending requests' if current_user_type == 'A' else None, 
               'View table' if current_user_type == 'A' else None,
               'Execute custom SQL command' if current_user_type == 'A' else None,
               #'Edit data' if current_user_type == 'A' else None,
               'Log out' if current_user_data != None else None,
               'Log in' if current_user_data == None else None,
               'Exit']
    options_menu_str, options_dict = zampy.make_menu_from_options(options, True)
    return all_options, options_menu_str, options_dict
all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
#Doctor's/Patients Panel
while True:
    if checkIfNonNull(current_user_data) == False or checkIfNonNull(current_user_type) == False:
        start_program()
    #    all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
    all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
    updateAppointments(current_user_type)
    print('Account:\t', current_user_data)
    log(f"Account used: {current_user_type}")
    print("Enter action: ")
    try:
        tempIndex = int(input(options_menu_str))
        action = options_dict[tempIndex]
    except ValueError:
        print("Enter data of correct data-type.")
    else:
        try:
            index = all_options.index(action)
        except Exception as e:
            print(f"Error occured:", e)
            log(f'Error occured while trying to read index: {e}')
        else:
            if index == 0:
                patientID = (input("Enter patient ID: "))
                data = viewPatientDetails(patientID)
                #print("Requested data:", data)
                makePrettyTable('patients', [data])
            elif index == 1:
                doctorID = (input("Enter doctor ID: "))
                data = viewDoctorDetails(doctorID)
                #print("Requested data:", data)
                makePrettyTable('doctors', [data])
            elif index == 2:
                #Make an appointment
                doctorID = input("Enter doctor ID to make appointment to: ")
                #appointmentDate = input("Enter date of appointment (Format: YYYY-MM-DD): ")
                appointmentDate = zampy.choose_date()
                appointmentTime = zampy.choose_time()

                appointmentReasonIndex = int(input(zampy.make_menu_from_options(['Check-up', 'Surgery', 'Physical Exam', 'Health Assessment'])))
                if appointmentReasonIndex == 1:
                    appointmentReason = "Check-up"
                elif appointmentReasonIndex == 2:
                    appointmentReason = "Surgery"
                elif appointmentReasonIndex == 3:
                    appointmentReason = 'Physical Exam'
                elif appointmentReasonIndex == 4:
                    appointmentReason = 'Health Assessment'
                makeAppointment(current_user_data[0], doctorID, appointmentDate, appointmentTime, appointmentReason)
            elif index == 3:
                historyOptions = ['Access using a recordID', 'Access your records by specific doctor (doctorID)', 'Access your history'] #add more options here
                historyIndex = int(input(zampy.make_menu_from_options(historyOptions)))
                current_patient_id = current_user_data[0]
                if historyIndex == 1:
                    recordID = (input("Enter recordID: "))
                    data = viewRecordDetails(current_patient_id, recordID=recordID)
                    #print(data)
                elif historyIndex == 2:
                    doctorID = (input("Enter doctor ID: "))
                    data = viewRecordDetails(current_patient_id, doctorID=doctorID)
                    #print(data)
                elif historyIndex == 3:
                    data = viewRecordDetails(current_patient_id, all=True)
                makePrettyTable('medicalhistory', data)
            elif index == 4:
                idOrAll = int(input(zampy.make_menu_from_options(['View all prescriptions', 'View by ID'])))
                if idOrAll == 1:
                    data = viewPrescriptions(all=True) #expand to finding by name, and id
                    #print(data)
                    #makePrettyTable('prescriptions', data)
                elif idOrAll == 2:
                    data = viewPrescriptions(all=False, pID=input("Enter prescription ID: "))
                makePrettyTable('prescriptions', data)
            elif index == 5:
                #Access medical history of a patient
                patientID = input("Enter patient ID: ")
                data = viewRecordDetails(patientID=patientID, all=True)
                makePrettyTable('medicalhistory', data)
            elif index == 6:
                #Access appointments history
                options = ['Upcoming appointments', 'Completed appointments']
                index = int(input(zampy.make_menu_from_options(options)))
                if index == 1:
                    c.execute("SELECT * FROM appointments WHERE doctorID = %s AND status = %s AND appointmentDate <= %s", (current_user_data[0], 'Scheduled', str(date.today().isoformat())))
                    data = c.fetchall()
                    #print(data) 
                    makePrettyTable('appointments', data)
                    # print(from_db_cursor(c))
                elif index == 2:
                    c.execute("SELECT * FROM medicalhistory WHERE doctorID = %s AND status = %s", (current_user_data[0], 'Completed'))
                    data = c.fetchall()
                    print(data)
                    makePrettyTable('medicalhistory', data)
                    # print(from_db_cursor(c))
            elif index == 7:
                dealWithPendingRequests()
            elif index == 8:
                #View table
                table_name = input("Enter table name to access: ")
                c.execute(f'select * from {table_name}')
                data = c.fetchall()
                #print(data)
                makePrettyTable(f'{table_name}', data)
            elif index == 9:
                #Execute custom SQL command
                sql_command = input("Enter sql command:\n")
                try:
                    c.execute(sql_command)
                    if 'select' in sql_command:
                        data = c.fetchall()
                        try:
                            tablename = sql_command.split(' ')[3]
                            makePrettyTable(tablename, data)
                        except Exception as e:
                            print("Couldn't make table from given data.")
                            log(f'Error while prettyTable: {e}')
                            print(data)
                except Exception as e:
                    print(f"Error while running command: {e}")
                    log(f"Error while running command: {e}")
                else:
                    print('No error in running command.')
                '''        elif index == 10:
                #Edit data
                table_name = input("Enter table name to access: ")
                table = c.execute(f"select * from {table_name}")
                if checkIfNonNull(table):
                    '''
            elif index == 10:
                #Log out
                current_user_data = None
                current_user_type = None
            elif index == 11:
                #Log in
                start_program()
            elif index == 12:
                print("Thank you for using this program.")
                exit()
            else:
                print("Something went wrong.")
                log(f"Unforeseen error when index was {index}.")