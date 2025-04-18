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
    conn.close()  # Fixed indentation here

    if user:
        return "Login Successful"
    else:
        return "Invalid credentials"

@app.route("/sqli", methods=["GET", "POST"])
def sqli():
    result = None
    if request.method == "POST":
        username = request.form.get("username")

        # INSECURE SQL Query (VULNERABLE!)
        conn = sqlite3.connect("vulnerable.db")
        cursor = conn.cursor()
        try:
            query = f"SELECT * FROM users WHERE username = '{username}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                result = f"User '{username}' found! (🔓 Vulnerable!)"
            else:
                result = "No such user."
        except Exception as e:
            result = f"Error: {e}"
        finally:
            conn.close()

    return render_template("sqli.html", result=result)

@app.route('/csrf-demo', methods=['GET', 'POST'])
def csrf_demo():
    if request.method == 'POST':
        return "CSRF attack successful!"
    return render_template('csrf.html')


@app.route('/xss-demo', methods=['GET', 'POST'])
def xss_demo():
    if request.method == 'POST':
        username = request.form.get('username')  # Use .get() to avoid KeyError
        message = request.form.get('message')

        if not username or not message:
            flash("Both username and message are required!", "danger")
            return render_template('xss.html')

        return f"Hello, {username}!<br>Your message: {message}"

    return render_template('xss.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
