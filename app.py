from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', secrets.token_hex(32))

DATABASE = 'transport.db'

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

def validate_csrf_token():
    token = request.form.get('csrf_token')
    if not token or token != session.get('csrf_token'):
        flash('Invalid security token. Please try again.', 'danger')
        return False
    return True

app.jinja_env.globals['csrf_token'] = generate_csrf_token

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS requests')
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS buses')
    cursor.execute('DROP TABLE IF EXISTS drivers')
    cursor.execute('DROP TABLE IF EXISTS routes')
    cursor.execute('DROP TABLE IF EXISTS admin')
    
    cursor.execute('''
        CREATE TABLE admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT NOT NULL,
            stops TEXT NOT NULL,
            timings TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT UNIQUE NOT NULL,
            route_id INTEGER,
            driver_id INTEGER,
            capacity INTEGER NOT NULL,
            FOREIGN KEY (route_id) REFERENCES routes (id),
            FOREIGN KEY (driver_id) REFERENCES drivers (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bus_id INTEGER,
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                   ('admin', generate_password_hash('admin123')))
    
    routes_data = [
        ('Miyapur Route', 'Hyderabad → Miyapur → BHEL → Patancheru → BVRIT', '7:00 AM - 8:30 AM'),
        ('Kukatpally Route', 'Kukatpally → JNTU → Chandanagar → BHEL → BVRIT', '7:10 AM - 8:40 AM'),
        ('Lingampally Route', 'Lingampally → RC Puram → Patancheru → Isnapur → BVRIT', '7:15 AM - 8:45 AM'),
        ('BHEL Route', 'BHEL → Beeramguda → Isnapur → BVRIT', '7:20 AM - 8:50 AM'),
        ('Narsapur Town Route', 'Narsapur → BVRIT', '7:40 AM - 8:10 AM')
    ]
    cursor.executemany("INSERT INTO routes (route_name, stops, timings) VALUES (?, ?, ?)", routes_data)
    
    drivers_data = [
        ('Ramesh Kumar', '9876543210', generate_password_hash('driver123')),
        ('Mahesh Goud', '9876543220', generate_password_hash('driver123')),
        ('Suresh Naik', '9876543230', generate_password_hash('driver123')),
        ('Ravi Teja', '9876543240', generate_password_hash('driver123')),
        ('Krishna Reddy', '9876543250', generate_password_hash('driver123'))
    ]
    cursor.executemany("INSERT INTO drivers (name, contact, password) VALUES (?, ?, ?)", drivers_data)
    
    buses_data = [
        ('SA3', 1, 1, 40),
        ('J9', 2, 2, 45),
        ('J10', 3, 3, 40),
        ('BHEL4', 4, 4, 35),
        ('N1', 5, 5, 30)
    ]
    cursor.executemany("INSERT INTO buses (bus_number, route_id, driver_id, capacity) VALUES (?, ?, ?, ?)", buses_data)
    
    students_data = [
        ('B SAI RISHIK REDDY', '24211A0538', generate_password_hash('student123'), 2),
        ('A SANDEEP', '24211A0512', generate_password_hash('student123'), 1)
    ]
    cursor.executemany("INSERT INTO students (name, roll_number, password, bus_id) VALUES (?, ?, ?, ?)", students_data)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        
        if role == 'admin' and username and password:
            cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['role'] = 'admin'
                session['username'] = user['username']
                conn.close()
                return redirect(url_for('admin_dashboard'))
        
        elif role == 'student' and username and password:
            cursor.execute("SELECT * FROM students WHERE roll_number = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['role'] = 'student'
                session['name'] = user['name']
                conn.close()
                return redirect(url_for('student_dashboard'))
        
        elif role == 'driver' and username and password:
            cursor.execute("SELECT * FROM drivers WHERE contact = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['role'] = 'driver'
                session['name'] = user['name']
                conn.close()
                return redirect(url_for('driver_dashboard'))
        
        conn.close()
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash('Please login as admin to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM students")
    students_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM buses")
    buses_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM drivers")
    drivers_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM routes")
    routes_count = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                           students_count=students_count,
                           buses_count=buses_count,
                           drivers_count=drivers_count,
                           routes_count=routes_count)

@app.route('/admin/students')
def manage_students():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, b.bus_number 
        FROM students s
        LEFT JOIN buses b ON s.bus_id = b.id
        ORDER BY s.name
    ''')
    students = cursor.fetchall()
    
    cursor.execute("SELECT * FROM buses ORDER BY bus_number")
    buses = cursor.fetchall()
    
    conn.close()
    
    return render_template('manage_students.html', students=students, buses=buses)

