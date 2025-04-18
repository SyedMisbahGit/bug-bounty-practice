from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create a simple in-memory database for practice
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    flash('Welcome to the Bug Bounty Practice App!', 'info')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # SQL Injection Vulnerability
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # SQL Injection Vulnerability
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    user = c.fetchone()
    conn.close()

    if user:
        return "Login Successful"
    else:
        return "Invalid credentials"

@app.route('/csrf-demo', methods=['GET', 'POST'])
def csrf_demo():
    if request.method == 'POST':
        return "CSRF attack successful!"
    return render_template('csrf.html')

@app.route('/xss-demo', methods=['GET', 'POST'])
def xss_demo():
    if request.method == 'POST':
        return f"Hello, {request.form['username']}!<br>Your message: {request.form['message']}"
    return render_template('xss.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
