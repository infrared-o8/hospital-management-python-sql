1. run the install_database.bat file, to install the sample hospital_main database i created and used
for this project.

NOTE:
if u receive an error, follow the following instructions to add mysql to PATH variables.

you will need to know ur mysql.exe path. it should be in the format:
"C:\Program Files\MySQL\MySQL Server x.x\bin\mysql.exe" where x.x is ur server version.
go to settings, search for edit environment variables, modify the path variable and add the mysql.exe path.
apply the changes.

refer https://www.basedash.com/blog/adding-mysql-to-path-in-windows for details.

2. the bat file should install all dependencies from the requirements.txt. if it fails, please manually
install all dependencies using pip from the command line.

3. the bat file should run the main.py program. if you had come across an error earlier and fixed it, run the main.py
program manually.