import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database Successfully")

# conn.execute("CREATE TABLE User (id INTEGER PRIMARY KEY,firstname TEXT NOT NULL, lastname TEXT NOT NULL, dob DATE NOT NULL,email TEXT UNIQUE NOT NULL,  password TEXT NOT NULL)")
# print("Table Successfully Created!")

cur = conn.cursor()
# firstname='jon'
# lastname='do'
# dob='1995-01-03'
# email='abc@abc.com'
# password='asdf'
# cur.execute("INSERT INTO User (firstname, lastname, dob, email, password) VALUES (?,?,?,?,?)",(firstname,lastname, dob, email, password))
# cur.execute("SELECT * FROM user")
# cur.execute("SELECT * FROM User WHERE email = 'abc@abc.com' AND password = 'asdf'")
# users = cur.fetchall()
cursor = conn.cursor()
cursor.execute("SELECT * FROM Appointment")
appointments = cursor.fetchall()
# print(f" users = {users},  appointments =  {appointments}")
conn.execute('ALTER TABLE Appointment RENAME TO appointments_temp')
conn.execute('CREATE TABLE IF NOT EXISTS Appointment ( id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, lastname TEXT NOT NULL, dob DATE NOT NULL, email TEXT NOT NULL, other TEXT NOT NULL)')
# cursor.execute('INSERT INTO user (id, firstname, lastname, email, dob) SELECT id, firstname, lastname, email, dob FROM user_temp')
cursor.execute('DROP TABLE appointments_temp')
# cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = 'user';")
users = cursor.fetchall()
print(f" indexes = {users}")


conn.close()