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

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")
c = database.cursor()
#c = database.cursor(buffered=True)

current_user_type = None
current_user_data = None

# Define the path to the local directory
directory = Path.home() / "HospitalManagement-PythonSQL"  # This creates a folder in the user's home directory

debug = True
# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define the login file path
login_file = directory / "creds.dat"

def checkPasswords(correct_password: str, name: str = "current user", usebcrypt = False) -> bool:
    print(f"Enter password for:\t {name}")
    inpPassword = getpass.getpass()
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
    number = int(text[1:]) + 1
    return text[0] + str(number)

def getHighestID(ordered_table):
    highestNum = 0
    #highestID = None
    for record in ordered_table:
        currentNum = int(record[0][1:])
        if currentNum > highestNum:
            highestNum = currentNum
    return ordered_table[0][0][0] + str(highestNum)  

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
                print("Details are:", existingPrescription)
                prescriptionID = existingPrescription[0]
    else:
        prescriptionID = incrementNumericPart(getHighestID(retreiveData('prescriptions')))
        dosage = input("Enter general dosage: ")
        add_value_to_table('prescriptions', ['prescriptionID', 'medication_name', 'dosage'], [prescriptionID, prescription, dosage])
    if returnPCID:
        return prescriptionID

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
                print(f"You have an appointment scheduled with Dr. {viewDoctorDetails(appointment[2])[1]} on {appointment[3]}")
        if len(appointmentsPendingToday) > 0:
            for appointment in appointmentsPendingToday:
                if appointment[6] not in [None, 'None', 'NULL']:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time < appointment_time:
                        print(f"You have an upcoming appointment at {appointment_time} with Dr. {viewDoctorDetails(appointment[2])[1]}")
                    #else:
                        #Check for whether the record with same date and time, patientID and doctorID was added to medicalhistory. 
                        #print(f"You missed an appointment that was scheduled for {appointment_time}")
                else:
                    print(f"Your appointment scheduled for {date.today()} was found to have no time assigned.\nChoose a time: ")
                    timeInput = zampy.choose_time()
                    timeDateTime = datetime.strptime(timeInput, "%H:%M").time()
                    flag = False
                    #check if the patient has another appointment at chosen time
                    if timeDateTime > datetime.now().time():
                        c.execute(f"select * from appointments where patientID = '{appointment[1]}' and appointmentTime = '{timeInput}'")
                        potentialPatientAlreadyOccupied = c.fetchall()
                        if len(potentialPatientAlreadyOccupied) == 0:
                            for appointment in appointmentsPendingToday:
                                if timeDateTime == datetime.strptime(appointment[6], '%H:%M').time():
                                    flag = True
                                    break
                            if not flag:
                            #check if doctor has another appointment at chosen time
                                c.execute(f"select * from appointments where doctorID = '{appointment[2]}' and appointmentTime = '{timeInput}'")
                                potentialDoctorBusy = c.fetchall()
                                if len(potentialDoctorBusy) > 0:
                                    print("Sorry! The doctor is busy at that time. Please try another time.")
                                else:
                                    c.execute(f"update appointments set appointmentTime = '{timeInput}' where LOWER(appointmentID) = '{appointment[0].lower()}'")
                                    database.commit()
                        else:
                            print("You already have an appointment at that time:", potentialPatientAlreadyOccupied[0])
                    else:
                        print("A time in the past cannot be chosen. Please choose an appropriate time.")

                    #c.execute("select * from appointments where patientID = '{}' and ")

        else:
            print("You have no appointments upcoming today.")
    elif current_user_type == "D":
        doctorID = current_user_data[0]
        c.execute(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and '{date.today().isoformat()}' <= appointmentDate")
        appointmentsPendingToday = c.fetchall()
        if len(appointmentsPendingToday) > 0:
            for appointment in appointmentsPendingToday:
                if appointment[6] not in [None, 'None', 'NULL']:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time < appointment_time:
                        print(f"You have an upcoming appointment at {appointment_time} with {viewPatientDetails(appointment[1])[1]}")
        else:
            print("No upcoming appointments.")
        #print(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and {date.today().isoformat()} >= appointmentDate")
        c.execute(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and '{date.today().isoformat()}' >= appointmentDate")
        assumedDoneAppointments = c.fetchall()
        doneAppointments = []
        for assumedAppointment in assumedDoneAppointments:
            if appointment[6] not in [None, 'None', 'NULL']:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time > appointment_time:
                        doneAppointments.append(assumedAppointment)
        print('doneAppointments', doneAppointments)
        if len(doneAppointments) > 0:
            if debug:
                print(len(doneAppointments), "completed appointments were found in appointments table. attempting to move them to medicalhistory...")
            for appointment in doneAppointments:
                patientID = appointment[1]
                patientName = viewPatientDetails(patientID)[1]
                print(f"Has the appointment scheduled with {patientName} been completed?")
                choice = int(input(zampy.make_menu_from_options()))
                if choice == 1:
                    diagnosis = input("Enter diagnosis: ")
                    prescriptionID = input("Enter prescriptionID: ") #check if it exists. if it doesnt make a new one and then reference it.
                    print(f"Is this the prescription: {viewPrescriptions(prescriptionID,False)}?")
                    confirm = int(input(zampy.make_menu_from_options()))
                    if confirm == 1:
                        #log into medical history
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [incrementNumericPart(getHighestID(retreiveData('medicalhistory'))), patientID, doctorID, appointment[3], appointment[6], diagnosis, prescriptionID, 'Completed'])
                        #delete from appointments.

                    else:
                        print("Attempting to make a new prescription...")
                        pcID = makeNewPrescription()
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [incrementNumericPart(getHighestID(retreiveData('medicalhistory'))), patientID, doctorID, appointment[3], appointment[6], diagnosis, pcID, 'Completed'])
                        #delete from appointments.

                        #make a new prescription here!
                    c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                    database.commit()
                else:
                    print("Was the appointment cancelled?")
                    choice = int(input(zampy.make_menu_from_options()))
                    if choice == 1:
                        #log into medical history, 
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [incrementNumericPart(getHighestID(retreiveData('medicalhistory'))), patientID, doctorID, appointment[3], appointment[6], 'NULL', 'NULL','Cancelled']) 
                        #delete from appointments.
                        c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                        database.commit()
                    #delay mechanism?
                    
