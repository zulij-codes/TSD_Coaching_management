# API Documentation - TSD Coaching Management System

## Base URL
```
http://localhost:5000
```

## Authentication
All protected routes require the user to be logged in with an active session.

---

## Public Routes

### 1. Home Page
- **URL**: `/`
- **Method**: `GET`
- **Description**: Landing page with login options
- **Response**: HTML page

### 2. Login
- **URL**: `/login/<role>`
- **Method**: `GET, POST`
- **Parameters**:
  - `role` (path): `admin`, `teacher`, or `student`
- **POST Parameters**:
  - `username` (string, required)
  - `password` (string, required)
- **Response**: Redirects to respective dashboard or returns login page

### 3. Register
- **URL**: `/register/<role>`
- **Method**: `GET, POST`
- **Parameters**:
  - `role` (path): `teacher` or `student`
- **POST Parameters**:
  - `username` (string, required)
  - `password` (string, required)
  - `reference_id` (string, optional)
- **Response**: Success message or registration page

### 4. Logout
- **URL**: `/logout`
- **Method**: `GET`
- **Response**: Redirects to home page

---

## Protected Routes (Admin Only)

### Dashboard
- **URL**: `/admin/dashboard`
- **Method**: `GET`
- **Auth**: Admin required
- **Response**: Admin dashboard HTML

### Student Management

#### Add Student
- **URL**: `/admin/student/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `student_id` (string, required)
  - `student_name` (string, required)
  - `gender` (string)
  - `email_id` (string)
  - `address` (string)
  - `contact_number` (string)
  - `category` (string)
  - `date_of_birth` (string)

#### Edit Student
- **URL**: `/admin/student/edit/<student_id>`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**: Same as Add Student

#### Delete Student
- **URL**: `/admin/student/delete/<student_id>`
- **Method**: `GET`
- **Auth**: Admin required

### Faculty Management

#### Add Faculty
- **URL**: `/admin/faculty/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `faculty_id` (string, required)
  - `full_name` (string, required)
  - `education` (string)
  - `specialization` (string)
  - `category` (string)
  - `contact_details` (string)

#### Edit Faculty
- **URL**: `/admin/faculty/edit/<faculty_id>`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**: Same as Add Faculty

#### Delete Faculty
- **URL**: `/admin/faculty/delete/<faculty_id>`
- **Method**: `GET`
- **Auth**: Admin required

### Course Management

#### Add Course
- **URL**: `/admin/course/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `course_code` (string, required)
  - `course_name` (string, required)
  - `course_category` (string)
  - `course_description` (string)
  - `course_duration` (string)
  - `course_fees` (integer)

#### Edit Course
- **URL**: `/admin/course/edit/<course_code>`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**: Same as Add Course

#### Delete Course
- **URL**: `/admin/course/delete/<course_code>`
- **Method**: `GET`
- **Auth**: Admin required

### Batch Management

#### Add Batch
- **URL**: `/admin/batch/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `batch_id` (string, required)
  - `start_date` (string)
  - `end_date` (string)
  - `timings` (string)
  - `course_code` (string)

#### Edit Batch
- **URL**: `/admin/batch/edit/<batch_id>`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**: Same as Add Batch

#### Delete Batch
- **URL**: `/admin/batch/delete/<batch_id>`
- **Method**: `GET`
- **Auth**: Admin required

### Enrollment Management

