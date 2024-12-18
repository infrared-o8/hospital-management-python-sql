import mysql.connector #sql
from datetime import datetime, date #utilities
import zampy
from prettytable.colortable import ColorTable
import pickle #utilities
import bcrypt #password
import os #login_file destination
from pathlib import Path #login_file destination
import getpass #password
from termcolor import colored, cprint #text 
from colorama import init #text
import pyfiglet #text
import time
from tqdm import tqdm #progress bar
from halo import Halo

current_user_type = None
current_user_data = None

request_sign_up = "Request to Sign Up"
# Define the path to the local directory
directory = Path.home() / "HospitalManagement-PythonSQL"  # This creates a folder in the user's home directory

debug = False

os.makedirs(directory, exist_ok=True)

login_file = directory / "creds.dat"
log_file = directory / 'log.txt'
sql_creds = directory / 'sqlcreds.dat'

spinnerType = 'dots'


MESSAGE_STYLES = {
    'success': {'symbol': '✅', 'color': 'light_green'},
    'error': {'symbol': '❌', 'color': 'light_red'},
    'ask': {'symbol': '🟡', 'color': 'yellow'},
    'fatalerror': {'symbol': '💀', 'color': 'red'},
    'preheader': {'symbol': '🟡', 'color': 'white'},
    'info': {'symbol': 'ℹ️', 'color': 'light_blue'},
    'debug': {'symbol': '🐞', 'color': 'magenta'}
}

def slow_print(message, color, delay=0.01785, end=False):
    for char in message:
        #sys.stdout.write(char)
        #sys.stdout.flush()
        cprint(char, color=color, end='')
        time.sleep(delay)
    if not end:
        print()

def colorify(message, type='info', end=False):
    style = MESSAGE_STYLES.get(type, {'symbol': '❔', 'color': 'white'})
    symbol = style['symbol']
    color = style['color']
    if 'success' in message.lower() or 'succes' in message.lower():
        type = 'success'
    if end == False:
        slow_print(f"[{symbol}]\t{message}", color, end=False)
    else:
        slow_print(f"[{symbol}]\t{message}", color, end=True)

def cinput(prompt: str = 'Input: ', datatype = 'str'):
    while True:
        try:
            if datatype == 'int':
                data = int(input(prompt))
            else:
                data = input(prompt)
            return data
        except ValueError:
            colorify(f'Please input data of correct data type. {datatype} was expected.', 'error')
        except Exception as e:
            colorify(f'Error while trying to read input: {e}', 'error')

def vanilla_sql_login():
    userinp = cinput('Enter SQL username: ')
    userpassword = cinput("Enter SQL password: ")
    colorify('Store SQL credentials?')
    storeInFile = cinput(zampy.make_menu_from_options(), 'int')

    if storeInFile == 1:
        file = open(sql_creds, 'wb')
        data = [userinp, userpassword]
        pickle.dump(data, file)
        file.close()
    return userinp, userpassword

userinp, userpassword = None, None

try:
    file = open(sql_creds, 'rb')
except FileNotFoundError:
    colorify('SQL creds file not found.', 'error')
    userinp, userpassword = vanilla_sql_login()
else:
    data = pickle.load(file)
    userinp, userpassword = data[0], data[1]

database = mysql.connector.connect(host="localhost", user = userinp, password=userpassword)
if database.is_connected():
    colorify('Succesfully established connection to SQL.', 'success')

c = database.cursor(buffered=True)
with Halo(text='Attempting to use hospital_main...', spinner=spinnerType):
    try:
        c.execute('use hospital_main;')
    except mysql.connector.errors.ProgrammingError:
        #database doesnt exist. create one
        c.execute('CREATE database hospital_main;')
        c.execute('USE hospital_main;')

        #creating all tables.
        c.execute("""CREATE TABLE `admin_requests` (
        `requestID` varchar(10) NOT NULL,
        `requestReason` varchar(50) DEFAULT NULL,
        `signUpRequestName` varchar(30) DEFAULT NULL,
        PRIMARY KEY (`requestID`)
        )""")

        c.execute("""CREATE TABLE `admins` (
    `adminID` varchar(10) NOT NULL,
    `adminName` varchar(50) DEFAULT NULL,
    `emailID` varchar(45) DEFAULT NULL,
    PRIMARY KEY (`adminID`)
    )""")

        c.execute("""CREATE TABLE `appointments` (
    `appointmentID` varchar(15) NOT NULL,
    `patientID` varchar(15) DEFAULT NULL,
    `doctorID` varchar(15) DEFAULT NULL,
    `appointmentDate` date DEFAULT NULL,
    `appointmentReason` varchar(150) DEFAULT NULL,
    `status` varchar(30) DEFAULT NULL,
    `appointmentTime` varchar(9) DEFAULT NULL,
    PRIMARY KEY (`appointmentID`)
    )""")
        
        c.execute("""CREATE TABLE `credentials` (
    `userid` varchar(30) NOT NULL,
    `password` varchar(50) DEFAULT NULL,
    PRIMARY KEY (`userid`)
    )""")
        
        c.execute("""CREATE TABLE `doctors` (
    `DoctorID` varchar(10) NOT NULL,
    `Name` varchar(50) DEFAULT NULL,
    `Specialization` varchar(30) DEFAULT NULL,
    `Phone` int DEFAULT NULL,
    `ConsultationFee` int DEFAULT NULL,
    PRIMARY KEY (`DoctorID`)
    )""")
        
        c.execute("""CREATE TABLE `medicalhistory` (
    `recordID` varchar(30) NOT NULL,
    `patientID` varchar(30) DEFAULT NULL,
    `doctorID` varchar(30) DEFAULT NULL,
    `visitDate` date DEFAULT NULL,
    `diagnosis` varchar(300) DEFAULT NULL,
    `prescriptionID` varchar(20) DEFAULT NULL,
    `status` varchar(20) DEFAULT NULL,
    `time` varchar(9) DEFAULT NULL,
    PRIMARY KEY (`recordID`)
    )""")
        
        c.execute("""CREATE TABLE `patients` (
    `PatientID` varchar(10) NOT NULL,
    `Name` varchar(50) DEFAULT NULL,
    `Gender` char(1) DEFAULT NULL,
    `DOB` date DEFAULT NULL,
    `Phone` int DEFAULT NULL,
    PRIMARY KEY (`PatientID`)
    )""")
        
        c.execute("""CREATE TABLE `prescriptions` (
    `prescriptionID` varchar(20) NOT NULL,
    `medication_name` varchar(30) DEFAULT NULL,
    `dosage` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`prescriptionID`)
    )""")
        
        c.execute('INSERT INTO admins values ("ADM1", "admin1", "admin1@xyz.com")')
        c.execute('INSERT INTO credentials values ("ADM1", "admin")')
    
database.database = 'hospital_main'

message_types = ['success', 'error', 'ask', 'fatalerror', 
                 'preheader', 'info', 'debug']

init(autoreset=True)

