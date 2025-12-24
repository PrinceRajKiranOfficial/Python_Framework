# 🚀 Code Workflows for Flask Development

A comprehensive guide to effective development workflows, code organization, and best practices for building scalable Flask applications.

## 📋 Table of Contents

- [Introduction to Code Workflows](#introduction-to-code-workflows)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Organization Patterns](#code-organization-patterns)
- [Application Factory Pattern](#application-factory-pattern)
- [Configuration Management](#configuration-management)
- [Error Handling Strategies](#error-handling-strategies)
- [Testing Workflows](#testing-workflows)
- [Documentation Workflows](#documentation-workflows)
- [Deployment Preparation](#deployment-preparation)
- [Performance Optimization](#performance-optimization)
- [Team Collaboration](#team-collaboration)
- [Maintenance and Updates](#maintenance-and-updates)

## Introduction to Code Workflows

Effective code workflows are the backbone of successful Flask development. They ensure:

- **Consistent development** practices across the team
- **Maintainable code** that can be easily understood and modified
- **Scalable applications** that grow with requirements
- **Reliable deployments** with minimal issues
- **Quality assurance** through testing and review processes

### Why Workflows Matter

```python
# Bad Workflow: Everything in one file
# app.py (500+ lines)
from flask import Flask
app = Flask(__name__)
# All routes, models, utilities mixed together

# Good Workflow: Organized structure
# Clear separation of concerns
# Easy to maintain and test
```

## Project Structure

A well-organized Flask project follows a logical structure that separates concerns and promotes maintainability.

### Basic Flask Project Structure

```
flask_project/
├── app/                      # Main application package
│   ├── __init__.py          # Application factory
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   ├── routes/              # URL routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   ├── static/              # CSS, JS, images
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── forms.py
│   │   └── helpers.py
│   ├── config.py            # Configuration settings
│   └── errors/              # Error handlers
│       ├── __init__.py
│       ├── handlers.py
│       └── 404.html
├── tests/                   # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_utils.py
├── migrations/              # Database migrations
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── run.py                  # Application entry point
├── config.py               # Configuration file
└── README.md               # Project documentation
```

### Application Factory Structure

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    
    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
```

## Development Workflow

### Daily Development Cycle

1. **Plan and Design**
   - Define features or fixes needed
   - Design database schema if needed
   - Plan API endpoints or routes

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/user-authentication
   ```

3. **Write Code**
   - Implement features following project structure
   - Add docstrings and comments
   - Follow coding standards

4. **Test Locally**
   ```bash
   # Run Flask application
   python run.py
   
   # Run tests
   pytest tests/
   
   # Check code quality
   flake8 app/
   black app/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add user authentication functionality"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/user-authentication
   # Create Pull Request on GitHub
   ```

### Feature Development Workflow

#### Step 1: Analysis and Planning

```python
# Before coding, plan your feature:
# 1. What functionality is needed?
# 2. What database changes are required?
# 3. What routes/endpoints are needed?
# 4. What tests should be written?

# Example: User Profile Feature
# - Database: User model needs profile fields
# - Routes: /profile, /profile/edit
# - Templates: profile.html, profile_edit.html
# - Tests: Test profile views, forms, validation
```

#### Step 2: Implementation

```python
# models/user.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # New profile fields
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    
# routes/profile.py
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update user profile
        pass
    return render_template('profile_edit.html', form=form)
```

#### Step 3: Testing

```python
# tests/test_profile.py
def test_profile_page_access(client):
    """Test that profile page requires login"""
    response = client.get('/profile')
    assert response.status_code == 302  # Redirect to login

def test_profile_page_content(logged_in_client):
    """Test profile page shows user information"""
    response = logged_in_client.get('/profile')
    assert response.status_code == 200
    assert b'John Doe' in response.data
```

#### Step 4: Documentation

```markdown
# docs/features/user-profile.md
# User Profile Feature

## Overview
Allows users to view and edit their profile information.

## Routes
- `GET /profile` - View profile
- `GET/POST /profile/edit` - Edit profile

## Models
- User model extended with profile fields

## Templates
- `profile.html` - Profile display
- `profile_edit.html` - Profile editing form
```

## Code Organization Patterns

### Blueprint Pattern

Blueprints organize routes and related functionality into modular components.

```python
# app/routes/auth.py
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.routes import auth  # Import routes at bottom to avoid circular imports

# app/routes/__init__.py
from app.routes.auth import bp as auth_bp
from app.routes.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    return app
```

### Service Layer Pattern

Separate business logic from routes and models.

```python
# app/services/user_service.py
from app.models.user import User
from app import db

class UserService:
    @staticmethod
    def create_user(username, email, password):
        """Create a new user with hashed password"""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """Update user profile information"""
        user = User.query.get(user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user

# app/routes/profile.py
from app.services.user_service import UserService

@bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    user_service = UserService()
    user_service.update_user_profile(
        current_user.id,
        first_name=form.first_name.data,
        last_name=form.last_name.data
    )
    return redirect(url_for('profile'))
```

### Repository Pattern

Abstract database operations for better testability.

```python
# app/repositories/user_repository.py
from abc import ABC, abstractmethod
from app.models.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user_data):
        pass
    
    @abstractmethod
    def find_by_id(self, user_id):
        pass
    
    @abstractmethod
    def find_by_email(self, email):
        pass

class SQLAlchemyUserRepository(UserRepositoryInterface):
    def create(self, user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    def find_by_id(self, user_id):
        return User.query.get(user_id)
    
    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

# Dependency injection
user_repository = SQLAlchemyUserRepository()
```

## Application Factory Pattern

The application factory pattern allows for better testing and configuration management.

### Basic Factory Pattern

```python
# app/factory.py
from flask import Flask
from app.extensions import db, login_manager, ma

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.{config_name.title()}Config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    from app.routes import register_blueprints
    register_blueprints(app)

def register_error_handlers(app):
    from app.errors import register_error_handlers
    register_error_handlers(app)
```

### Factory with Testing Support

```python
# app/factory.py
import os
import tempfile

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object(test_config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints and error handlers
    register_blueprints(app)
    register_error_handlers(app)
    
    @app.before_first_request
    def create_tables():
        db.create_all()
    
    return app

def create_test_app():
    """Create test application with in-memory database"""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }
    return create_app(test_config)
```

## Configuration Management

### Environment-Based Configuration

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///app.db'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.ERROR)
        app.logger.addHandler(syslog_handler)

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### Environment Variables

```bash
# .env (add to .gitignore)
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

```python
# app/utils/environment.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name, default=None):
    """Get environment variable with fallback"""
    return os.environ.get(name, default)

def require_env_variable(name):
    """Get environment variable, raise error if missing"""
    value = os.environ.get(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is required")
    return value
```

## Error Handling Strategies

### Custom Error Handlers

```python
# app/errors/handlers.py
from flask import render_template
from app import db

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

# app/errors/handlers.py
from flask import Blueprint

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
```

### Form Validation and Error Handling

```python
# app/utils/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    email = StringField('Email Address', [
        validators.Length(min=6, max=35),
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

# app/routes/auth.py
from app.utils.forms import RegistrationForm

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process valid form
        return redirect(url_for('auth.login'))
    else:
        # Form has validation errors
        return render_template('auth/register.html', form=form)
```

```html
<!-- templates/auth/register.html -->
<form method="POST" action="{{ url_for('auth.register') }}">
    {{ form.hidden_tag() }}
    
    <div class="form-group">
        {{ form.username.label }}
        {{ form.username(class="form-control") }}
        {% if form.username.errors %}
            <div class="text-danger">
                {% for error in form.username.errors %}
                    <span>{{ error }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <div class="form-group">
        {{ form.email.label }}
        {{ form.email(class="form-control") }}
        {% if form.email.errors %}
            <div class="text-danger">
                {% for error in form.email.errors %}
                    <span>{{ error }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    {{ form.submit(class="btn btn-primary") }}
</form>
```

## Testing Workflows

### Unit Testing

```python
# tests/test_user_model.py
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(app, client):
    """Test user model creation"""
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    
    db.session.add(user)
    db.session.commit()
    
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')

def test_user_authentication(client):
    """Test user authentication"""
    # Test login with valid credentials
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Test login with invalid credentials
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200  # Form with errors
```

### Integration Testing

```python
# tests/test_routes.py
def test_user_registration_flow(client):
    """Test complete user registration workflow"""
    # Register new user
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Please check your email' in response.data
    
    # Login with new credentials
    response = client.post('/auth/login', data={
        'email': 'new@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome' in response.data

@pytest.mark.parametrize("email,password,expected", [
    ('test@example.com', 'wrongpassword', False),
    ('nonexistent@example.com', 'password', False),
    ('test@example.com', 'password123', True),
])
def test_login_validation(client, email, password, expected):
    """Test login validation with various inputs"""
    response = client.post('/auth/login', data={
        'email': email,
        'password': password
    })
    
    if expected:
        assert response.status_code == 302  # Redirect on success
    else:
        assert response.status_code == 200  # Form with errors
```

### Testing Fixtures

```python
# tests/conftest.py
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def user(app):
    """Create a test user"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def logged_in_client(client, user):
    """Create a logged-in test client"""
    with client.session_transaction() as sess:
        sess['user_id'] = user.id
        sess['_fresh'] = True
    return client
```

## Documentation Workflows

### API Documentation

```python
# app/routes/api.py
from flask import jsonify, request
from app import db
from app.models.user import User
from app.utils.decorators import api_required

@bp.route('/api/users/<int:user_id>', methods=['GET'])
@api_required
def get_user(user_id):
    """
    Get user by ID
    
    ---
    get:
        summary: Retrieve a user
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
        responses:
            200:
                description: User found
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                        username:
                            type: string
                        email:
                            type: string
            404:
                description: User not found
    """
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })
```

### Code Documentation

```python
# app/models/user.py
class User(db.Model):
    """
    User model for the application.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username
        email (str): Unique email address
        password_hash (str): Hashed password
        created_at (datetime): Account creation timestamp
        
    Relationships:
        posts (relationship): One-to-many relationship with Post model
        
    Example:
        >>> user = User(username='john', email='john@example.com')
        >>> user.set_password('secret')
        >>> db.session.add(user)
    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """
        Set password hash using Werkzeug security.
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if provided password matches hash.
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
```

## Deployment Preparation

### Production Configuration

```python
# config.py
class ProductionConfig(Config):
    """Production configuration with security best practices"""
    DEBUG = False
    TESTING = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Database configuration
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.ERROR)
        app.logger.addHandler(syslog_handler)
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

```dockerfile
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/app
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Performance Optimization

### Database Optimization

```python
# app/models/user.py
class User(db.Model):
    __tablename__ = 'users'
    
    # Add indexes for frequently queried fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Use selectinload for relationships
    posts = db.relationship('Post', backref='author', lazy='selectin')

# app/routes/users.py
@bp.route('/users/<username>')
def user_profile(username):
    # Use get_or_404 for efficiency
    user = User.query.filter_by(username=username).first_or_404()
    
    # Use pagination for large result sets
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('user.html', user=user, posts=posts)
```

### Caching Strategy

```python
# app/utils/cache.py
from flask_caching import Cache

cache = Cache()

def cache_key(*args, **kwargs):
    """Generate cache key from function arguments"""
    key_parts = []
    if args:
        key_parts.extend(str(arg) for arg in args)
    if kwargs:
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)

# app/routes/users.py
from app.utils.cache import cache, cache_key

@bp.route('/users/<username>')
@cache.cached(timeout=300, key_func=cache_key)
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

# app/__init__.py
def create_app():
    app = Flask(__name__)
    
    # Configure caching
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    
    cache.init_app(app)
    
    return app
```

## Team Collaboration

### Git Workflow

```bash
# Feature development workflow
git checkout main
git pull origin main
git checkout -b feature/new-feature

# Work on feature
git add .
git commit -m "Add new feature functionality"

# Before pushing
git fetch origin
git rebase origin/main
git push origin feature/new-feature

# Create pull request on GitHub
# After review and approval
git checkout main
git pull origin main
git branch -d feature/new-feature
```

### Code Review Process

```markdown
# Pull Request Template

## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated

## Screenshots
If applicable, add screenshots of changes.
```

### Code Standards

```python
# .flake8
[flake8]
max-line-length = 88
exclude = 
    .git,
    __pycache__,
    venv,
    migrations
ignore = 
    E203,  # whitespace before ':'
    W503,  # line break before binary operator

# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 21.9b0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
    -   id: flake8
```

## Maintenance and Updates

### Dependency Management

```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package-name

# Update all packages
pip list --outdated | cut -d'=' -f1 | xargs pip install -U

# Use requirements.txt for reproducible environments
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Database Migrations

```python
# Using Flask-Migrate
from flask_migrate import Migrate, upgrade

# Create migration
flask db migrate -m "Add user profile fields"

# Apply migrations
flask db upgrade

# Downgrade if needed
flask db downgrade
```

### Monitoring and Logging

```python
# app/utils/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug and not app.testing:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log', maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')
```

## 🎯 Summary

Effective code workflows for Flask development include:

- **Well-organized project structure** with clear separation of concerns
- **Consistent development workflow** from planning to deployment
- **Application factory pattern** for better testing and configuration
- **Comprehensive error handling** and validation strategies
- **Robust testing workflows** covering unit, integration, and end-to-end tests
- **Clear documentation** for code, APIs, and processes
- **Production-ready configuration** with security best practices
- **Performance optimization** through caching and database optimization
- **Team collaboration** standards and code review processes
- **Maintenance procedures** for updates and monitoring

With solid code workflows established, you're ready for **Advanced Workflows** to take your Flask development to the next level!

*Next: [Advanced Workflows](./15-advanced-workflows)*

*Previous: [Virtual Environment Creation](./13-virtual-environment-creation.md)*
