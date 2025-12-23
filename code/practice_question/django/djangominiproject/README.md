# Django Student Information Project

[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#current-status)
[![Demo](https://img.shields.io/badge/Demo-Running-brightgreen.svg)](#demo)

A Django mini project demonstrating student information display using the MVT (Model-View-Template) architecture pattern.

## 🎯 Project Overview

This project serves as a practical example of Django web development, showcasing how to build a simple yet complete web application that displays student information. The project demonstrates key Django concepts including views, templates, URL routing, and the separation of concerns principle.

## 📊 Student Information Display

The application displays the following student information:

- **Student Name**: John Doe
- **Roll Number**: 2024001
- **Branch**: Computer Science
- **Semester**: 6th

> **Note**: The student data is hardcoded in the view function as requested (not stored in database).

## 🏗️ Architecture Overview

This project follows Django's MVT (Model-View-Template) architecture:

```
┌─────────────────────────────────────────────────────┐
│                 REQUEST FLOW                        │
├─────────────────────────────────────────────────────┤
│  User Request (/)                                   │
│  ↓                                                  │
│  URL Router → hello/urls.py                        │
│  ↓                                                  │
│  View Function → hello/views.py:student_info()     │
│  ↓                                                  │
│  Template Rendering → hello/student_info.html      │
│  ↓                                                  │
│  HTML Response to User                              │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
djangominiproject/
├── manage.py                           # Django project management
├── djangominiproject/                  # Main project configuration
│   ├── settings.py                     # Project settings (hello app registered)
│   ├── urls.py                         # Main URL configuration
│   ├── __init__.py                     # Package initialization
│   ├── asgi.py                         # ASGI configuration
│   └── wsgi.py                         # WSGI configuration
├── hello/                              # Django application
│   ├── views.py                        # Student info view function
│   ├── urls.py                         # Application URL routing
│   ├── templates/                      # HTML templates
│   │   └── hello/
│   │       └── student_info.html       # Student information template
│   ├── models.py                       # Data models (not used)
│   ├── admin.py                        # Admin interface
│   ├── apps.py                         # App configuration
│   ├── tests.py                        # Unit tests
│   └── migrations/                     # Database migrations
└── db.sqlite3                          # SQLite database (Django default)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Django 4.0+ (installed in project environment)

### Installation & Setup

1. **Navigate to project directory**:
   ```bash
   cd /workspaces/Python_Framework/code/practice_question/django/djangominiproject
   ```

2. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the application**:
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - You should see the student information page

4. **Stop the server**:
   - Press `Ctrl+C` in the terminal

### Alternative Commands

```bash
# Run on specific port
python manage.py runserver 8080

# Run on specific host
python manage.py runserver 0.0.0.0:8000

# Enable debug mode (already enabled by default)
# Set DEBUG = True in settings.py
```

## 💻 Code Walkthrough

### 1. View Function (hello/views.py)

```python
from django.shortcuts import render

def student_info(request):
    """
    Display student information
    """
    # Hardcoded student data (not from database as requested)
    student_data = {
        'student_name': 'John Doe',
        'roll_number': '2024001',
        'branch': 'Computer Science',
        'semester': '6th'
    }
    
    return render(request, 'hello/student_info.html', {'student_data': student_data})
```

**Key Features**:
- Simple function-based view
- Hardcoded data as per requirements
- Uses Django's `render()` function
- Passes data to template via context dictionary

### 2. Template (hello/templates/hello/student_info.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Information</title>
    <style>
        /* Professional CSS styling */
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        /* ... additional styling ... */
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Student Information</h1>
        
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Student Name</div>
                <div class="info-value">{{ student_data.student_name }}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Roll Number</div>
                <div class="info-value">{{ student_data.roll_number }}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Branch</div>
                <div class="info-value">{{ student_data.branch }}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Semester</div>
                <div class="info-value">{{ student_data.semester }}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>📚 Django Mini Project - Student Information Display</p>
        </div>
    </div>
</body>
</html>
```

**Key Features**:
- Responsive design with CSS Grid
- Professional styling with shadows and rounded corners
- Django Template Language (DTL) for dynamic content
- Clean, modern UI design

### 3. URL Configuration

#### App URLs (hello/urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_info, name='student_info'),
]
```

#### Main URLs (djangominiproject/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hello.urls")),
]
```

**URL Flow**:
1. User visits `http://127.0.0.1:8000/`
2. Django's URL router matches empty path `""`
3. Request forwarded to `hello.urls`
4. `hello/urls.py` routes to `views.student_info`
5. View function processes request and returns rendered template

### 4. App Registration (settings.py)

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "hello",  # ← Our app is registered here
]
```

## 🎨 Design Features

### Professional UI Design

- **Clean Layout**: Uses CSS Grid for responsive design
- **Modern Styling**: Rounded corners, shadows, and hover effects
- **Color Scheme**: Professional blue and gray color palette
- **Typography**: Clean, readable Arial font
- **Responsive**: Works on desktop and mobile devices

### CSS Grid Layout

```css
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
}
```

This creates a 2x2 grid layout for the student information cards.

## 🧪 Testing the Application

### Manual Testing

1. **Start the server**:
   ```bash
   python manage.py runserver
   ```

2. **Test the webpage**:
   - Visit `http://127.0.0.1:8000/`
   - Verify all student information displays correctly
   - Check responsive design on different screen sizes

