## Brief Summary
This project was made for the CBSE computer science practicals 2024-25, using SQL and Python. This project intends to allow quicker and easier handling of data relevant to the hospital environment, such as doctors' data, patients' data, and medication data. It also attempts to implement an appointment-scheduling system. 

## Quick Configuration

Run the `init.bat` file to install all dependencies and set up the sample `hospital_main` database used in this project. I personally prefer logging in as an admin first, to view all the tables in the database. 

Some login credentials for testing purposes:
1. Patient: 
   PatientID: P1,
   PatientName: andrew,
   Password: adgro

2. Doctor:
   DoctorID: D1,
   DoctorName: doc1,
   Password: hxbzj

3. Admin:
   AdminID: ADM1,
   AdminName: Zeeman,
   Password: adminboi
---

## Adding MySQL to PATH Variables

To add MySQL to your PATH variables, follow these steps:

1. **Locate MySQL Path**:  
   Find the path to `mysql.exe` on your machine. It is usually located in:  
   `"C:\Program Files\MySQL\MySQL Server x.x\bin\mysql.exe"`  
   where `x.x` represents your MySQL server version.

2. **Open Environment Variables**:  
   - Go to **Settings**.
   - Search for **Edit environment variables for your account**.
   - Open the **Environment Variables** window.

3. **Edit PATH Variable**:
   - In the **System Variables** section, find and select the `Path` variable.
   - Click on **Edit** and add the path to `mysql.exe` (e.g., `"C:\Program Files\MySQL\MySQL Server x.x\bin\"`).
   - **Apply** the changes and close the dialog.

For more detailed instructions, refer to this guide: [Adding MySQL to PATH in Windows](https://www.basedash.com/blog/adding-mysql-to-path-in-windows).

---