#### Add Enrollment
- **URL**: `/admin/enrollment/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `student_id` (string, required)
  - `batch_id` (string, required)
  - `enrollment_date` (string)
  - `status` (string)

#### Edit Enrollment
- **URL**: `/admin/enrollment/edit/<enrollment_id>`
- **Method**: `POST`
- **Auth**: Admin required

#### Delete Enrollment
- **URL**: `/admin/enrollment/delete/<enrollment_id>`
- **Method**: `GET`
- **Auth**: Admin required

### Payment Management

#### Add Payment
- **URL**: `/admin/payment/add`
- **Method**: `POST`
- **Auth**: Admin required
- **Parameters**:
  - `student_id` (string, required)
  - `amount` (integer, required)
  - `payment_date` (string)
  - `payment_mode` (string)
  - `status` (string)

#### Edit Payment
- **URL**: `/admin/payment/edit/<transaction_id>`
- **Method**: `POST`
- **Auth**: Admin required

#### Delete Payment
- **URL**: `/admin/payment/delete/<transaction_id>`
- **Method**: `GET`
- **Auth**: Admin required

---

## Protected Routes (Teacher Only)

### Dashboard
- **URL**: `/teacher/dashboard`
- **Method**: `GET`
- **Auth**: Teacher required
- **Response**: Teacher dashboard HTML

### Attendance Management

#### Add Attendance
- **URL**: `/teacher/attendance/add`
- **Method**: `POST`
- **Auth**: Teacher required
- **Parameters**:
  - `student_id` (string, required)
  - `batch_id` (string, required)
  - `date` (string)
  - `status` (string)

#### Edit Attendance
- **URL**: `/teacher/attendance/edit/<attendance_id>`
- **Method**: `POST`
- **Auth**: Teacher required

#### Delete Attendance
- **URL**: `/teacher/attendance/delete/<attendance_id>`
- **Method**: `GET`
- **Auth**: Teacher required

### Exam Schedule Management

#### Add Exam Schedule
- **URL**: `/teacher/exam_schedule/add`
- **Method**: `POST`
- **Auth**: Teacher required
- **Parameters**:
  - `exam_name` (string, required)
  - `batch_id` (string)
  - `exam_date` (string)
  - `exam_time` (string)
  - `duration` (string)

#### Edit Exam Schedule
- **URL**: `/teacher/exam_schedule/edit/<exam_id>`
- **Method**: `POST`
- **Auth**: Teacher required

#### Delete Exam Schedule
- **URL**: `/teacher/exam_schedule/delete/<exam_id>`
- **Method**: `GET`
- **Auth**: Teacher required

### Exam Result Management

#### Add Exam Result
- **URL**: `/teacher/exam_result/add`
- **Method**: `POST`
- **Auth**: Teacher required
- **Parameters**:
  - `exam_id` (string)
  - `student_id` (string, required)
  - `marks_obtained` (integer)
  - `total_marks` (integer)
  - `grade` (string)

#### Edit Exam Result
- **URL**: `/teacher/exam_result/edit/<result_id>`
- **Method**: `POST`
- **Auth**: Teacher required

#### Delete Exam Result
- **URL**: `/teacher/exam_result/delete/<result_id>`
- **Method**: `GET`
- **Auth**: Teacher required

### Study Material Management

#### Add Study Material
- **URL**: `/teacher/study_material/add`
- **Method**: `POST`
- **Auth**: Teacher required
- **Parameters**:
  - `title` (string, required)
  - `description` (string)
  - `content` (string)
  - `batch_id` (string)

#### Edit Study Material
- **URL**: `/teacher/study_material/edit/<material_id>`
- **Method**: `POST`
- **Auth**: Teacher required

#### Delete Study Material
- **URL**: `/teacher/study_material/delete/<material_id>`
- **Method**: `GET`
- **Auth**: Teacher required

---

## Protected Routes (Student Only)

### Dashboard
- **URL**: `/student/dashboard`
- **Method**: `GET`
- **Auth**: Student required
- **Response**: Student dashboard with personal information, enrollments, attendance, exams, and study materials

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```

### 302 Redirect
Redirects to appropriate login page if authentication fails

---

## Data Types

### Date Format
- Format: `MM/DD/YYYY` or `YYYY-MM-DD`
- Example: `01/15/2003` or `2003-01-15`

### Amount Format
- Integer value in Indian Rupees
- Example: `100000` (₹1,00,000)

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 301/302 | Redirect |
| 401 | Unauthorized |
| 404 | Not Found |

---

## Limitations & Notes

1. **File Upload**: Study materials currently store text content only
2. **Pagination**: Not implemented (all records displayed)
3. **Search**: Not implemented
4. **Export**: Not available
5. **Report Generation**: Not available

## Future Enhancements

- API responses in JSON format
- Advanced filtering and search
- File upload support
- Bulk operations
- Report generation
- Email notifications
- Analytics dashboard

---

**Last Updated**: April 2026
