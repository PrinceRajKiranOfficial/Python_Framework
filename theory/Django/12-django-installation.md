# Django Installation and Environment Setup

[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)
[![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-brightgreen.svg)](#difficulty-level)

## 🎯 Overview

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. This comprehensive guide will walk you through installing Django and setting up your development environment for professional web development.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Django Installation](#django-installation)
- [Version Verification](#version-verification)
- [Project Structure Creation](#project-structure-creation)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## 🔧 Prerequisites

Before installing Django, ensure you have the following:

### Required Software

- **Python 3.8 or higher** - Django requires Python 3.8+
- **pip** - Python package manager (usually comes with Python)
- **virtualenv** - Virtual environment manager (recommended)

### System Requirements

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Python | 3.8+ | 3.11+ |
| pip | 19.0+ | Latest |
| virtualenv | 16.0+ | Latest |

### Python Installation Check

```bash
# Check Python version
python --version
# or
python3 --version

# Check pip installation
pip --version
# or
pip3 --version
```

**Expected Output:**
```
Python 3.11.7
pip 23.3.1
```

## 🛠️ Installation Methods

Django can be installed using several methods. We'll cover the most reliable approaches:

### Method  (Recommended)

The most straightforward method using1: pip pip:

```bash
# Install latest Django version
pip install django

# Install specific version
pip install django==4.2.7

# Install with specific Python version
python -m pip install django
```

### Method 2: pip3 (Linux/macOS)

For systems with multiple Python versions:

```bash
# Use pip3 explicitly
pip3 install django

# Install for specific Python version
python3 -m pip install django
```

### Method 3: pipx (Advanced)

For isolated application installations:

```bash
# Install pipx first
pip install pipx

# Install Django in isolated environment
pipx install django
```

## 🔄 Virtual Environment Setup

Using a virtual environment is **highly recommended** to avoid conflicts with system packages.

### Creating a Virtual Environment

```bash
# Create virtual environment named 'django-env'
python -m venv django-env

# Activate virtual environment
# On Windows:
django-env\Scripts\activate

# On macOS/Linux:
source django-env/bin/activate

# Verify activation (you should see (django-env) in your prompt)
which python
```

### Using virtualenv (Alternative)

```bash
# Install virtualenv if not available
pip install virtualenv

# Create virtual environment
virtualenv django-env

# Activate
# Windows:
django-env\Scripts\activate
# macOS/Linux:
source django-env/bin/activate
```

### Virtual Environment Best Practices

```bash
# Install Django in activated virtual environment
pip install django

# Freeze requirements for deployment
pip freeze > requirements.txt

# Install from requirements in production
pip install -r requirements.txt
```

## 📦 Django Installation

Once your virtual environment is activated, install Django:

### Latest Stable Version

```bash
pip install django
```

### Specific Version Installation

```bash
# Install Django 4.2.7 (LTS version)
pip install django==4.2.7

# Install with additional packages
pip install django pillow requests
```

### Development Installation

For contributing to Django or using bleeding-edge features:

```bash
# Install from source
pip install https://github.com/django/django/archive/main.zip

# Install in development mode
pip install -e /path/to/django/source
```

## ✅ Version Verification

Verify your Django installation:

### Basic Verification

```bash
# Check Django version
django-admin --version

# Alternative method
python -c "import django; print(django.get_version())"
```

### Expected Output

```
4.2.7
```

### Comprehensive Check

Create a test script to verify Django is working:

```python
# test_django_installation.py
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        SECRET_KEY='test-key-for-verification',
    )

# Test Django imports
try:
    from django.db import models
    from django.http import HttpResponse
    from django.shortcuts import render
    from django.urls import path
    
    print("✅ Django installation successful!")
    print(f"📊 Django version: {django.get_version()}")
    print("🔧 All core modules imported successfully")
    
except ImportError as e:
    print(f"❌ Django installation failed: {e}")
```

Run the test:

```bash
python test_django_installation.py
```

## 🏗️ Project Structure Creation

After successful installation, create your first Django project:

### Create New Project

```bash
# Create new project named 'myproject'
django-admin startproject myproject

# Navigate to project directory
cd myproject

# Project structure created:
myproject/
├── manage.py
└── myproject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

### Verify Project Creation

```bash
# Test project setup
python manage.py runserver

# Should see:
# Starting development server at http://127.0.0.1:8000/
```

## 🚨 Troubleshooting

### Common Installation Issues

#### 1. Permission Errors

**Problem:** `Permission denied` during pip install

**Solution:**
```bash
# Use --user flag
pip install --user django

# Or use virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate  # Linux/macOS
myenv\Scripts\activate     # Windows
pip install django
```

#### 2. Python Version Issues

**Problem:** "Django requires Python 3.8+"

**Solution:**
```bash
# Check Python version
python --version

# Install specific Python version
# Ubuntu/Debian:
sudo apt install python3.11 python3.11-venv

# macOS:
brew install python@3.11

# Windows: Download from python.org
```

#### 3. pip Not Found

**Problem:** `pip: command not found`

**Solution:**
```bash
# Install pip
python -m ensurepip --upgrade

# Or use get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### 4. SSL Certificate Errors

**Problem:** SSL certificate verification failed

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with trusted hosts
pip install django --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

#### 5. Virtual Environment Issues

**Problem:** Virtual environment not activating

**Solution:**
```bash
# Check virtualenv installation
pip install virtualenv

# Create with explicit python version
virtualenv -p python3 myenv

# Or use python -m venv
python3 -m venv myenv
source myenv/bin/activate
```

## 📋 Best Practices

### Environment Management

1. **Always use virtual environments**
   ```bash
   # Create project-specific virtual environment
   python -m venv myproject-env
   source myproject-env/bin/activate
   pip install django
   ```

2. **Use requirements.txt**
   ```bash
   # Save dependencies
   pip freeze > requirements.txt
   
   # Install in new environment
   pip install -r requirements.txt
   ```

3. **Version pinning for production**
   ```bash
   # requirements.txt
   django==4.2.7
   pillow==10.0.1
   requests==2.31.0
   ```

### Security Considerations

1. **Keep Django updated**
   ```bash
   pip install --upgrade django
   ```

2. **Use environment variables for secrets**
   ```python
   # settings.py
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   SECRET_KEY = os.getenv('SECRET_KEY')
   DEBUG = os.getenv('DEBUG', 'False') == 'True'
   ```

3. **Use HTTPS in production**
   ```python
   # settings.py
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

### Development Workflow

1. **Create virtual environment first**
2. **Install Django and dependencies**
3. **Start project immediately**
4. **Run migrations before development**
5. **Use development server for testing**

## 🎯 Next Steps

With Django successfully installed, you're ready to:

1. **[Create Your First Django Project](./13-django-project-creation.md)** - Learn project structure and organization
2. **[Understand Django Architecture](./1DjangoArchitecture.md)** - Dive into MVT pattern and framework design
3. **[Explore Django Project Structure](./2.DjangoProjectStructure.md)** - Master file organization and responsibilities

## 🔗 Additional Resources

### Official Documentation
- [Django Official Installation Guide](https://docs.djangoproject.com/en/stable/topics/install/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/topics/best-practices/)

### Community Resources
- [Django Community](https://www.djangoproject.com/foundation/)
- [Django Packages](https://djangopackages.org/)
- [Django Reddit](https://www.reddit.com/r/django/)

### Video Tutorials
- [Django Official Tutorial](https://docs.djangoproject.com/en/stable/intro/)
- [Django for Beginners](https://djangoforbeginners.com/)

---

**✅ Django Installation Complete!**

*You're now ready to start building professional web applications with Django. Next, learn how to create and structure your Django projects.*

*Previous: [Django Workflow](../11DjangoWorkFLow.md)*  
*Next: [Django Project Creation](./13-django-project-creation.md)*
