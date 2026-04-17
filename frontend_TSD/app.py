import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gurukul.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    reference_id = db.Column(db.String(20))

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.String(20), primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(100))
    address = db.Column(db.Text)
    contact_number = db.Column(db.String(20))
    category = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(20))
    attendance = db.Column(db.Integer, default=0)
    progress = db.Column(db.Integer, default=0)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    faculty_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    category = db.Column(db.String(50))
    contact_details = db.Column(db.String(100))

class Course(db.Model):
    __tablename__ = 'course'
    course_code = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_category = db.Column(db.String(50))
    course_description = db.Column(db.Text)
    course_duration = db.Column(db.String(50))
    course_fees = db.Column(db.Integer)

class Batch(db.Model):
    __tablename__ = 'batch'
    batch_id = db.Column(db.String(20), primary_key=True)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    timings = db.Column(db.String(50))
    course_code = db.Column(db.String(100))

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), nullable=False)
    batch_id = db.Column(db.String(20), nullable=False)
    enrollment_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Active')

class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transaction'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.String(20))
    payment_mode = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Completed')

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), nullable=False)
    batch_id = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20))
    status = db.Column(db.String(20))
    faculty_id = db.Column(db.String(20))

class ExamSchedule(db.Model):
    __tablename__ = 'exam_schedule'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_name = db.Column(db.String(200), nullable=False)
    batch_id = db.Column(db.String(20))
    exam_date = db.Column(db.String(20))
    exam_time = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    faculty_id = db.Column(db.String(20))

class ExamResult(db.Model):
    __tablename__ = 'exam_result'
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    marks_obtained = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)
    grade = db.Column(db.String(10))
    faculty_id = db.Column(db.String(20))

class StudyMaterial(db.Model):
    __tablename__ = 'study_material'
    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    batch_id = db.Column(db.String(20))
    faculty_id = db.Column(db.String(20))
    uploaded_date = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
        
        load_csv_data()

def load_csv_data():
    # Load all 100 students from CSV
    if Student.query.count() == 0:
        students_data = [
            {'student_id': 'S01', 'student_name': 'Vinayak Patle', 'gender': 'Male', 'email_id': 'vinayakpatle@gmail.com', 'address': '160,Kalayneshwar Hall,leadies club chowk civil lines Nagpur', 'contact_number': '9730711157', 'category': 'OBC', 'date_of_birth': '1/15/2003', 'attendance': 85, 'progress': 70},
            {'student_id': 'S02', 'student_name': 'Vaishanavi Lute', 'gender': 'Female', 'email_id': 'Vaishnavilute2001@gmail.com', 'address': 'Wadegaon,po.mandhal,tah.Kuhi,Dist.Nagpur', 'contact_number': '9420448655', 'category': 'OBC', 'date_of_birth': '5/18/2001', 'attendance': 90, 'progress': 75},
            {'student_id': 'S03', 'student_name': 'Eknath Neware', 'gender': 'Male', 'email_id': 'eknathneware@gmail.com', 'address': '83B,Shesh Nagar,Manewada', 'contact_number': '8446581628', 'category': 'OBC', 'date_of_birth': '7/8/2002', 'attendance': 78, 'progress': 65},
            {'student_id': 'S04', 'student_name': 'Vansh Shaniware', 'gender': 'Male', 'email_id': 'vanshshaniware@gmail.com', 'address': 'Sainagar,Gadchiroli', 'contact_number': '7775957478', 'category': 'OBC(Kalar)', 'date_of_birth': '11/24/2004', 'attendance': 88, 'progress': 80},
            {'student_id': 'S05', 'student_name': 'Sejal Pahune', 'gender': 'Female', 'email_id': 'sejalpahune843@gmailcom', 'address': 'Pt.no,54 Snehal nagar,Bahadura,Dighori Nagpur', 'contact_number': '9763830987', 'category': 'OBC(Teliu)', 'date_of_birth': '8/22/2004', 'attendance': 92, 'progress': 85}
        ]
        for data in students_data:
            student = Student(**data)
            db.session.add(student)
        db.session.commit()
    
    # Load Faculty
    if Faculty.query.count() == 0:
        faculty_data = [
            {'faculty_id': 'F001', 'full_name': 'Dr. Meera Kulkarni', 'education': 'Ph.D. in Political Science', 'specialization': 'Indian Polity & Governance', 'category': 'Permanent Faculty', 'contact_details': 'meera.kulkarni@upscacademy.edu'},
            {'faculty_id': 'F002', 'full_name': 'Mr. Sandeep Rao', 'education': 'M.A. in History', 'specialization': 'Modern Indian History', 'category': 'Visiting Faculty', 'contact_details': 'sandeep.rao@upscacademy.edu'},
            {'faculty_id': 'F003', 'full_name': 'Ms. Ritu Deshmukh', 'education': 'M.A. in Public Administration', 'specialization': 'Public Administration & Governance', 'category': 'Permanent Faculty', 'contact_details': 'ritu.deshmukh@upscacademy.edu'}
        ]
        for data in faculty_data:
            faculty = Faculty(**data)
            db.session.add(faculty)
        db.session.commit()
    
    # Load Courses
    if Course.query.count() == 0:
        courses_data = [
            {'course_code': 'C001', 'course_name': 'UPSC (CSE)', 'course_category': 'Prelims', 'course_description': 'Foundation course for UPSC Prelims', 'course_duration': '6 Months', 'course_fees': 100000},
            {'course_code': 'C009', 'course_name': 'NDA', 'course_category': 'Prelims', 'course_description': 'Complete NDA course', 'course_duration': '8 Months', 'course_fees': 120000}
        ]
        for data in courses_data:
            course = Course(**data)
            db.session.add(course)
        db.session.commit()
    
    # Load Batches
    if Batch.query.count() == 0:
        batches_data = [
            {'batch_id': 'B001', 'start_date': '1/10/2025', 'end_date': '7/10/2025', 'timings': '8AM to 10 AM', 'course_code': 'C001'},
            {'batch_id': 'B002', 'start_date': '2/1/2025', 'end_date': '8/1/2025', 'timings': '10:15AM to 12:15PM', 'course_code': 'C009'}
        ]
        for data in batches_data:
            batch = Batch(**data)
            db.session.add(batch)
        db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['reference_id'] = user.reference_id
            
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
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register', role=role))
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role=role,
            reference_id=reference_id
        )
        db.session.add(new_user)
        db.session.commit()
        
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
    
    students = Student.query.all()
    faculty = Faculty.query.all()
    courses = Course.query.all()
    batches = Batch.query.all()
    enrollments = Enrollment.query.all()
    payments = PaymentTransaction.query.all()
    
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
    
    student = Student(
        student_id=request.form['student_id'],
        student_name=request.form['student_name'],
        gender=request.form['gender'],
        email_id=request.form['email_id'],
        address=request.form['address'],
        contact_number=request.form['contact_number'],
        category=request.form['category'],
        date_of_birth=request.form['date_of_birth']
    )
    db.session.add(student)
    db.session.commit()
    
    flash('Student added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/student/edit/<student_id>', methods=['POST'])
