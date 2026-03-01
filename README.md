# Student Result Management System

A simple, easy-to-understand college mini-project built with Flask, HTML, CSS (Bootstrap), and SQLite.

## Features

### 🔐 Authentication
- **Admin Login** - Username & Password based authentication
- **Student Login** - Roll Number based authentication
- Flask sessions for secure session management

### 👨‍💼 Admin Features
- **Add Student** - Add new student with roll number, name, and marks
- **View All Students** - Table view of all students with their results
- **Edit Student** - Update student name and marks
- **Delete Student** - Remove student records with confirmation
- **Admin Dashboard** - Overview of all records

### 🎓 Student Features
- **View Own Result** - Students can only see their own result
- **Result Card** - Clean, professional result display card
- **Print Result** - Print button to generate result sheet
- **Grade Display** - Clear visualization of marks and grade

### 📊 Additional Features
- Automatic grade calculation based on marks
- Responsive design using Bootstrap
- Flash messages for feedback
- Input validation on all forms
- Error handling for duplicate roll numbers

## Project Structure

```
result_system/
│
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── login.html             # Side-by-side login page
│   ├── dashboard.html         # Admin dashboard
│   ├── add_student.html       # Add new student form
│   ├── edit_student.html      # Edit student form
│   ├── view_students.html     # View all students table
│   └── search.html            # Student result display
│
└── static/                     # Static files (CSS, JS, images)
    └── (optional custom CSS)
```

## Database Schema

### students table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    marks INTEGER NOT NULL CHECK(marks >= 0 AND marks <= 100),
    grade TEXT NOT NULL
);
```

### admin table
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd result_system
pip install -r requirements.txt
```

Required packages:
- Flask==2.3.0
- Werkzeug==2.3.0

### 2. Run the Application

```bash
python app.py
```

The app will start at: `http://localhost:5000`

### 3. Default Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

**Student Login:**
- Create students in admin panel first
- Students login with their Roll Number

## How to Use

### For Admins

1. **Login** - Go to login page, click "Admin Login", enter credentials
2. **Add Student** - Click "Add New Student", fill details (Roll No, Name, Marks)
3. **View All** - See all students in table with edit/delete options
4. **Edit** - Click Edit button on any student row to update details
5. **Delete** - Click Delete button to remove a record (with confirmation)
6. **Logout** - Click logout in navbar

### For Students

1. **Login** - Go to login page, click "Student Login", enter your Roll Number
2. **View Result** - Automatically shown after login
3. **Print** - Click "Print Result" to generate result document
4. **Logout** - Click logout in navbar

## Validation Rules

- **Roll Number** - Must be unique, cannot be empty
- **Name** - Must be at least 1 character, cannot be empty
- **Marks** - Must be between 0 and 100
- All fields are required

## Grade Calculation

| Grade | Marks   |
|-------|---------|
| A     | 90-100  |
| B     | 80-89   |
| C     | 70-79   |
| D     | 60-69   |
| F     | < 60    |

## Routes

### Public Routes
- `/` - Home page
- `/login` - Login page (GET, POST)

### Admin Routes (Protected)
- `/admin/dashboard` - Admin dashboard
- `/admin/add-student` - Add student page (GET, POST)
- `/admin/view-students` - View all students
- `/admin/edit-student/<id>` - Edit student page (GET, POST)
- `/admin/delete-student/<id>` - Delete student

### Student Routes (Protected)
- `/student/result` - View student's result

### Common Routes
- `/logout` - Logout user

## Security Features

- ✅ Session-based authentication
- ✅ Role-based access control (admin/student)
- ✅ Protected routes with decorators
- ✅ Input validation on all forms
- ✅ Unique constraints on database
- ✅ Delete confirmation dialogs

## Technologies Used

- **Backend** - Python Flask 2.3.0
- **Database** - SQLite3
- **Frontend** - HTML5, CSS3, Bootstrap 5
- **Sessions** - Flask sessions with secure key
- **Styling** - Bootstrap + Custom CSS

## Important Notes for Viva/Presentation

1. **Code is Simple** - Easy to explain, no advanced Python concepts
2. **Well-Commented** - Comments explain what each function does
3. **Follows Best Practices** - Uses decorators for auth, proper error handling
4. **Scalable** - Can be extended with more features easily
5. **User-Friendly** - Clean UI, responsive design
6. **Database Driven** - Uses proper database relationships

## Common Issues & Solutions

### Database Issues
**Problem:** App doesn't create database.db
**Solution:** Ensure write permissions in the folder

### Port Already in Use
**Problem:** Address already in use error
**Solution:** Change port in app.py: `app.run(port=5001)`

### Template Not Found
**Problem:** TemplateNotFound error
**Solution:** Ensure templates/ folder exists in same directory as app.py

### Session Issues
**Problem:** Session data not persisting
**Solution:** Don't clear cookies, ensure secret_key is set

## Extension Ideas

These features can be added to enhance the project:

1. Hash passwords for security
2. Add email notifications
3. Upload student photos
4. Generate PDF results
5. Add more subjects/courses
6. Implement search by name
7. Add filters by grade/status
8. Create analytical reports
9. Add user roles (teacher, librarian, etc.)
10. Implement soft deletes (archive instead of delete)

## File Descriptions

### app.py
Main Flask application containing:
- Database initialization and connection
- All route handlers
- Authentication decorators
- Input validation logic
- Grade calculation function

### templates/base.html
Base template with:
- Navigation bar
- Flash message display
- Generic page styling
- User session display

### templates/login.html
Login page with:
- Side-by-side admin and student forms
- Separate input fields for each role
- Styling and form validation
- Demo credentials display

### templates/dashboard.html
Admin dashboard showing:
- Student statistics
- Table of all students
- Edit/Delete action buttons
- Total students count

### templates/add_student.html
Add student form with:
- Roll number input
- Student name input
- Marks input with grade preview
- Form validation messages

### templates/edit_student.html
Edit student form with:
- Read-only roll number field
- Editable name and marks fields
- Grade preview on marks change
- Cancel/Save buttons

### templates/view_students.html
View all students page with:
- Table with sortable columns
- Action buttons for edit/delete
- Pass/Fail status display
- Student count summary

### templates/search.html
Student result page with:
- Result card display
- Student information
- Marks and grade visualization
- Progress bar for marks
- Print button

## Video Explanation Points

1. **Database Design** - Show the simple 2-table schema
2. **Authentication Flow** - Explain how login works with sessions
3. **Admin Operations** - Demo add, edit, view, delete
4. **Student Experience** - Show login and result viewing
5. **Code Structure** - Explain app.py organization
6. **Error Handling** - Show validation and error messages
7. **Security** - Explain decorators and access control
8. **UI/UX** - Show responsive design on mobile

## License

This is a college mini-project. Feel free to modify and use for educational purposes.

## Author

Created as a simple Student Result Management System for college coursework.

---

**Last Updated:** February 2024
