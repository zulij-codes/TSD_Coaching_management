# TSD Coaching Management System

## Overview

The TSD Coaching Management System is a comprehensive web application designed to streamline the operations of a coaching institute. It provides a complete solution for managing students, faculty, courses, batches, enrollments, payments, attendance, exams, and study materials. The system supports three user roles: Admin, Teacher, and Student, each with tailored dashboards and functionalities.

## Features

### Admin Dashboard
- **User Management**: Register and manage admin, teacher, and student accounts
- **Student Management**: Add, edit, delete, and view student profiles with personal details
- **Faculty Management**: Manage faculty information including education, specialization, and contact details
- **Course Management**: Create and manage courses with details like name, category, description, duration, and fees
- **Batch Management**: Organize students into batches with start/end dates and timings
- **Enrollment Management**: Handle student enrollments in batches
- **Payment Tracking**: Record and manage payment transactions for students
- **System Overview**: View comprehensive statistics and data across all modules

### Teacher Dashboard
- **Attendance Management**: Mark and track student attendance for their batches
- **Exam Scheduling**: Create and manage exam schedules for batches
- **Exam Results**: Record and update student exam results and grades
- **Study Materials**: Upload and manage study materials for students
- **Student Overview**: View student information and progress

### Student Dashboard
- **Personal Profile**: View and manage personal information
- **Enrollment Information**: See enrolled batches and courses
- **Attendance Records**: Check personal attendance history
- **Exam Schedules**: View upcoming exams for enrolled batches
- **Exam Results**: Access personal exam results and grades
- **Study Materials**: Access study materials provided by teachers
- **Payment History**: View payment transaction records

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, Bootstrap (via Jinja2 templates)
- **Authentication**: Flask-Session with password hashing
- **ORM**: PyMongo for MongoDB integration

## Installation and Setup

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TSD_Coaching_management
   ```

2. **Install dependencies**:
   ```bash
   pip install flask pymongo flask-session werkzeug
   ```

3. **Configure MongoDB**:
   - Update the MongoDB connection string in `frontend_TSD/app.py`
   - Replace `'your-mongodb-connection-string'` with your actual MongoDB URI

4. **Run the application**:
   ```bash
   cd frontend_TSD
   python app.py
   ```

5. **Access the application**:
   - Open your browser and go to `http://localhost:5000`
   - Default admin credentials: username: `admin`, password: `admin123`

## Database Schema

The system uses the following main collections in MongoDB:

- **users**: User accounts with roles (admin, teacher, student)
- **students**: Student personal and academic information
- **faculty**: Faculty/teacher information
- **courses**: Course details and metadata
- **batches**: Batch information linked to courses
- **enrollments**: Student-batch enrollment records
- **payments**: Payment transaction records
- **attendance**: Daily attendance records
- **exam_schedules**: Exam scheduling information
- **exam_results**: Student exam results
- **study_materials**: Educational materials uploaded by teachers

## Usage

### For Administrators
1. Login with admin credentials
2. Manage users, students, faculty, courses, and batches
3. Oversee enrollments and payments
4. Monitor system-wide statistics

### For Teachers
1. Login with teacher credentials
2. Mark student attendance
3. Schedule and manage exams
4. Record exam results
5. Upload study materials

### For Students
1. Login with student credentials
2. View personal information and enrolled courses
3. Check attendance and exam results
4. Access study materials

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection via Flask-WTF (if implemented)

## Future Enhancements

- Email notifications for important events
- Advanced reporting and analytics
- Mobile application
- Integration with learning management systems
- Automated fee reminders
- Online payment gateway integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact the development team or create an issue in the repository.
