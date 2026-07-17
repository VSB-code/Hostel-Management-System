# Hostel Management System

A Flask-based Hostel Management System that automates room allocation, occupancy tracking, and hostel administration using MySQL. The system follows a First-Come-First-Serve (FCFS) room allocation strategy and provides both student-facing and admin-facing functionality.

## Features

### Student Features

* Room booking through a simple web interface
* Roll number validation
* Automatic room allocation
* Prevents duplicate active allocations
* Real-time hostel occupancy status

### Admin Features

* Secure admin login
* View all active room allocations
* Vacate allocated rooms
* Monitor occupancy statistics
* Reset hostel allocation system
* Dashboard with summary statistics

### System Features

* Flask backend
* MySQL database integration
* Session-based authentication
* Password hashing using Werkzeug
* REST API endpoints
* Dynamic occupancy tracking
* Error handling and transaction support

---

## Tech Stack

### Backend

* Python
* Flask

### Database

* MySQL

### Frontend

* HTML
* CSS
* JavaScript

### Security

* Password Hashing
* Session Authentication

---


## 📂 Project Directory Structure

```text
hostel_management_system/
│
├── app.py                  # Central Flask Engine & Application Controller Routes
├── README.md               # Professional Technical Systems Documentation
│
├── static/
│   └── style.css           # Custom Structural Component UI Style Rules
│
└── templates/
    ├── index.html          # Student Registration Portal & Booking Viewport
    ├── status.html         # Live Macro Metrics Summary Grid Dashboard
    ├── rooms.html          # Deep-Dive Structural Micro-Room Matrix View
    ├── admin_login.html    # Administrative Authentication Entry Panel
    └── admin_dashboard.html# High-Privilege System Management Workspace


---

## Database Schema

### Hostels

Stores hostel information.

```sql
hostel_id
hostel_name
```

### Rooms

Stores room details and occupancy.

```sql
room_id
hostel_id
room_number
floor_number
capacity
occupied_count
status
```

### Students

Stores student information.

```sql
student_id
student_name
```

### Allocations

Stores room allocations.

```sql
allocation_id
student_id
room_id
status
allocated_at
vacated_at
```

### Admins

Stores admin login credentials.

```sql
admin_id
username
password_hash
```

---

## Room Allocation Workflow

```text
Student submits form
        │
        ▼
Validate roll number
        │
        ▼
Check existing allocation
        │
        ▼
Find available room
        │
        ▼
Create allocation
        │
        ▼
Update occupancy
        │
        ▼
Return success message
```

---

## API Endpoints

### Get Occupancy Statistics

```http
GET /api/occupancy
```

Response:

```json
{
  "success": true,
  "stats": [
    {
      "hostel_id": 1,
      "hostel_name": "BH-A",
      "total_rooms": 20,
      "total_beds": 60,
      "occupied_beds": 45,
      "available_beds": 15
    }
  ]
}
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd hostel-management
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install flask
pip install mysql-connector-python
pip install werkzeug
```

### Configure MySQL

Create database:

```sql
CREATE DATABASE hostel_management;
```

Import schema and sample data.

### Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
(Running on http://127.0.0.1:5000)
```

---

## Security Features

* Password hashing
* Session management
* Login-protected admin routes
* Input validation
* SQL parameterized queries
* Transaction handling

---

## Future Improvements

* JWT Authentication
* Email Notifications
* Hostel Analytics Dashboard
* Student Profile Management
* Room Preference Selection
* PDF Reports
* RESTful API Expansion
* Docker Deployment
* Cloud Deployment

---

## Learning Outcomes

This project demonstrates:

* Flask Routing
* Jinja Templates
* MySQL Integration
* CRUD Operations
* REST APIs
* Session Authentication
* SQL JOINs
* Aggregation Queries
* Error Handling
* Transaction Management
* Frontend-Backend Communication

---
## 🚀 Key Engineering & Core CS Features

### 1. Concurrency Control & Race Condition Mitigation
During peak registration hours, multiple student requests might target a single residual room capacity boundary simultaneously. The application backend utilizes atomic SQL transactions. By bundling execution paths inside explicit try-catch blocks backed by `conn.commit()` and handling runtime rollbacks (`conn.rollback()`), the system guarantees **ACID compliance**, preventing double-booking phenomena.

### 2. Linear Memory Optimization ($O(N)$ Parsing)
The newly introduced `/rooms` component extracts flat query matrices from the relational space via optimized `INNER JOIN` operations and shifts sorting overhead into an in-memory associative array (Python Dictionary) grouping profile. This ensures linear $O(N)$ runtime mapping, avoiding expensive multi-pass loops inside the Jinja2 rendering pipeline.

### 3. Custom Input Stream Validation & Security
* **Regex Integration:** Roll numbers are statically verified against standard institutional patterns (`r'^\d{2}[A-Z]{2}\d{4}$'`) prior to opening connection pools.
* **State Protection:** Administrative actions (such as `vacate_room` and `reset_all`) are isolated using custom Python Function Decorators (`@login_required`) interacting with cryptographically secured session headers.

---

## Author
Virendra Singh

Computer Science Student | Python Developer | Flask Enthusiast
