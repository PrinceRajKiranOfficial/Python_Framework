# 🔧 App Maintenance and Updates: Production Best Practices

A comprehensive guide to maintaining, updating, and managing Flask applications in production environments, covering version management, deployment strategies, and ongoing maintenance procedures.

## 📋 Table of Contents

- [Introduction to App Maintenance](#introduction-to-app-maintenance)
- [Version Management](#version-management)
- [Update Procedures](#update-procedures)
- [Database Migration Strategies](#database-migration-strategies)
- [Configuration Management](#configuration-management)
- [Rollback Procedures](#rollback-procedies)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Security Updates](#security-updates)
- [Performance Maintenance](#performance-maintenance)
- [Backup and Recovery](#backup-and-recovery)
- [Documentation Maintenance](#documentation-maintenance)
- [Dependency Management](#dependency-management)
- [Deployment Automation](#deployment-automation)
- [Maintenance Scheduling](#maintenance-scheduling)

## Introduction to App Maintenance

Application maintenance is crucial for keeping your Flask application running smoothly, securely, and efficiently in production. This guide covers essential practices for maintaining production Flask applications.

### Why App Maintenance Matters

- **Security**: Regular updates patch vulnerabilities
- **Performance**: Ongoing optimization prevents degradation
- **Reliability**: Proactive monitoring prevents outages
- **Feature Evolution**: Business needs require continuous updates
- **Technical Debt**: Regular refactoring prevents code decay

### Maintenance Categories

1. **Preventive Maintenance**: Regular updates, monitoring, backups
2. **Corrective Maintenance**: Bug fixes, security patches
3. **Adaptive Maintenance**: Updates for new environments, dependencies
4. **Perfective Maintenance**: Feature enhancements, performance improvements

## Version Management

### Semantic Versioning

```python
# version.py
"""
Flask Application Version Management

Version format: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes that require migration
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible
"""

__version__ = "2.1.0"
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Usage in application
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/version')
def get_version():
    """Return application version information"""
    return jsonify({
        'version': __version__,
        'build_date': '2024-01-15',
        'commit_hash': 'a1b2c3d'
    })

if __name__ == '__main__':
    print(f"Starting Flask App v{__version__}")
    app.run()
```

### Version Tracking

```python
# app/utils/version.py
import subprocess
import os
from datetime import datetime

def get_git_info():
    """Get Git version information"""
    try:
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            universal_newlines=True
        ).strip()
        
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            universal_newlines=True
        ).strip()
        
        return {
            'commit': commit_hash[:8],
            'branch': branch,
            'dirty': subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0
        }
    except:
        return {
            'commit': 'unknown',
            'branch': 'unknown',
            'dirty': False
        }

def get_build_info():
    """Get build information"""
    try:
        build_time = datetime.fromtimestamp(
            os.path.getmtime(__file__)
        ).isoformat()
    except:
        build_time = datetime.now().isoformat()
    
    return {
        'build_time': build_time,
        'python_version': subprocess.check_output(
            ['python', '--version'],
            universal_newlines=True
        ).strip()
    }

# Configuration
class VersionInfo:
    VERSION = "2.1.0"
    GIT_INFO = get_git_info()
    BUILD_INFO = get_build_info()
    
    @classmethod
    def get_full_info(cls):
        return {
            'version': cls.VERSION,
            'git': cls.GIT_INFO,
            'build': cls.BUILD_INFO,
            'environment': os.environ.get('FLASK_ENV', 'unknown')
        }
```

### Database Version Control

```python
# app/database/versions.py
from flask_migrate import Migrate
from datetime import datetime

def create_migration(app, db):
    """Create database migration for version tracking"""
    
    @app.before_first_request
    def create_version_table():
        """Create version tracking table"""
        db.create_all()
        
        # Create version tracking table if it doesn't exist
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS app_versions (
                id SERIAL PRIMARY KEY,
                version VARCHAR(50) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                rollback_script TEXT
            )
        """)
        db.session.commit()
    
    @app.route('/admin/version-info')
    def version_info():
        """Display version information"""
        result = db.session.execute(
            "SELECT version, applied_at, description FROM app_versions ORDER BY applied_at DESC"
        ).fetchall()
        
        return {
            'current_version': app.config.get('APP_VERSION', 'unknown'),
            'version_history': [
                {
                    'version': row[0],
                    'applied_at': row[1].isoformat() if row[1] else None,
                    'description': row[2]
                }
                for row in result
            ]
        }
    
    return app
```

## Update Procedures

### Update Checklist

```python
# update_checklist.py
"""
Pre-deployment Update Checklist for Flask Applications
"""

UPDATE_CHECKLIST = {
    "pre_update": [
        "Backup database",
        "Backup application files",
        "Test update in staging environment",
        "Review breaking changes",
        "Update dependencies",
        "Run test suite",
        "Check security vulnerabilities",
        "Review performance impact"
    ],
    "deployment": [
        "Set maintenance mode",
        "Update database schema",
        "Deploy application code",
        "Run database migrations",
        "Update configuration",
        "Restart services",
        "Verify health checks",
        "Test critical functions"
    ],
    "post_update": [
        "Monitor application logs",
        "Check performance metrics",
        "Verify all features work",
        "Update documentation",
        "Notify stakeholders",
        "Schedule post-update review",
        "Monitor for 24-48 hours"
    ]
}

def print_checklist(category):
    """Print update checklist for a category"""
    print(f"\n=== {category.upper()} CHECKLIST ===")
    for i, item in enumerate(UPDATE_CHECKLIST[category], 1):
        print(f"{i}. {item}")
    print("=" * 30)
```

### Automated Update Script

```bash
#!/bin/bash
# update_app.sh - Automated Flask application update script

set -e  # Exit on any error

APP_NAME="flask_app"
APP_DIR="/opt/flask_app"
BACKUP_DIR="/opt/backups"
VENV_DIR="$APP_DIR/venv"

echo "Starting Flask app update..."

# 1. Pre-update backup
echo "Creating backup..."
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_code.tar.gz" -C "$APP_DIR" .
pg_dump "$APP_NAME" > "$BACKUP_DIR/${BACKUP_NAME}_db.sql"

# 2. Maintenance mode
echo "Enabling maintenance mode..."
echo "MAINTENANCE_MODE=true" > "$APP_DIR/.env"

# 3. Update code
echo "Updating application code..."
cd "$APP_DIR"
git fetch origin
git checkout main
git pull origin main

# 4. Update dependencies
echo "Updating dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

# 5. Run database migrations
echo "Running database migrations..."
flask db upgrade

# 6. Run tests
echo "Running tests..."
pytest tests/ --tb=short

# 7. Restart application
echo "Restarting application..."
systemctl restart "$APP_NAME"

# 8. Health check
echo "Performing health check..."
sleep 10
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed - rolling back..."
    # Rollback logic here
    exit 1
fi

# 9. Disable maintenance mode
echo "Disabling maintenance mode..."
sed -i '/MAINTENANCE_MODE/d' "$APP_DIR/.env"

echo "✅ Update completed successfully!"
```

### Environment-Specific Updates

```python
# app/utils/update_manager.py
import os
import json
import subprocess
from datetime import datetime

class UpdateManager:
    def __init__(self, app):
        self.app = app
        self.environment = os.environ.get('FLASK_ENV', 'development')
        self.version = os.environ.get('APP_VERSION', '1.0.0')
    
    def is_maintenance_mode(self):
        """Check if application is in maintenance mode"""
        return self.app.config.get('MAINTENANCE_MODE', False)
    
    def enable_maintenance_mode(self, reason="Scheduled maintenance"):
        """Enable maintenance mode"""
        with self.app.app_context():
            self.app.config['MAINTENANCE_MODE'] = True
            self.app.config['MAINTENANCE_REASON'] = reason
            
            # Log maintenance mode activation
            print(f"Maintenance mode enabled: {reason}")
    
    def disable_maintenance_mode(self):
        """Disable maintenance mode"""
        with self.app.app_context():
            self.app.config['MAINTENANCE_MODE'] = False
            print("Maintenance mode disabled")
    
    def update_dependencies(self):
        """Update application dependencies"""
        if self.environment == 'production':
            # Production: careful dependency updates
            subprocess.run(['pip', 'install', '--upgrade', '-r', 'requirements.txt'])
        else:
            # Development: allow minor updates
            subprocess.run(['pip', 'install', '--upgrade', '-r', 'requirements-dev.txt'])
    
    def run_migrations(self):
        """Run database migrations"""
        try:
            subprocess.run(['flask', 'db', 'upgrade'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def health_check(self):
        """Perform application health check"""
        try:
            with self.app.test_client() as client:
                response = client.get('/health')
                return response.status_code == 200
        except:
            return False

# Maintenance mode route
@app.before_request
def check_maintenance_mode():
    """Check if application is in maintenance mode"""
    if app.config.get('MAINTENANCE_MODE', False):
        return render_template('maintenance.html', 
                             reason=app.config.get('MAINTANCE_REASON', 'Maintenance'),
                             estimated_duration=app.config.get('MAINTENANCE_DURATION', 'Unknown')), 503

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'version': app.config.get('APP_VERSION'),
        'timestamp': datetime.utcnow().isoformat()
    }
```

## Database Migration Strategies

### Safe Migration Pattern

```python
# app/migrations/safe_migrations.py
from flask_migrate import Migrate
import sqlalchemy as sa

def safe_migration_upgrade():
    """Execute migration with rollback capability"""
    
    def upgrade():
        # Step 1: Add new column as nullable
        op.add_column('users', sa.Column('new_field', sa.String(100), nullable=True))
        
        # Step 2: Populate data (if needed)
        # Use raw SQL for performance with large datasets
        op.execute("""
            UPDATE users 
            SET new_field = 'default_value' 
            WHERE new_field IS NULL
        """)
        
        # Step 3: Make column non-nullable
        op.alter_column('users', 'new_field', nullable=False)
        
        # Step 4: Add constraints
        op.create_unique_constraint('uq_users_new_field', 'users', ['new_field'])
    
    def downgrade():
        # Safe rollback
        op.drop_constraint('uq_users_new_field', 'users', type_='unique')
        op.drop_column('users', 'new_field')
    
    return upgrade, downgrade

# Migration file example: versions/001_add_user_field.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # This migration adds a new field to users table safely
    op.add_column('users', sa.Column('new_field', sa.String(100), nullable=True))
    
    # Populate existing records
    op.execute("UPDATE users SET new_field = 'default_value' WHERE new_field IS NULL")
    
    # Now make it non-nullable
    op.alter_column('users', 'new_field', nullable=False)
    
    # Add unique constraint
    op.create_unique_constraint('uq_users_new_field', 'users', ['new_field'])

def downgrade():
    op.drop_constraint('uq_users_new_field', 'users', type_='unique')
    op.drop_column('users', 'new_field')
```

### Data Migration Scripts

```python
# app/migrations/data_migration.py
from flask import Flask
from datetime import datetime
import sqlalchemy as sa

def create_data_migration_script():
    """Create a script for data migration"""
    
    migration_script = """
-- Data Migration: User Email Updates
-- Description: Update user emails to lowercase and validate format
-- Date: 2024-01-15

-- Step 1: Backup existing data
CREATE TABLE users_backup_{timestamp} AS SELECT * FROM users;

-- Step 2: Update email format
UPDATE users 
SET email = LOWER(TRIM(email))
WHERE email IS NOT NULL;

-- Step 3: Validate email format
-- Remove invalid emails (you might want to notify users instead)
DELETE FROM users 
WHERE email !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{{2,}}$';

-- Step 4: Create index for performance
CREATE INDEX CONCURRENTLY idx_users_email_lower ON users (LOWER(email));

-- Step 5: Update statistics
ANALYZE users;
    """.format(timestamp=datetime.now().strftime('%Y%m%d_%H%M%S'))
    
    return migration_script

def execute_migration_safely(app, migration_func):
    """Execute migration with safety measures"""
    
    with app.app_context():
        try:
            # 1. Start transaction
            db.session.begin()
            
            # 2. Execute migration
            migration_func()
            
            # 3. Commit transaction
            db.session.commit()
            
            # 4. Log success
            app.logger.info("Migration completed successfully")
            
        except Exception as e:
            # 4. Rollback on error
            db.session.rollback()
            app.logger.error(f"Migration failed: {str(e)}")
            raise
```

## Configuration Management

### Environment-Based Configuration

```python
# config/environments.py
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # App maintenance settings
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    MAINTENANCE_MODE = os.environ.get('MAINTENANCE_MODE', 'false').lower() == 'true'
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS', 30))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev_app.db'
    
    # Development maintenance settings
    AUTO_BACKUP = False
    DETAILED_LOGGING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Production maintenance settings
    AUTO_BACKUP = True
    BACKUP_SCHEDULE = '0 2 * * *'  # Daily at 2 AM
    HEALTH_CHECK_INTERVAL = 300  # 5 minutes
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Performance settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # Testing maintenance settings
    AUTO_BACKUP = False
    DETAILED_LOGGING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### Dynamic Configuration Updates

```python
# app/utils/config_manager.py
import json
import os
from threading import Lock
from flask import current_app

config_lock = Lock()

class ConfigManager:
    """Manage application configuration updates"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f, indent=2)
    
    def update_config(self, updates):
        """Update configuration with thread safety"""
        with config_lock:
            # Backup current config
            backup = self.config_data.copy()
            
            try:
                # Apply updates
                self.config_data.update(updates)
                
                # Validate configuration
                self.validate_config()
                
                # Save to file
                self.save_config()
                
                # Log configuration change
                current_app.logger.info(f"Configuration updated: {list(updates.keys())}")
                
                return True
                
            except Exception as e:
                # Restore backup on error
                self.config_data = backup
                current_app.logger.error(f"Configuration update failed: {str(e)}")
                return False
    
    def validate_config(self):
        """Validate configuration settings"""
        required_fields = ['maintenance_mode', 'log_level']
        
        for field in required_fields:
            if field not in self.config_data:
                raise ValueError(f"Missing required configuration field: {field}")
    
    def get_config(self, key, default=None):
        """Get configuration value"""
        return self.config_data.get(key, default)

# Usage in routes
@app.route('/admin/config', methods=['GET', 'POST'])
@admin_required
def manage_config():
    """Manage application configuration"""
    config_manager = ConfigManager()
    
    if request.method == 'POST':
        updates = request.json
        if config_manager.update_config(updates):
            return {'status': 'success', 'message': 'Configuration updated'}
        else:
            return {'status': 'error', 'message': 'Configuration update failed'}, 400
    
    return config_manager.config_data
```

## Rollback Procedures

### Automatic Rollback System

```python
# app/utils/rollback_manager.py
import os
import shutil
import subprocess
from datetime import datetime

class RollbackManager:
    """Manage application rollback procedures"""
    
    def __init__(self, app_dir, backup_dir):
        self.app_dir = app_dir
        self.backup_dir = backup_dir
        self.current_version = self.get_current_version()
    
    def create_backup(self, description=""):
        """Create backup before update"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}_{self.current_version}"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup application code
        shutil.copytree(
            self.app_dir,
            os.path.join(backup_path, 'app_code'),
            ignore=shutil.ignore_patterns('venv', '__pycache__', '*.pyc')
        )
        
        # Backup database
        if os.path.exists('instance/app.db'):
            shutil.copy2('instance/app.db', backup_path)
        
        # Create rollback script
        self.create_rollback_script(backup_path, description)
        
        return backup_path
    
    def create_rollback_script(self, backup_path, description):
        """Create rollback script for backup"""
        script_content = f"""#!/bin/bash
# Rollback script created: {datetime.now().isoformat()}
# Description: {description}
# Source version: {self.current_version}

echo "Starting rollback to previous version..."
echo "Backup path: {backup_path}"

# Stop application
sudo systemctl stop flask_app

# Restore application code
rm -rf {self.app_dir}/*
cp -r {backup_path}/app_code/* {self.app_dir}/

# Restore database
if [ -f "{backup_path}/app.db" ]; then
    cp {backup_path}/app.db instance/
fi

# Update version info
echo "{self.current_version}" > version.txt

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart application
sudo systemctl start flask_app

# Health check
sleep 10
if curl -f http://localhost:5000/health; then
    echo "Rollback completed successfully"
else
    echo "Rollback failed - manual intervention required"
    exit 1
fi
"""
        
        script_path = os.path.join(backup_path, 'rollback.sh')
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
    
    def execute_rollback(self, backup_path):
        """Execute rollback from backup"""
        try:
            # Execute rollback script
            result = subprocess.run(
                ['bash', os.path.join(backup_path, 'rollback.sh')],
                capture_output=True,
                text=True,
                cwd=self.app_dir
            )
            
            if result.returncode == 0:
                current_app.logger.info(f"Rollback completed successfully from {backup_path}")
                return True
            else:
                current_app.logger.error(f"Rollback failed: {result.stderr}")
                return False
                
        except Exception as e:
            current_app.logger.error(f"Rollback execution failed: {str(e)}")
            return False
    
    def get_current_version(self):
        """Get current application version"""
        try:
            with open('version.txt', 'r') as f:
                return f.read().strip()
        except:
            return 'unknown'

# Emergency rollback route
@app.route('/admin/emergency-rollback', methods=['POST'])
@admin_required
def emergency_rollback():
    """Emergency rollback endpoint"""
    rollback_manager = RollbackManager(
        app_dir=os.getcwd(),
        backup_dir='/opt/backups'
    )
    
    # Get latest backup
    backup_dirs = [d for d in os.listdir('/opt/backeps') 
                   if os.path.isdir(os.path.join('/opt/backups', d))]
    
    if not backup_dirs:
        return {'error': 'No backups found'}, 404
    
    latest_backup = sorted(backup_dirs)[-1]
    backup_path = os.path.join('/opt/backups', latest_backup)
    
    success = rollback_manager.execute_rollback(backup_path)
    
    if success:
        return {'status': 'success', 'message': 'Emergency rollback completed'}
    else:
        return {'status': 'error', 'message': 'Emergency rollback failed'}, 500
```

## Monitoring and Health Checks

### Comprehensive Health Monitoring

```python
# app/utils/health_monitor.py
import time
import psutil
import redis
import sqlalchemy as sa
from datetime import datetime
from flask import jsonify

class HealthMonitor:
    """Comprehensive health monitoring for Flask application"""
    
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.start_time = time.time()
    
    def get_system_health(self):
        """Check system-level health metrics"""
        health = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime_seconds': time.time() - self.start_time,
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'process_count': len(psutil.pids())
        }
        
        # Determine overall health status
        if (health['cpu_percent'] > 90 or 
            health['memory_percent'] > 90 or 
            health['disk_percent'] > 90):
            health['status'] = 'critical'
        elif (health['cpu_percent'] > 70 or 
              health['memory_percent'] > 70 or 
              health['disk_percent'] > 70):
            health['status'] = 'warning'
        
        return health
    
    def get_database_health(self):
        """Check database connectivity and performance"""
        try:
            # Test database connection
            result = self.db.session.execute(sa.text('SELECT 1'))
            result.fetchone()
            
            # Get database stats
            db_health = {
                'status': 'healthy',
                'connection_test': 'passed',
                'connection_pool_size': self.db.engine.pool.size(),
                'checked_out_connections': self.db.engine.pool.checkedout(),
                'overflow_connections': self.db.engine.pool.overflow()
            }
            
            # Check for long-running queries
            long_queries = self.db.session.execute("""
                SELECT pid, now() - pg_stat_activity.query_start AS duration, query
                FROM pg_stat_activity 
                WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
            """)
            
            db_health['long_running_queries'] = len(long_queries.fetchall())
            
            return db_health
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'connection_test': 'failed',
                'error': str(e)
            }
    
    def get_cache_health(self):
        """Check Redis/cache connectivity"""
        try:
            if hasattr(self.app, 'redis'):
                # Test Redis connection
                self.app.redis.ping()
                
                # Get Redis info
                info = self.app.redis.info()
                
                return {
                    'status': 'healthy',
                    'connection_test': 'passed',
                    'redis_version': info.get('redis_version'),
                    'used_memory': info.get('used_memory_human'),
                    'connected_clients': info.get('connected_clients'),
                    'uptime_in_seconds': info.get('uptime_in_seconds')
                }
            else:
                return {
                    'status': 'not_configured',
                    'connection_test': 'skipped',
                    'message': 'Redis not configured'
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'connection_test': 'failed',
                'error': str(e)
            }
    
    def get_application_health(self):
        """Check application-level health"""
        try:
            # Test critical routes
            with self.app.test_client() as client:
                routes_to_test = [
                    ('/health', 'GET'),
                    ('/version', 'GET'),
                ]
                
                route_results = {}
                for route, method in routes_to_test:
                    try:
                        response = client.open(route, method=method)
                        route_results[route] = {
                            'status': 'ok' if response.status_code < 400 else 'error',
                            'status_code': response.status_code
                        }
                    except Exception as e:
                        route_results[route] = {
                            'status': 'error',
                            'error': str(e)
                        }
                
                return {
                    'status': 'healthy' if all(r['status'] == 'ok' for r in route_results.values()) else 'unhealthy',
                    'routes': route_results,
                    'flask_version': self.app.version if hasattr(self.app, 'version') else 'unknown'
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def get_comprehensive_health(self):
        """Get comprehensive health report"""
        health_checks = {
            'system': self.get_system_health(),
            'database': self.get_database_health(),
            'cache': self.get_cache_health(),
            'application': self.get_application_health()
        }
        
        # Determine overall status
        statuses = [check.get('status', 'unknown') for check in health_checks.values()]
        
        if 'critical' in statuses:
            overall_status = 'critical'
        elif 'unhealthy' in statuses:
            overall_status = 'unhealthy'
        elif 'warning' in statuses:
            overall_status = 'warning'
        else:
            overall_status = 'healthy'
        
        return {
            'overall_status': overall_status,
            'checks': health_checks,
            'timestamp': datetime.utcnow().isoformat(),
            'version': self.app.config.get('APP_VERSION', 'unknown')
        }

# Health check routes
@app.route('/health')
def health_check():
    """Basic health check endpoint"""
    health_monitor = HealthMonitor(app, db)
    health_report = health_monitor.get_comprehensive_health()
    
    status_code = 200
    if health_report['overall_status'] in ['critical', 'unhealthy']:
        status_code = 503
    
    return jsonify(health_report), status_code

@app.route('/health/detailed')
def detailed_health_check():
    """Detailed health check for monitoring systems"""
    health_monitor = HealthMonitor(app, db)
    return jsonify(health_monitor.get_comprehensive_health())
```

## Security Updates

### Security Vulnerability Monitoring

```python
# app/utils/security_updater.py
import subprocess
import requests
from datetime import datetime, timedelta

class SecurityUpdater:
    """Monitor and apply security updates"""
    
    def __init__(self):
        self.last_update_check = None
        self.vulnerability_feed_url = "https://pyup.io/api/v1/safety/"
    
    def check_for_vulnerabilities(self):
        """Check for known vulnerabilities in dependencies"""
        try:
            # Run safety check
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'status': 'clean',
                    'vulnerabilities': [],
                    'last_check': datetime.utcnow().isoformat()
                }
            else:
                # Parse safety output
                vulnerabilities = []
                try:
                    vulnerabilities = json.loads(result.stdout)
                except:
                    vulnerabilities = [{'package': 'unknown', 'vulnerability': 'parse_error'}]
                
                return {
                    'status': 'vulnerabilities_found',
                    'vulnerabilities': vulnerabilities,
                    'last_check': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'check_failed',
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            }
    
    def update_dependencies(self, security_only=False):
        """Update dependencies with security focus"""
        try:
            if security_only:
                # Update only security patches
                result = subprocess.run(
                    ['pip', 'install', '--upgrade', '-r', 'requirements.txt'],
                    capture_output=True,
                    text=True
                )
            else:
                # Full update
                result = subprocess.run(
                    ['pip', 'install', '--upgrade', '-r', 'requirements.txt'],
                    capture_output=True,
                    text=True
                )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def generate_security_report(self):
        """Generate security status report"""
        vulnerabilities = self.check_for_vulnerabilities()
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'vulnerability_check': vulnerabilities,
            'recommendations': []
        }
        
        # Generate recommendations
        if vulnerabilities['status'] == 'vulnerabilities_found':
            report['recommendations'].append({
                'priority': 'high',
                'action': 'Update vulnerable packages immediately',
                'details': f"Found {len(vulnerabilities['vulnerabilities'])} vulnerabilities"
            })
        
        if vulnerabilities['status'] == 'check_failed':
            report['recommendations'].append({
                'priority': 'medium',
                'action': 'Fix vulnerability check system',
                'details': 'Unable to check for vulnerabilities'
            })
        
        return report

# Security monitoring routes
@app.route('/admin/security-report')
@admin_required
def security_report():
    """Get security status report"""
    security_updater = SecurityUpdater()
    report = security_updater.generate_security_report()
    return jsonify(report)

@app.route('/admin/update-security', methods=['POST'])
@admin_required
def update_security():
    """Update dependencies for security"""
    security_updater = SecurityUpdater()
    result = security_updater.update_dependencies(security_only=True)
    
    if result['success']:
        return {'status': 'success', 'message': 'Security updates applied'}
    else:
        return {'status': 'error', 'message': 'Security update failed'}, 500
```

## 🎯 Summary

App maintenance and updates encompass:

- **Version management** with semantic versioning and tracking
- **Safe update procedures** with checklists and automation
- **Database migration strategies** with rollback capabilities
- **Configuration management** for dynamic updates
- **Rollback procedures** for emergency recovery
- **Health monitoring** for proactive maintenance
- **Security updates** for vulnerability management
- **Performance maintenance** for ongoing optimization

These practices ensure your Flask application remains secure, reliable, and performant throughout its lifecycle.

*Previous: [Advanced Workflows](./15-advanced-workflows)*
