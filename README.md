<<<<<<< HEAD
# Hostel Management System
=======

# 🏠 NIT Durgapur Hostel Allocation System
>>>>>>> 01420ea295ec3f700bba21599871757e25f4ecbf

A Flask-based Hostel Management System that automates room allocation, occupancy tracking, and hostel administration using MySQL. The system follows a First-Come-First-Serve (FCFS) room allocation strategy and provides both student-facing and admin-facing functionality.

<<<<<<< HEAD
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
=======
> **A full‑stack hostel seat allocation system designed for NIT Durgapur's 4 hostels (400 rooms).**  
> Built with Flask, MySQL, and a modular architecture – features real‑time occupancy tracking, an admin dashboard, and ACID transactions to ensure data integrity.
>>>>>>> 01420ea295ec3f700bba21599871757e25f4ecbf

---

## Tech Stack

### Backend

* Python
* Flask

### Database

<<<<<<< HEAD
* MySQL

### Frontend

* HTML
* CSS
* JavaScript

### Security

* Password Hashing
* Session Authentication
=======
- **Data Integrity**
  - ACID transactions for allocation/vacate operations – prevent double‑booking.
  - Foreign key constraints for referential integrity.
  - Allocation history preserved with `ACTIVE` / `VACATED` status and timestamps.

- **Scalable Architecture**
  - Blueprint‑based modular routing.
  - The service layer separates business logic from controllers.
  - Environment variable configuration for easy deployment.
>>>>>>> 01420ea295ec3f700bba21599871757e25f4ecbf

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
<<<<<<< HEAD
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
=======
    ├── index.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── rooms.html
    └── status.html
>>>>>>> 01420ea295ec3f700bba21599871757e25f4ecbf



## Room Allocation Workflow

<<<<<<< HEAD
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
=======
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/hostel-management.git
   cd hostel-management
   ```

2. **Create & activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL**
   - Create a database: `CREATE DATABASE hostel_management;`
   - Run `database/schema.sql` to create tables.
   - Run `database/seed.sql` to populate hostels, rooms, and default admin.
   - (Optional) Generate admin password hash:
     ```python
     from werkzeug.security import generate_password_hash
     print(generate_password_hash("admin123"))
     ```
     Insert that hash into `Admins` table.

5. **Configure environment**
   - Copy `.env.example` to `.env` and fill in your DB credentials:
     ```env
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=your_password
     DB_NAME=hostel_management
     SECRET_KEY=your-secret-key
     DEBUG=True
     ```

6. **Run the application**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` – the student form is ready.

7. **Admin login**
   - Go to `/admin/login`
   - Default credentials: `admin` / `admin123` (as per seed data).

---

## 🌐 Deployment (Render)

1. Push code to GitHub.
2. On Render, create a new Web Service and connect your repository.
3. Add the following environment variables in Render dashboard:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (use a cloud MySQL like Aiven or Clever Cloud).
   - `SECRET_KEY`
   - (No need to set `DEBUG` in production)
4. Render will automatically detect `Procfile` and run:
   ```
   web: gunicorn app:create_app()
   ```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/` | Student allocation form |
| POST   | `/book` | Allocate room (form data: `student_id`, `student_name`) |
| GET    | `/api/occupancy` | JSON: occupancy stats per hostel |
| GET    | `/status` | Full page with detailed stats |
| GET    | `/rooms` | Rooms grouped by hostel |
| GET    | `/admin/login` | Admin login page |
| POST   | `/admin/login` | Admin login form submit |
| GET    | `/admin/logout` | Logout admin |
| GET    | `/admin/dashboard` | Admin dashboard (protected) |
| POST   | `/admin/vacate/<id>` | Vacate an allocation (protected) |
| POST   | `/admin/reset_all` | Reset all allocations (protected, requires confirmation) |

---

## 🧪 Testing & Concurrency

- **Concurrency handled** – MySQL transactions with `START TRANSACTION` and row‑level locking ensure that simultaneous booking requests do not double‑allocate a room.
- **Atomic operations** – Allocation and room update are performed in a single transaction; on error, a rollback restores consistency.

---

## 🔮 Future Improvements

- ✅ Email notifications to students on allocation.
- ✅ Waitlist system when all rooms are full.
- ✅ Student preferences (choose hostel) with priority.
- ✅ Bulk import/export of student data (CSV).
- ✅ Room maintenance scheduling.
- ✅ Audit logs for admin actions.
- ✅ Caching (Redis) for occupancy stats to reduce DB load.

---

## 👨‍💻 Author

**Virendra Singh**  
- [GitHub](https://github.com/VSB-code)  
- [LinkedIn](https://www.linkedin.com/in/virendra-singh-752864409/)  
- Project built as a semester/mini project for **NIT Durgapur** – demonstrates full‑stack engineering, database design, and scalable architecture.

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.


> **Built with ❤️ for the hostel management needs of NIT Durgapur.**
```

---
>>>>>>> 01420ea295ec3f700bba21599871757e25f4ecbf
