from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbs6'

# Intialize MySQL
mysql = MySQL(app)
run_with_ngrok(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email = %s AND Password = %s', [email, password])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['First Name'] = account['First Name']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Output message if something goes wrong...
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        # Create variables for easy access
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email = %s AND Password=%s', [email, password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', first_name):
            msg = 'Username must contain only letters!'
        elif not first_name or not last_name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES(%s, %s, %s, %s)', (first_name, last_name, email, password))
            mysql.connection.commit()
            msg = 'Successfully registered! Please Sign-In'
            return render_template('index.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html',msg=msg)

@app.route('/fake-news', methods=['GET', 'POST'])
def fakenews():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM fakenews;')
    entries=cursor.fetchall()
    return render_template('fake-news.html',entries=entries)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotpassword():
    # Output message if something goes wrong...
    return render_template('forgot-password.html')

@app.route('/verified', methods=['GET', 'POST'])
def verified():
    return render_template('verified.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    msg=''
    if request.method=="POST" and "news" in request.form:
        news=request.form["news"]
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")
        driver.maximize_window()
        time.sleep(3)
        searchbar=driver.find_element_by_class_name("Ax4B8")
        searchbar.send_keys(news)
        searchbar.send_keys(Keys.ENTER)
        time.sleep(5)
        lst=[]
        link1=driver.find_elements_by_class_name("ekueJc")
        for i in link1:
            if i.text!='':
                lst.append(i.text)
        time.sleep(3)
        driver.close()
        stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        text = news
        text_token=text.lower().split()
        text_token_fil=[]
        for i in text_token:
            if i not in stopwords:
                text_token_fil.append(i)
        final_count=0
        for i in text_token_fil:
            c=0
            for j in range(50):
                if i in lst[j].lower().split():
                    c=c+1
            if c>10:
                final_count+=1
        print(final_count)
        if final_count<=int(len(text.split())/2):
            msg='Fake'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM fakenews WHERE News = %s', [news])
            account = cursor.fetchone()
            if account:
                pass
            else:
                print("Fake insert")
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO fakenews VALUES(%s)', [news])
                mysql.connection.commit()
        elif 1.5*(len(text.split())/2)>=final_count and final_count>(len(text.split())/2):
            msg='Partially True'
        else:
            msg='True'
        return render_template('verified.html',msg=msg,lsts=lst[0:10])
    return render_template('verify.html')


if __name__=="__main__":
    app.run()