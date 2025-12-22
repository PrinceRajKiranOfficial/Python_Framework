# Context Management in Flask

## Table of Contents
- [Introduction](#introduction)
- [What is Context?](#what-is-context)
- [Flask Context Types](#flask-context-types)
- [Application Context](#application-context)
- [Request Context](#request-context)
- [Context Locals](#context-locals)
- [Context Usage Patterns](#context-usage-patterns)
- [Custom Context Usage](#custom-context-usage)
- [Best Practices](#best-practices)
- [Summary](#summary)

## Introduction

Understanding Flask's context system is crucial for building robust web applications. Context provides access to request data, application configuration, and global objects throughout your application lifecycle. This module explores Flask's context system and how to use it effectively.

## What is Context?

**Context** in Flask refers to the environment in which your application code executes. It provides access to objects that are globally available during request processing without explicitly passing them around.

### Why Context Matters

- **Request Data Access**: Access HTTP request data anywhere in your application
- **Global Object Management**: Maintain application state during request lifecycle
- **Thread Safety**: Ensure each request has its own isolated context
- **Simplified Code**: Avoid passing common objects through every function call

### Real-World Analogy

Think of context like a **hotel room service tray**:
- **Request Context**: The individual guest's room (isolated to that guest)
- **Application Context**: The hotel's general services (available throughout hotel)
- **Objects on Tray**: Request data, session info, application config
- **Room Service**: Your functions that can access the tray without carrying it around

## Flask Context Types

Flask provides two main types of context:

### 1. Application Context
- Contains application-level objects
- Lives throughout the application lifecycle
- Created when application starts

### 2. Request Context  
- Contains request-specific objects
- Created for each HTTP request
- Destroyed when request ends

```
Flask Context Hierarchy
┌─────────────────────────────────┐
│     Application Context          │
│  ┌─────────────────────────────┐ │
│  │     Request Context          │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │    Current Request      │ │ │
│  │  │   (g, request, session) │ │ │
│  │  └─────────────────────────┘ │ │
│  └─────────────────────────────┘ │
└─────────────────────────────────┘
```

## Application Context

The application context provides access to the current Flask application instance and configuration.

### Application Context Objects

| Object | Description |
|--------|-------------|
| `current_app` | Current application instance |
| `g` | Object for storing data during request |
| `app` | Alias for `current_app` |

### When Application Context is Active

- During request processing
- In CLI commands executed with Flask CLI
- In custom WSGI applications
- During application startup/shutdown

### Using Application Context

```python
from flask import current_app, g, has_app_context

# Access current application
def get_app_config():
    if has_app_context():
        return current_app.config
    else:
        return {'DEBUG': False, 'SECRET_KEY': 'default'}

# Use application context in functions
def expensive_database_query():
    if not hasattr(g, 'database'):
        g.database = create_database_connection(current_app.config['DATABASE_URL'])
    return g.database.execute('SELECT * FROM users')

@app.route('/users')
def list_users():
    # Application context is active here
    users = expensive_database_query()
    return jsonify(users)
```

### Manual Application Context

```python
from flask import Flask, current_app

# Method 1: Using app context manager
app = Flask(__name__)

with app.app_context():
    # Inside this block, current_app is available
    config_value = current_app.config['DEBUG']
    print(f"Debug mode: {config_value}")

# Method 2: Using application context pushing
app = Flask(__name__)

with app.app_context():
    # Application context is active
    current_app.config['CUSTOM_SETTING'] = 'value'
    
    # Can also push context manually
    app.app_context().push()
    
    # Now available
    print(current_app.config['CUSTOM_SETTING'])
```

## Request Context

The request context contains information about the current HTTP request and user session.

### Request Context Objects

| Object | Description | Type |
|--------|-------------|------|
| `request` | Current request object | Request |
| `session` | User session dictionary | dict |
| `g` | Request-scoped storage | object |

### Request Context Lifecycle

1. **Request Arrives**: Flask creates request context
2. **Context Pushed**: Request context becomes active
3. **Processing**: Your route functions execute
4. **Context Popped**: Request context is destroyed
5. **Cleanup**: All request-specific data is cleared

### Accessing Request Data

```python
from flask import request, session, g

@app.route('/api/users', methods=['POST'])
def create_user():
    # Request object - contains HTTP request data
    data = request.get_json()  # JSON data from request body
    
    # Access headers
    content_type = request.headers.get('Content-Type')
    user_agent = request.headers.get('User-Agent')
    
    # Access query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Access form data
    username = request.form.get('username')
    email = request.form.get('email')
    
    # Access files
    avatar = request.files.get('avatar')
    
    # Session data - persists across requests
    if 'user_id' not in session:
        session['user_id'] = create_anonymous_user()
    
    # Request-scoped storage
    g.request_start_time = time.time()
    
    # Process user creation
    user = User.create(username, email)
    session['user_id'] = user.id
    
    return jsonify({'user': user.to_dict()})

@app.route('/api/timing')
def get_request_timing():
    # Access data stored in g during request
    duration = time.time() - g.request_start_time
    return jsonify({'duration': duration})
```

### Handling Different Content Types

```python
from flask import request, jsonify

@app.route('/api/data', methods=['POST'])
def handle_data():
    content_type = request.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        # JSON data
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
            
    elif 'application/x-www-form-urlencoded' in content_type:
        # Form data
        data = request.form.to_dict()
        
    elif 'multipart/form-data' in content_type:
        # Form data with files
        data = request.form.to_dict()
        files = {key: file for key, file in request.files.items()}
        
    else:
        return jsonify({'error': 'Unsupported content type'}), 415
    
    return jsonify({'received': data})
```

## Context Locals

Context locals are thread-local objects that provide access to context data from anywhere in your application.

### Thread Safety

Flask's context locals ensure that each request has its own isolated data, even in multi-threaded environments.

```python
import threading
from flask import request

# Simulate multiple requests in different threads
def handle_request(thread_id):
    # Each thread has its own request context
    with app.test_request_context(f'/thread-{thread_id}'):
        request.data = f"Data from thread {thread_id}"
        print(f"Thread {thread_id}: {request.data}")

# Create multiple threads
threads = []
for i in range(3):
    thread = threading.Thread(target=handle_request, args=(i,))
    threads.append(thread)
    thread.start()

# Each thread maintains its own request data
# No interference between threads
```

### Context Local Objects

```python
from flask import Flask, g, request, session, current_app

app = Flask(__name__)

@app.before_request
def load_user_context():
    """Load user data before each request."""
    g.user = None
    
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    
    # Track request data
    g.request_id = generate_request_id()
    g.request_start_time = time.time()

@app.after_request
def log_request(response):
    """Log request completion."""
    duration = time.time() - g.request_start_time
    logger.info(f"Request {g.request_id} completed in {duration:.3f}s")
    return response

@app.route('/profile')
def get_profile():
    # Access user loaded in before_request
    if not g.user:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Access other context data
    return jsonify({
        'user': g.user.to_dict(),
        'request_id': g.request_id
    })
```

## Context Usage Patterns

### 1. Database Connection Management

```python
from flask import g
import sqlite3

def get_db():
    """Get database connection from context."""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/users')
def get_users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(user) for user in users])
```

### 2. Authentication Context

```python
from flask import g, session
from functools import wraps

def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            if 'user_id' in session:
                g.user = User.query.get(session['user_id'])
            
            if not g.user:
                return jsonify({'error': 'Authentication required'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected_route():
    return jsonify({'message': f'Hello, {g.user.name}!'})
```

### 3. Rate Limiting Context

```python
from flask import g, request
import time
from collections import defaultdict

# In-memory rate limiting storage
rate_limits = defaultdict(list)

def check_rate_limit():
    """Check if request exceeds rate limit."""
    client_ip = request.remote_addr
    now = time.time()
    
    # Clean old requests
    rate_limits[client_ip] = [
        req_time for req_time in rate_limits[client_ip]
        if now - req_time < 60  # Last minute
    ]
    
    # Check if over limit
    if len(rate_limits[client_ip]) >= 10:  # 10 requests per minute
        return False
    
    # Record this request
    rate_limits[client_ip].append(now)
    return True

@app.before_request
def enforce_rate_limit():
    """Enforce rate limiting before each request."""
    if not check_rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    g.rate_limit_ok = True
```

### 4. Logging and Monitoring

```python
import logging
from flask import g, request

@app.before_request
def setup_logging_context():
    """Setup logging context for each request."""
    g.request_id = str(uuid.uuid4())
    g.request_start = time.time()
    g.client_ip = request.remote_addr
    g.user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Log request start
    logger.info(f"Request started: {g.request_id} from {g.client_ip}")

@app.after_request
def log_response(response):
    """Log response completion."""
    duration = time.time() - g.request_start
    
    logger.info(
        f"Request completed: {g.request_id} "
        f"Status: {response.status_code} "
        f"Duration: {duration:.3f}s"
    )
    
    return response

@app.errorhandler(Exception)
def log_errors(error):
    """Log unhandled exceptions."""
    logger.error(
        f"Unhandled exception in request {g.request_id}: {str(error)}",
        exc_info=True
    )
    return jsonify({'error': 'Internal server error'}), 500
```

## Custom Context Usage

### Creating Custom Context Processors

```python
from flask import g, current_app

@app.context_processor
def inject_user():
    """Make user available in all templates."""
    return {'current_user': g.user}

@app.context_processor
def inject_app_config():
    """Make app config available in templates."""
    return {
        'app_name': current_app.config.get('APP_NAME', 'My App'),
        'debug_mode': current_app.config.get('DEBUG', False)
    }

# In templates, these variables are automatically available
# {{ current_user.name }}  # User object
# {{ app_name }}           # Application name
```

### Custom Context Managers

```python
import contextlib
from flask import g, current_app

@contextlib.contextmanager
def database_transaction():
    """Context manager for database transactions."""
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

@app.route('/create-post', methods=['POST'])
def create_post():
    data = request.get_json()
    
    with database_transaction() as db:
        # Create post
        post_id = db.execute(
            'INSERT INTO posts (title, content) VALUES (?, ?)',
            data['title'], data['content']
        ).lastrowid
        
        # Update user post count
        db.execute(
            'UPDATE users SET post_count = post_count + 1 WHERE id = ?',
            g.user.id
        )
        
        g.created_post_id = post_id
    
    return jsonify({'post_id': g.created_post_id})
```

### Thread-Local Storage Patterns

```python
import threading
from flask import g

# Custom thread-local storage
_thread_locals = threading.local()

def get_thread_data():
    """Get data stored in current thread."""
    return getattr(_thread_locals, 'data', {})

def set_thread_data(data):
    """Set data for current thread."""
    _thread_locals.data = data

class ThreadContext:
    """Context manager for thread-local data."""
    def __init__(self, **kwargs):
        self.data = kwargs
        self.original_data = None
    
    def __enter__(self):
        self.original_data = get_thread_data()
        set_thread_data(self.data)
        return self.data
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        set_thread_data(self.original_data)

# Usage
@app.before_request
def setup_thread_context():
    """Setup thread-local context."""
    with ThreadContext(
        request_id=str(uuid.uuid4()),
        start_time=time.time(),
        client_ip=request.remote_addr
    ):
        # This context is available in current thread
        data = get_thread_data()
        g.request_id = data['request_id']
```

## Best Practices

### 1. Context Safety

```python
from flask import has_app_context, has_request_context

def safe_function():
    """Function that works with or without context."""
    if has_app_context():
        config = current_app.config
    else:
        config = get_default_config()
    
    if has_request_context():
        user_id = session.get('user_id')
    else:
        user_id = None
    
    return process_with_config(config, user_id)
```

### 2. Avoid Context Leakage

```python
# Good: Clean up context data
@app.teardown_appcontext
def cleanup_resources(error):
    """Clean up resources when context ends."""
    if hasattr(g, 'database'):
        g.database.close()
        del g.database
    
    if hasattr(g, 'temp_files'):
        for temp_file in g.temp_files:
            temp_file.close()
        del g.temp_files

# Avoid: Leaving resources open
@app.route('/bad-example')
def bad_example():
    # Creates resource but never cleans it up
    g.file = open('/tmp/temp.txt', 'w')
    return "Done"
```

### 3. Context in Background Tasks

```python
from flask import current_app
from celery import Celery

celery = Celery(__name__)

@celery.task
def background_task(user_id):
    """Background task that needs app context."""
    # Need to push application context for background tasks
    with current_app.app_context():
        user = User.query.get(user_id)
        send_notification_email(user.email)
        return f"Notification sent to {user.email}"

# In Flask route
@app.route('/trigger-task')
def trigger_background_task():
    background_task.delay(g.user.id)
    return jsonify({'message': 'Task queued'})
```

### 4. Testing with Context

```python
import pytest
from flask import Flask

@pytest.fixture
def app():
    """Create test application."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # Setup test database
        db.create_all()
        yield app
        # Cleanup
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_with_context(client):
    """Test that requires request context."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    
    response = client.get('/protected')
    assert response.status_code == 200
```

## Summary

Flask's context system is a powerful feature that provides global access to request and application data. Understanding context locals, application context, and request context is essential for building sophisticated Flask applications.

### Key Takeaways

- **Application Context**: Provides application-level objects (`current_app`, `g`)
- **Request Context**: Provides request-specific objects (`request`, `session`)
- **Context Locals**: Thread-safe access to context data
- **Lifecycle Management**: Contexts are created/destroyed automatically
- **Best Practices**: Clean up resources, avoid context leakage, handle background tasks properly

### Next Steps

With context management understood, we'll explore **Templates** - how Flask uses Jinja2 to generate dynamic HTML and create dynamic web pages.

---

*Previous: [Modules & Packages](./06-modules-packages.md)*  
*Next: [Templates](./08-templates.md)*