months = {1: 'Jan', 2: 'Feb', 3:'Mar', 4:'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}



def friendlyYear(yeariso: str, convertMD: bool = False) -> str:
    split = str(yeariso).split('-')
    year, month, day = split[0], split[1], split[2]
    if convertMD:
        return f"{day} {months[int(month)]} {year}"
    return f"{day}/{month}/{year}"



def print_header(header_text: str = "Table"):
    print(colored(f"{'*'*10} {header_text.upper()} {'*'*10}", 'yellow', attrs=['bold', 'reverse']))

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



def fetchTableNameFromUserType(current_user_type):
    tablename = None
    if current_user_type == 'P':
        tablename = 'patients'
    elif current_user_type == 'D':
        tablename = 'doctors'
    elif current_user_type == 'A':
        tablename = 'admins'
    id = tablename[:-1] + 'ID'
    return tablename, id

def checkIfNonNull(variable):
    '''If null, returns False.'''
    if variable in [None, 'None', 'NULL', 'Null', (None,), ('NULL',), (), '', [], {}]:
        if debug:
            colorify(f"{variable} was null.", 'debug')
        return False
    else:
        return True

def returnNewID(tableName):
    return incrementNumericPart(getHighestID(retreiveData(tableName), tableName))

def fetchAccountInfo(requiredID, current_user_type):
    with Halo(text='Retrieving data...', spinner=spinnerType):
        tablename, id = fetchTableNameFromUserType(current_user_type)

        c.execute(f'select * from {tablename} where {id} = "{requiredID}"')
        return c.fetchone()

def fetchColumns(tableName):
    '''Returns column names from the given tableName.'''
    if checkIfNonNull(tableName) == True:
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute(f'select * from {tableName}')
            #columnNames = c.fetchall()
            sampleData = c.fetchall()
        del sampleData
        columnNames = [desc[0] for desc in c.description]
        return columnNames
    else:
        return None

def returnOrderedTableFromTableName(tableName: str):
    c.execute(f"select * from {tableName} ORDER BY {tableName[:len(tableName)-1]+'ID'}")
    return c.fetchall()

def makePrettyTable(tableName, data, makeHeader: bool = True):
    # fetch column names for the table
    #c.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{tableName}'")
    columnNames = fetchColumns(tableName)
    if checkIfNonNull(columnNames) == False:
        return
    #create PrettyTable with the column names
    if data and checkIfNonNull(data) == True:
        if makeHeader == True:
            if tableName.endswith(';'):
                print_header(tableName[:-1])
            else:
                print_header(tableName)
        if debug:
            colorify(f'{[columnNames[x] for x in range(len(columnNames))]}', 'debug')
        table = ColorTable([columnNames[x] for x in range(len(columnNames))])
        #table.sortby = None
        #table.border = True
        #table.hrules = FRAME  # Add horizontal rules
        #table.vrules = ALL    # Add vertical rules
        #print data for debugging purposes
        if debug:
            colorify(f'data in makePrettyTable: {data}', 'debug')
        
        #check if data is a single row (tuple or list) or multiple rows (list of tuples/lists)
        try:
            if isinstance(data[0], (tuple, list)):  # Multiple rows case (list of lists/tuples)
                table.add_rows([x for x in data])
            else:  #single row case (tuple or list)
                table.add_row([x for x in data])
        except Exception as e:
            colorify('Error while trying to display table.', 'error')
            if debug:
                colorify(f'Error while displaying table: {e}', 'error')
            log(f'Error while displaying table: {e}')
        # raw display the table
        print(table)
    

def viewPendingRequests():
    global current_user_data, current_user_type
    if current_user_type == 'A': #confirm its an admin
        #all signup requests.
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute(f'select * from admin_requests where requestReason = \'{request_sign_up}\'')
            signUpRequests = c.fetchall()
        if len(signUpRequests) > 0:
            colorify('Pending signup requests:\n', 'preheader')
            makePrettyTable('admin_requests', signUpRequests)
        return signUpRequests

def dealWithPendingRequests():
    signupReq = viewPendingRequests()
    for req in signupReq:
        name = req[2]
        id = returnNewID('admins')
        colorify(f"Approve pending sign-up of {name} as admin:", 'ask')
        choice = cinput(zampy.make_menu_from_options(), 'int')
        if choice == 1:
            #delete from admin_requests
            c.execute(f'delete from admin_requests where requestID = "{req[0]}";')
            database.commit()
            #add new user to credentials and admin table
            add_value_to_table('admins', ['adminID', 'adminName'], [id, name])
            add_value_to_table('credentials', ['userID'], [id])
        else:
            c.execute(f'delete from admin_requests where requestID = "{req[0]}";')
            database.commit()
            continue

def log(text):
    file = None
    try:
        file = open(log_file, 'a')
    except Exception as e:
        colorify(f"Error while trying to open log_file: {e}", 'error')
        file = open(log_file, "w")
    file.write(f'{str(datetime.now())}: {text}\n')

def askForPassword(name: str = "current user"):
    colorify(f"Enter password for:\t {name}", 'ask')
    inpPassword = getpass.getpass()
    return inpPassword

def checkPasswords(correct_password: str, name: str = "current user", usebcrypt = False) -> bool:
    '''Asks for a password, and checks it against correct_password. If name is provided, input() will display name.'''
    inpPassword = askForPassword(name)
    if usebcrypt:
        if bcrypt.checkpw(inpPassword.encode('utf-8'), correct_password):
            return True
    else:
        if correct_password == inpPassword:
            return True
    return False

def incorrectPassword():
    colorify("Incorrect password!", 'fatalerror')

def incrementNumericPart(text):
    number = (text[1:])
    x = 0
    while not number.isnumeric():
        x += 1
        number = (text[1+x:])
    number = int(number) + 1
    return text[0:1+x] + str(number)

def getHighestID(ordered_table, table_name):
    highestNum = 0
    if checkIfNonNull(ordered_table) == True:
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
    else:
        return table_name[0].upper() + "1"

def makeNewPrescription(returnPCID = True):
    prescription = cinput("Enter prescription name: ")
    prescriptionID = None
    #check if it already exists
    with Halo(text='Retrieving data...', spinner=spinnerType):
        c.execute(f"select * from prescriptions where medication_name = '{prescription}'")
        existingPrescriptions = c.fetchall()
    if len(existingPrescriptions) > 0:
        #exists already!
        colorify(f"A prescription already recorded with the same name was found.\n", 'info')
        for existingPrescription in existingPrescriptions:
            if existingPrescription[1] == prescription:
                colorify("Details are:\n", 'info')
                makePrettyTable('prescriptions', existingPrescription)
                prescriptionID = existingPrescription[0]
    else:
        data = retreiveData('prescriptions')
        prescriptionID = None
        if zampy.checkEmpty(data):
            prescriptionID = "PRC1"
        else:
            prescriptionID = f"{returnNewID('prescriptions')}"
        #prescriptionID = returnNewID('prescriptions')
        dosage = cinput("Enter general dosage: ")
        add_value_to_table('prescriptions', ['prescriptionID', 'medication_name', 'dosage'], [prescriptionID, prescription, dosage])
        log(f'New prescription added with: {[prescriptionID, prescription, dosage]}')
    if returnPCID:
        return prescriptionID

def requestExistingAdminToSignUp(adminName):
    #c.execute(f"insert into admin_requests values('{}', 'Request to Sign Up', ')")
    with Halo(text='Retrieving data...', spinner=spinnerType):
        c.execute('select * from admin_requests')
        ordered_table = c.fetchall()
    new_request_id = ''
    if len(ordered_table) > 0:
        new_request_id = f"{returnNewID('admin_requests')}" 
    else:
        new_request_id = 'REQ1'
    add_value_to_table('admin_requests', ['requestID', 'requestReason', 'signUpRequestName'], [new_request_id, request_sign_up, adminName])
    colorify(f'Successfully requested for the sign-up of {adminName}', 'success')
def updateAppointments(current_user_type):
    global current_user_data
    if current_user_type == "P":
        #appointmentsPending = retreiveData('appointments', conditionNames=['patientID'], conditionValues=[current_user_data[0]])
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate")
            appointmentsPendingToday = c.fetchall()
            c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' < appointmentDate")
            appointmentsPendingLater = c.fetchall()

        if len(appointmentsPendingLater) > 0:
            colorify(f"You have an appointment scheduled with: ", 'info')
            for appointment in appointmentsPendingLater:
                colorify(f"\t\tDr. {viewDoctorDetails(appointment[2])[1]} on {friendlyYear(appointment[3], convertMD=True)} at {convertTime(appointment[-1])}", 'info')
                #else:
                #    colorify(f"You have an appointment scheduled with Dr. {viewDoctorDetails(appointment[2])[1]} on {friendlyYear(appointment[3], convertMD=True)} at {convertTime(appointment[-1])}", 'info')
        if len(appointmentsPendingToday) > 0:
            for appointment in appointmentsPendingToday:
                if checkIfNonNull(appointment[6]) == True:
                    appointment_time = datetime.strptime(appointment[6], '%H:%M').time()  # Convert to time object
                    
                    # Get the current time
                    current_time = datetime.now().time()
                    
                    # Compare the times
                    if current_time < appointment_time:
                        colorify(f"You have an upcoming appointment at {convertTime(appointment_time)} with Dr. {viewDoctorDetails(appointment[2])[1]}", 'info')
                    else:
                        #Check for whether the record with same date and time, patientID and doctorID was added to medicalhistory. 
                        #missedRecordConfirm = retreiveData('medicalhistory', conditionNames=['patientID', 'doctorID', 'visitDate', 'time'], conditionValues=[current_user_data[0], appointment[2], str(date.today().isoformat()), appointment_time])
                        c.execute(f"select * from medicalhistory where patientID = '{current_user_data[0]}' and doctorID = '{appointment[2]}' and visitDate = '{date.today().isoformat()}' and time = '{appointment_time}'")
                        missedRecordConfirm = c.fetchall()
                        if checkIfNonNull(missedRecordConfirm) == True:
                            if len(missedRecordConfirm) > 0:
                                colorify(f"You missed an appointment that was scheduled for {convertTime(appointment_time)}", 'error')
                                log(f'{current_user_data[1]} missed an appointment: {missedRecordConfirm}')
                else:
                    colorify(f"Your appointment scheduled for {date.today()} with {viewDoctorDetails(appointment[2])[1]} was found to have no time assigned.\nChoose a time: ", 'ask')
                    timeInput = zampy.choose_time()
                    timeDateTime = datetime.strptime(timeInput, "%H:%M").time()
                    #check if the patient has another appointment at chosen time
                    #ensure time doesnt overlap.
                    if timeDateTime > datetime.now().time(): #check if its not in the past
                        #with Halo(text='Retrieving data...', spinner=spinnerType):
                        c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                        potentialPatientAlreadyHasAppointment = c.fetchall()
                        if len(potentialPatientAlreadyHasAppointment) > 0:
                            colorify("You already have an appointment at that time!", 'error')
                        else:
                            #check if doctor has another appointment at chosen time
                            c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}'")
                            potentialDoctorBusy = c.fetchall()
                            if len(potentialDoctorBusy) > 0:
                                colorify("Sorry! The doctor is busy at that time. Please try another time.", 'error')
                            else:
                                add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointment[0], patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                                if debug:
                                    log("Succeeded in making appointment!")
                                colorify("Succeeded in making appointment!", 'success')
                    else:
                        colorify("Time cannot be chosen in the past.", 'error')
        else:
            colorify("You have no appointments upcoming today.", 'info')
    elif current_user_type == "D":
        if current_user_data:
            doctorID = current_user_data[0]
        with Halo(text='Retrieving data...', spinner=spinnerType):
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
                        colorify(f"You have an upcoming appointment at {convertTime(appointment_time)} with {viewPatientDetails(appointment[1])[1]}", 'info')
        else:
            colorify("No upcoming appointments today.", 'info')
        #print(f"select * from appointments where LOWER(doctorID) = '{doctorID.lower()}' and {date.today().isoformat()} >= appointmentDate")
        with Halo(text='Retrieving data...', spinner=spinnerType):
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
                colorify(f"{len(doneAppointments)} completed appointments found in appointments table. attempting to move them to medicalhistory...", 'debug')
                log(f"{len(doneAppointments), } completed appointments found in appointments table. attempting to move them to medicalhistory...")
            for appointment in doneAppointments:
                patientID = appointment[1]
                patientName = viewPatientDetails(patientID)[1]
                colorify(f"Has the appointment scheduled with {patientName} been completed?", 'ask')
                choice = cinput(zampy.make_menu_from_options(), 'int')
                if choice == 1:
                    diagnosis = cinput("Enter diagnosis: ")
                    prescriptionID = cinput("Enter prescriptionID: ")
                    colorify(f"Is this the prescription: {viewPrescriptions(prescriptionID,False)}?", 'ask')
                    confirm = cinput(zampy.make_menu_from_options(), 'int')
                    if confirm == 1:
                        #log into medical history
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], diagnosis, prescriptionID, 'Completed'])
                        #delete from appointments.

                    else:
                        if debug:
                            colorify("Attempting to make a new prescription...", 'debug')
                            log(f"Attempting to make a new prescription.")
                        pcID = makeNewPrescription()
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], diagnosis, pcID, 'Completed'])
                        #delete from appointments.

                        #make a new prescription here!
                    c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                    database.commit()
                else:
                    colorify("Was the appointment cancelled?", 'ask')
                    choice = cinput(zampy.make_menu_from_options(), 'int')
                    if choice == 1:
                        #log into medical history, 
                        add_value_to_table('medicalhistory', ['recordID', 'patientID', 'doctorID', 'visitDate', 'time', 'diagnosis', 'prescriptionID', 'status'], [returnNewID('medicalhistory'), patientID, doctorID, appointment[3], appointment[6], 'NULL', 'NULL','Cancelled']) 
                        #delete from appointments.
                        c.execute(f"delete from appointments where LOWER(appointmentID) = '{appointment[0].lower()}'")
                        database.commit()
                    #delay mechanism?

