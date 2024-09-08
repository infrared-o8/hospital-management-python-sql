import random
import string
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(host="localhost", user = "root", password="admin", database="hospital_main")

c = db.cursor()

# Function to generate a random 5-letter password
def generate_password():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

# List of user IDs
user_ids = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'D1', 'D2']

# Inserting random passwords for each user
for user_id in user_ids:
    password = generate_password()
    c.execute(f"INSERT INTO credentials (userid, password) VALUES ('{user_id}', '{password}')")

# Commit changes to the database
db.commit()

# Close the connection
c.close()
db.close()

print("Passwords inserted successfully.")
