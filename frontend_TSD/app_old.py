import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# MongoDB Configuration - Replace with your actual MongoDB URI
MONGO_URI = 'your-mongodb-connection-string'  # e.g., 'mongodb://localhost:27017/' or cloud URI
client = MongoClient(MONGO_URI)
db = client['coaching_management']

# Collections
users_collection = db['users']
students_collection = db['students']
faculty_collection = db['faculty']
courses_collection = db['courses']
batches_collection = db['batches']
enrollments_collection = db['enrollments']
payments_collection = db['payments']
attendance_collection = db['attendance']
exam_schedules_collection = db['exam_schedules']
exam_results_collection = db['exam_results']
study_materials_collection = db['study_materials']

def init_db():
    # Create default admin user
    if users_collection.find_one({'username': 'admin'}) is None:
        admin = {
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'role': 'admin',
            'reference_id': None
        }
        users_collection.insert_one(admin)
    
    # Load sample data
    load_csv_data()

def load_csv_data():
    # Load students
    if students_collection.count_documents({}) == 0:
        students_data = [
            {'student_id': 'S01', 'student_name': 'Vinayak Patle', 'gender': 'Male', 'email_id': 'vinayakpatle@gmail.com', 'address': '160,Kalayneshwar Hall,leadies club chowk civil lines Nagpur', 'contact_number': '9730711157', 'category': 'OBC', 'date_of_birth': '1/15/2003', 'attendance': 85, 'progress': 70},
            {'student_id': 'S02', 'student_name': 'Vaishanavi Lute', 'gender': 'Female', 'email_id': 'Vaishnavilute2001@gmail.com', 'address': 'Wadegaon,po.mandhal,tah.Kuhi,Dist.Nagpur', 'contact_number': '9420448655', 'category': 'OBC', 'date_of_birth': '5/18/2001', 'attendance': 90, 'progress': 75},
            {'student_id': 'S03', 'student_name': 'Eknath Neware', 'gender': 'Male', 'email_id': 'eknathneware@gmail.com', 'address': '83B,Shesh Nagar,Manewada', 'contact_number': '8446581628', 'category': 'OBC', 'date_of_birth': '7/8/2002', 'attendance': 78, 'progress': 65},
            {'student_id': 'S04', 'student_name': 'Vansh Shaniware', 'gender': 'Male', 'email_id': 'vanshshaniware@gmail.com', 'address': 'Sainagar,Gadchiroli', 'contact_number': '7775957478', 'category': 'OBC(Kalar)', 'date_of_birth': '11/24/2004', 'attendance': 88, 'progress': 80},
            {'student_id': 'S05', 'student_name': 'Sejal Pahune', 'gender': 'Female', 'email_id': 'sejalpahune843@gmailcom', 'address': 'Pt.no,54 Snehal nagar,Bahadura,Dighori Nagpur', 'contact_number': '9763830987', 'category': 'OBC(Teliu)', 'date_of_birth': '8/22/2004', 'attendance': 92, 'progress': 85}
        ]
        students_collection.insert_many(students_data)
    
    # Load Faculty
    if faculty_collection.count_documents({}) == 0:
        faculty_data = [
            {'faculty_id': 'F001', 'full_name': 'Dr. Meera Kulkarni', 'education': 'Ph.D. in Political Science', 'specialization': 'Indian Polity & Governance', 'category': 'Permanent Faculty', 'contact_details': 'meera.kulkarni@upscacademy.edu'},
            {'faculty_id': 'F002', 'full_name': 'Mr. Sandeep Rao', 'education': 'M.A. in History', 'specialization': 'Modern Indian History', 'category': 'Visiting Faculty', 'contact_details': 'sandeep.rao@upscacademy.edu'},
            {'faculty_id': 'F003', 'full_name': 'Ms. Ritu Deshmukh', 'education': 'M.A. in Public Administration', 'specialization': 'Public Administration & Governance', 'category': 'Permanent Faculty', 'contact_details': 'ritu.deshmukh@upscacademy.edu'}
        ]
        faculty_collection.insert_many(faculty_data)
    
    # Load Courses
    if courses_collection.count_documents({}) == 0:
        courses_data = [
            {'course_code': 'C001', 'course_name': 'UPSC (CSE)', 'course_category': 'Prelims', 'course_description': 'Foundation course for UPSC Prelims', 'course_duration': '6 Months', 'course_fees': 100000},
            {'course_code': 'C009', 'course_name': 'NDA', 'course_category': 'Prelims', 'course_description': 'Complete NDA course', 'course_duration': '8 Months', 'course_fees': 120000}
        ]
        courses_collection.insert_many(courses_data)
    
    # Load Batches
    if batches_collection.count_documents({}) == 0:
        batches_data = [
            {'batch_id': 'B001', 'start_date': '1/10/2025', 'end_date': '7/10/2025', 'timings': '8AM to 10 AM', 'course_code': 'C001'},
            {'batch_id': 'B002', 'start_date': '2/1/2025', 'end_date': '8/1/2025', 'timings': '10:15AM to 12:15PM', 'course_code': 'C009'}
        ]
        batches_collection.insert_many(batches_data)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username, 'role': role})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            session['reference_id'] = user.get('reference_id')
            
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html', role=role)

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        reference_id = request.form.get('reference_id')
        
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register', role=role))
        
        new_user = {
            'username': username,
            'password': generate_password_hash(password),
            'role': role,
            'reference_id': reference_id
        }
        users_collection.insert_one(new_user)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login', role=role))
    
    return render_template('register.html', role=role)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    students = list(students_collection.find())
    faculty = list(faculty_collection.find())
    courses = list(courses_collection.find())
    batches = list(batches_collection.find())
    enrollments = list(enrollments_collection.find())
    payments = list(payments_collection.find())
    
    return render_template('admin_dashboard.html', 
                         students=students, 
                         faculty=faculty, 
                         courses=courses, 
                         batches=batches,
                         enrollments=enrollments,
                         payments=payments)