def vanilla_login():
    global current_user_data
    global current_user_type
    try:
        colorify("Using as:\n", 'ask')
        user = cinput(zampy.make_menu_from_options(['Patient', 'Doctor', 'Admin']), 'int')
        if user == 1:
            #logging in as patient
            current_user_type = 'P'
        elif user == 2:
            #logging in as doctor
            current_user_type = 'D'
        elif user == 3:
            current_user_type = 'A'
        else:
            colorify("Something went wrong. Try again...\n", 'error')
            start_program()
    except ValueError:
        colorify("Input was of incorrect datatype. Try again...\n", 'error')
        start_program()
    else:
        if checkIfNonNull(current_user_data) == False:
            attain_creds(current_user_type)

def start_program():
    global current_user_type
    global current_user_data
    try:
        bfile = open(login_file, "rb")
        bfilecontents = pickle.load(bfile)
        found_user_type = bfilecontents[0]
        found_user_data = bfilecontents[1]
        found_user_password = bfilecontents[2]
    except FileNotFoundError:
        colorify('The login-file was not found. Proceeding to normal login...', 'error')
        vanilla_login()
        return None
    except Exception as e:
        colorify(f"Some error occured while trying to access login file.", 'error')
        if debug:
            colorify(f"Some error occured while trying to access login file: {e}", 'error')
        log(f"Some error occured while trying to access existing login-file: {e}.\nProceeding to normal login.")
        colorify("Proceeding to normal login...", 'error')
        vanilla_login()
        return None
    else:
        id = bfilecontents[1][0]
        try:
            nameInfo = fetchAccountInfo(id, str(found_user_type))
            if checkIfNonNull(nameInfo) == True:
                name = nameInfo[1]
            else:
                colorify('Login file found invalid credentials. Proceeding to normal login...', 'fatalerror')
                vanilla_login()
                return None
        except Exception as e:
            colorify(f'Error occured while trying to read login file: {e}. Continuing to normal login...', 'error')
            log(f"Some error occured while trying to access existing login-file: {e}.\nProceeding to normal login.")
            vanilla_login()
            return None
        colorify(f"Found an existing login file for {name}. Confirm login with these credentials?", 'ask')
        confirmLogin = cinput(zampy.make_menu_from_options(), 'int')
        if confirmLogin == 1:
            #print("found)user_password", found_user_password)
            if checkPasswords(found_user_password, name, usebcrypt=True):
                current_user_type = bfilecontents[0]
                found_id = bfilecontents[1][0]

                current_user_data = fetchAccountInfo(found_id, str(current_user_type))

                colorify(f"Succesfully logged in as {current_user_data[1]}.", 'success') #Succesfully logged in as zeeman4
                
            else:
                incorrectPassword()
        else:
            vanilla_login()



