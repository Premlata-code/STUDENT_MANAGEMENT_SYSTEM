from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Change this to a random secret key

# File path for JSON database
DATA_FILE = 'students.json'

def init_data_file():
    """Initialize the data file if it doesn't exist"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"students": [], "next_id": 1}, f, indent=4)

def load_students():
    """Load all students from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"students": [], "next_id": 1}

def save_students(data):
    """Save students data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def find_student_by_id(student_id):
    """Find a student by ID"""
    data = load_students()
    for student in data['students']:
        if student['id'] == student_id:
            return student
    return None

# ========== ROUTES ==========

# Homepage
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

# View all students
@app.route('/view_students')
def view_students():
    data = load_students()
    students = data['students']
    return render_template('view_students.html', students=students)

# View single student
@app.route('/view_student/<int:student_id>')
def view_student(student_id):
    student = find_student_by_id(student_id)
    if student:
        return render_template('view_student.html', student=student)
    else:
        flash('Student not found!', 'error')
        return redirect(url_for('view_students'))

# Add new student (GET & POST)
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    
    elif request.method == 'POST':
        # Get form data
        roll_no = request.form.get('roll_no', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        year = request.form.get('year', '').strip()
        grade = request.form.get('grade', '').strip()
        attendance = request.form.get('attendance', '0').strip()
        fees_paid = request.form.get('fees_paid') == 'true'
        address = request.form.get('address', '').strip()
        
        # Basic validation
        if not all([roll_no, name, email, phone, course, year, grade, attendance]):
            flash('Please fill all required fields!', 'error')
            return render_template('add_student.html')
        
        try:
            attendance = int(attendance)
            if attendance < 0 or attendance > 100:
                flash('Attendance must be between 0 and 100!', 'error')
                return render_template('add_student.html')
        except ValueError:
            flash('Invalid attendance value!', 'error')
            return render_template('add_student.html')
        
        # Load existing data
        data = load_students()
        
        # Check if roll number already exists
        for student in data['students']:
            if student['roll_no'] == roll_no:
                flash(f'Roll number {roll_no} already exists!', 'error')
                return render_template('add_student.html')
        
        # Create new student
        new_student = {
            'id': data['next_id'],
            'roll_no': roll_no,
            'name': name,
            'email': email,
            'phone': phone,
            'course': course,
            'year': year,
            'grade': grade,
            'attendance': attendance,
            'attendance_percent': f"{attendance}%",
            'fees_paid': fees_paid,
            'address': address,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to students list
        data['students'].append(new_student)
        data['next_id'] += 1
        
        # Save to file
        save_students(data)
        
        flash(f'Student {name} added successfully!', 'success')
        return redirect(url_for('view_students'))

# Edit student (GET & POST)
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    # Find the student
    student = find_student_by_id(student_id)
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('view_students'))
    
    if request.method == 'GET':
        return render_template('edit_student.html', student=student)
    
    elif request.method == 'POST':
        # Get form data
        roll_no = request.form.get('roll_no', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        year = request.form.get('year', '').strip()
        grade = request.form.get('grade', '').strip()
        attendance = request.form.get('attendance', '0').strip()
        fees_paid = request.form.get('fees_paid') == 'true'
        address = request.form.get('address', '').strip()
        
        # Basic validation
        if not all([roll_no, name, email, phone, course, year, grade, attendance]):
            flash('Please fill all required fields!', 'error')
            return render_template('edit_student.html', student=student)
        
        try:
            attendance = int(attendance)
            if attendance < 0 or attendance > 100:
                flash('Attendance must be between 0 and 100!', 'error')
                return render_template('edit_student.html', student=student)
        except ValueError:
            flash('Invalid attendance value!', 'error')
            return render_template('edit_student.html', student=student)
        
        # Load existing data
        data = load_students()
        
        # Check if roll number already exists (excluding current student)
        for s in data['students']:
            if s['id'] != student_id and s['roll_no'] == roll_no:
                flash(f'Roll number {roll_no} already exists!', 'error')
                return render_template('edit_student.html', student=student)
        
        # Update student data
        for s in data['students']:
            if s['id'] == student_id:
                s['roll_no'] = roll_no
                s['name'] = name
                s['email'] = email
                s['phone'] = phone
                s['course'] = course
                s['year'] = year
                s['grade'] = grade
                s['attendance'] = attendance
                s['attendance_percent'] = f"{attendance}%"
                s['fees_paid'] = fees_paid
                s['address'] = address
                s['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
        
        # Save to file
        save_students(data)
        
        flash(f'Student {name} updated successfully!', 'success')
        return redirect(url_for('view_student', student_id=student_id))

# Delete student
@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    # Load existing data
    data = load_students()
    
    # Find and remove student
    student_name = None
    for student in data['students']:
        if student['id'] == student_id:
            student_name = student['name']
            break
    
    if student_name:
        data['students'] = [s for s in data['students'] if s['id'] != student_id]
        save_students(data)
        flash(f'Student {student_name} deleted successfully!', 'success')
    else:
        flash('Student not found!', 'error')
    
    return redirect(url_for('view_students'))

# Search students
@app.route('/search')
def search_students():
    query = request.args.get('q', '').lower().strip()
    data = load_students()
    
    if not query:
        return redirect(url_for('view_students'))
    
    # Filter students based on search query
    filtered_students = []
    for student in data['students']:
        if (query in student['name'].lower() or 
            query in student['roll_no'].lower() or 
            query in student['course'].lower() or
            query in student['email'].lower()):
            filtered_students.append(student)
    
    return render_template('view_students.html', 
                          students=filtered_students, 
                          search_query=query)

# API endpoints for statistics
@app.route('/api/stats')
def api_stats():
    data = load_students()
    students = data['students']
    
    # Calculate statistics
    total_students = len(students)
    
    # Count unique courses
    courses = set()
    for student in students:
        courses.add(student['course'])
    total_courses = len(courses)
    
    # Count students with fees paid
    active_students = sum(1 for student in students if student['fees_paid'])
    
    return jsonify({
        'total_students': total_students,
        'total_courses': total_courses,
        'active_students': active_students
    })

# API endpoint to get all students (JSON format)
@app.route('/api/students')
def api_students():
    data = load_students()
    return jsonify(data['students'])

# ========== MAIN ==========
if __name__ == "__main__":
    # Initialize data file and directories
    init_data_file()
    
    # Create templates directory if not exists
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    
    app.run(debug=True, port=5000)