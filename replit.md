# BVRIT Bus Transport System

## Overview
A complete Flask-based bus transport management system for BVRIT College (Narsapur, Hyderabad). The system provides role-based access for admins, students, and drivers to manage and view bus transport information.

## Features
- **Admin Panel**: Full CRUD operations for buses, routes, students, and drivers
- **Student Dashboard**: View assigned bus, route details, stops, and timings
- **Driver Dashboard**: View assigned route and complete passenger list
- **Role-Based Authentication**: Secure login system with password hashing
- **CSRF Protection**: All delete operations protected against cross-site request forgery
- **Responsive UI**: Bootstrap 5 responsive design for all devices

## Technology Stack
- **Backend**: Python 3.11, Flask 3.1.2
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Security**: Werkzeug password hashing, session-based auth, CSRF tokens

## Database Schema
- `admin`: Admin user credentials
- `students`: Student information and bus assignments
- `drivers`: Driver details and credentials
- `buses`: Bus information linked to routes and drivers
- `routes`: Route details with stops and timings
- `requests`: Student requests (future feature)

## Preloaded Data

### Students
- B SAI RISHIK REDDY (24211A0538) → Bus J9
- A SANDEEP (24211A0512) → Bus SA3

### Buses & Routes
1. **SA3** → Miyapur Route (7:00 AM - 8:30 AM)
2. **J9** → Kukatpally Route (7:10 AM - 8:40 AM)
3. **J10** → Lingampally Route (7:15 AM - 8:45 AM)
4. **BHEL4** → BHEL Route (7:20 AM - 8:50 AM)
5. **N1** → Narsapur Town Route (7:40 AM - 8:10 AM)

### Drivers
- Ramesh Kumar (9876543210)
- Mahesh Goud (9876543220)
- Suresh Naik (9876543230)
- Ravi Teja (9876543240)
- Krishna Reddy (9876543250)

## Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Students
- Username: Roll Number (e.g., `24211A0538`)
- Password: `student123` (default for preloaded students)

### Drivers
- Username: Contact Number (e.g., `9876543210`)
- Password: `driver123` (default for preloaded drivers)

## Project Structure
```
.
├── app.py                          # Main Flask application
├── transport.db                    # SQLite database (auto-created)
├── templates/
│   ├── base.html                   # Base template with navbar
│   ├── login.html                  # Login page for all roles
│   ├── admin_dashboard.html        # Admin overview dashboard
│   ├── student_dashboard.html      # Student bus information view
│   ├── driver_dashboard.html       # Driver route and passenger list
│   ├── manage_students.html        # Student CRUD operations
│   ├── manage_buses.html           # Bus CRUD operations
│   ├── manage_routes.html          # Route CRUD operations
│   └── manage_drivers.html         # Driver CRUD operations
└── static/
    └── style.css                   # Custom CSS styles
```

## Security Features
- Password hashing using Werkzeug's `generate_password_hash`
- Session-based authentication with secure session secrets
- Role-based access control for all admin operations
- CSRF token protection on all destructive operations
- POST-only delete endpoints to prevent CSRF attacks

## Recent Changes (Oct 27, 2025)
- Initial project setup with Flask and SQLite
- Implemented complete authentication system with role-based access
- Created all CRUD operations for admins
- Built responsive Bootstrap 5 UI
- Added CSRF protection for delete operations
- Preloaded database with sample data

## Running the Application
The app runs automatically via the configured workflow on port 5000. The database is initialized automatically on first run with all preloaded data.

## Future Enhancements
- Student request system for bus changes
- Bus capacity validation and warnings
- Search and filter functionality
- Route visualization with maps
- Export functionality (CSV/PDF)
- Email notifications for route changes