def make_new_record(ordered_table, name, usertype):
        global current_user_data
        global current_user_type
        if usertype == "P":
            data = retreiveData('patients')
            new_patient_id = None
            if zampy.checkEmpty(data):
                new_patient_id = "P1"
            else:
                new_patient_id = f"{returnNewID('patients')}"
            new_patient_data = [new_patient_id, name]
            colorify("Type a new ", 'ask',end=True)
            new_p = getpass.getpass()
            new_p_bytes = new_p.encode('utf-8')
            add_value_to_table("credentials", ['userid', 'password'], [new_patient_id, new_p])
            add_value_to_table("patients", ['PatientID', 'Name'], new_patient_data)

            confirm_data = retreiveData('patients', allColumns=True)
            if debug:
                colorify(f"Updated patients table: {confirm_data}")
            log(f"Updated patients table: {confirm_data}")

            current_user_data = retreiveData("patients", allColumns=True, conditionNames=['PatientID'], conditionValues=[new_patient_data[0]], returnAllData=False)
            colorify('One time login?', 'ask')
            onetimelogin = cinput(zampy.make_menu_from_options(), 'int')
            if onetimelogin == 2:
                bfile = open(login_file, "wb")
                pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)
        elif usertype == "D":
            new_doctor_id = f"{incrementNumericPart(getHighestID(ordered_table, 'doctors'))}"
            new_doctor_data = [new_doctor_id, name]

            #c.execute("INSERT into doctors (doctorID, Name) values (%s, %s)", new_doctor_data)
            #database.commit()
            colorify("Type a new ", 'ask',end=True)
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

            colorify('One time login?', 'ask')
            onetimelogin = cinput(zampy.make_menu_from_options(), 'int')
            if onetimelogin == 2:
                bfile = open(login_file, "wb")
                pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(new_p_bytes, bcrypt.gensalt())], bfile)

def signup(user_type):
    global current_user_data
    #get required info
    if user_type == "P":
        patient_name = cinput("Enter patient name: ")
        #check if it already exists in patients table.
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute('select * FROM patients ORDER BY PatientID') ##orderby functionality here!
            ordered_patient_table = c.fetchall()

        #ordered_patient_table = retreiveData("patients", )

        (pExists, patient_record) = zampy.check_record_exists(patient_name, 1, ordered_patient_table)
        if pExists:
            colorify(f"Username already exists with patient data: {patient_record}!", 'error') #add column names - !!
            confirm = cinput("Do you confirm this is your data? (Y/N): ") #add password protection here
            if confirm in 'Yy':
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[patient_record[0]], returnAllData=False)
                password = password[0]
                if checkPasswords(password, patient_record[1]):
                    current_user_data = patient_record
                    colorify(f"Succesfully logged in as {current_user_data[1]}", 'success')
                else:
                    incorrectPassword()
            else:
                colorify("Would you like to create a new account with this name?", 'ask')
                choice = cinput(zampy.make_menu_from_options(), 'int')
                if choice == 1:
                    make_new_record(ordered_patient_table, patient_name, user_type)
        else:
            colorify("Patient record doesn't exist! Making new record...", 'info')
            #doesnt exist, make a new record.
            make_new_record(ordered_patient_table, patient_name, user_type)
    elif user_type == "D":
        doctor_name = cinput("Enter doctor name: ")
        #check if it already exists in doctors table.
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute('select * FROM doctors ORDER BY DoctorID') ##orderby functionality here!
            ordered_doctor_table = c.fetchall()
        (dExists, doctor_record) = zampy.check_record_exists(doctor_name, 1, ordered_doctor_table)
        if dExists:
            colorify(f"Username already exists with doctor data: {doctor_record}!", 'error') #add column names - !!
            confirm = cinput("Do you confirm this is your data? (Y/N): ")
            if confirm in 'Yy':
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[doctor_record[0]], returnAllData=False)
                password = password[0]
                if checkPasswords(password, doctor_record[1]):
                    current_user_data = doctor_record
                    colorify(f"Succesfully logged in as {current_user_data[1]}", 'success')
                else:
                    incorrectPassword()
            else:
                colorify("Would you like to create a new account with this name?", 'ask')
                choice = cinput(zampy.make_menu_from_options(), 'int')
                if choice == 1:
                    make_new_record(ordered_doctor_table, doctor_name, user_type)
        else:
            colorify("Doctor record doesn't exist! Making new record...", 'info')
            #doesnt exist, make a new record.
            make_new_record(ordered_doctor_table, doctor_name, user_type)
    elif user_type == 'A':
        admin_name = cinput("Enter admin name: ")
        #check if it already exists in doctors table.
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute('select * FROM admins ORDER BY adminID') ##orderby functionality here!
            ordered_admin_table = c.fetchall()
        (aExists, admin_record) = zampy.check_record_exists(admin_name, 1, ordered_admin_table)
        if aExists:
            colorify(f"Username already exists with admin data: {admin_record}!", 'error') #add column names - !!
            colorify("Do you confirm this is your data?", 'ask')
            confirm = cinput(zampy.make_menu_from_options(), 'int')
            if confirm == 1:
                password = retreiveData("credentials", columnNames=["password"], conditionNames=['userid'], conditionValues=[admin_record[0]], returnAllData=False)
                #print('password:', password)
                if password and checkIfNonNull(password) == True:
                    password = password[0]
                    if checkPasswords(password, admin_record[1]):
                        current_user_data = admin_record
                        colorify(f"Succesfully logged in as {current_user_data[1]}", 'success')
                    else:
                        incorrectPassword()
                else:
                    colorify("The user was found with no password. Enter new password?", 'ask')
                    choice = cinput(zampy.make_menu_from_options(), 'int')
                    if choice == 1:
                        colorify("Type a new ", 'ask',end=True)
                        newPassword = askForPassword()
                        while newPassword == None:
                            newPassword = askForPassword()
                        c.execute(f'update credentials set password = "{newPassword}" where userid = "{admin_record[0]}"')
                        database.commit()
                    else:
                        start_program()
            else:
                colorify("Would you like to create a new account with this name?", 'ask')
                choice = cinput(zampy.make_menu_from_options(), 'int')
                if choice == 1:
                    #make_new_record(ordered_admin_table, admin_name, user_type)
                    requestExistingAdminToSignUp(admin_name)
        else:
            colorify("Admin record doesn't exist! Making new record...", 'info')
            requestExistingAdminToSignUp(admin_name)

