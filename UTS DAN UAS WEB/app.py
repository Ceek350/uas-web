from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import sqlite3


app = Flask(__name__)

app.secret_key = 'zerostore'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'sql.freedb.tech'
app.config['MYSQL_USER'] = 'freedb_zerostore'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = '9XcMJypct#5tX&J'
app.config['MYSQL_DB'] = 'freedb_zerostore'

# Intialize MySQL
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('index.html')

def success_login():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_data WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    return render_template('HomeLogin.html', msg='')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_data WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO user_data (id, email, password) VALUES (NULL, %s, %s)', (email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered! now u can login'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    # Check if account exists using MySQL
    return render_template('register.html', msg=msg)


@app.route("/cekinvoice/")
def cek():
    return render_template('Cek_Invoice.html')

@app.route("/aboutus/")
def aboutus():
    return render_template('aboutus.html')

#GAME
@app.route("/freefire")
def ff():
    return render_template('freefire.html')

@app.route("/genshin")
def gi():
    return render_template('genshin.html')

@app.route("/mlbb")
def mlbb():
    return render_template('mlbb.html')

@app.route("/pubgm")
def pubgm():
    return render_template('pubgm.html')



if __name__ == '__main__' :
    app.run(debug=True)