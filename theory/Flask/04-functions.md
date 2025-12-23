# Functions in Python & Flask

## Table of Contents
- [Introduction](#introduction)
- [What are Functions?](#what-are-functions)
- [Function Fundamentals](#function-fundamentals)
- [Functions in Flask](#functions-in-flask)
- [Best Practices](#best-practices)
- [Advanced Concepts](#advanced-concepts)
- [Common Patterns](#common-patterns)
- [Summary](#summary)

## Introduction

Functions are the building blocks of any Python application, and they're especially crucial in Flask development. This module covers function concepts, syntax, and their specific role in web applications.

## What are Functions?

A **function** is a reusable block of code that performs a specific task. Functions help organize code, eliminate repetition, and create modular, maintainable applications.

### Key Benefits

- **Code Reusability**: Write once, use many times
- **Better Organization**: Group related functionality together
- **Easier Maintenance**: Update logic in one place
- **Testing**: Functions can be tested independently

## Function Fundamentals

### Basic Function Syntax

```python
# Function definition
def greet_user(name):
    """Greet a user by name."""
    return f"Hello, {name}! Welcome!"

# Function call
message = greet_user("Alice")
print(message)  # Output: Hello, Alice! Welcome!
```

### Function Components

1. **Function Declaration**: `def` keyword + function name
2. **Parameters**: Input values the function accepts
3. **Docstring**: Documentation string (optional but recommended)
4. **Function Body**: Code that executes when function is called
5. **Return Statement**: Output value (if any)

### Function Types

#### 1. Simple Functions
```python
def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

result = add_numbers(5, 3)  # result = 8
```

#### 2. Functions with Default Parameters
```python
def greet_user(name, greeting="Hello"):
    """Greet user with optional custom greeting."""
    return f"{greeting}, {name}!"

print(greet_user("Bob"))           # Hello, Bob!
print(greet_user("Bob", "Hi"))     # Hi, Bob!
```

#### 3. Functions with Variable Arguments
```python
def calculate_average(*numbers):
    """Calculate average of any number of arguments."""
    if numbers:
        return sum(numbers) / len(numbers)
    return 0

print(calculate_average(1, 2, 3, 4, 5))  # 3.0
```

#### 4. Functions with Keyword Arguments
```python
def create_user_profile(name, **details):
    """Create user profile with flexible fields."""
    profile = {'name': name}
    profile.update(details)
    return profile

profile = create_user_profile(
    "Alice", 
    email="alice@email.com", 
    age=25, 
    city="New York"
)
```

## Functions in Flask

In Flask, functions serve as **route handlers** - they execute when users visit specific URLs. This is where the magic of web development happens.

### Basic Route Handler

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    """Handle requests to the home page."""
    return "Welcome to our Flask application!"
```

### Dynamic Routes

```python
@app.route('/user/<username>')
def show_user_profile(username):
    """Display user profile for specific username."""
    return f"Profile for user: {username}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Display specific blog post."""
    return f"Blog Post #{post_id}"
```

### Multiple HTTP Methods

```python
from flask import request, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login - GET shows form, POST processes it."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if validate_user(username, password):
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    
    # GET request - show login form
    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''
```

### Template Rendering

```python
from flask import render_template

@app.route('/dashboard')
def dashboard():
    """Display user dashboard with data."""
    user = get_current_user()
    recent_posts = get_user_posts(user.id)
    
    return render_template('dashboard.html', 
                         user=user, 
                         posts=recent_posts)
```

### JSON API Responses

```python
from flask import jsonify

@app.route('/api/user/<int:user_id>')
def get_user_api(user_id):
    """Return user data as JSON."""
    user = User.query.get_or_404(user_id)
    
    return 'id': user jsonify({
       .id,
        'name': user.name,
        'email': user.email,
        'posts_count': len(user.posts)
    })
```

## Best Practices

### 1. Use Descriptive Names
```python
# Bad
def f(x):
    return x * 2

# Good
def calculate_doubled_value(number):
    return number * 2
```

### 2. Write Docstrings
```python
def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg (float): Weight in kilograms
        height_m (float): Height in meters
    
    Returns:
        float: BMI value
    """
    return weight_kg / (height_m ** 2)
```

### 3. Keep Functions Small and Focused
```python
# Bad - Function does too many things
def process_user_registration():
    # Validate form data
    # Send email
    # Create database record
    # Log activity
    # Send welcome message
    pass

# Good - Single responsibility
def validate_registration_data(form_data):
    """Validate registration form data."""
    # Validation logic
    pass

def create_user_account(valid_data):
    """Create new user account."""
    # Account creation logic
    pass

def send_welcome_email(user_email):
    """Send welcome email to new user."""
    # Email sending logic
    pass
```

### 4. Use Type Hints (Python 3.6+)
```python
from typing import List, Dict

def process_user_data(data: Dict[str, str]) -> List[str]:
    """Process user data and return formatted fields."""
    processed = []
    for key, value in data.items():
        processed.append(f"{key.title()}: {value}")
    return processed
```

## Advanced Concepts

### Closures
```python
def create_multiplier(factor):
    """Create a function that multiplies by a specific factor."""
    def multiplier(number):
        return number * factor
    return multiplier

# Usage
double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(4))  # 12
```

### Lambda Functions
```python
# Traditional function
def square(x):
    return x ** 2

# Lambda equivalent
square_lambda = lambda x: x ** 2

# In Flask context
@app.route('/api/sort')
def sort_items():
    items = request.args.getlist('item')
    sorted_items = sorted(items, key=lambda x: len(x))
    return jsonify(sorted_items)
```

### Decorators (Preview)
```python
def login_required(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile')
@login_required
def user_profile():
    """Protected user profile page."""
    return render_template('profile.html')
```

## Common Patterns

### 1. Data Processing Functions
```python
def format_currency(amount):
    """Format amount as currency string."""
    return f"${amount:,.2f}"

def validate_email(email):
    """Simple email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### 2. Template Helper Functions
```python
from flask import current_app

def get_current_theme():
    """Get current application theme."""
    return current_app.config.get('THEME', 'default')

def format_datetime(dt):
    """Format datetime for display."""
    return dt.strftime('%B %d, %Y at %I:%M %p')
```

### 3. Utility Functions
```python
def generate_slug(title):
    """Generate URL-friendly slug from title."""
    import re
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def paginate_query(query, page=1, per_page=20):
    """Paginate database query."""
    return query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
```

## Summary

Functions are the fundamental building blocks that make Flask applications work. Understanding how to create, organize, and use functions effectively is crucial for building maintainable web applications.

### Key Takeaways

- Functions provide code reusability and organization
- In Flask, functions serve as route handlers for URLs
- Follow best practices: descriptive names, docstrings, single responsibility
- Use advanced concepts like closures and decorators for powerful patterns
- Keep functions small, focused, and well-documented

### Next Steps

Now that you understand functions, let's explore **Decorators** - a powerful Python feature that Flask uses extensively for routing and other functionality.

---

*Previous: [Flask Introduction](./03-flask-introduction.md)*  
*Next: [Decorators](./05-decorators.md)*
