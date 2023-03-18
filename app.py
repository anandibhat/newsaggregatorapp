from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import json
import re
import eventregistry
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nandi@1986'
app.config['MYSQL_DB'] = 'myapp'

mysql = MySQL(app)

gnews_api_key = '86fce51575f8e4fa75311fe6dc80fac1'
gnews_api_url = f'https://gnews.io/api/v4/search?q=tech&lang=en&country=sg&max=10&token={gnews_api_key}'

gnews_api_response = requests.get(gnews_api_url)
print(gnews_api_response.json())
gnews_articles = gnews_api_response.json()['articles']

for article in gnews_articles:
    print(article['title'])

@app.route('/', methods=['GET', 'POST'])
def home():
    # GNews API
    gnews_api_key = '86fce51575f8e4fa75311fe6dc80fac1'
    gnews_api_url = f'https://gnews.io/api/v4/search?q=tech&lang=en&country=sg&max=10&token={gnews_api_key}'

    gnews_api_response = requests.get(gnews_api_url)
    gnews_articles = gnews_api_response.json().get('articles', [])
    
    if 'loggedin' in session:
        return render_template('dashboard.html', name=session['name'], email=session['email'], news_articles=gnews_articles)
    else:
        return render_template('index.html', news_articles=gnews_articles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        else:
            cursor.execute('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)', (name, email, password))
            mysql.connection.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['name'] = account[1]
            session['email'] = account[2]
            return redirect(url_for('home'))
        else:
            flash('Incorrect email/password!')
    
    return render_template('login.html')




