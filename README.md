# BVRIT Bus Transport Management System

A comprehensive web application for managing bus transportation services at BVRIT (BVR Institute of Technology).

## Features

- **Admin Dashboard**: Manage students, buses, routes, and drivers
- **Student Portal**: View bus information and submit requests
- **Driver Portal**: View assigned bus and student list
- **Role-based Authentication**: Secure login for different user types
- **Database Management**: SQLite database for data persistence

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Install Dependencies**
   ```bash
   pip install flask werkzeug
   ```

2. **Run the Application**
   ```bash
   python3 app.py
   ```

3. **Access the Website**
   Open your browser and go to: http://localhost:8000

### Default Login Credentials

#### Admin
- **Username**: `admin`
- **Password**: `admin123`

#### Student
- **Username**: `24211A0538` (roll number)
- **Password**: `student123`

#### Driver
- **Username**: `9876543210` (contact number)
- **Password**: `driver123`

## Project Structure

```
sed project/
├── app.py                 # Main Flask application
├── transport.db          # SQLite database
├── templates/            # HTML templates
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── driver_dashboard.html
│   ├── login.html
│   ├── manage_buses.html
│   ├── manage_drivers.html
│   ├── manage_routes.html
│   ├── manage_students.html
│   └── student_dashboard.html
├── static/              # Static files
│   └── style.css
├── archive/             # Archived files
│   ├── *.zip files
│   ├── main.py
│   └── replit.md
├── pyproject.toml       # Project dependencies
├── uv.lock             # Lock file
└── README.md           # This file
```

## Usage

### Admin Functions
- Add, edit, and delete students
- Manage bus assignments
- Create and modify routes
- Add and manage drivers
- View system statistics

### Student Functions
- View assigned bus information
- Check route details and timings
- View driver contact information
- Submit requests to admin

### Driver Functions
- View assigned bus details
- See list of students on the bus
- Check route information

## Database

The application uses SQLite database (`transport.db`) with the following tables:
- `admin` - Administrator accounts
- `students` - Student information
- `buses` - Bus details and assignments
- `drivers` - Driver information
- `routes` - Route details
- `requests` - Student requests

## Development

### Running in Debug Mode
The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Debug console

### Stopping the Application
Press `Ctrl+C` in the terminal where the app is running.

## Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
1. Try a different port by modifying `app.py` line 597
2. Or stop the conflicting service (like AirPlay Receiver on macOS)

### Database Issues
The database is automatically created on first run. If you need to reset it, delete `transport.db` and restart the application.

## Security Notes

- Change default passwords in production
- Use environment variables for sensitive configuration
- Implement proper session management
- Use HTTPS in production

## License

This project is for educational purposes at BVRIT.
