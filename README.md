# CodeCampus 🎓

**CodeCampus** is an open-source web platform built with **Flask (Python)** that allows beginner developers to learn, practice, and master coding skills in an interactive and visually appealing environment.

---

## Overview

CodeCampus is designed as a modern, feature-rich web application that demonstrates:

* Backend development with **Flask**
* Frontend integration using **HTML, CSS, Bootstrap, and Jinja2 templates**
* Persistent data storage with **SQLite**
* Code execution support for **Python, Java, and C++**
* Modern UI/UX with gradient backgrounds and glassmorphism effects

---

## Features

### 🎯 Core Features
- **Advanced Code Editor** - Modern code editor with syntax highlighting for Python, Java, and C++
- **Code Execution** - Run code directly in the browser with support for multiple languages
- **Practice Questions** - Collection of coding challenges at different difficulty levels (Easy, Medium, Hard)
- **Progress Tracking** - Track your progress, solve exercises, and view performance statistics
- **User Authentication** - Sign up, login, or continue as guest
- **Admin Panel** - Manage questions (add, edit, delete) for administrators

### 🌍 Internationalization
- Full support for **Hebrew** and **English**
- Dynamic language switching
- RTL/LTR layout support

### 🎨 Modern Design
- Beautiful gradient backgrounds with animations
- Glassmorphism effects
- Responsive design
- Modern UI components

---

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AmiramAMS/CodeCampus.git
   cd CodeCampus
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy werkzeug
   ```

3. **Create admin user**
   ```bash
   python create_admin.py
   ```
   Default admin credentials:
   - Username: `admin`
   - Password: `admin123`

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5001`

---

## Usage

### For Users
1. Visit the landing page
2. Sign up for a new account, sign in, or continue as guest
3. Explore the code editor and practice questions
4. Track your progress in the profile section

### For Administrators
1. Login with admin credentials
2. Navigate to the Questions page
3. Add, edit, or delete questions as needed

---

## Project Structure

```
CodeCampus/
├── app.py                 # Main Flask application
├── create_admin.py        # Script to create admin user
├── instance/
│   └── database.db         # SQLite database
├── static/
│   ├── css/
│   │   ├── c_style.css   # Main stylesheet
│   │   └── form.css      # Form styles
│   └── images/
│       └── logo.png      # Application logo
└── templates/
    ├── base.html         # Base template
    ├── landing.html      # Landing page
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── index.html        # Code editor page
    ├── questions.html    # Questions page
    └── profile.html      # User profile page
```

---

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Werkzeug
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Code Editor**: CodeMirror
- **Database**: SQLite
- **Icons**: Bootstrap Icons

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is open source and available under the MIT License.

---

## Author

**AmiramAMS**

---

## Acknowledgments

- Built with Flask
- UI inspired by modern design trends
- CodeMirror for code editing capabilities