def login(user_type):
    global current_user_data
    global current_user_type
    if user_type == "P":
        requested_id = cinput("Enter patient ID: ")
        record = retreiveData("patients", conditionNames=['patientID'], conditionValues=[requested_id], returnAllData=False)
        if record is None:
            requSignUp = cinput("Requested ID doesnt exist. Sign up? (Y/N)")
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
                colorify(f"Succesfully logged in as {current_user_data[1]}.", 'success') #Succesfully logged in as zeeman4
                
                colorify('One time login?', 'ask')
                onetimelogin = cinput(zampy.make_menu_from_options(), 'int')
                if onetimelogin == 2:
                    bfile = open(login_file, "wb")
                    pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
            else:
                incorrectPassword()

    elif user_type == "D":
        requested_id = cinput("Enter doctor ID: ")
        #c.execute(f"select * from doctors where doctorid = '{requested_id}'")
        #record = c.fetchone()

        record = retreiveData("doctors", conditionNames=['doctorID'], conditionValues=[requested_id], returnAllData=False)


        if record is None:
            requSignUp = cinput("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup(user_type)
        else:
            cpassword = retreiveData('credentials', False, ['password'], ['userid'], [record[0]], returnAllData=False)
            cpassword = cpassword[0]
            cpasswordbytes = cpassword.encode('utf-8')
            if checkPasswords(cpassword, record[1]):
                current_user_data = record
                colorify(f"Succesfully logged in as {current_user_data[1]}", 'success')
                colorify('One time login?', 'ask')
                onetimelogin = cinput(zampy.make_menu_from_options(), 'int')
                if onetimelogin == 2:
                    bfile = open(login_file, "wb")
                    pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
            else:
                incorrectPassword()
    elif user_type == 'A':
        requested_id = cinput("Enter admin ID: ")
        record = retreiveData("admins", conditionNames=['adminID'], conditionValues=[requested_id], returnAllData=False)

        if record is None:
            requSignUp = cinput("Requested ID doesnt exist. Sign up? (Y/N)")
            if requSignUp in 'Yy':
                signup(user_type)
        else:
            cpassword = retreiveData('credentials', False, ['password'], ['userid'], [record[0]], returnAllData=False)
            if checkIfNonNull(cpassword) == True:
                cpassword = cpassword[0]
                if checkPasswords(cpassword, record[1]):
                    cpasswordbytes = cpassword.encode('utf-8')
                    current_user_data = record
                    colorify(f"Succesfully logged in as {current_user_data[1]}", 'success')
                    colorify('One time login?', 'ask')
                    onetimelogin = cinput(zampy.make_menu_from_options(), 'int')
                    if onetimelogin == 2:
                        bfile = open(login_file, "wb")
                        pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
                    #bfile = open(login_file, "wb")
                    #pickle.dump([current_user_type, current_user_data, bcrypt.hashpw(cpasswordbytes, bcrypt.gensalt())], bfile)
                else:
                    incorrectPassword()
            else:
                colorify("The user was found with no password. Enter new password?", 'ask')
                choice = cinput(zampy.make_menu_from_options(), 'int')
                if choice == 1:
                    newPassword = askForPassword()
                    while newPassword == None or newPassword == "":
                        newPassword = askForPassword()
                    c.execute(f'update credentials set password = "{newPassword}" where userid = "{record[0]}"')
                    database.commit()
                else:
                    start_program()

def attain_creds(currentUserType):
    if currentUserType == 'P':
        colorify("Log in or sign up as patient?", 'ask')
        useridentify = cinput(zampy.make_menu_from_options(['Sign up', 'Log in']), 'int')
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)
    elif currentUserType == 'D':
        colorify("Log in or sign up as doctor?", 'ask')
        useridentify = cinput(zampy.make_menu_from_options(['Sign up', 'Log in']), 'int')
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)
    elif current_user_type == 'A':
        colorify("Log in or sign up as admin?", 'ask')
        useridentify = cinput(zampy.make_menu_from_options(['Sign up', 'Log in']), 'int')
        if useridentify == 1:
            signup(current_user_type)
            
        elif useridentify == 2:
            login(current_user_type)

def viewPatientDetails(patientID):
    return retreiveData("patients", conditionNames=['patientID'], conditionValues=[patientID], returnAllData=False)

def viewDoctorDetails(doctorID):
    return retreiveData("doctors", conditionNames=['doctorID'], conditionValues=[doctorID], returnAllData=False)
    

def viewPrescriptions(pID = None, all = True):
    if all:
        return retreiveData("prescriptions", allColumns=True)
    else:
        if pID:
            return retreiveData("prescriptions", allColumns=True, returnAllData=False, conditionNames=['prescriptionID'], conditionValues=[pID])

