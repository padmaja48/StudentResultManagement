from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os
from datetime import timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_2024'  # Change this in production
app.permanent_session_lifetime = timedelta(minutes=30)

# Database configuration
DATABASE = 'database.db'

# ===================== DATABASE SETUP =====================
def get_db_connection():
    """Connect to SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Drop existing tables if they exist (for fresh start)
    c.execute('DROP TABLE IF EXISTS students')
    c.execute('DROP TABLE IF EXISTS admin')
    
    # Create students table with 3 subjects
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            python_marks INTEGER NOT NULL CHECK(python_marks >= 0 AND python_marks <= 100),
            cpp_marks INTEGER NOT NULL CHECK(cpp_marks >= 0 AND cpp_marks <= 100),
            java_marks INTEGER NOT NULL CHECK(java_marks >= 0 AND java_marks <= 100),
            average_marks REAL NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    
    # Create admin table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()
else:
    # Check if admin table exists, if not recreate it
    try:
        conn = get_db_connection()
        conn.execute('SELECT 1 FROM admin LIMIT 1')
        conn.close()
    except sqlite3.OperationalError:
        # Table doesn't exist, reinitialize
        init_db()

# ===================== AUTHENTICATION MIDDLEWARE =====================
def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'admin':
            flash('Access denied! Admin only.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator to check if user is student"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'student':
            flash('Access denied! Student only.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===================== HELPER FUNCTIONS =====================
def calculate_grade(marks):
    """Calculate grade based on marks"""
    if marks >= 90:
        return 'A'
    elif marks >= 80:
        return 'B'
    elif marks >= 70:
        return 'C'
    elif marks >= 60:
        return 'D'
    else:
        return 'F'

# ===================== ROUTES =====================

@app.route('/')
def home():
    """Home page - redirect to login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with Admin and Student forms"""
    if request.method == 'POST':
        login_type = request.form.get('login_type')  # 'admin' or 'student'
        
        if login_type == 'admin':
            # Admin login
            username = request.form.get('admin_username')
            password = request.form.get('admin_password')
            
            # Validate inputs
            if not username or not password:
                flash('Please enter username and password!', 'danger')
                return redirect(url_for('login'))
            
            conn = get_db_connection()
            admin = conn.execute(
                'SELECT * FROM admin WHERE username = ?',
                (username,)
            ).fetchone()
            conn.close()
            
            if admin and check_password_hash(admin['password'], password):
                session.permanent = True
                session['user_id'] = admin['id']
                session['username'] = admin['username']
                session['user_type'] = 'admin'
                flash(f'Welcome Admin {username}!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials!', 'danger')
                return redirect(url_for('login'))
        
        elif login_type == 'student':
            # Student login
            roll_no = request.form.get('student_roll')
            
            # Validate input
            if not roll_no:
                flash('Please enter your roll number!', 'danger')
                return redirect(url_for('login'))
            
            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM students WHERE roll_no = ?',
                (roll_no,)
            ).fetchone()
            conn.close()
            
            if student:
                session.permanent = True
                session['user_id'] = student['id']
                session['roll_no'] = student['roll_no']
                session['user_type'] = 'student'
                flash(f'Welcome {student["name"]}!', 'success')
                return redirect(url_for('student_result'))
            else:
                flash('Invalid roll number!', 'danger')
                return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """Admin registration page"""
    if request.method == 'POST':
        username = request.form.get('admin_username')
        password = request.form.get('admin_password')
        confirm_password = request.form.get('admin_confirm_password')
        
        # Validation
        errors = []
        
        if not username or not password or not confirm_password:
            errors.append('All fields are required!')
        
        if username and len(username) < 3:
            errors.append('Username must be at least 3 characters long!')
        
        if password and len(password) < 6:
            errors.append('Password must be at least 6 characters long!')
        
        if password != confirm_password:
            errors.append('Passwords do not match!')
        
        if not errors:
            conn = get_db_connection()
            # Check if username already exists
            existing = conn.execute(
                'SELECT * FROM admin WHERE username = ?',
                (username,)
            ).fetchone()
            
            if existing:
                errors.append('Username already exists! Please choose a different one.')
            else:
                # Hash password and insert new admin
                hashed_password = generate_password_hash(password)
                conn.execute(
                    'INSERT INTO admin (username, password) VALUES (?, ?)',
                    (username, hashed_password)
                )
                conn.commit()
                conn.close()
                flash('Registration successful! Please login with your credentials.', 'success')
                return redirect(url_for('login'))
            conn.close()
        
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('admin_register'))
    
    return render_template('admin_register.html')

# ===================== ADMIN ROUTES =====================

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY roll_no').fetchall()
    conn.close()
    return render_template('dashboard.html', students=students)

@app.route('/admin/add-student', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    """Add new student"""
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        name = request.form.get('name')
        python_marks = request.form.get('python_marks')
        cpp_marks = request.form.get('cpp_marks')
        java_marks = request.form.get('java_marks')
        
        # Validation
        errors = []
        
        if not roll_no or not name or not python_marks or not cpp_marks or not java_marks:
            errors.append('All fields are required!')
        
        if python_marks and cpp_marks and java_marks:
            try:
                py = int(python_marks)
                cpp = int(cpp_marks)
                java = int(java_marks)
                
                if py < 0 or py > 100:
                    errors.append('Python marks must be between 0 and 100!')
                if cpp < 0 or cpp > 100:
                    errors.append('C++ marks must be between 0 and 100!')
                if java < 0 or java > 100:
                    errors.append('Java marks must be between 0 and 100!')
            except ValueError:
                errors.append('All marks must be numbers!')
        
        if not errors:
            py = int(python_marks)
            cpp = int(cpp_marks)
            java = int(java_marks)
            average = (py + cpp + java) / 3
            grade = calculate_grade(average)
            
            try:
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO students (roll_no, name, python_marks, cpp_marks, java_marks, average_marks, grade) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (roll_no, name, py, cpp, java, average, grade)
                )
                conn.commit()
                conn.close()
                flash('Student added successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            except sqlite3.IntegrityError:
                errors.append('Roll number already exists!')
        
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('add_student'))
    
    return render_template('add_student.html')

@app.route('/admin/view-students')
@login_required
@admin_required
def view_students():
    """View all students"""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY roll_no').fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/admin/edit-student/<int:student_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(student_id):
    """Edit student details"""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    if not student:
        flash('Student not found!', 'danger')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        python_marks = request.form.get('python_marks')
        cpp_marks = request.form.get('cpp_marks')
        java_marks = request.form.get('java_marks')
        
        # Validation
        errors = []
        
        if not name or not python_marks or not cpp_marks or not java_marks:
            errors.append('All fields are required!')
        
        if python_marks and cpp_marks and java_marks:
            try:
                py = int(python_marks)
                cpp = int(cpp_marks)
                java = int(java_marks)
                
                if py < 0 or py > 100:
                    errors.append('Python marks must be between 0 and 100!')
                if cpp < 0 or cpp > 100:
                    errors.append('C++ marks must be between 0 and 100!')
                if java < 0 or java > 100:
                    errors.append('Java marks must be between 0 and 100!')
            except ValueError:
                errors.append('All marks must be numbers!')
        
        if not errors:
            py = int(python_marks)
            cpp = int(cpp_marks)
            java = int(java_marks)
            average = (py + cpp + java) / 3
            grade = calculate_grade(average)
            
            conn.execute(
                'UPDATE students SET name = ?, python_marks = ?, cpp_marks = ?, java_marks = ?, average_marks = ?, grade = ? WHERE id = ?',
                (name, py, cpp, java, average, grade, student_id)
            )
            conn.commit()
            conn.close()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            for error in errors:
                flash(error, 'danger')
    
    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/admin/delete-student/<int:student_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_student(student_id):
    """Delete student record"""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    if student:
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        flash(f'Student {student["name"]} deleted successfully!', 'success')
    else:
        flash('Student not found!', 'danger')
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

# ===================== STUDENT ROUTES =====================

@app.route('/student/result')
@login_required
@student_required
def student_result():
    """Student view their result"""
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (session.get('user_id'),)
    ).fetchone()
    conn.close()
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login'))
    
    return render_template('search.html', student=student)

# ===================== LOGOUT ROUTE =====================

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