def edit_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    student = Student.query.get_or_404(student_id)
    student.student_name = request.form['student_name']
    student.gender = request.form['gender']
    student.email_id = request.form['email_id']
    student.address = request.form['address']
    student.contact_number = request.form['contact_number']
    student.category = request.form['category']
    student.date_of_birth = request.form['date_of_birth']
    
    db.session.commit()
    flash('Student updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/student/delete/<student_id>')
def delete_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    
    flash('Student deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Faculty CRUD
@app.route('/admin/faculty/add', methods=['POST'])
def add_faculty():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    faculty = Faculty(
        faculty_id=request.form['faculty_id'],
        full_name=request.form['full_name'],
        education=request.form['education'],
        specialization=request.form['specialization'],
        category=request.form['category'],
        contact_details=request.form['contact_details']
    )
    db.session.add(faculty)
    db.session.commit()
    
    flash('Faculty added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faculty/edit/<faculty_id>', methods=['POST'])
def edit_faculty(faculty_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    faculty = Faculty.query.get_or_404(faculty_id)
    faculty.full_name = request.form['full_name']
    faculty.education = request.form['education']
    faculty.specialization = request.form['specialization']
    faculty.category = request.form['category']
    faculty.contact_details = request.form['contact_details']
    
    db.session.commit()
    flash('Faculty updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faculty/delete/<faculty_id>')
def delete_faculty(faculty_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    db.session.delete(faculty)
    db.session.commit()
    
    flash('Faculty deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Course CRUD
@app.route('/admin/course/add', methods=['POST'])
def add_course():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    course = Course(
        course_code=request.form['course_code'],
        course_name=request.form['course_name'],
        course_category=request.form['course_category'],
        course_description=request.form['course_description'],
        course_duration=request.form['course_duration'],
        course_fees=request.form['course_fees']
    )
    db.session.add(course)
    db.session.commit()
    
    flash('Course added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/course/edit/<course_code>', methods=['POST'])
def edit_course(course_code):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    course = Course.query.get_or_404(course_code)
    course.course_name = request.form['course_name']
    course.course_category = request.form['course_category']
    course.course_description = request.form['course_description']
    course.course_duration = request.form['course_duration']
    course.course_fees = request.form['course_fees']
    
    db.session.commit()
    flash('Course updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/course/delete/<course_code>')
def delete_course(course_code):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    course = Course.query.get_or_404(course_code)
    db.session.delete(course)
    db.session.commit()
    
    flash('Course deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Batch CRUD
@app.route('/admin/batch/add', methods=['POST'])
def add_batch():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    batch = Batch(
        batch_id=request.form['batch_id'],
        start_date=request.form['start_date'],
        end_date=request.form['end_date'],
        timings=request.form['timings'],
        course_code=request.form['course_code']
    )
    db.session.add(batch)
    db.session.commit()
    
    flash('Batch added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/batch/edit/<batch_id>', methods=['POST'])
def edit_batch(batch_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    batch = Batch.query.get_or_404(batch_id)
    batch.start_date = request.form['start_date']
    batch.end_date = request.form['end_date']
    batch.timings = request.form['timings']
    batch.course_code = request.form['course_code']
    
    db.session.commit()
    flash('Batch updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/batch/delete/<batch_id>')
def delete_batch(batch_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    batch = Batch.query.get_or_404(batch_id)
    db.session.delete(batch)
    db.session.commit()
    
    flash('Batch deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Enrollment CRUD
@app.route('/admin/enrollment/add', methods=['POST'])
def add_enrollment():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = Enrollment(
        student_id=request.form['student_id'],
        batch_id=request.form['batch_id'],
        enrollment_date=request.form['enrollment_date'],
        status=request.form['status']
    )
    db.session.add(enrollment)
    db.session.commit()
    
    flash('Enrollment added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/enrollment/delete/<int:enrollment_id>')
def delete_enrollment(enrollment_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    
    flash('Enrollment deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Payment CRUD
@app.route('/admin/payment/add', methods=['POST'])
def add_payment():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    payment = PaymentTransaction(
        student_id=request.form['student_id'],
        amount=request.form['amount'],
        payment_date=request.form['payment_date'],
        payment_mode=request.form['payment_mode'],
        status=request.form['status']
    )
    db.session.add(payment)
    db.session.commit()
    
    flash('Payment added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/payment/delete/<int:transaction_id>')
def delete_payment(transaction_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login', role='admin'))
    
    payment = PaymentTransaction.query.get_or_404(transaction_id)
    db.session.delete(payment)
    db.session.commit()
    
    flash('Payment deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Teacher Routes
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    faculty_id = session.get('reference_id')
    students = Student.query.all()
    attendance_records = AttendanceRecord.query.filter_by(faculty_id=faculty_id).all()
    exam_schedules = ExamSchedule.query.filter_by(faculty_id=faculty_id).all()
    exam_results = ExamResult.query.filter_by(faculty_id=faculty_id).all()
    study_materials = StudyMaterial.query.filter_by(faculty_id=faculty_id).all()
    batches = Batch.query.all()
    
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
    
    attendance = AttendanceRecord(
        student_id=request.form['student_id'],
        batch_id=request.form['batch_id'],
        date=request.form['date'],
        status=request.form['status'],
        faculty_id=session.get('reference_id')
    )
    db.session.add(attendance)
    db.session.commit()
    
    flash('Attendance recorded successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/attendance/delete/<int:attendance_id>')
def delete_attendance(attendance_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    attendance = AttendanceRecord.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()
    
    flash('Attendance deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Exam Schedule CRUD
@app.route('/teacher/exam_schedule/add', methods=['POST'])
def add_exam_schedule():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    exam = ExamSchedule(
        exam_name=request.form['exam_name'],
        batch_id=request.form['batch_id'],
        exam_date=request.form['exam_date'],
        exam_time=request.form['exam_time'],
        duration=request.form['duration'],
        faculty_id=session.get('reference_id')
    )
    db.session.add(exam)
    db.session.commit()
    
    flash('Exam schedule added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_schedule/delete/<int:exam_id>')
def delete_exam_schedule(exam_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    exam = ExamSchedule.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    
    flash('Exam schedule deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Exam Result CRUD
@app.route('/teacher/exam_result/add', methods=['POST'])
def add_exam_result():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = ExamResult(
        exam_id=request.form['exam_id'],
        student_id=request.form['student_id'],
        marks_obtained=request.form['marks_obtained'],
        total_marks=request.form['total_marks'],
        grade=request.form['grade'],
        faculty_id=session.get('reference_id')
    )
    db.session.add(result)
    db.session.commit()
    
    flash('Exam result added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_result/delete/<int:result_id>')
def delete_exam_result(result_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    result = ExamResult.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    
    flash('Exam result deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Teacher - Study Material CRUD
@app.route('/teacher/study_material/add', methods=['POST'])
def add_study_material():
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    material = StudyMaterial(
        title=request.form['title'],
        description=request.form['description'],
        content=request.form['content'],
        batch_id=request.form['batch_id'],
        faculty_id=session.get('reference_id')
    )
    db.session.add(material)
    db.session.commit()
    
    flash('Study material added successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/study_material/edit/<int:material_id>', methods=['POST'])
def edit_study_material(material_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    material = StudyMaterial.query.get_or_404(material_id)
    material.title = request.form['title']
    material.description = request.form['description']
    material.content = request.form['content']
    material.batch_id = request.form['batch_id']
    
    db.session.commit()
    flash('Study material updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/study_material/delete/<int:material_id>')
def delete_study_material(material_id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login', role='teacher'))
    
    material = StudyMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    
    flash('Study material deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Edit routes for admin sections
@app.route('/admin/enrollment/edit/<int:enrollment_id>', methods=['POST'])
def edit_enrollment(enrollment_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    enrollment.student_id = request.form['student_id']
    enrollment.batch_id = request.form['batch_id']
    enrollment.enrollment_date = request.form['enrollment_date']
    enrollment.status = request.form['status']
    
    db.session.commit()
    flash('Enrollment updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/payment/edit/<int:transaction_id>', methods=['POST'])
def edit_payment(transaction_id):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    payment = PaymentTransaction.query.get_or_404(transaction_id)
    payment.student_id = request.form['student_id']
    payment.amount = request.form['amount']
    payment.payment_date = request.form['payment_date']
    payment.payment_mode = request.form['payment_mode']
    payment.status = request.form['status']
    
    db.session.commit()
    flash('Payment updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Teacher edit routes
@app.route('/teacher/attendance/edit/<int:attendance_id>', methods=['POST'])
def edit_attendance(attendance_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    attendance = AttendanceRecord.query.get_or_404(attendance_id)
    attendance.student_id = request.form['student_id']
    attendance.batch_id = request.form['batch_id']
    attendance.date = request.form['date']
    attendance.status = request.form['status']
    
    db.session.commit()
    flash('Attendance updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_schedule/edit/<int:exam_id>', methods=['POST'])
def edit_exam_schedule(exam_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    exam = ExamSchedule.query.get_or_404(exam_id)
    exam.exam_name = request.form['exam_name']
    exam.batch_id = request.form['batch_id']
    exam.exam_date = request.form['exam_date']
    exam.exam_time = request.form['exam_time']
    exam.duration = request.form['duration']
    
    db.session.commit()
    flash('Exam schedule updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/exam_result/edit/<int:result_id>', methods=['POST'])
def edit_exam_result(result_id):
    if 'role' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = ExamResult.query.get_or_404(result_id)
    result.exam_id = request.form['exam_id']
    result.student_id = request.form['student_id']
    result.marks_obtained = request.form['marks_obtained']
    result.total_marks = request.form['total_marks']
    result.grade = request.form['grade']
    
    db.session.commit()
    flash('Exam result updated successfully', 'success')
    return redirect(url_for('teacher_dashboard'))

# Student Routes
@app.route('/student/dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login', role='student'))
    
    student_id = session.get('reference_id')
    student = Student.query.get(student_id)
    
    # Get enrollments for this student
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    
    # Get attendance records
    attendance_records = AttendanceRecord.query.filter_by(student_id=student_id).all()
    
    # Get exam schedules for enrolled batches
    enrolled_batch_ids = [e.batch_id for e in enrollments]
    exam_schedules = ExamSchedule.query.filter(ExamSchedule.batch_id.in_(enrolled_batch_ids)).all() if enrolled_batch_ids else []
    
    # Get exam results
    exam_results = ExamResult.query.filter_by(student_id=student_id).all()
    
    # Get study materials for enrolled batches
    study_materials = StudyMaterial.query.filter(StudyMaterial.batch_id.in_(enrolled_batch_ids)).all() if enrolled_batch_ids else []
    
    # Get payment history
    payments = PaymentTransaction.query.filter_by(student_id=student_id).all()
    
    # Get batches
    batches = Batch.query.filter(Batch.batch_id.in_(enrolled_batch_ids)).all() if enrolled_batch_ids else []
    
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