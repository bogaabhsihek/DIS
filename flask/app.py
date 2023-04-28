from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import re
from datetime import datetime, date
import sqlite3


app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route("/")
def home():
    user_id = session.get('user_id')
    if user_id:
        # User is logged in, display icon and signout button
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE id = ? ', (int(user_id), ))
        user = cursor.fetchone()
        return render_template('index.html', logged_in=True, user=user)
    else:
        return render_template("index.html", logged_in=False)

@app.route("/product", methods=["GET"])
def product():
    user_id = session.get('user_id')
    if user_id:
        # User is logged in, display icon and signout button
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE id = ? ', (int(user_id), ))
        user = cursor.fetchone()
        return render_template('ProdDescription.html', logged_in=True, user=user)
    else:
        return render_template("ProdDescription.html")

connect = sqlite3.connect('database.db')
connect.execute('CREATE TABLE IF NOT EXISTS Appointment ( id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, lastname TEXT NOT NULL, dob DATE NOT NULL, email TEXT UNIQUE NOT NULL, other TEXT NOT NULL)')
@app.route("/bookappointment", methods=["POST"])
def bookappointment():
    msg = ''
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        email = request.form['email']
        other = request.form['other']
        if not firstname or not lastname or not dob or not email:
            msg = 'Please fill out the form !'
        elif not firstname:
            msg = 'Please enter your firstname'
        elif not lastname:
            msg = 'Please enter your lastname'
        elif datetime.strptime(dob, '%Y-%m-%d').date() <= date(1950, 1,1):
            msg = 'Your Date of Birth year should be after 1950'
        elif datetime.strptime(dob, '%Y-%m-%d').date() >= date.today():
            msg = 'Your Date of Birth should be before todays date'
        elif email:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Please enter valid email'
        if msg:
            return jsonify(errors=msg)
        else: 
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO appointment (firstname, lastname, dob, email, other) VALUES (?, ?, ?, ?, ?)', (firstname, lastname, dob, email, other ))
            conn.commit()
            msg = 'You have successfully booked appointment !'
            return jsonify(success=True, msg='')
        
@app.route("/about", methods=["GET"])
def about():
    user_id = session.get('user_id')
    if user_id:
        # User is logged in, display icon and signout button
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE id = ? ', (int(user_id), ))
        user = cursor.fetchone()
        return render_template('AboutUs.html', logged_in=True, user=user)
    else:
        return render_template("AboutUs.html", logged_in=False)

connect = sqlite3.connect('database.db')
connect.execute('CREATE TABLE IF NOT EXISTS User ( id INTEGER PRIMARY KEY, firstname TEXT NOT NULL, lastname TEXT NOT NULL, dob DATE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        password = request.form['password']
        email = request.form['email']
        confirmpassword = request.form['confirmpassword']
        if not firstname or not lastname or not dob or not email or not password or not confirmpassword:
            msg = 'Please fill out the form !'
        elif datetime.strptime(dob, '%Y-%m-%d').date() <= date(1950, 1,1):
            msg = 'Your Date of Birth year should be after 1950'
        elif datetime.strptime(dob, '%Y-%m-%d').date() >= date.today():
            msg = 'Your Date of Birth should be before todays date'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Please enter valid email'
        elif not len(password) > 6:
                msg = 'Your password should be more than 6 characters'
        elif not password == confirmpassword:
            msg = 'password and confirm password should be same' 
        if msg == '': 
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            else:
                cursor.execute('INSERT INTO user (firstname, lastname, dob, email, password) VALUES (?, ?, ?, ?, ?)', (firstname, lastname, dob, email, password ))
                conn.commit()
                cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
                user = cursor.fetchone()
                session['user_id'] = user[0]
                msg = 'You have successfully registered !'
                return render_template('index.html', msg = msg, user = user)
    return render_template('registration.html', msg = msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Please enter valid email'
        elif not len(password) > 6:
                msg = 'Your password should be more than 6 characters'
        if msg == '':
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute("SELECT * FROM User WHERE email = ? AND password = ?", (email, password))
                user = cursor.fetchone()
                if user:
                    session['user_id'] = user[0]
                    msg = 'Logged in successfully !'
                    return render_template('index.html', msg = msg, user = user)
                else:
                    msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/profile', methods=["GET", "POST", "PUT"])
def profile():
    user_id = session.get('user_id')
    if user_id:
        # User is logged in, display icon and signout button
        if request.method == "POST":
            msg = ''
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            dob = request.form.get('dob')
            if not firstname or not lastname or not dob or not email:
                msg = 'Please do not leave the fileds empty !'
            elif datetime.strptime(dob, '%Y-%m-%d').date() <= date(1950, 1,1):
                msg = 'Your Date of Birth year should be after 1950'
            elif datetime.strptime(dob, '%Y-%m-%d').date() >= date.today():
                msg = 'Your Date of Birth should be before todays date'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Please enter valid email'
            if not msg:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute('UPDATE user SET firstname=?, lastname=?, email=?, dob=? WHERE id=?', (firstname, lastname, email, dob, int(user_id)))
                conn.commit()
                conn.close()
                return redirect(url_for('profile'))
            else:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM user WHERE id = ? ', (int(user_id), ))
                user = cursor.fetchone()
                return render_template('profile.html', logged_in=True, msg=msg, user=user)
        else:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE id = ? ', (int(user_id), ))
            user = cursor.fetchone()
            return render_template('profile.html', logged_in=True, user=user)
    else:
        return render_template("login.html", logged_in=False)

# Signout route
@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/users')
def users():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall();
    return render_template("users.html", rows=rows)

@app.route('/appointments')
def appointments():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM appointment")

    rows = cur.fetchall();
    return render_template("appointments.html", rows=rows)
