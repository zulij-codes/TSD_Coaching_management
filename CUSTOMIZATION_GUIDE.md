# 🛠️ Customization & Extension Guide

## Overview
This guide helps you customize and extend the TSD Coaching Management System for your specific needs.

---

## 🎨 UI/UX Customization

### Change Colors & Branding

**File**: `frontend_TSD/templates/base.html` and individual dashboard HTML files

Look for the `<style>` sections:

```css
/* Primary Color */
background: #1e3c72;  /* Change this to your brand color */

/* Accent Color */
#2a5298  /* Change this color */
```

### Common Color Changes:
- **Primary Blue**: `#1e3c72` → Change to your color
- **Secondary Blue**: `#2a5298` → Change to your accent
- **Success Green**: `#28a745`
- **Danger Red**: `#dc3545`
- **Warning Yellow**: `#ffc107`

### Change Logo/Name
1. Find: `Gurukul` in templates
2. Replace with your institution name
3. Update in all dashboard headers

---

## 📋 Add New Features

### Example: Adding a "Notices" Module

#### Step 1: Add Collection in `app.py`

```python
# Around line 25, add:
notices_collection = db['notices']
```

#### Step 2: Add Routes in `app.py`

```python
@app.route('/admin/notice/add', methods=['POST'])
def add_notice():
    notice = {
        'title': request.form['title'],
        'content': request.form['content'],
        'date_posted': datetime.utcnow(),
        'posted_by': session.get('username')
    }
    notices_collection.insert_one(notice)
    flash('Notice posted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/notice/delete/<notice_id>')
def delete_notice(notice_id):
    from bson import ObjectId
    notices_collection.delete_one({'_id': ObjectId(notice_id)})
    flash('Notice deleted', 'success')
    return redirect(url_for('admin_dashboard'))
```

#### Step 3: Update Admin Dashboard

Add to `admin_dashboard.html`:

```html
<!-- Notices Tab -->
<div id="notices" class="tab-content">
    <button class="btn-add" onclick="showAddForm('notice')">+ Post Notice</button>
    {% for notice in notices %}
    <div class="notice-item">
        <h4>{{ notice['title'] }}</h4>
        <p>{{ notice['content'] }}</p>
        <small>Posted by {{ notice['posted_by'] }} on {{ notice['date_posted'] }}</small>
    </div>
    {% endfor %}
</div>
```

#### Step 4: Update Dashboard Route

In `app.py`, modify `admin_dashboard()`:

```python
@app.route('/admin/dashboard')
def admin_dashboard():
    # ... existing code ...
    notices = list(notices_collection.find())
    return render_template('admin_dashboard.html', 
                         # ... existing params ...
                         notices=notices)
```

---

## 🔐 Enhance Security

### 1. Update Secret Key (Important!)

**File**: `frontend_TSD/app.py`, Line 9

```python
# Change from:
app.config['SECRET_KEY'] = 'your-secret-key-here'

# To:
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

### 2. Add Rate Limiting

```bash
pip install flask-limiter
```

Then in `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login/<role>', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login(role):
    # ... existing code ...
```

### 3. Add CSRF Protection

```bash
pip install flask-wtf
```

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

---

## 📧 Add Email Notifications

### Setup Email Configuration

```python
# Add to app.py (around line 10):
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

from flask_mail import Mail, Message
mail = Mail(app)
```

### Send Welcome Email

```python
@app.route('/register/<role>', methods=['POST'])
def register(role):
    # ... existing registration code ...
    
    # Send email
    msg = Message(
        'Welcome to TSD Coaching',
        sender='noreply@tsdcoaching.com',
        recipients=[username + '@example.com']
    )
    msg.body = f'Welcome {username}! Your account has been created.'
    mail.send(msg)
    
    return redirect(url_for('login', role=role))
```

---

## 📊 Add Reporting Features

### Create Attendance Report

```python
@app.route('/admin/reports/attendance/<student_id>')
def attendance_report(student_id):
    records = list(attendance_collection.find({'student_id': student_id}))
    
    # Calculate statistics
    total = len(records)
    present = len([r for r in records if r['status'] == 'Present'])
    attendance_percent = (present / total * 100) if total > 0 else 0
    
    return render_template('attendance_report.html',
                         student_id=student_id,
                         records=records,
                         attendance_percent=attendance_percent)
```

---

## 🔄 Database Migrations

### Add New Field to Existing Collection

```python
# Run this once
from pymongo import UpdateMany

# Add a new field 'phone' to all students
students_collection.update_many(
    {},
    {'$set': {'phone': None}}
)
```

### Rename Field

```python
students_collection.update_many(
    {},
    {'$rename': {'contact_number': 'phone'}}
)
```

---

## 🎯 Custom Dashboards

### Create Custom Analytics Dashboard

```python
@app.route('/admin/analytics')
def analytics():
    total_students = students_collection.count_documents({})
    total_faculty = faculty_collection.count_documents({})
    total_courses = courses_collection.count_documents({})
    total_revenue = sum([p['amount'] for p in payments_collection.find({'status': 'Completed'})])
    
    return render_template('analytics.html',
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_courses=total_courses,
                         total_revenue=total_revenue)
```

---

## 🔌 API Integration

### Call External API (Example: SMS Notification)

```python
import requests

def send_sms(phone, message):
    api_key = 'your-api-key'
    url = 'https://api.sms-provider.com/send'
    
    payload = {
        'api_key': api_key,
        'phone': phone,
        'message': message
    }
    
    response = requests.post(url, json=payload)
    return response.status_code == 200
```

---

## 🐳 Docker Deployment

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY frontend_TSD . 

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
```

### Create `docker-compose.yml`

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      MONGO_URI: ${MONGO_URI}
```

---

## 🧪 Testing

### Create Test File: `test_app.py`

```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.app.get('/login/admin')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_app.py
```

---

## 📈 Performance Optimization

### Add Database Indexes

```python
# In app.py, inside init_db():
students_collection.create_index('student_id', unique=True)
faculty_collection.create_index('faculty_id', unique=True)
courses_collection.create_index('course_code', unique=True)
batches_collection.create_index('batch_id', unique=True)
```

### Cache Results

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_students():
    return list(students_collection.find())
```

---

## 🚀 Deployment Checklist

- [ ] Update SECRET_KEY
- [ ] Set FLASK_ENV = production
- [ ] Enable HTTPS
- [ ] Set up proper error logging
- [ ] Configure backup strategy for MongoDB
- [ ] Set up monitoring
- [ ] Create admin user with strong password
- [ ] Test all functionality
- [ ] Document custom changes
- [ ] Set up CI/CD pipeline

---

## 📚 Useful Resources

- Flask Documentation: https://flask.palletsprojects.com/
- PyMongo Documentation: https://pymongo.readthedocs.io/
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- Werkzeug Security: https://werkzeug.palletsprojects.com/

---

**Happy Customizing! 🎉**

For questions or issues, refer to the project documentation or the API documentation file.
