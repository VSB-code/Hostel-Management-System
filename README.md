```markdown
# 🏠 NIT Durgapur Hostel Allocation System

[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-blue)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)](https://www.mysql.com/)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-success)](https://render.com)
![License](https://img.shields.io/badge/License-MIT-green)

> **A full‑stack hostel seat allocation system designed for NIT Durgapur's 4 hostels (400 rooms).**  
> Built with Flask, MySQL, and a modular architecture – features real‑time occupancy tracking, admin dashboard, and ACID transactions to ensure data integrity.

---

## ✨ Key Features

- **Student Side**
  - Request room allocation using college roll number (e.g., `24CS1001`).
  - Real‑time occupancy stats per hostel (AJAX updates every 15 seconds).
  - Instant allocation success/failure messages with hostel and room number.
  - Responsive glass‑morphism UI.

- **Admin Side**
  - Secure login with hashed passwords.
  - Dashboard showing all active allocations (student, hostel, room, allocated time).
  - Summary stats: total active students, available/full/maintenance rooms.
  - Vacate rooms with one click – updates allocation history and room occupancy.
  - System reset (with confirmation) to clear all allocations.

- **Room Management**
  - View all rooms grouped by hostel with status indicators.
  - Track room capacity, occupied count, and floor number.

- **Data Integrity**
  - ACID transactions for allocation/vacate operations – prevents double‑booking.
  - Foreign key constraints for referential integrity.
  - Allocation history preserved with `ACTIVE` / `VACATED` status and timestamps.

- **Scalable Architecture**
  - Blueprint‑based modular routing.
  - Service layer separates business logic from controllers.
  - Environment‑variable configuration for easy deployment.

---

## 🛠 Tech Stack

| Layer         | Technology |
|---------------|------------|
| Backend       | Python 3, Flask 3 |
| Database      | MySQL 8.0 (with `mysql-connector-python`) |
| Frontend      | HTML5, CSS3 (Glassmorphism), Vanilla JS (Fetch API) |
| Authentication | Werkzeug (password hashing) |
| Deployment    | Render (Gunicorn) |
| Environment   | `python-dotenv` |

---

## 🗄️ Database Schema

**6 Tables** – Normalized with relationships:

- `Hostels` – hostel_id, name, total_rooms.
- `Rooms` – room_id, hostel_id (FK), room_number, floor, capacity (default 2), occupied_count, status (`AVAILABLE`/`FULL`/`MAINTENANCE`).
- `Students` – student_id (PK, roll number), name, email.
- `Admins` – admin_id, username, password_hash.
- `Allocations` – allocation_id, student_id (FK), room_id (FK), allocated_at, vacated_at, status (`ACTIVE`/`VACATED`).

**Relationships:**  
- `Rooms` ⟶ `Hostels` (many‑to‑one)  
- `Allocations` ⟶ `Students` & `Rooms` (many‑to‑one)  

*Check `database/schema.sql` for full DDL.*

---

## 📁 Project Structure

```
hostel-management/
├── app.py                 # Flask app factory
├── config.py              # Configuration from .env
├── requirements.txt
├── Procfile               # Gunicorn entry
├── .env.example           # Environment variables template
├── database/
│   ├── schema.sql
│   └── seed.sql           # Sample data (hostels, rooms, admin)
├── models/
│   └── db.py              # get_db_connection()
├── services/              # Business logic
│   ├── student_service.py
│   ├── room_service.py
│   └── allocation_service.py
├── routes/                # Blueprints
│   ├── __init__.py
│   ├── student_routes.py
│   ├── admin_routes.py
│   └── room_routes.py
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── index.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── rooms.html
    └── status.html
```

---

## 🚀 Local Setup

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

---

> **Built with ❤️ for the hostel management needs of NIT Durgapur.**
```

---

### Notes for You:
- Replace placeholders like `your-username`, `your-profile`, and the author details with your own.
- Add actual screenshots if you have them – the README can include image links.
- If you're using a different cloud MySQL (like Aiven), mention it in deployment section.
- The README is designed to be impressive to interviewers – it shows a clear understanding of architecture, security, and deployment.