def viewRecordDetails(patientID ,recordID = None, doctorID = None, all = False):
    if recordID:
        return retreiveData("medicalhistory", True, conditionNames=['recordID', 'patientID'], conditionValues=[recordID, patientID])
    if doctorID:
        return retreiveData("medicalhistory", True, conditionNames=['doctorID', 'patientID'], conditionValues=[doctorID, patientID])
    if all:
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
        colorify("Received no tableName.", 'error')
        #return None
    if debug:
        colorify(f"Final commmand: {command}", 'debug')
    log(f"Final commmand: {command}")

    try:
        with Halo(text='Retrieving data...', spinner=spinnerType):
            c.execute(command)
    except Exception as e:
        colorify(f"Error while trying to retrieve data: {e}",'debug')
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
                if debug:
                    colorify("appointmentdate chosen was today!", 'debug')
                log("appointmentdate chosen was today!")
                #ensure time doesnt overlap.
                if appointDateTimeFormat > datetime.now().time(): #check if its not in the past of today.
                    c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{date.today().isoformat()}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                    potentialPatientAlreadyHasAppointment = c.fetchall()
                    if len(potentialPatientAlreadyHasAppointment) > 0:
                        colorify("You already have an appointment at that time!", 'error')
                        log(f"You already have an appointment at that time: {potentialPatientAlreadyHasAppointment}")
                    else:
                        #check if doctor has another appointment at chosen time
                        c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and '{date.today().isoformat()}' = appointmentDate")
                        potentialDoctorBusy = c.fetchall()
                        if len(potentialDoctorBusy) > 0:
                            colorify("Sorry! The doctor is busy at that time. Please try another time.", 'error')
                            log(f"Doctor already has appointment at that time: {convertTime(potentialDoctorBusy)}")
                        else:
                            add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])
                            colorify("Succeeded in making appointment!", 'success')
                            if debug:
                                log('Succeeded in making appointment!')
                else:
                    colorify("Time cannot be chosen in the past.", 'error')
            elif appointmentDate > todayStr:
                if debug:
                    colorify("appointmentdate chosen was after today!", 'debug')
                #ensure time doesnt overlap.
                c.execute(f"select * from appointments where LOWER(patientID) = '{current_user_data[0].lower()}' and '{appointmentDate}' = appointmentDate and appointmentTime = '{appointmentTime}'")
                potentialPatientAlreadyHasAppointment = c.fetchall()
                if len(potentialPatientAlreadyHasAppointment) > 0:
                    colorify("You already have an appointment at that time!", 'error')
                else:
                    #check if doctor has another appointment at chosen time
                    c.execute(f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = '{appointmentDate}'")
                    potentialDoctorBusy = c.fetchall()
                    #print("command: ", f"select * from appointments where doctorID = '{doctorID}' and appointmentTime = '{appointmentTime}' and appointmentDate = '{appointmentDate}'")
                    #print("potentialDoctorBusy: ", potentialDoctorBusy)
                    if len(potentialDoctorBusy) > 0:
                        colorify("Sorry! The doctor is busy at that time. Please try another time.", 'error')
                    else:
                        add_value_to_table('appointments', ['appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'appointmentReason', 'status'], [appointmentID, patientID, doctorID, appointmentDate, appointmentTime, appointmentReason, "Scheduled"])               
                        colorify("Succeeded in making appointment!", 'success')
                        if debug:
                            log("Succeeded in making appointment!")
        else:
            colorify("Cant choose a date in the past!", 'error')
            

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
                    'Modify patient database',
                    'Modify doctor database',
                    'Execute custom SQL command',
                    'Edit your data',
                    'Log out',
                    'Log in',
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
               'Modify patient database' if current_user_type == 'A' else None,
               'Modify doctor database' if current_user_type == 'A' else None,
               'Execute custom SQL command' if current_user_type == 'A' else None,
               'Edit your data' if current_user_type != None else None,
               'Log out' if current_user_data != None else None,
               'Log in' if current_user_data == None else None,
               'Exit']
    options_menu_str, options_dict = zampy.make_menu_from_options(options, True)
    return all_options, options_menu_str, options_dict
all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)

result = pyfiglet.figlet_format('Hospital Management System', font='doom')
print(colored(result, 'yellow'))

start_program()

while True:
    while checkIfNonNull(current_user_data) == False or checkIfNonNull(current_user_type) == False:
        start_program()
    
    all_options, options_menu_str, options_dict = resetMenuOptions(current_user_type)
    print('\n\n')
    updateAppointments(current_user_type)

    try:
        current_user_data = fetchAccountInfo(current_user_data[0], current_user_type) #update account info if info was edited.
        colorify(f'Account:', 'info')
        makePrettyTable(fetchTableNameFromUserType(current_user_type)[0], current_user_data, makeHeader=False)
    except Exception as e:
        colorify('Fatal error while trying to access account...', 'fatalerror')
        log('Fatal error while trying to access account... {}'.format(e))
        break
    log(f"Account used: {current_user_type}")


    colorify("Enter action: ", 'ask')
    try:
        tempIndex = cinput(options_menu_str, 'int')
        action = options_dict[tempIndex]
    except ValueError:
        colorify("Enter data of correct datatype.", 'error')
    except KeyError:
        colorify('The index entered was out of range. Try again.', 'error')
    else:
        try:
            index = all_options.index(action)
        except Exception as e:
            colorify(f"Error occured: {e}", 'error')
            log(f'Error occured while trying to read index: {e}')
        else:
            if index == 0:
                patientID = cinput("Enter patient ID: ")
                data = viewPatientDetails(patientID)
                #print("Requested data:", data)
                #print_header('Patient Details')
                makePrettyTable('patients', [data])
            elif index == 1:
                doctorID = cinput("Enter doctor ID: ")
                data = viewDoctorDetails(doctorID)
                #print("Requested data:", data)
                makePrettyTable('doctors', [data])
            elif index == 2:
                #Make an appointment
                doctorName = cinput("Enter doctor name to make appointment to: ")
                doctorID = None
                with Halo(text='Retrieving data...', spinner=spinnerType):
                    c.execute(f'select * from doctors where LOWER(name) = "{doctorName.lower()}"')
                    possibleDoctorIDs = c.fetchall()
                if possibleDoctorIDs and checkIfNonNull(possibleDoctorIDs) == True:
                    if len(possibleDoctorIDs) > 1:
                        colorify('Choose doctor:', 'ask')
                        choice = cinput(zampy.make_menu_from_options(possibleDoctorIDs), 'int')
                        doctorID = possibleDoctorIDs[choice-1][0]
                    else:
                        doctorID = possibleDoctorIDs[0][0]
                else:
                    colorify(f'No doctor with name {doctorName} was found.', 'error')
                    continue
                #appointmentDate = input("Enter date of appointment (Format: YYYY-MM-DD): ")
                appointmentDate = zampy.choose_date()
                appointmentTime = zampy.choose_time()

                appointmentReasonIndex = cinput(zampy.make_menu_from_options(['Check-up', 'Surgery', 'Physical Exam', 'Health Assessment']), 'int')
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
                historyIndex = cinput(zampy.make_menu_from_options(historyOptions), 'int')
                current_patient_id = current_user_data[0]
                data = None
                if historyIndex == 1:
                    recordID = cinput("Enter recordID: ")
                    c.execute(f'select * from medicalhistory where recordID = "{recordID}"')
                    assumedRecord = c.fetchone()
                    if assumedRecord[1] == current_user_data[0]:
                        data = viewRecordDetails(current_patient_id, recordID=recordID)
                    else:
                        colorify('You can\'t access another patient\'s medical history!', 'error')
                    #print(data)
                elif historyIndex == 2:
                    doctorID = cinput("Enter doctor ID: ")
                    data = viewRecordDetails(current_patient_id, doctorID=doctorID)
                    #print(data)
                elif historyIndex == 3:
                    data = viewRecordDetails(current_patient_id, all=True)
                if data:
                    makePrettyTable('medicalhistory', data)
            elif index == 4:
                idOrAll = cinput(zampy.make_menu_from_options(['View all prescriptions', 'View by ID']), 'int')
                if idOrAll == 1:
                    data = viewPrescriptions(all=True) #expand to finding by name, and id
                    #print(data)
                    #makePrettyTable('prescriptions', data)
                elif idOrAll == 2:
                    data = viewPrescriptions(all=False, pID=cinput("Enter prescription ID: "))
                makePrettyTable('prescriptions', data)
            elif index == 5:
                #Access medical history of a patient
                patientID = cinput("Enter patient ID: ")
                data = viewRecordDetails(patientID=patientID, all=True)
                makePrettyTable('medicalhistory', data)
            elif index == 6:
                #Access appointments history
                options = ['Upcoming appointments', 'Completed appointments']
                index = cinput(zampy.make_menu_from_options(options), 'int')
                if index == 1:
                    with Halo(text='Retrieving data...', spinner=spinnerType):
                        c.execute("SELECT * FROM appointments WHERE doctorID = %s AND status = %s AND appointmentDate >= %s", (current_user_data[0], 'Scheduled', str(date.today().isoformat())))
                        data = c.fetchall()
                    #print(data) 
                    makePrettyTable('appointments', data)
                    # print(from_db_cursor(c))
                elif index == 2:
                    with Halo(text='Retrieving data...', spinner=spinnerType):
                        c.execute("SELECT * FROM medicalhistory WHERE doctorID = %s AND status = %s", (current_user_data[0], 'Completed'))
                        data = c.fetchall()
                    #print(data)
                    makePrettyTable('medicalhistory', data)
                    # print(from_db_cursor(c))
            elif index == 7:
                dealWithPendingRequests()
            elif index == 8:
                #View table
                table_name = cinput("Enter table name to access: ")
                try:
                    with Halo(text='Retrieving data...', spinner=spinnerType):
                        c.execute(f'select * from {table_name}')
                        data = c.fetchall()
                    #print(data)
                    makePrettyTable(f'{table_name}', data)
                except Exception as e:
                    colorify(f'Error while trying to access table {table_name}. Details in log.txt', 'error')
                    log(f'Error while trying to access table {table_name}: {e}')
            elif index == 9:
                #Modify patient database
                tablename = 'patients'
                c.execute(f'SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "{tablename}";')
                columntypestuples = c.fetchall()
                dict_columntypes = dict()
                
                for column_tuple in columntypestuples:
                    dict_columntypes[column_tuple[0].lower()] = column_tuple[1] #name = type
                if debug:
                    colorify(f'Modify {tablename[:len(tablename)-1]} database', 'debug')
                data = retreiveData(tablename, allColumns=True)
                if len(data) > 0 and checkIfNonNull(data) == True:
                    options = [f'Add {tablename[:len(tablename)-1]}', f'Modify existing {tablename[:len(tablename)-1]}', f'Delete {tablename[:len(tablename)-1]}']
                    choice = cinput(zampy.make_menu_from_options(options), 'int')
                    if choice == 1:
                        #Add patient
                        allColumns = fetchColumns(tablename)
                        tempRecord = []
                        for column in allColumns:
                            if 'id' in column.lower():
                                tempRecord.append(returnNewID(tablename))
                                continue
                            if column == 'DOB':
                                data = zampy.choose_date()
                            elif column == 'Phone':
                                data = cinput('Enter phone number: ', 'int')
                            else:
                                data = cinput(f'Enter {column}: ')
                            tempRecord.append(data)
                        #Try adding to patient table
                        try:
                            add_value_to_table(tablename, allColumns, tempRecord)
                        except Exception as e:
                            colorify(f'Error while trying to edit data: {e}', 'error')
                            log(f'Error while trying to edit data for {current_user_data}: {e}')
                        else:
                            colorify(f'Succefully created new {tablename[:len(tablename)-1]} record.', 'success')
                    elif choice == 2:
                        #Modify existing patient
                        reqID = (cinput(f'Enter {tablename[:len(tablename)-1]} ID:'))
                        c.execute(f'select * from {tablename} where {tablename[:len(tablename)-1]}ID = "{reqID}";')
                        data = c.fetchone()
                        if len(data) > 0 and checkIfNonNull(data) == True:
                            allColumns = fetchColumns(tablename)
                            for columnName in allColumns:
                                if 'id' in columnName.lower():
                                    continue
                                datatypehere = dict_columntypes[columnName.lower()]
                                if 'date' in datatypehere:
                                    colorify(f'Edit {columnName}?', 'ask')
                                else:
                                    colorify(f'Edit {columnName}?', 'ask')
                                confirmEdit = cinput(zampy.make_menu_from_options(), 'int')
                                if confirmEdit == 1:
                                    if 'date' in (datatypehere):
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                        input_data = zampy.choose_date()
                                    elif 'int' in (datatypehere):
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                        try:
                                            input_data = cinput("Enter new data: ", 'int')
                                        except ValueError:
                                            colorify('Enter data of correct type.', 'error')
                                        except Exception as e:
                                            colorify(f'Some error occured: {e}', 'error')
                                    else:
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                        input_data = cinput('Enter new data: ')
                                    try:
                                        c.execute(f'update {tablename} set {columnName} = "{input_data}" where {tablename[:len(tablename)-1]}ID = "{reqID}"')
                                        database.commit()
                                    except Exception as e:
                                        colorify(f'Error while trying to edit data: {e}', 'error')
                                        log(f'Error while trying to edit data for {current_user_data}: {e}')
                                    else:
                                        colorify(f'Succesfully updated {columnName}.', 'success')
                            colorify(f'Succesfully updated {tablename[:len(tablename)-1]}.', 'success')
                        else:
                            colorify(f'Requested {tablename[:len(tablename)-1]} ID doesn\'t exist.', 'error')

                    elif choice == 3:
                        #Delete patient
                        reqID = (cinput(f'Enter {tablename[:len(tablename)-1]} ID:'))
                        c.execute(f'select * from {tablename} where {tablename[:len(tablename)-1]}ID = "{reqID}";')
                        data = c.fetchone()
                        try:
                            if len(data) > 0 and checkIfNonNull(data) == True:
                                c.execute(f'delete from {tablename} where {tablename[:len(tablename)-1]}ID="{reqID}"')
                                database.commit()
                        except Exception as e:
                            colorify(f'Error while trying to delete data: {e}', 'error')
                            log(f'Error while trying to delete data for {reqID}: {e}')
                        else:
                            colorify(f'Succesfully deleted {tablename[:len(tablename)-1]} from {tablename}.', 'success')
            
            elif index == 10:
                #Modify doctor database
                if debug:
                    colorify('Modify doctor database', 'debug')
                tablename = 'doctors'
                c.execute(f'SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "{tablename}";')
                columntypestuples = c.fetchall()
                dict_columntypes = dict()
                
                for column_tuple in columntypestuples:
                    dict_columntypes[column_tuple[0].lower()] = column_tuple[1] #name = type

                data = retreiveData(tablename, allColumns=True)
                if len(data) > 0 and checkIfNonNull(data) == True:
                    options = [f'Add {tablename[:len(tablename)-1]}', f'Modify existing {tablename[:len(tablename)-1]}', f'Delete {tablename[:len(tablename)-1]}']
                    choice = cinput(zampy.make_menu_from_options(options), 'int')
                    if choice == 1:
                        #Add patient
                        allColumns = fetchColumns(tablename)
                        tempRecord = []
                        for column in allColumns:
                            if 'id' in column.lower():
                                tempRecord.append(returnNewID(tablename))
                                continue
                            if column == 'DOB':
                                data = zampy.choose_date()
                            elif column == 'Phone':
                                data = cinput('Enter phone number: ', 'int')
                            else:
                                data = cinput(f'Enter {column}: ')
                            tempRecord.append(data)
                        #Try adding to patient table
                        try:
                            add_value_to_table(tablename, allColumns, tempRecord)
                        except Exception as e:
                            colorify(f'Error while trying to edit data: {e}', 'error')
                            log(f'Error while trying to edit data for {current_user_data}: {e}')
                        else:
                            colorify(f'Succefully created new {tablename[:len(tablename)-1]} record.', 'success')
                    elif choice == 2:
                        #Modify existing patient
                        reqID = cinput(f'Enter {tablename[:len(tablename)-1]} ID:')
                        c.execute(f'select * from {tablename} where {tablename[:len(tablename)-1]}ID = "{reqID}";')
                        data = c.fetchone()
                        if len(data) > 0 and checkIfNonNull(data) == True:
                            allColumns = fetchColumns(tablename)
                            for columnName in allColumns:
                                if 'id' in columnName.lower():
                                    continue
                                datatypehere = dict_columntypes[columnName.lower()]
                                if 'date' in datatypehere:
                                    colorify(f'Edit {columnName}?', 'ask')
                                else:
                                    colorify(f'Edit {columnName}?', 'ask')
                                confirmEdit = cinput(zampy.make_menu_from_options(), 'int')
                                if confirmEdit == 1:
                                    if 'date' in (datatypehere):
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                        input_data = zampy.choose_date()
                                    elif 'int' in (datatypehere):
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                            input_data = cinput("Enter new data: ", 'int')
                                    else:
                                        if debug:
                                            colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                        input_data = cinput('Enter new data: ')
                                    try:
                                        c.execute(f'update {tablename} set {columnName} = "{input_data}" where {tablename[:len(tablename)-1]}ID = "{reqID}"')
                                        database.commit()
                                    except Exception as e:
                                        colorify(f'Error while trying to edit data: {e}', 'error')
                                        log(f'Error while trying to edit data for {current_user_data}: {e}')
                                    else:
                                        colorify(f'Succesfully updated {columnName}.', 'success')
                            colorify(f'Succesfully updated {tablename[:len(tablename)-1]}.', 'success')
                        else:
                            colorify(f'Requested {tablename[:len(tablename)-1]} ID doesn\'t exist.', 'error')

                    elif choice == 3:
                        #Delete patient
                        reqID = (cinput(f'Enter {tablename[:len(tablename)-1]} ID:'))
                        c.execute(f'select * from {tablename} where {tablename[:len(tablename)-1]}ID = "{reqID}";')
                        data = c.fetchone()
                        try:
                            if len(data) > 0 and checkIfNonNull(data) == True:
                                c.execute(f'delete from {tablename} where {tablename[:len(tablename)-1]}ID="{reqID}"')
                                database.commit()
                        except Exception as e:
                            colorify(f'Error while trying to delete data: {e}', 'error')
                            log(f'Error while trying to delete data for {reqID}: {e}')
                        else:
                            colorify(f'Succesfully deleted {tablename[:len(tablename)-1]} from {tablename}.', 'success')
            elif index == 11:
                #Execute custom SQL command
                sql_command = cinput("Enter sql command:\n")
                try:
                    with Halo(text='Retrieving data...', spinner=spinnerType):
                        c.execute(sql_command)
                        if 'select' in sql_command:
                            data = c.fetchall()
                    try:
                        tablename = sql_command.split(' ')[3]
                        makePrettyTable(tablename, data)
                    except Exception as e:
                        colorify("Couldn't make table from given data.", 'error')
                        log(f'Error while prettyTable: {e}')
                        #print(data)
                except Exception as e:
                    colorify(f"Error while running command: {e}", 'error')
                    log(f"Error while running command: {e}")
                else:
                    if debug:
                        colorify('No error in running command.', 'debug')
            elif index == 12:
                #Edit your data
                tablename, id = fetchTableNameFromUserType(current_user_type)
                c.execute(f'select * from {tablename} where {id} = "{current_user_data[0]}"')
                user_record = c.fetchone()
                c.execute(f'SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "{tablename}";')
                columntypestuples = c.fetchall()
                dict_columntypes = dict()
                
                for column_tuple in columntypestuples:
                    dict_columntypes[column_tuple[0].lower()] = column_tuple[1] #name = type
                
                if debug:
                    colorify(dict_columntypes, 'debug')

                allColumns = fetchColumns(tablename)

                if debug:
                    colorify(user_record, 'debug') 
                for index in range(len(user_record)):
                    datavalue = user_record[index]
                    columnName = allColumns[index]
                    if checkIfNonNull(datavalue) == False:
                        colorify(f'{columnName} was found to be empty. Enter data now?', 'ask')
                        choice = cinput(zampy.make_menu_from_options(), 'int')
                        if choice == 1:
                            #c.execute(f'SELECT frs.name, frs.system_type_name FROM sys.dm_exec_describe_first_result_set("select * from {tablename}",NULL,NULL) frs;')
                            datatypehere = dict_columntypes[columnName.lower()]
                            if 'date' in (datatypehere):
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                input_data = zampy.choose_date()
                            elif 'int' in (datatypehere):
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                    input_data = cinput("Enter data: ", 'int')
                            else:
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                input_data = cinput('Enter data: ')
                            try:
                                c.execute(f'update {tablename} set {columnName} = "{input_data}" where {id} = "{current_user_data[0]}"')
                                database.commit()
                            except Exception as e:
                                colorify(f'Error while trying to edit data: {e}', 'error')
                                log(f'Error while trying to edit data for {current_user_data}: {e}')
                            else:
                                colorify(f'Succesfully updated {columnName}.', 'success')
                        else:
                            continue 
                    else:
                        if 'id' in columnName.lower():
                            continue
                        datatypehere = dict_columntypes[columnName.lower()]
                        if 'date' in datatypehere:
                            colorify(f'Would you like to edit {columnName}? (Current Value: {friendlyYear(datavalue, convertMD=True)})', 'ask')
                        else:
                            colorify(f'Would you like to edit {columnName}? (Current Value: {datavalue})', 'ask')
                        confirmEdit = cinput(zampy.make_menu_from_options(), 'int')
                        if confirmEdit == 1:
                            #colorify(f'{columnName} was found to be empty. Enter data now?', 'ask')
                            #choice = int(input(zampy.make_menu_from_options()))
                            #if choice == 1:
                                #c.execute(f'SELECT frs.name, frs.system_type_name FROM sys.dm_exec_describe_first_result_set("select * from {tablename}",NULL,NULL) frs;')
                            if 'date' in (datatypehere):
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                input_data = zampy.choose_date()
                            elif 'int' in (datatypehere):
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                try:
                                    input_data = cinput("Enter new data: ", 'int')
                                except ValueError:
                                    colorify('Enter data of correct type.', 'error')
                                except Exception as e:
                                    colorify(f'Some error occured: {e}', 'error')
                            else:
                                if debug:
                                    colorify(f'{columnName} is of type {datatypehere}', 'debug')
                                input_data = cinput('Enter new data: ')
                            try:
                                c.execute(f'update {tablename} set {columnName} = "{input_data}" where {id} = "{current_user_data[0]}"')
                                database.commit()
                            except Exception as e:
                                colorify(f'Error while trying to edit data: {e}', 'error')
                                log(f'Error while trying to edit data for {current_user_data}: {e}')
                            else:
                                colorify(f'Succesfully updated {columnName}.', 'success')
                        else:
                            continue
            elif index == 13:
                #Log out
                current_user_data = None
                current_user_type = None
            elif index == 14:
                #Log in
                start_program()
            elif index == 15:
                colorify("Thank you for using this program.", 'success')
                exit()
            else:
                colorify("Something went wrong.",'fatalerror')
                log(f"Unforeseen error when index was {index}.")