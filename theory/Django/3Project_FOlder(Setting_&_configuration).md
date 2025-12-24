# Django Settings & Configuration

[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![Configuration](https://img.shields.io/badge/Configuration-Settings-orange.svg)](#settings-overview)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Level](https://img.shields.io/badge/Level-Intermediate-yellow.svg)](#learning-objectives)

## Overview

The **project folder contains the core configuration** of your Django project and is the central nervous system that controls how your entire application behaves. This folder houses the critical configuration files that define database connections, installed applications, security settings, and deployment parameters.

## Settings Overview

Django settings are managed through the `settings.py` file, which is the **single source of truth** for your application's configuration. This file controls virtually every aspect of how Django behaves, from database connections to template rendering.

## Core Configuration Files

### ⚙️ **settings.py** - Main Configuration File

**Purpose**: Central configuration for the entire Django project  
**Responsibilities**:
- Database configuration and connection settings
- Installed applications and middleware
- Security settings and authentication
- Template engine configuration
- Static and media file handling
- Cache and session management

### 🌐 **urls.py** - URL Routing Configuration

**Purpose**: Main URL dispatcher and routing configuration  
**Responsibilities**:
- Route incoming URLs to appropriate views
- Include app-specific URL patterns
- Define URL namespaces for reverse resolution
- Configure admin interface URLs

### 🔌 **wsgi.py / asgi.py** - Server Gateway Interfaces

**Purpose**: Deploy Django on web servers  
**Responsibilities**:
- WSGI: Traditional synchronous web server interface
- ASGI: Modern asynchronous server interface
- Bridge between Django and web servers
- Production deployment configuration

## Detailed settings.py Configuration

### Database Configuration

#### SQLite (Default Development Database)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Production Recommended)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}
```

#### MySQL Configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### Installed Applications (INSTALLED_APPS)

#### Core Django Applications

```python
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin interface
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session management
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file handling
]
```

#### Third-Party Applications

```python
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',               # Django REST Framework
    'crispy_forms',                 # Enhanced form rendering
    'widget_tweaks',                # Template widgets
    'import_export',                # Data import/export
    
    # Your custom apps
    'students',                     # Student management
    'courses',                      # Course management
    'grades',                       # Grade management
]
```

### Middleware Configuration

#### Basic Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',   # Session management
    'django.middleware.common.CommonMiddleware',              # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',   # Messaging
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
]
```

#### Extended Middleware for Production

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',             # Static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Caching middleware
    'django.middleware.cache.UpdateCacheMiddleware',          # Cache update
    'django.middleware.common.CommonMiddleware',              # Cached responses
    'django.middleware.cache.FetchFromCacheMiddleware',       # Cache fetch
]
```

### Template Configuration

#### Default Template Settings

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                                           # Project templates
        'APP_DIRS': True,                                     # App templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### Enhanced Template Configuration

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',                          # Project-wide templates
            BASE_DIR / 'templates' / 'common',               # Common templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',    # Internationalization
                'django.template.context_processors.static',  # Static files
                'django.template.context_processors.tz',      # Timezone
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',  # File system loader
                'django.template.loaders.app_directories.Loader',  # App directories
            ],
        },
    },
]
```

### Static Files Configuration

#### Development Static Files

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'                       # Production collection
STATICFILES_DIRS = [BASE_DIR / 'static']                     # Development directories
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

#### Production Static Files (with WhiteNoise)

```python
# Install WhiteNoise: pip install whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files Configuration

```python
# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Security Settings

#### Basic Security Configuration

```python
# Security
SECRET_KEY = 'your-secret-key-here'                          # Change in production
DEBUG = True                                                 # False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']                   # Production domains
```

#### Enhanced Security for Production

```python
# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')    # Environment variable
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'  # Environment variable
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')  # Environment variable

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Authentication
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

### Cache Configuration

#### Development Cache (Local Memory)

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

#### Production Cache (Redis)

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Internationalization

```python
# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Localized settings
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

### Logging Configuration

```python
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Real-World Example: Student Information Project Settings

Let's examine the actual configuration from our [Student Information Project](../../code/practice_question/django/djangominiproject/djangominiproject/settings.py):

```python
# Key configurations in our project:

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "hello",  # ← Our custom app registered here
]

ROOT_URLCONF = "djangominiproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # ← Enables app-specific templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

**Key Points in Our Configuration**:
1. **App Registration**: `hello` app is properly registered in `INSTALLED_APPS`
2. **Template Discovery**: `APP_DIRS: True` allows Django to find templates in `hello/templates/`
3. **Database**: Using SQLite for development (can be changed for production)
4. **Root URL**: Points to main URL configuration file

## Environment-Specific Configuration

### Using Environment Variables