def start_program():
    global current_user_type
    global current_user_data

    try:
        bfile = open(login_file, "rb")
        bfilecontents = pickle.load(bfile)
        found_user_type = bfilecontents[0]
        found_user_data = bfilecontents[1]
        found_user_password = bfilecontents[2]
    except Exception as e:
        print("Some error occured while trying to access existing login-file:", e)
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

            print("Updated patients table\n", confirm_data)

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
            print("Updated doctors table\n", confirm_data)

            #c.execute(f"select * from doctors where doctorID = '{new_doctor_data[0]}'")
            #current_user_data = c.fetchone()

            current_user_data = retreiveData("doctors", allColumns=True, conditionNames=['DoctorID'], conditionValues=[new_doctor_data[0]], returnAllData=False)


            bfile = open(login_file, "wb")
            pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)

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

    try:
        c.execute(command)
    except Exception as e:
        print("Error while trying to retrieve data:", e)
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
            appointmentID = f"{incrementNumericPart(getHighestID(retreiveData('appointments')))}"
        
        #c.execute(f"insert into appointments (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, status) values (%s, %s, %s, %s, %s, %s)", (appointmentID, patientID, doctorID, appointmentDate, appointmentReason, "Scheduled"))
        #timeInput = zampy.choose_time()
        appointDateTimeFormat = datetime.strptime(appointmentTime, "%H:%M").time() 
        #check if the patient has another appointment at chosen time
        todayStr = str(datetime.today().date())
        if appointmentDate >= todayStr: #check if the appointmentDate is today. If it is, 
            if appointmentDate == todayStr:
                print("appointmentdate chosen was today!")
                #ensure time doesnt overlap.
                if appointDateTimeFormat > datetime.now().time(): #check if its not in the past
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
                            add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                            if debug:
                                print("Succeeded in making appointment!")
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
                    c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = {appointmentDate}")
                    potentialDoctorBusy = c.fetchall()
                    print("command: ", f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = '{appointmentDate}'")
                    print("potentialDoctorBusy: ", potentialDoctorBusy)
                    if len(potentialDoctorBusy) > 0:
                        print("Sorry! The doctor is busy at that time. Please try another time.")
                    else:
                        add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                        if debug:
                            print("Succeeded in making appointment!")
        else:
            print("Cant choose a date in the past!")


start_program()

def resetMenuOptions(current_user_type):
    all_options = ['View a patient\'s details', 'View a doctor\'s details', 'Make an appointment', 'Access medical history', 'View prescriptions', 'Access medical history of a patient', 'Access appointments panel', 'Exit'] #also update own info, group doctors by specialization, view pending appointments
    options = ['View a patient\'s details' if current_user_type == "D" else None, 'View a doctor\'s details', 'Make an appointment' if current_user_type == "P" else None, 'Access medical history' if current_user_type == "P" else None, 'Access medical history of a patient' if current_user_type == "D" else None, 'View prescriptions', 'Access appointments panel' if current_user_type == "D" else None, 'Exit']
    options_menu_str, options_dict = zampy.make_menu_from_options(options, True)
    return all_options, options_menu_str, options_dict
all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
#Doctor's/Patients Panel
while True:
    if current_user_data == None:
        start_program()
    #    all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
    all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
    updateAppointments(current_user_type)
    print('Account:\t', current_user_data)
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
                print(data)
            elif historyIndex == 2:
                doctorID = (input("Enter doctor ID: "))
                data = viewRecordDetails(current_patient_id, doctorID=doctorID)
                print(data)
            elif historyIndex == 3:
                data = viewRecordDetails(current_patient_id, all=True)
                print(data)
        elif index == 4:
            idOrAll = int(input(zampy.make_menu_from_options(['View all prescriptions', 'View by ID'])))
            if idOrAll == 1:
                data = viewPrescriptions(all=True) #expand to finding by name, and id
                print(data)
            elif idOrAll == 2:
                data = viewPrescriptions(all=False, pID=input("Enter prescription ID: "))
        elif index == 5:
            #Access medical history of a patient
            patientID = input("Enter patient ID: ")
            data = viewRecordDetails(patientID=patientID, all=True)
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
        elif index == 7:
            print("Thank you for using this program.")
            exit()
        else:
            print("Something went wrong.")