from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from auth import jwt_required, verify_token, generate_token
import os
import subprocess
import sqlite3
import jwt

app = Flask(__name__)
app.secret_key = "REDACTED_KEY"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Functions
def sqlite_setup():
    """Initialize SQLite database and create required tables."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS files 
                 (username TEXT, file_id TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Create and return database connection."""
    return sqlite3.connect('database.db')

# Utility Functions
def extract_zip(file, path):
    """Extract zip file to specified path."""
    try:
        subprocess.run(['unzip', '-o', file, '-d', path], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error extracting zip file: {e}") from e

# Route Handlers
@app.route('/', methods=['GET'])
def index():
    if request.cookies.get('auth_token') and verify_token(request.cookies.get('auth_token')):
        return render_template('index.html', login=True)
    return render_template('index.html', login=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('login.html', error_message='Username and password are required!')

        with get_db_connection() as conn:
            c = conn.cursor()
            user = c.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()

        if user:
            token = generate_token(user[0])
            response = redirect(url_for('index'))
            response.set_cookie('auth_token', token)
            return response
            
        return render_template('login.html', error_message='Invalid credentials!')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'

        if not username or not password:
            return render_template('register.html', error_message='Username and password are required!')

        with get_db_connection() as conn:
            c = conn.cursor()
            if c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone():
                return render_template('register.html', error_message='Username already exists!')

            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                     (username, password, role))
            conn.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
@jwt_required
def upload():
    if request.method == 'POST':
        if 'zipfile' not in request.files or request.files['zipfile'].filename == '':
            return render_template('upload.html', error_message='No file part', login=True)

        file = request.files['zipfile']
        password = os.urandom(8).hex()

        with get_db_connection() as conn:
            c = conn.cursor()
            file_count = c.execute('SELECT file_id FROM files').fetchall()
            ID = int(file_count[-1][0]) + 1 if file_count else 1

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            extract_path = file_path.replace('.zip', '')

            file.save(file_path)
            extract_zip(file_path, extract_path)
            os.makedirs(extract_path, exist_ok=True)

            subprocess.run(['zip', '-P', password, f'uploads/uploads_{str(ID)}.zip', 
                          '-r', extract_path], check=True)
            os.remove(file_path)

            c.execute('INSERT INTO files (username, file_id, password) VALUES (?, ?, ?)', 
                     (request.user_id, ID, password))
            conn.commit()

        return render_template('upload.html', 
                             success_message=f'File uploaded successfully!\nID:{ID}', 
                             login=True)

    return render_template('upload.html', login=True)

@app.route('/download', methods=['GET', 'POST'])
@jwt_required
def download():
    if request.method == 'POST':
        file_id = request.form['file_id']
        password = request.form['password']

        with get_db_connection() as conn:
            c = conn.cursor()
            file = c.execute(f'SELECT * FROM files WHERE file_id = ? and password = {password}', 
                           (file_id,)).fetchone()

        if file:
            return send_file(f'uploads/uploads_{file_id}.zip')
        return render_template('download.html', error_message='Invalid ID or password!', login=True)

    return render_template('download.html', login=True)

@app.route('/logout')
def logout():
    response = redirect(url_for('index'))
    response.set_cookie('auth_token', expires=0)
    return response

@app.route('/files', methods=['GET', 'POST'])
@jwt_required
def file():
    with get_db_connection() as conn:
        c = conn.cursor()
        files = c.execute(f'SELECT * FROM files WHERE username = "{request.user_id}"').fetchall()
    
    flash(f'You are logged in as {request.user_id}')
    return render_template('files.html', files=files, login=True)

@app.route('/admin', methods=['GET'])
@jwt_required
def admin():
    if verify_token(request.cookies.get('auth_token'))['role'] == 'admin':
        return os.environ['FLAG']
    return "You are not admin!"

if __name__ == '__main__':
    sqlite_setup()
    app.run(debug=False, host='0.0.0.0', port=5000)
