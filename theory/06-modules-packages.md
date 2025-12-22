# Modules & Packages

## Table of Contents
- [Introduction](#introduction)
- [What are Modules?](#what-are-modules)
- [What are Packages?](#what-are-packages)
- [Creating Modules](#creating-modules)
- [Creating Packages](#creating-packages)
- [Import Statements](#import-statements)
- [Modules in Flask Applications](#modules-in-flask-applications)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Summary](#summary)

## Introduction

As applications grow in complexity, organizing code becomes crucial. Modules and packages provide a way to structure Python code logically, making it more maintainable, reusable, and easier to understand. Flask applications heavily rely on these concepts for organization.

## What are Modules?

A **module** is simply a Python file (with `.py` extension) that contains Python definitions and statements. Modules help break down large programs into smaller, manageable pieces.

### Benefits of Modules

- **Organization**: Group related functionality together
- **Reusability**: Use code across different parts of your application
- **Maintainability**: Easier to debug and update
- **Namespace Management**: Avoid naming conflicts

### Basic Module Example

```python
# math_utils.py
def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

PI = 3.14159

class Calculator:
    """Simple calculator class."""
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        result = operation(a, b)
        self.history.append(f"{a} {operation.__name__} {b} = {result}")
        return result
```

Using the module:

```python
# main.py
import math_utils
from math_utils import add, multiply, PI

# Method 1: Import entire module
result1 = math_utils.add(5, 3)
print(result1)  # 8

# Method 2: Import specific items
result2 = multiply(4, 7)
print(result2)  # 28

# Method 3: Import with alias
import math_utils as mu
result3 = mu.add(10, 15)

print(f"Value of PI: {PI}")
```

## What are Packages?

A **package** is a collection of modules organized in directories. Packages help organize related modules under a common namespace.

### Package Structure

```
my_package/
├── __init__.py          # Makes it a package
├── module1.py           # Regular module
├── module2.py           # Regular module
└── subpackage/
    ├── __init__.py      # Makes subdirectory a package
    ├── sub_module1.py   # Module in subpackage
    └── sub_module2.py   # Module in subpackage
```

### The `__init__.py` File

This file:
- Makes a directory a Python package
- Can be empty or contain initialization code
- Controls what gets imported when using `from package import *`

```python
# my_package/__init__.py
# Import key classes and functions for easy access
from .module1 import important_function
from .module2 import ImportantClass

__all__ = ['important_function', 'ImportantClass']
```

## Creating Modules

### 1. Simple Module

```python
# validators.py
import re

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

class ValidationError(Exception):
    """Custom validation error."""
    pass
```

### 2. Module with Configuration

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class Config:
    """Application configuration."""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## Creating Packages

### 1. User Management Package

```
user_management/
├── __init__.py
├── models.py
├── views.py
├── forms.py
├── utils.py
└── validators/
    ├── __init__.py
    ├── email_validator.py
    └── password_validator.py
```

```python
# user_management/__init__.py
"""User management package for Flask application."""

from .models import User, UserProfile
from .views import user_bp
from .forms import RegistrationForm, LoginForm

__all__ = ['User', 'UserProfile', 'user_bp', 'RegistrationForm', 'LoginForm']
```

```python
# user_management/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Hash and set password."""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class UserProfile(db.Model):
    """Extended user profile information."""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
```

### 2. API Package

```
api/
├── __init__.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── posts.py
├── serializers/
│   ├── __init__.py
│   ├── user_serializer.py
│   └── post_serializer.py
└── utils/
    ├── __init__.py
    ├── responses.py
    └── decorators.py
```

## Import Statements

### Basic Imports

```python
# Import entire module
import math

# Import specific items
from math import pi, sqrt, floor

# Import with alias
import numpy as np
from flask import Flask as FlaskApp

# Import all (not recommended)
from math import *
```

### Relative Imports

```python
# In package structure:
# my_package/
#   ├── __init__.py
#   ├── module_a.py
#   └── sub_package/
#       ├── __init__.py
#       └── module_b.py

# From module_b.py importing from parent package:

# Same level import
from .module_a import function_from_a

# From subpackage import
from .sub_package.module_b import function_from_b

# From parent package
from .. import function_from_parent

# Absolute import
from my_package.module_a import function_from_a
```

### Import Patterns in Flask

```python
# Circular import solution
# app/__init__.py
from flask import Flask

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Import blueprints after app creation
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# api/routes/__init__.py
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import views after blueprint creation
from . import auth, users, posts

# api/routes/auth.py
from flask import request, jsonify
from .. import api_bp

@api_bp.route('/login', methods=['POST'])
def login():
    # Login logic
    pass
```

## Modules in Flask Applications

### 1. Blueprint Organization

```python
# api/users/__init__.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)

from . import views, models, forms

# api/users/models.py
from .. import db

class User(db.Model):
    # User model definition
    pass

# api/users/views.py
from flask import request, jsonify
from . import users_bp

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    # Get user logic
    pass
```

### 2. Application Factory Pattern

```python
# app/factory.py
from flask import Flask

def create_app(config_name='development'):
    """Application factory."""
    app = Flask(__name__)
    
    # Load configuration
    from .config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from .extensions import db, login_manager, migrate
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app

# app/__init__.py
from .factory import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```

### 3. Utilities Module

```python
# app/utils/decorators.py
from functools import wraps
from flask import jsonify, request
from .auth import token_required

def json_required(f):
    """Decorator to require JSON content."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function

def paginated_results(f):
    """Decorator to add pagination to results."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = f(*args, **kwargs)
        
        if isinstance(result, dict) and 'items' in result:
            result['pagination'] = {
                'page': page,
                'per_page': per_page,
                'total': result['total']
            }
        
        return result
    return decorated_function
```

## Best Practices

### 1. Package Structure

```
your_app/
├── app.py                 # Entry point
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── instance/
│   └── config.py         # Instance-specific config
├── your_app/             # Main application package
│   ├── __init__.py
│   ├── models/           # Database models
│   ├── views/            # Route handlers
│   ├── forms/            # Form classes
│   ├── utils/            # Utility functions
│   ├── static/           # Static files
│   └── templates/        # HTML templates
└── tests/                # Test files
```

### 2. Clear Module Names

```python
# Good
user_management.py
database_connection.py
email_sender.py
api_client.py

# Avoid
utils.py
helper.py
main.py (unless it's entry point)
functions.py
```

### 3. Use `__all__` for Public APIs

```python
# __init__.py in your package
__all__ = [
    'User',           # Public classes
    'create_user',    # Public functions
    'UserForm'        # Public forms
]

# Private modules/functions
from .models import _PrivateModel
from .utils import _internal_function
```

### 4. Handle Imports Properly

```python
# Separate imports
import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify

# Group by source
import third_party
from my_package import module_a
from my_package.sub_package import module_b

# Local imports (at bottom)
from .models import User
from .forms import UserForm
```

### 5. Avoid Circular Imports

```python
# Problem: Circular import
# models.py
from views import process_user

# views.py  
from models import User

# Solution: Move shared imports to third module
# common.py
from database import db

# models.py
from .common import db

# views.py
from .common import db
```

## Common Patterns

### 1. Configuration Module

```python
# config.py
import os

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev.db'

class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### 2. Extension Initialization

```python
# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# app.py
from extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    return app
```

### 3. Blueprint Registration

```python
# api/__init__.py
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes to register them
from . import routes

# api/routes.py
from . import api_bp

@api_bp.route('/users')
def get_users():
    # Implementation
    pass
```

## Summary

Modules and packages are fundamental to organizing Python code effectively. They provide structure, promote reusability, and make large applications manageable.

### Key Takeaways

- **Modules**: Individual Python files containing code
- **Packages**: Collections of modules organized in directories
- **Organization**: Break large applications into logical components
- **Reusability**: Write once, use many times across your application
- **Maintainability**: Easier to debug, test, and update
- **Flask Integration**: Use blueprints and application factory pattern

### Next Steps

Understanding modules and packages sets the foundation for **Context Management** in Flask, where we'll learn how Flask handles request data and application state.

---

*Previous: [Decorators](./05-decorators.md)*  
*Next: [Context Management](./07-context-management.md)*