```python
# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment-based configuration
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],
        }
    }
else:
    DEBUG = True
    SECRET_KEY = 'development-secret-key'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### Configuration Files Structure

```
myproject/
├── settings/
│   ├── __init__.py
│   ├── base.py              # Common settings
│   ├── development.py       # Development overrides
│   ├── production.py        # Production overrides
│   └── testing.py           # Testing overrides
└── manage.py
```

### Using Multiple Settings Files

```python
# base.py - Common settings
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... common apps
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

```python
# development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',  # Development-only app
]
```

## Best Practices for Django Settings

### 🔒 **Security Best Practices**

1. **Never commit secret keys to version control**
   ```python
   # Good
   SECRET_KEY = os.environ.get('SECRET_KEY')
   
   # Bad
   SECRET_KEY = 'hardcoded-secret-key'
   ```

2. **Use environment variables for sensitive data**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.environ['DB_NAME'],
           'USER': os.environ['DB_USER'],
           'PASSWORD': os.environ['DB_PASSWORD'],
       }
   }
   ```

3. **Disable debug mode in production**
   ```python
   DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
   ```

### 🏗️ **Configuration Organization**

1. **Separate settings by environment**
   ```python
   # Development settings
   if DEBUG:
       INSTALLED_APPS += ['debug_toolbar']
       MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
   ```

2. **Use meaningful variable names**
   ```python
   # Good
   STUDENT_APP_INSTALLED = True
   MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
   
   # Avoid
   FLAG1 = True
   SIZE_LIMIT = 10485760
   ```

3. **Document complex configurations**
   ```python
   # Cache configuration with explanation
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://localhost:6379/1',
           'TIMEOUT': 300,      # 5 minutes cache timeout
           'KEY_PREFIX': 'myapp',  # Cache key prefix to avoid collisions
       }
   }
   ```

### 🚀 **Performance Optimization**

1. **Configure caching appropriately**
   ```python
   # Production cache configuration
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
               'CONNECTION_POOL_KWARGS': {'max_connections': 50},
           }
       }
   }
   ```

2. **Optimize static file serving**
   ```python
   # Use WhiteNoise for static file compression
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

3. **Database connection pooling**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'OPTIONS': {
               'MAX_CONNS': 20,
           },
       }
   }
   ```

## Common Configuration Issues

### 🐛 **Debugging Configuration Problems**

1. **Template not found**
   - Check `APP_DIRS: True` in template configuration
   - Verify template is in correct app directory
   - Ensure app is in `INSTALLED_APPS`

2. **Static files not loading**
   - Verify `STATIC_URL` is configured
   - Check `STATICFILES_DIRS` for custom locations
   - Run `python manage.py collectstatic`

3. **Database connection errors**
   - Verify database credentials
   - Check database engine configuration
   - Ensure database server is running

### 🔧 **Configuration Testing**

```python
# settings_test.py - Test-specific settings
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
```

## Learning Objectives

By the end of this module, you should understand:

- [ ] Django's settings.py structure and organization
- [ ] How to configure databases for different environments
- [ ] Setting up installed apps and middleware
- [ ] Template and static file configuration
- [ ] Security settings for production deployment
- [ ] Environment-specific configuration patterns
- [ ] Cache and session configuration
- [ ] Best practices for settings organization

## Next Steps

1. **Application Logic**: Learn about Django apps in [Application Logic](./4AppFolder(Application_Logic).md)
2. **Templates**: Understand template system in [Templates](./5Templates.md)
3. **URL Configuration**: Master URL routing in [URL Configuration](./16Step4:_Register_App.md)
4. **Security**: Explore production security best practices and deployment considerations

## Quick Reference

### Essential Settings Categories

| Category | Key Settings | Purpose |
|----------|-------------|---------|
| **Database** | `DATABASES` | Database connection and configuration |
| **Apps** | `INSTALLED_APPS` | Django and third-party applications |
| **Middleware** | `MIDDLEWARE` | Request/response processing pipeline |
| **Templates** | `TEMPLATES` | Template engine configuration |
| **Static Files** | `STATIC_*` | Static file handling and serving |
| **Security** | `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` | Security and authentication settings |
| **Cache** | `CACHES` | Cache backend configuration |
| **Internationalization** | `LANGUAGE_CODE`, `TIME_ZONE` | Multi-language and timezone settings |

### Configuration Commands

```bash
# Check settings configuration
python manage.py check

# Validate database configuration
python manage.py check --database

# Show all settings
python manage.py diffsettings

# Test email configuration
python manage.py sendtestemail admin@example.com
```

---

**💡 Key Takeaway**: Django's settings system provides comprehensive configuration options that can be tailored for different environments while maintaining security and performance best practices.

---

*Next: [Application Logic](./4AppFolder(Application_Logic).md)*