3. **Test URL routing**:
   - Main page: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### Automated Testing

```bash
# Run Django tests
python manage.py test

# Run tests with verbose output
python manage.py test -v 2

# Run specific app tests
python manage.py test hello
```

## 🔧 Customization Options

### 1. Modify Student Data

Edit `hello/views.py` to change student information:

```python
student_data = {
    'student_name': 'Jane Smith',
    'roll_number': '2024002',
    'branch': 'Information Technology',
    'semester': '8th'
}
```

### 2. Change Styling

Modify the CSS in `hello/templates/hello/student_info.html`:

```css
/* Change primary color */
.container {
    background-color: #f8f9fa;
    border-left: 4px solid #28a745; /* Green accent */
}

/* Modify grid layout */
.info-grid {
    grid-template-columns: 1fr; /* Single column layout */
}
```

### 3. Add More Information

Extend the student data and template:

```python
# In views.py
student_data = {
    'student_name': 'John Doe',
    'roll_number': '2024001',
    'branch': 'Computer Science',
    'semester': '6th',
    'cgpa': '8.5',  # New field
    'email': 'john.doe@university.edu'  # New field
}
```

```html
<!-- Add to template -->
<div class="info-item">
    <div class="info-label">CGPA</div>
    <div class="info-value">{{ student_data.cgpa }}</div>
</div>

<div class="info-item">
    <div class="info-label">Email</div>
    <div class="info-value">{{ student_data.email }}</div>
</div>
```

## 📈 Learning Objectives

This project demonstrates:

- **Django MVT Architecture**: Model-View-Template pattern implementation
- **URL Routing**: How Django handles URL patterns and request routing
- **Template Rendering**: Using Django Template Language (DTL)
- **Static File Management**: CSS styling and HTML structure
- **Separation of Concerns**: Keeping logic, presentation, and routing separate
- **Professional Web Design**: Modern, responsive CSS design
- **Development Workflow**: From project creation to deployment

## 🔗 Related Theory

- **[Django Architecture](../../theory/Django/1DjangoArchitecture.md)**: Understanding MVT pattern
- **[Project Structure](../../theory/Django/2.DjangoProjectStructure.md)**: Django project organization
- **[Templates](../../theory/Django/5Templates.md)**: Django Template Language
- **[URL Configuration](../../theory/Django/16Step4:_Register_App.md)**: URL routing patterns

## 🚀 Next Steps

### Enhancements You Can Add

1. **Database Integration**:
   - Replace hardcoded data with database models
   - Add student creation, editing, and deletion
   - Implement search and filtering

2. **User Interface**:
   - Add navigation menu
   - Implement multiple student views
   - Add forms for data entry

3. **Functionality**:
   - Student login/logout system
   - Admin panel for student management
   - Export student data to PDF/Excel

4. **Advanced Features**:
   - API endpoints for mobile apps
   - Real-time updates with WebSockets
   - Email notifications for updates

### Other Django Projects

- Explore [Flask Applications](../../flask/) for comparison
- Check out [Additional Django Projects](../) for more examples

## 📝 Technical Notes

### Django Configuration

- **Debug Mode**: Enabled for development
- **Database**: SQLite (default Django database)
- **Static Files**: Configured for development
- **Templates**: App-specific template directories enabled

### Performance Considerations

- **Static Files**: In production, use proper static file serving
- **Database**: Consider PostgreSQL or MySQL for production
- **Caching**: Implement caching for improved performance
- **Security**: Review security settings for production deployment

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Use a different port
   python manage.py runserver 8080
   ```

2. **Template not found**:
   - Ensure `APP_DIRS: True` in settings.py
   - Check template path: `hello/templates/hello/student_info.html`

3. **App not registered**:
   - Add `'hello'` to `INSTALLED_APPS` in settings.py

### Debug Mode

Django's debug mode provides detailed error pages. Make sure `DEBUG = True` in settings.py for development.

## 📊 Current Status

- ✅ **Development Server**: Running successfully on port 8000
- ✅ **URL Routing**: Working correctly
- ✅ **Template Rendering**: Student information displaying properly
- ✅ **Styling**: Professional CSS design implemented
- ✅ **Documentation**: Comprehensive project documentation

## 🎉 Conclusion

This Django mini project successfully demonstrates the core concepts of Django web development in a simple, practical example. It showcases the MVT architecture, URL routing, template rendering, and professional web design principles.

The project serves as an excellent starting point for understanding Django's capabilities and can be extended to build more complex applications with database integration, user authentication, and advanced features.

---

**Happy Django Learning! 🐍✨**

*For more Django learning resources, visit our [Django Theory Guide](../../theory/Django/README.md)*
