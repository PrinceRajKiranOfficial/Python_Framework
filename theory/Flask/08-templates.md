# Templates in Flask (Jinja2)

## Table of Contents
- [Introduction](#introduction)
- [What are Templates?](#what-are-templates)
- [Jinja2 Template Engine](#jinja2-template-engine)
- [Template Basics](#template-basics)
- [Template Syntax](#template-syntax)
- [Template Inheritance](#template-inheritance)
- [Template Filters](#template-filters)
- [Template Functions](#template-functions)
- [Flask Template Integration](#flask-template-integration)
- [Advanced Template Patterns](#advanced-template-patterns)
- [Best Practices](#best-practices)
- [Summary](#summary)

## Introduction

Templates are the bridge between your Flask application's logic and the HTML that users see in their browsers. Flask uses the powerful Jinja2 template engine to generate dynamic HTML content, enabling you to create flexible, maintainable web pages.

## What are Templates?

**Templates** are files containing HTML with placeholders for dynamic content. They allow you to separate the presentation layer (HTML/CSS/JavaScript) from the application logic (Python).

### Why Use Templates?

- **Separation of Concerns**: Keep business logic separate from presentation
- **Code Reusability**: Create reusable components and layouts
- **Dynamic Content**: Insert data from your Flask application
- **Maintainability**: Easier to update and modify HTML structure
- **Security**: Built-in escaping prevents XSS attacks

### Template Analogy

Think of templates like **restaurant menus**:
- **Static Layout**: The menu structure (categories, sections)
- **Dynamic Content**: Daily specials, prices, availability
- **Template Engine**: The kitchen that combines menu template with daily data
- **Final Output**: The printed menu customers see

## Jinja2 Template Engine

Jinja2 is a fast, expressive, and extensible template engine for Python. Flask integrates seamlessly with Jinja2.

### Key Features

- **Template Inheritance**: Build upon base templates
- **Macros**: Create reusable components
- **Filters**: Transform data for display
- **Control Structures**: Loop and condition in templates
- **Automatic Escaping**: Security by default

### Jinja2 in Flask

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Data to pass to template
    user = {'name': 'Alice', 'email': 'alice@example.com'}
    posts = [
        {'title': 'First Post', 'content': 'Hello World!'},
        {'title': 'Second Post', 'content': 'More content here.'}
    ]
    
    # Render template with data
    return render_template('index.html', user=user, posts=posts)
```

## Template Basics

### Template File Structure

```
your_app/
├── templates/          # Templates directory
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── profile.html   # User profile
│   └── partials/      # Reusable components
│       ├── navbar.html
│       └── footer.html
└── static/            # Static files
    ├── css/
    ├── js/
    └── images/
```

### Basic Template

```html
<!-- templates/hello.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My App</title>
</head>
<body>
    <h1>Hello, {{ user.name }}!</h1>
    
    {% if user.is_new %}
        <p>Welcome to our platform!</p>
    {% else %}
        <p>Good to see you again!</p>
    {% endif %}
    
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post.title }}</h2>
                <p>{{ post.content }}</p>
                <small>Published on {{ post.created_at }}</small>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

## Template Syntax

### Variables

```html
<!-- Basic variable output -->
<p>User name: {{ user.name }}</p>
<p>Email: {{ user.email }}</p>

<!-- Complex expressions -->
<p>Full name: {{ user.first_name + " " + user.last_name }}</p>
<p>Age in 5 years: {{ user.age + 5 }}</p>

<!-- Dictionary/Object access -->
<p>User ID: {{ user['id'] }} or {{ user.id }}</p>
<p>Config value: {{ config.APP_NAME }}</p>

<!-- Fallback for undefined variables -->
<p>Bio: {{ user.bio or "No bio available" }}</p>
```

### Control Structures

#### If Statements

```html
<!-- Basic if -->
{% if user.is_authenticated %}
    <p>Welcome back, {{ user.name }}!</p>
{% endif %}

<!-- If-else -->
{% if user.is_admin %}
    <a href="/admin">Admin Panel</a>
{% else %}
    <a href="/profile">My Profile</a>
{% endif %}

<!-- If-elif-else -->
{% if user.status == 'active' %}
    <span class="status active">Active</span>
{% elif user.status == 'inactive' %}
    <span class="status inactive">Inactive</span>
{% else %}
    <span class="status unknown">Unknown</span>
{% endif %}
```

#### For Loops

```html
<!-- Basic loop -->
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}

<!-- Loop with index -->
{% for post in posts %}
    <article class="post">
        <h2>{{ loop.index }}. {{ post.title }}</h2>
        <p>{{ post.content }}</p>
    </article>
{% endfor %}

<!-- Loop with conditions -->
{% for user in users %}
    {% if user.is_active %}
        <div class="user-card">
            <h3>{{ user.name }}</h3>
            <p>Email: {{ user.email }}</p>
        </div>
    {% endif %}
{% endfor %}

<!-- Nested loops -->
{% for category in categories %}
    <h2>{{ category.name }}</h2>
    <ul>
        {% for product in category.products %}
            <li>{{ product.name }} - ${{ product.price }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

### Loop Variables

```html
{% for item in items %}
    <p>Item {{ loop.index }} of {{ loop.length }}</p>
    
    {% if loop.first %}
        <p>This is the first item</p>
    {% elif loop.last %}
        <p>This is the last item</p>
    {% endif %}
    
    {% if loop.index % 2 == 0 %}
        <p>This is an even-numbered item</p>
    {% endif %}
{% endfor %}
```

## Template Inheritance

Template inheritance allows you to create a base template with common elements and extend it in child templates.

### Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    <!-- Page-specific styles -->
    {% block styles %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    {% include 'partials/navbar.html' %}
    
    <!-- Main content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    {% include 'partials/footer.html' %}
    
    <!-- JavaScript -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    
    <!-- Page-specific scripts -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Child Template

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Home - My App{% endblock %}

{% block content %}
<div class="hero">
    <h1>Welcome to My App</h1>
    <p>Your ultimate solution for web development</p>
    <a href="/signup" class="btn btn-primary">Get Started</a>
</div>

<section class="features">
    <h2>Features</h2>
    <div class="feature-grid">
        {% for feature in features %}
        <div class="feature-card">
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
        </div>
        {% endfor %}
    </div>
</section>
{% endblock %}

{% block scripts %}
<script>
// Page-specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Home page loaded');
});
</script>
{% endblock %}
```

### Template Includes

```html
<!-- Include reusable components -->
{% include 'partials/navbar.html' %}
{% include 'partials/flash_messages.html' %}
{% include 'partials/user_card.html' with context %}

<!-- Include with specific context -->
{% include 'partials/weather_widget.html' with context %}
```

## Template Filters

Filters transform variables for display. They are applied using the pipe operator (`|`).

### Built-in Filters

```html
<!-- Text formatting -->
<p>{{ user.bio | default('No bio available') }}</p>
<p>{{ post.title | upper }}</p>
<p>{{ user.name | lower }}</p>
<p>{{ post.content | title }}</p>
<p>{{ user.email | capitalize }}</p>

<!-- Length and truncation -->
<p>{{ posts | length }} posts found</p>
<p>{{ post.content | truncate(100) }}</p>
<p>{{ post.content | truncate(100, end='...') }}</p>

<!-- Date formatting -->
<p>{{ post.created_at | date }}</p>
<p>{{ post.created_at | date('%B %d, %Y') }}</p>
<p>{{ post.created_at | time }}</p>

<!-- Number formatting -->
<p>Price: ${{ product.price | round(2) }}</p>
<p>Rating: {{ product.rating | int }}/5</p>

<!-- List operations -->
<p>Tags: {{ post.tags | join(', ') }}</p>
<p>First tag: {{ post.tags | first }}</p>
<p>Last tag: {{ post.tags | last }}</p>
<p>Unique tags: {{ post.tags | unique | list }}

<!-- Safe HTML (use carefully!) -->
<div class="content">
    {{ post.content | safe }}
</div>
```

### Custom Filters

```python
from flask import Flask

app = Flask(__name__)

@app.template_filter('datetime')
def format_datetime(value, format='%B %d, %Y at %I:%M %p'):
    """Format datetime for display."""
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('pluralize')
def pluralize(value, singular='', plural='s'):
    """Pluralize words based on value."""
    return singular if value == 1 else singular + plural

@app.template_filter('currency')
def format_currency(value):
    """Format number as currency."""
    return f"${value:,.2f}"

# Usage in templates
# {{ post.created_at | datetime }}
# {{ comment.count }} {{ comment.count | pluralize('comment') }}
# {{ product.price | currency }}
```

## Template Functions

### Built-in Functions

```html
<!-- URL generation -->
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('user_profile', username='alice') }}">Profile</a>

<!-- Static file URLs -->
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
<link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">

<!-- Length -->
<p>Total users: {{ users | length }}</p>

<!-- Sum -->
<p>Total price: {{ products | sum(attribute='price') }}</p>

<!-- Groupby -->
{% for category, items in products | groupby('category') %}
    <h2>{{ category }}</h2>
    <ul>
        {% for product in items %}
            <li>{{ product.name }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

### Custom Template Functions

```python
@app.template_function()
def current_year():
    """Get current year."""
    from datetime import datetime
    return datetime.now().year

@app.template_function()
def format_phone(phone):
    """Format phone number."""
    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    return phone

@app.template_function()
def random_choice(items):
    """Return random item from list."""
    import random
    return random.choice(items)

# Usage in templates
# <p>&copy; {{ current_year() }} My Company</p>
# <p>Call us: {{ phone_number | format_phone }}</p>
# <p>Random tip: {{ tips | random_choice }}
```

## Flask Template Integration

### Rendering Templates

```python
from flask import render_template, render_template_string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    
    return render_template('profile.html', 
                         user=user, 
                         posts=posts)

@app.route('/api/data')
def api_data():
    data = {'key': 'value'}
    return render_template_string('{"data": {{ data | tojson }} }')
```

### Template Context Processing

```python
from flask import g, current_app

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'current_year': datetime.now().year,
        'app_name': current_app.config.get('APP_NAME', 'My App'),
        'is_debug': current_app.config.get('DEBUG', False)
    }

@app.context_processor
def inject_user():
    """Inject current user into all templates."""
    return {'current_user': g.user}

# Global template functions
@app.template_global()
def get_config(key, default=None):
    return current_app.config.get(key, default)

# Usage in templates
# <p>&copy; {{ current_year }} {{ app_name }}</p>
# <p>Debug mode: {{ is_debug }}</p>
# <p>Setting: {{ get_config('MY_SETTING', 'default') }}</p>
```

### Flash Messages in Templates

```python
from flask import flash, get_flashed_messages

@app.route('/login', methods=['POST'])
def login():
    if check_credentials(username, password):
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials.', 'error')
        return redirect(url_for('login'))

# Template
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="flash-messages">
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

## Advanced Template Patterns

### Macros

Macros are reusable template components.

```html
<!-- templates/macros.html -->
{% macro render_user_card(user, show_email=false) %}
<div class="user-card">
    <img src="{{ user.avatar_url }}" alt="{{ user.name }}" class="avatar">
    <div class="user-info">
        <h3>{{ user.name }}</h3>
        {% if show_email %}
            <p>{{ user.email }}</p>
        {% endif %}
        <p class="join-date">Joined {{ user.created_at | date }}</p>
    </div>
</div>
{% endmacro %}

{% macro render_post_card(post, show_author=true) %}
<article class="post-card">
    <h2><a href="{{ url_for('post_detail', id=post.id) }}">{{ post.title }}</a></h2>
    {% if show_author %}
        <p class="author">By {{ post.author.name }}</p>
    {% endif %}
    <p class="content">{{ post.content | truncate(200) }}</p>
    <div class="meta">
        <span class="date">{{ post.created_at | date }}</span>
        <span class="comments">{{ post.comments | length }} comments</span>
    </div>
</article>
{% endmacro %}
```

Using macros:

```html
<!-- In any template -->
{% from "macros.html" import render_user_card, render_post_card %}

<div class="users-section">
    <h2>Featured Users</h2>
    {% for user in featured_users %}
        {{ render_user_card(user, show_email=true) }}
    {% endfor %}
</div>

<div class="posts-section">
    {% for post in recent_posts %}
        {{ render_post_card(post) }}
    {% endfor %}
</div>
```

### Template Loaders and Includes

```python
# Custom template loader
from jinja2 import DictLoader

app = Flask(__name__)

# Load templates from database
@app.before_first_request
def load_templates():
    templates = {}
    for template in Template.query.all():
        templates[template.name] = template.content
    
    app.jinja_loader = DictLoader(templates)

# Include templates from database
@app.route('/dynamic')
def dynamic():
    template = Template.query.filter_by(name='dynamic').first()
    return render_template_string(template.content)
```

### Template Testing

```python
# Template tests
@app.template_test('odd')
def test_odd(value):
    return value % 2 == 1

@app.template_test('even')
def test_even(value):
    return value % 2 == 0

# Usage
{% if number is odd %}
    <p>{{ number }} is odd</p>
{% endif %}

{% if number is even %}
    <p>{{ number }} is even</p>
{% endif %}
```

## Best Practices

### 1. Keep Logic Simple

```html
<!-- Good: Simple conditional -->
{% if user.is_active %}
    <span class="status active">Active</span>
{% endif %}

<!-- Bad: Complex logic in template -->
{% if user.status == 'active' and user.last_login and 
      (now() - user.last_login).days < 30 and 
      user.posts.count() > 0 %}
    <span class="vip-user">VIP User</span>
{% endif %}
```

**Better approach:**

```python
# In Python code
@app.context_processor
def inject_user_status():
    user = g.get('user')
    if not user:
        return {}
    
    return {
        'user_is_vip': (
            user.is_active and 
            user.last_login and 
            (datetime.now() - user.last_login).days < 30 and
            user.posts.count() > 0
        )
    }

# In template
{% if user_is_vip %}
    <span class="vip-user">VIP User</span>
{% endif %}
```

### 2. Use Template Inheritance

```html
<!-- Good: Use base template -->
{% extends "base.html" %}
{% block content %}
    <!-- Page-specific content -->
{% endblock %}

<!-- Bad: Duplicate HTML structure -->
<!DOCTYPE html>
<html>...same structure repeated...</html>
```

### 3. Organize Templates Logically

```
templates/
├── base/
│   ├── base.html
│   ├── admin.html
│   └── auth.html
├── pages/
│   ├── home.html
│   ├── about.html
│   └── contact.html
├── users/
│   ├── profile.html
│   ├── settings.html
│   └── list.html
└── partials/
    ├── navbar.html
    ├── footer.html
    └── sidebar.html
```

### 4. Secure Template Practices

```html
<!-- Good: Automatic escaping -->
<p>{{ user_input }}</p>

<!-- Use |safe only when necessary and verified -->
<div class="content">
    {{ trusted_content | safe }}
</div>

<!-- Explicit escaping if needed -->
<div class="raw-content">
    {{ user_input | e }}
</div>
```

### 5. Performance Optimization

```python
# Cache compiled templates
app = Flask(__name__)
app.jinja_env.cache = {}

# Use template fragments for frequently updated content
@app.route('/dashboard')
def dashboard():
    # Render static parts once
    base_content = render_template('dashboard_base.html')
    
    # Update dynamic content via AJAX
    return base_content

# Template caching in production
app.jinja_env.cache_size = 400
```

## Summary

Templates are a powerful tool for creating dynamic, maintainable web applications. Jinja2 provides a rich set of features for template inheritance, reusable components, and flexible data presentation.

### Key Takeaways

- **Separation of Concerns**: Keep logic separate from presentation
- **Template Inheritance**: Create reusable base layouts
- **Dynamic Content**: Pass data from Flask to templates
- **Security**: Built-in escaping prevents XSS attacks
- **Reusability**: Use macros and includes for components
- **Best Practices**: Keep templates simple, organize logically

### Completion Checklist

With this module, you've completed the comprehensive theory guide covering:

✅ **Python Fundamentals** - Core concepts and features  
✅ **Framework Concepts** - Understanding web frameworks  
✅ **Flask Introduction** - Flask philosophy and basics  
✅ **Functions** - Building blocks of Flask applications  
✅ **Decorators** - Python's powerful feature for Flask routing  
✅ **Modules & Packages** - Code organization  
✅ **Context Management** - Request and application context  
✅ **Templates** - Dynamic HTML generation with Jinja2  

### Next Steps

You now have a solid foundation in Python and Flask theory! Consider exploring:

- **Database Integration** - SQLAlchemy and database design
- **API Development** - Building RESTful APIs
- **Testing** - Unit and integration testing
- **Deployment** - Production deployment strategies
- **Advanced Patterns** - Application architecture and scaling

---

*Previous: [Context Management](./07-context-management.md)*  
*Course Complete!* 🎉
