# 🚀 Advanced Code Workflows for Production Flask Development

A comprehensive guide to advanced development workflows, production patterns, deployment strategies, and scaling considerations for building robust Flask applications.

## 📋 Table of Contents

- [Introduction to Advanced Workflows](#introduction-to-advanced-workflows)
- [Production Deployment Patterns](#production-deployment-patterns)
- [Performance Optimization Strategies](#performance-optimization-strategies)
- [Security Best Practices](#security-best-practices)
- [Scaling Considerations](#scaling-considerations)
- [Monitoring and Logging](#monitoring-and-logging)
- [CI/CD Integration](#cicd-integration)
- [Advanced Configuration Management](#advanced-configuration-management)
- [Database Optimization](#database-optimization)
- [Caching Strategies](#caching-strategies)
- [Error Handling and Recovery](#error-handling-and-recovery)
- [Production Maintenance](#production-maintenance)

## Introduction to Advanced Workflows

Advanced code workflows take your Flask application from development to production-ready, scalable systems. This guide covers the essential patterns and practices used by professional Flask developers.

### Key Principles

- **Production-First Mindset**: Design with production constraints in mind
- **Scalability**: Build systems that can handle growth
- **Reliability**: Ensure consistent uptime and data integrity
- **Security**: Implement defense-in-depth security measures
- **Observability**: Monitor and log everything important

### Workflow Evolution

```python
# Development Workflow
# Simple, single-file Flask app for learning
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)

# Production Workflow
# Modular, configurable, scalable Flask application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

## Production Deployment Patterns

### WSGI Server Deployment

Flask applications run on WSGI (Web Server Gateway Interface) servers in production.

#### Gunicorn Configuration

```bash
# Install Gunicorn
pip install gunicorn

# Basic deployment
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Advanced configuration
gunicorn \
    --workers 4 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --bind 0.0.0.0:8000 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    app:app
```

#### Gunicorn Configuration File

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "gthread"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "flask_app"

# SSL (if using HTTPS directly)
keyfile = "/path/to/key.pem"
certfile = "/path/to/cert.pem"
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/app
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Nginx Reverse Proxy

```nginx
# nginx.conf
upstream flask_app {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/x-javascript
        application/xml+rss
        application/javascript
        application/json;
    
    # Proxy to Flask app
    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Static files
    location /static {
        alias /app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        proxy_pass http://flask_app;
        access_log off;
    }
}
```

## Performance Optimization Strategies

### Database Query Optimization

```python
# app/models/user.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Add composite indexes for common queries
    __table_args__ = (
        Index('idx_username_created', 'username', 'created_at'),
    )
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')

# app/routes/users.py
from sqlalchemy import select

@bp.route('/users/<username>')
def get_user_profile(username):
    # Use select() for explicit queries
    stmt = select(User).where(User.username == username).limit(1)
    user = db.session.execute(stmt).scalar_one_or_none()
    
    if not user:
        abort(404)
    
    # Eager load relationships to avoid N+1 queries
    stmt = select(User).options(selectinload(User.posts)).where(User.username == username)
    user = db.session.execute(stmt).scalar_one()
    
    return render_template('profile.html', user=user)

@bp.route('/users')
def list_users():
    # Use pagination for large datasets
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    stmt = select(User).order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('users.html', users=stmt.items, pagination=stmt)
```

### Connection Pooling

```python
# config.py
class ProductionConfig(Config):
    # Database configuration with connection pooling
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,  # Recycle connections every hour
        'pool_pre_ping': True,  # Verify connections before use
        'max_overflow': 20,  # Allow 20 extra connections
        'pool_timeout': 30,  # Wait 30 seconds for connection
    }
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL')
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Configure SQLAlchemy engine
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                             **app.config['SQLALCHEMY_ENGINE_OPTIONS'])
        db.engine = engine
```

### Async Processing

```python
# app/tasks.py
from celery import Celery
from flask import Flask

def create_celery_app(app=None):
    celery = Celery(
        app.import_name if app else 'app',
        backend=app.config['CELERY_RESULT_BACKEND'] if app else None,
        broker=app.config['CELERY_BROKER_URL'] if app else None,
    )
    
    if app:
        celery.conf.update(app.config)
        
        class ContextTask(celery.Task):
            """Make celery tasks work with Flask app context"""
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
    
    return celery

# Usage in routes
@bp.route('/send-email', methods=['POST'])
def send_email():
    # Queue email sending task
    send_email_task.delay(user_id, email_data)
    return {'status': 'queued'}, 202

# Task definition
@celery.task
def send_email_task(user_id, email_data):
    """Send email asynchronously"""
    user = User.query.get(user_id)
    if user:
        # Send email logic here
        pass
```

## Security Best Practices

### Authentication and Authorization

```python
# app/auth/decorators.py
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# app/models/permissions.py
class Permission:
    VIEW_USERS = 'view_users'
    EDIT_USERS = 'edit_users'
    DELETE_USERS = 'delete_users'
    ADMIN_USERS = 'admin_users'

# app/models/role.py
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Text)  # JSON array of permissions
    users = db.relationship('User', backref='role', lazy='dynamic')

# Usage in routes
@bp.route('/admin/users')
@admin_required
@permission_required(Permission.VIEW_USERS)
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)
```

### Input Validation and Sanitization

```python
# app/utils/validators.py
from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError
import re

def validate_username(form, field):
    """Custom username validator"""
    if not re.match(r'^[a-zA-Z0-9_]+$', field.data):
        raise ValidationError('Username can only contain letters, numbers, and underscores')

def validate_password_strength(form, field):
    """Validate password strength"""
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number')

# app/utils/forms.py
class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired(),
        validate_username
    ])
    email = StringField('Email', [
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validate_password_strength
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
```

### CSRF Protection

```python
# config.py
class ProductionConfig(Config):
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    WTF_CSRF_SSL_STRICT = True  # Only accept HTTPS requests

# app/forms.py
class SecureForm(FlaskForm):
    # Forms automatically include CSRF token
    pass

# Custom CSRF validation
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    return app
```

### Rate Limiting

```python
# config.py
class ProductionConfig(Config):
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL')
    RATELIMIT_DEFAULT = "100 per hour"

# app/routes/api.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)

@bp.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def api_login():
    # Rate limited login endpoint
    pass

@bp.route('/api/data')
@limiter.limit("100 per hour")
def get_data():
    # Rate limited data endpoint
    pass
```

## Scaling Considerations

### Horizontal Scaling

```python
# app/factory.py
from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions that support scaling
    cache.init_app(app)
    db.init_app(app)
    
    # Initialize rate limiter with Redis backend
    limiter.init_app(app)
    
    return app

# config.py
class ProductionConfig(Config):
    # Shared cache backend (Redis)
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Shared session storage
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(os.environ.get('REDIS_URL'))
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_session:'
```

### Database Scaling

```python
# app/models/replica.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, primary_url, replica_urls):
        self.primary_engine = create_engine(primary_url)
        self.replica_engines = [create_engine(url) for url in replica_urls]
        self.replica_index = 0
    
    def get_replica_session(self):
        """Get session for read replica"""
        engine = self.replica_engines[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.replica_engines)
        return sessionmaker(bind=engine)()
    
    def get_primary_session(self):
        """Get session for primary database"""
        return sessionmaker(bind=self.primary_engine)()

# Usage in routes
db_manager = DatabaseManager(
    primary_url=os.environ.get('PRIMARY_DATABASE_URL'),
    replica_urls=[os.environ.get('REPLICA1_URL'), os.environ.get('REPLICA2_URL')]
)

@bp.route('/users/<int:user_id>')
def get_user(user_id):
    # Use replica for reading
    session = db_manager.get_replica_session()
    try:
        user = session.query(User).get(user_id)
        return {'user': user.to_dict()}
    finally:
        session.close()

@bp.route('/users', methods=['POST'])
def create_user():
    # Use primary for writing
    session = db_manager.get_primary_session()
    try:
        user = User(username=form.username.data, email=form.email.data)
        session.add(user)
        session.commit()
        return {'user': user.to_dict()}, 201
    finally:
        session.close()
```

## Monitoring and Logging

### Application Monitoring

```python
# app/utils/monitoring.py
import time
import logging
from functools import wraps
from flask import request, g
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
request_count = Counter('flask_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('flask_request_duration_seconds', 'Request duration')

def monitor_requests(f):
    """Decorator to monitor request metrics"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            response = f(*args, **kwargs)
            status = response.status_code if hasattr(response, 'status_code') else 200
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start_time
            
            # Record metrics
            request_count.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown',
                status=status
            ).inc()
            
            request_duration.observe(duration)
        
        return response
    return decorated_function

# app/routes/monitoring.py
@bp.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@bp.route('/health')
def health_check():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': os.environ.get('APP_VERSION', 'unknown')
    }
    
    # Check database connectivity
    try:
        db.session.execute('SELECT 1')
        health_status['database'] = 'healthy'
    except Exception as e:
        health_status['database'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
    
    # Check cache connectivity
    try:
        cache.get('health_check')
        health_status['cache'] = 'healthy'
    except Exception as e:
        health_status['cache'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return health_status, status_code
```

### Structured Logging

```python
# app/utils/logging.py
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.setup_handler()
    
    def setup_handler(self):
        """Setup structured JSON logging"""
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        logHandler.setFormatter(formatter)
        self.logger.addHandler(logHandler)
        self.logger.setLevel(logging.INFO)
    
    def log_request(self, request, response, duration):
        """Log request with structured data"""
        log_data = {
            'event': 'request',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'user_agent': request.headers.get('User-Agent'),
            'remote_addr': request.remote_addr,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.logger.info(json.dumps(log_data))
    
    def log_error(self, error, context=None):
        """Log error with context"""
        log_data = {
            'event': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if context:
            log_data['context'] = context
        
        self.logger.error(json.dumps(log_data))

# Usage in application
from app.utils.logging import StructuredLogger
logger = StructuredLogger(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.log_request(request, response, duration)
    
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    logger.log_error(e, {'endpoint': request.endpoint, 'method': request.method})
    return {'error': 'Internal server error'}, 500
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:6
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
    
    - name: Format check with black
      run: black --check app/
    
    - name: Test with pytest
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install security tools
      run: |
        pip install bandit safety
        pip install -r requirements.txt
    
    - name: Run Bandit security check
      run: bandit -r app/ -f json -o bandit-report.json || true
    
    - name: Run Safety check
      run: safety check --json --output safety-report.json || true
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
```

### Docker Build and Push

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ghcr.io/${{ github.repository }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## 🎯 Summary

Advanced Flask workflows encompass:

- **Production deployment** with WSGI servers and reverse proxies
- **Performance optimization** through database tuning and caching
- **Security hardening** with authentication, input validation, and rate limiting
- **Scaling strategies** for horizontal growth and database replication
- **Monitoring and observability** with metrics and structured logging
- **CI/CD automation** for reliable deployment pipelines

These advanced patterns transform your Flask application into a production-ready, scalable system that can handle real-world traffic and requirements.

With advanced workflows mastered, you're ready to learn about **App Maintenance and Updates** to keep your application running smoothly in production!

*Next: [App Maintenance and Updates](./16update_app.py_.md)*

*Previous: [Code Workflows](./14-code-workflows)*
