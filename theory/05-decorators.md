# Decorators in Python & Flask

## Table of Contents
- [Introduction](#introduction)
- [What are Decorators?](#what-are-decorators)
- [How Decorators Work](#how-decorators-work)
- [Basic Decorator Examples](#basic-decorator-examples)
- [Decorators in Flask](#decorators-in-flask)
- [Common Flask Decorators](#common-flask-decorators)
- [Custom Decorators](#custom-decorators)
- [Best Practices](#best-practices)
- [Summary](#summary)

## Introduction

Decorators are one of Python's most powerful and elegant features. They modify the behavior of functions or methods without changing their actual code. In Flask, decorators are essential for routing and many other functionalities.

## What are Decorators?

A **decorator** is a function that takes another function as input and extends its behavior without explicitly modifying it. Think of it as a "wrapper" that adds functionality around the original function.

### Why Use Decorators?

- **DRY Principle**: Avoid repeating code across multiple functions
- **Cross-cutting Concerns**: Add functionality that applies to multiple functions
- **Clean Code**: Separate concerns and keep functions focused
- **Reusability**: Create reusable functionality components

### Simple Analogy

Think of a decorator like a gift wrapper:
- **Original Function**: The gift itself
- **Decorator**: The wrapper paper and ribbon
- **Decorated Function**: The wrapped gift

The gift remains the same, but now it has additional presentation and functionality.

## How Decorators Work

### Basic Decorator Pattern

```python
def decorator_function(original_function):
    def wrapper_function():
        # Add functionality before original function
        print("Before the function call")
        
        # Call the original function
        result = original_function()
        
        # Add functionality after original function
        print("After the function call")
        
        return result
    return wrapper_function
```

### Using the Decorator

```python
@decorator_function
def say_hello():
    print("Hello!")

# This is equivalent to:
# say_hello = decorator_function(say_hello)

# When called:
say_hello()
# Output:
# Before the function call
# Hello!
# After the function call
```

## Basic Decorator Examples

### 1. Timing Decorator

```python
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    time.sleep(1)
    print("Function completed!")

# Output: slow_function took 1.0012 seconds
```

### 2. Authentication Decorator

```python
def requires_auth(func):
    def wrapper(user):
        if not user.is_authenticated:
            print("Authentication required!")
            return None
        return func(user)
    return wrapper

@requires_auth
def get_user_dashboard(user):
    return f"Dashboard for {user.name}"

# Usage
admin = User("admin", authenticated=True)
guest = User("guest", authenticated=False)

get_user_dashboard(admin)     # Works
get_user_dashboard(guest)     # Authentication required!
```

### 3. Validation Decorator

```python
def validate_input(validation_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate all arguments
            for arg in args:
                if not validation_func(arg):
                    raise ValueError(f"Invalid input: {arg}")
            for key, value in kwargs.items():
                if not validation_func(value):
                    raise ValueError(f"Invalid {key}: {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_input(lambda x: isinstance(x, str) and len(x) > 0)
def process_text(text):
    return text.upper()

# process_text("hello")  # Works
# process_text("")       # Raises ValueError
```

## Decorators in Flask

Flask heavily uses decorators for routing, and understanding them is crucial for Flask development.

### Basic Flask Routing

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flask!"

@app.route('/about')
def about():
    return "About page"
```

What happens here:
1. `@app.route('/')` is a decorator that registers the function as a route handler
2. When someone visits `/`, Flask calls the `home()` function
3. The return value becomes the HTTP response

### Multiple Routes for Same Function

```python
@app.route('/')
@app.route('/home')
def index():
    return "Home page"
```

### HTTP Methods

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        return "Processing login..."
    else:
        # Show login form
        return "Login form"
```

### Dynamic Routes

```python
@app.route('/user/<username>')
def show_user(username):
    return f"User: {username}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post ID: {post_id}"
```

## Common Flask Decorators

### 1. Routing Decorators

```python
# Basic routing
@app.route('/path')
@app.route('/path/<variable>')
@app.route('/path/<int:variable>')

# HTTP methods
@app.route('/api/data', methods=['GET', 'POST', 'PUT', 'DELETE'])

# Subdomain routing
@app.route('/admin/', subdomain='admin')
```

### 2. Template Rendering

```python
from flask import render_template

@app.route('/profile/<username>')
def show_profile(username):
    user = get_user(username)
    return render_template('profile.html', user=user)
```

### 3. JSON Responses

```python
from flask import jsonify

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })
```

### 4. Redirects

```python
from flask import redirect, url_for

@app.route('/old-url')
def old_url():
    return redirect(url_for('new_url'))

@app.route('/new-url')
def new_url():
    return "New URL"
```

## Custom Decorators

### 1. Login Required Decorator

```python
from functools import wraps
from flask import request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard - User only content"
```

### 2. Admin Required Decorator

```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return "Access denied. Admin privileges required.", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/users')
@admin_required
def admin_users():
    return "Admin users page"
```

### 3. Rate Limiting Decorator

```python
from collections import defaultdict
import time

# Simple in-memory rate limiter
requests = defaultdict(list)

def rate_limit(max_requests=5, time_window=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = time.time()
            
            # Clean old requests
            requests[client_ip] = [
                req_time for req_time in requests[client_ip]
                if now - req_time < time_window
            ]
            
            # Check limit
            if len(requests[client_ip]) >= max_requests:
                return "Rate limit exceeded. Try again later.", 429
            
            # Record this request
            requests[client_ip].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/data')
@rate_limit(max_requests=3, time_window=60)
def get_data():
    return jsonify({'data': 'some information'})
```

### 4. Caching Decorator

```python
from functools import wraps

def cache(timeout=300):
    def decorator(f):
        cache = {}
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check cache
            if key in cache:
                cached_result, cached_time = cache[key]
                if time.time() - cached_time < timeout:
                    return cached_result
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        
        return decorated_function
    return decorator

@app.route('/weather/<city>')
@cache(timeout=600)  # Cache for 10 minutes
def get_weather(city):
    # Expensive API call
    return get_weather_from_api(city)
```

## Best Practices

### 1. Use `functools.wraps`

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Decorator logic
        return func(*args, **kwargs)
    return wrapper
```

**Why?** Preserves original function metadata (name, docstring, etc.)

### 2. Keep Decorators Simple

```python
# Good - Simple and focused
def require_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'JSON required'}), 400
        return func(*args, **kwargs)
    return wrapper

# Avoid - Too complex
def super_decorator_that_does_everything(func):
    # 100 lines of complex logic
    pass
```

### 3. Document Your Decorators

```python
def require_permissions(*permissions):
    """
    Decorator to require specific permissions.
    
    Args:
        *permissions: Variable list of required permission strings
        
    Example:
        @require_permissions('read', 'write')
        def edit_document():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_permissions = get_user_permissions()
            if not all(perm in user_permissions for perm in permissions):
                return "Insufficient permissions", 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 4. Handle Arguments Properly

```python
def robust_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Handle arguments
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            # Handle errors
            return jsonify({'error': str(e)}), 500
        return result
    return wrapper
```

## Summary

Decorators are a powerful feature that makes code more reusable, maintainable, and elegant. In Flask, they're essential for routing and implementing cross-cutting concerns like authentication and validation.

### Key Takeaways

- Decorators are functions that modify other functions
- They enable code reuse and separation of concerns
- Flask uses decorators extensively for routing
- Custom decorators allow you to add reusable functionality
- Always use `functools.wraps` to preserve function metadata
- Keep decorators simple and well-documented

### Next Steps

Now that you understand decorators, let's explore **Modules and Packages** - how Python and Flask organize code into manageable, reusable components.

---

*Previous: [Functions](./04-functions.md)*  
*Next: [Modules & Packages](./06-modules-packages.md)*