@app.route('/admin/students/add', methods=['POST'])
def add_student():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')
    password = request.form.get('password')
    bus_id = request.form.get('bus_id') or None
    
    if not password:
        flash('Password is required!', 'danger')
        return redirect(url_for('manage_students'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO students (name, roll_number, password, bus_id) VALUES (?, ?, ?, ?)",
                       (name, roll_number, generate_password_hash(password), bus_id))
        conn.commit()
        flash('Student added successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('Roll number already exists!', 'danger')
    
    conn.close()
    return redirect(url_for('manage_students'))

@app.route('/admin/students/edit/<int:id>', methods=['POST'])
def edit_student(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')
    password = request.form.get('password')
    bus_id = request.form.get('bus_id') or None
    
    conn = get_db()
    cursor = conn.cursor()
    
    if password and password.strip():
        cursor.execute("UPDATE students SET name = ?, roll_number = ?, password = ?, bus_id = ? WHERE id = ?",
                       (name, roll_number, generate_password_hash(password), bus_id, id))
    else:
        cursor.execute("UPDATE students SET name = ?, roll_number = ?, bus_id = ? WHERE id = ?",
                       (name, roll_number, bus_id, id))
    
    conn.commit()
    conn.close()
    flash('Student updated successfully!', 'success')
    return redirect(url_for('manage_students'))

@app.route('/admin/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if not validate_csrf_token():
        return redirect(url_for('manage_students'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('manage_students'))

@app.route('/admin/buses')
def manage_buses():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, r.route_name, d.name as driver_name
        FROM buses b
        LEFT JOIN routes r ON b.route_id = r.id
        LEFT JOIN drivers d ON b.driver_id = d.id
        ORDER BY b.bus_number
    ''')
    buses = cursor.fetchall()
    
    cursor.execute("SELECT * FROM routes ORDER BY route_name")
    routes = cursor.fetchall()
    
    cursor.execute("SELECT * FROM drivers ORDER BY name")
    drivers = cursor.fetchall()
    
    conn.close()
    
    return render_template('manage_buses.html', buses=buses, routes=routes, drivers=drivers)

@app.route('/admin/buses/add', methods=['POST'])
def add_bus():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    bus_number = request.form.get('bus_number')
    route_id = request.form.get('route_id') or None
    driver_id = request.form.get('driver_id') or None
    capacity = request.form.get('capacity')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO buses (bus_number, route_id, driver_id, capacity) VALUES (?, ?, ?, ?)",
                       (bus_number, route_id, driver_id, capacity))
        conn.commit()
        flash('Bus added successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('Bus number already exists!', 'danger')
    
    conn.close()
    return redirect(url_for('manage_buses'))

@app.route('/admin/buses/edit/<int:id>', methods=['POST'])
def edit_bus(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    bus_number = request.form.get('bus_number')
    route_id = request.form.get('route_id') or None
    driver_id = request.form.get('driver_id') or None
    capacity = request.form.get('capacity')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE buses SET bus_number = ?, route_id = ?, driver_id = ?, capacity = ? WHERE id = ?",
                   (bus_number, route_id, driver_id, capacity, id))
    conn.commit()
    conn.close()
    flash('Bus updated successfully!', 'success')
    return redirect(url_for('manage_buses'))

@app.route('/admin/buses/delete/<int:id>', methods=['POST'])
def delete_bus(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if not validate_csrf_token():
        return redirect(url_for('manage_buses'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM buses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Bus deleted successfully!', 'success')
    return redirect(url_for('manage_buses'))

@app.route('/admin/routes')
def manage_routes():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routes ORDER BY route_name")
    routes = cursor.fetchall()
    conn.close()
    
    return render_template('manage_routes.html', routes=routes)

@app.route('/admin/routes/add', methods=['POST'])
def add_route():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    route_name = request.form.get('route_name')
    stops = request.form.get('stops')
    timings = request.form.get('timings')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO routes (route_name, stops, timings) VALUES (?, ?, ?)",
                   (route_name, stops, timings))
    conn.commit()
    conn.close()
    flash('Route added successfully!', 'success')
    return redirect(url_for('manage_routes'))

@app.route('/admin/routes/edit/<int:id>', methods=['POST'])
def edit_route(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    route_name = request.form.get('route_name')
    stops = request.form.get('stops')
    timings = request.form.get('timings')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE routes SET route_name = ?, stops = ?, timings = ? WHERE id = ?",
                   (route_name, stops, timings, id))
    conn.commit()
    conn.close()
    flash('Route updated successfully!', 'success')
    return redirect(url_for('manage_routes'))

@app.route('/admin/routes/delete/<int:id>', methods=['POST'])
def delete_route(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if not validate_csrf_token():
        return redirect(url_for('manage_routes'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Route deleted successfully!', 'success')
    return redirect(url_for('manage_routes'))

@app.route('/admin/drivers')
def manage_drivers():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers ORDER BY name")
    drivers = cursor.fetchall()
    conn.close()
    
    return render_template('manage_drivers.html', drivers=drivers)

@app.route('/admin/drivers/add', methods=['POST'])
def add_driver():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    contact = request.form.get('contact')
    password = request.form.get('password')
    
    if not password:
        flash('Password is required!', 'danger')
        return redirect(url_for('manage_drivers'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO drivers (name, contact, password) VALUES (?, ?, ?)",
                   (name, contact, generate_password_hash(password)))
    conn.commit()
    conn.close()
    flash('Driver added successfully!', 'success')
    return redirect(url_for('manage_drivers'))

@app.route('/admin/drivers/edit/<int:id>', methods=['POST'])
def edit_driver(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    contact = request.form.get('contact')
    password = request.form.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if password and password.strip():
        cursor.execute("UPDATE drivers SET name = ?, contact = ?, password = ? WHERE id = ?",
                       (name, contact, generate_password_hash(password), id))
    else:
        cursor.execute("UPDATE drivers SET name = ?, contact = ? WHERE id = ?",
                       (name, contact, id))
    
    conn.commit()
    conn.close()
    flash('Driver updated successfully!', 'success')
    return redirect(url_for('manage_drivers'))

@app.route('/admin/drivers/delete/<int:id>', methods=['POST'])
def delete_driver(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if not validate_csrf_token():
        return redirect(url_for('manage_drivers'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drivers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Driver deleted successfully!', 'success')
    return redirect(url_for('manage_drivers'))

@app.route('/student/dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        flash('Please login as student to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, b.bus_number, b.capacity, r.route_name, r.stops, r.timings, d.name as driver_name, d.contact as driver_contact
        FROM students s
        LEFT JOIN buses b ON s.bus_id = b.id
        LEFT JOIN routes r ON b.route_id = r.id
        LEFT JOIN drivers d ON b.driver_id = d.id
        WHERE s.id = ?
    ''', (session['user_id'],))
    student_info = cursor.fetchone()
    conn.close()
    
    return render_template('student_dashboard.html', student=student_info)

@app.route('/driver/dashboard')
def driver_dashboard():
    if 'role' not in session or session['role'] != 'driver':
        flash('Please login as driver to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT b.*, r.route_name, r.stops, r.timings
        FROM buses b
        LEFT JOIN routes r ON b.route_id = r.id
        WHERE b.driver_id = ?
    ''', (session['user_id'],))
    bus_info = cursor.fetchone()
    
    if bus_info:
        cursor.execute('''
            SELECT name, roll_number
            FROM students
            WHERE bus_id = ?
            ORDER BY name
        ''', (bus_info['id'],))
        students = cursor.fetchall()
    else:
        students = []
    
    conn.close()
    
    return render_template('driver_dashboard.html', bus=bus_info, students=students)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    
    # Production vs Development configuration
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
