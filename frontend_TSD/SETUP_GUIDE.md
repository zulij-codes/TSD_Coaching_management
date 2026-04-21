# TSD Coaching Management System - Setup & Running Guide

## ✅ Project Status
- **Backend**: Complete with MongoDB integration
- **Frontend**: 7 HTML templates ready
- **Database**: MongoDB Atlas configured
- **Framework**: Flask with PyMongo

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
cd frontend_TSD
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 3: Access the System
- **Home Page**: http://localhost:5000/
- **Admin Login**: http://localhost:5000/login/admin
  - Username: `admin`
  - Password: `admin123`
- **Teacher Login**: http://localhost:5000/login/teacher
- **Student Login**: http://localhost:5000/login/student

## 📁 Project Structure

```
frontend_TSD/
├── app.py                 # Main Flask application with MongoDB integration
├── requirements.txt       # Python dependencies
├── instance/             # Instance folder for Flask
└── templates/            # HTML templates
    ├── base.html                # Base template
    ├── index.html               # Home page
    ├── login.html               # Login page
    ├── register.html            # Registration page
    ├── admin_dashboard.html     # Admin panel
    ├── teacher_dashboard.html   # Teacher panel
    └── student_dashboard.html   # Student panel
```

## 🗄️ Database Configuration

MongoDB Atlas Connection Details:
- **Database Name**: `coaching_management`
- **Connection URI**: Already configured in `app.py`

### Collections Created Automatically:
- `users` - User authentication
- `students` - Student information
- `faculty` - Faculty/Teacher information
- `courses` - Course details
- `batches` - Batch information
- `enrollments` - Student-Batch enrollments
- `payments` - Payment transactions
- `attendance` - Attendance records
- `exam_schedules` - Exam scheduling
- `exam_results` - Student exam results
- `study_materials` - Educational materials

## 🔑 Default Credentials

**Admin Account** (Auto-created on first run):
- Username: `admin`
- Password: `admin123`

**Registration**:
- Teachers and Students can register new accounts
- Each role has access to specific features

## 📋 Features by Role

### Admin
- ✅ Manage Students (CRUD operations)
- ✅ Manage Faculty/Teachers (CRUD operations)
- ✅ Manage Courses (CRUD operations)
- ✅ Manage Batches (CRUD operations)
- ✅ Handle Enrollments
- ✅ Track Payments
- ✅ View System-wide Statistics

### Teacher
- ✅ Mark Student Attendance
- ✅ Schedule Exams
- ✅ Record Exam Results
- ✅ Upload Study Materials
- ✅ View Student Information
- ✅ Manage Batches

### Student
- ✅ View Personal Profile
- ✅ Check Enrollments
- ✅ View Attendance Records
- ✅ Check Exam Schedules & Results
- ✅ Access Study Materials
- ✅ View Payment History

## 🔧 Troubleshooting

### MongoDB Connection Issues
- Verify internet connection
- Check MongoDB URI is correct in `app.py`
- Ensure MongoDB Atlas cluster is running
- Check firewall/VPN settings

### Port Already in Use
If port 5000 is in use:
```bash
python app.py --port 5001
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## 📊 Sample Data
The system comes pre-loaded with:
- 5 sample students
- 3 sample faculty members
- 2 sample courses
- 2 sample batches

Edit the `load_csv_data()` function in `app.py` to modify sample data.

## 🔒 Security Notes
- Passwords are hashed using Werkzeug
- Role-based access control on all routes
- Session-based authentication
- Production: Update SECRET_KEY in `app.py`

## 📱 Browser Support
- Chrome (Recommended)
- Firefox
- Safari
- Edge

## 🛠️ Development

### Adding New Features
1. Add routes in `app.py`
2. Create templates in `templates/`
3. Update collections as needed
4. Test with all user roles

### Database Schema Changes
Edit the collections structure in `app.py` init_db() function

## 📞 Support
For issues or questions, refer to the README.md file in the project root.

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: Production Ready ✅