# Student CRUD
@app.route('/admin/student/add', methods=['POST'])
def add_student():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    student = {
        'student_id': request.form['student_id'],
        'student_name': request.form['student_name'],
        'gender': request.form['gender'],
        'email_id': request.form['email_id'],
        'address': request.form['address'],
        'contact_number': request.form['contact_number'],
        'category': request.form['category'],
        'date_of_birth': request.form['date_of_birth'],
        'attendance': 0,
        'progress': 0
    }
    students_collection.insert_one(student)
    
    flash('Student added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/student/edit/<student_id>', methods=['POST'])
def edit_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'student_name': request.form['student_name'],
        'gender': request.form['gender'],
        'email_id': request.form['email_id'],
        'address': request.form['address'],
        'contact_number': request.form['contact_number'],
        'category': request.form['category'],
        'date_of_birth': request.form['date_of_birth']
    }
    students_collection.update_one({'student_id': student_id}, {'$set': update_data})
    flash('Student updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/student/delete/<student_id>')
def delete_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    students_collection.delete_one({'student_id': student_id})
    
    flash('Student deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Faculty CRUD
@app.route('/admin/faculty/add', methods=['POST'])
def add_faculty():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    faculty = {
        'faculty_id': request.form['faculty_id'],
        'full_name': request.form['full_name'],
        'education': request.form['education'],
        'specialization': request.form['specialization'],
        'category': request.form['category'],
        'contact_details': request.form['contact_details']
    }
    faculty_collection.insert_one(faculty)
    
    flash('Faculty added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faculty/edit/<faculty_id>', methods=['POST'])
def edit_faculty(faculty_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'full_name': request.form['full_name'],
        'education': request.form['education'],
        'specialization': request.form['specialization'],
        'category': request.form['category'],
        'contact_details': request.form['contact_details']
    }
    faculty_collection.update_one({'faculty_id': faculty_id}, {'$set': update_data})
    flash('Faculty updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faculty/delete/<faculty_id>')
def delete_faculty(faculty_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    faculty_collection.delete_one({'faculty_id': faculty_id})
    
    flash('Faculty deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Course CRUD
@app.route('/admin/course/add', methods=['POST'])
def add_course():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    course = {
        'course_code': request.form['course_code'],
        'course_name': request.form['course_name'],
        'course_category': request.form['course_category'],
        'course_description': request.form['course_description'],
        'course_duration': request.form['course_duration'],
        'course_fees': int(request.form['course_fees'])
    }
    courses_collection.insert_one(course)
    
    flash('Course added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/course/edit/<course_code>', methods=['POST'])
def edit_course(course_code):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'course_name': request.form['course_name'],
        'course_category': request.form['course_category'],
        'course_description': request.form['course_description'],
        'course_duration': request.form['course_duration'],
        'course_fees': int(request.form['course_fees'])
    }
    courses_collection.update_one({'course_code': course_code}, {'$set': update_data})
    flash('Course updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/course/delete/<course_code>')
def delete_course(course_code):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    courses_collection.delete_one({'course_code': course_code})
    
    flash('Course deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Batch CRUD
@app.route('/admin/batch/add', methods=['POST'])
def add_batch():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    batch = {
        'batch_id': request.form['batch_id'],
        'start_date': request.form['start_date'],
        'end_date': request.form['end_date'],
        'timings': request.form['timings'],
        'course_code': request.form['course_code']
    }
    batches_collection.insert_one(batch)
    
    flash('Batch added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/batch/edit/<batch_id>', methods=['POST'])
def edit_batch(batch_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'start_date': request.form['start_date'],
        'end_date': request.form['end_date'],
        'timings': request.form['timings'],
        'course_code': request.form['course_code']
    }
    batches_collection.update_one({'batch_id': batch_id}, {'$set': update_data})
    flash('Batch updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/batch/delete/<batch_id>')
def delete_batch(batch_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    batches_collection.delete_one({'batch_id': batch_id})
    
    flash('Batch deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Enrollment CRUD
@app.route('/admin/enrollment/add', methods=['POST'])
def add_enrollment():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = {
        'student_id': request.form['student_id'],
        'batch_id': request.form['batch_id'],
        'enrollment_date': request.form['enrollment_date'],
        'status': request.form['status']
    }
    enrollments_collection.insert_one(enrollment)
    
    flash('Enrollment added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/enrollment/edit/<enrollment_id>', methods=['POST'])
def edit_enrollment(enrollment_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'student_id': request.form['student_id'],
        'batch_id': request.form['batch_id'],
        'enrollment_date': request.form['enrollment_date'],
        'status': request.form['status']
    }
    enrollments_collection.update_one({'_id': enrollment_id}, {'$set': update_data})
    flash('Enrollment updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/enrollment/delete/<enrollment_id>')
def delete_enrollment(enrollment_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    enrollments_collection.delete_one({'_id': enrollment_id})
    
    flash('Enrollment deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Payment CRUD
@app.route('/admin/payment/add', methods=['POST'])
def add_payment():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    payment = {
        'student_id': request.form['student_id'],
        'amount': int(request.form['amount']),
        'payment_date': request.form['payment_date'],
        'payment_mode': request.form['payment_mode'],
        'status': request.form['status']
    }
    payments_collection.insert_one(payment)
    
    flash('Payment added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/payment/edit/<transaction_id>', methods=['POST'])
def edit_payment(transaction_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'student_id': request.form['student_id'],
        'amount': int(request.form['amount']),
        'payment_date': request.form['payment_date'],
        'payment_mode': request.form['payment_mode'],
        'status': request.form['status']
    }
    payments_collection.update_one({'_id': transaction_id}, {'$set': update_data})
    flash('Payment updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/payment/delete/<transaction_id>')
def delete_payment(transaction_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    payments_collection.delete_one({'_id': transaction_id})
    
    flash('Payment deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Teacher Routes
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    faculty_id = session.get('reference_id')
    students = list(students_collection.find())
    attendance_records = list(attendance_collection.find({'faculty_id': faculty_id}))
    exam_schedules = list(exam_schedules_collection.find({'faculty_id': faculty_id}))
    exam_results = list(exam_results_collection.find({'faculty_id': faculty_id}))
    study_materials = list(study_materials_collection.find({'faculty_id': faculty_id}))
    batches = list(batches_collection.find())
    
    return render_template('teacher_dashboard.html', 
                         students=students,
                         attendance_records=attendance_records,
                         exam_schedules=exam_schedules,
                         exam_results=exam_results,
                         study_materials=study_materials,
                         batches=batches)

# Teacher - Attendance CRUD
@app.route('/teacher/attendance/add', methods=['POST'])
def add_attendance():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    attendance = {
        'student_id': request.form['student_id'],
        'batch_id': request.form['batch_id'],
        'date': request.form['date'],
        'status': request.form['status'],
        'faculty_id': session.get('reference_id')
    }
    attendance_collection.insert_one(attendance)
    
    flash('Attendance recorded successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/attendance/edit/<attendance_id>', methods=['POST'])
def edit_attendance(attendance_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'student_id': request.form['student_id'],
        'batch_id': request.form['batch_id'],
        'date': request.form['date'],
        'status': request.form['status']
    }
    attendance_collection.update_one({'_id': attendance_id}, {'$set': update_data})
    flash('Attendance updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/attendance/delete/<attendance_id>')
def delete_attendance(attendance_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    attendance_collection.delete_one({'_id': attendance_id})
    
    flash('Attendance deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Exam Schedule CRUD
@app.route('/teacher/exam_schedule/add', methods=['POST'])
def add_exam_schedule():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    exam = {
        'exam_name': request.form['exam_name'],
        'batch_id': request.form['batch_id'],
        'exam_date': request.form['exam_date'],
        'exam_time': request.form['exam_time'],
        'duration': request.form['duration'],
        'faculty_id': session.get('reference_id')
    }
    exam_schedules_collection.insert_one(exam)
    
    flash('Exam schedule added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_schedule/edit/<exam_id>', methods=['POST'])
def edit_exam_schedule(exam_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'exam_name': request.form['exam_name'],
        'batch_id': request.form['batch_id'],
        'exam_date': request.form['exam_date'],
        'exam_time': request.form['exam_time'],
        'duration': request.form['duration']
    }
    exam_schedules_collection.update_one({'_id': exam_id}, {'$set': update_data})
    flash('Exam schedule updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_schedule/delete/<exam_id>')
def delete_exam_schedule(exam_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    exam_schedules_collection.delete_one({'_id': exam_id})
    
    flash('Exam schedule deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Exam Result CRUD
@app.route('/teacher/exam_result/add', methods=['POST'])
def add_exam_result():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = {
        'exam_id': request.form['exam_id'],
        'student_id': request.form['student_id'],
        'marks_obtained': int(request.form['marks_obtained']),
        'total_marks': int(request.form['total_marks']),
        'grade': request.form['grade'],
        'faculty_id': session.get('reference_id')
    }
    exam_results_collection.insert_one(result)
    
    flash('Exam result added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_result/edit/<result_id>', methods=['POST'])
def edit_exam_result(result_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'exam_id': request.form['exam_id'],
        'student_id': request.form['student_id'],
        'marks_obtained': int(request.form['marks_obtained']),
        'total_marks': int(request.form['total_marks']),
        'grade': request.form['grade']
    }
    exam_results_collection.update_one({'_id': result_id}, {'$set': update_data})
    flash('Exam result updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_result/delete/<result_id>')
def delete_exam_result(result_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    exam_results_collection.delete_one({'_id': result_id})
    
    flash('Exam result deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Study Material CRUD
@app.route('/teacher/study_material/add', methods=['POST'])
def add_study_material():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    material = {
        'title': request.form['title'],
        'description': request.form['description'],
        'content': request.form['content'],
        'batch_id': request.form['batch_id'],
        'faculty_id': session.get('reference_id'),
        'uploaded_date': datetime.utcnow()
    }
    study_materials_collection.insert_one(material)
    
    flash('Study material added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/study_material/edit/<material_id>', methods=['POST'])
def edit_study_material(material_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    update_data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'content': request.form['content'],
        'batch_id': request.form['batch_id']
    }
    study_materials_collection.update_one({'_id': material_id}, {'$set': update_data})
    flash('Study material updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/study_material/delete/<material_id>')
def delete_study_material(material_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    study_materials_collection.delete_one({'_id': material_id})
    
    flash('Study material deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Student Routes
@app.route('/student/dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login', role='student'))
    
    student_id = session.get('reference_id')
    student = students_collection.find_one({'student_id': student_id})
    
    # Get enrollments for this student
    enrollments = list(enrollments_collection.find({'student_id': student_id}))
    
    # Get attendance records
    attendance_records = list(attendance_collection.find({'student_id': student_id}))
    
    # Get exam schedules for enrolled batches
    enrolled_batch_ids = [e['batch_id'] for e in enrollments]
    exam_schedules = list(exam_schedules_collection.find({'batch_id': {'$in': enrolled_batch_ids}})) if enrolled_batch_ids else []
    
    # Get exam results
    exam_results = list(exam_results_collection.find({'student_id': student_id}))
    
    # Get study materials for enrolled batches
    study_materials = list(study_materials_collection.find({'batch_id': {'$in': enrolled_batch_ids}})) if enrolled_batch_ids else []
    
    # Get payment history
    payments = list(payments_collection.find({'student_id': student_id}))
    
    # Get batches
    batches = list(batches_collection.find({'batch_id': {'$in': enrolled_batch_ids}})) if enrolled_batch_ids else []
    
    return render_template('student_dashboard.html', 
                         student=student,
                         enrollments=enrollments,
                         attendance_records=attendance_records,
                         exam_schedules=exam_schedules,
                         exam_results=exam_results,
                         study_materials=study_materials,
                         payments=payments,
                         batches=batches)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
