import mysql.connector
from datetime import datetime

database = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital")
c = database.cursor()