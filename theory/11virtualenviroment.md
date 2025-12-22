# 🌍 Virtual Environments

Virtual environments are isolated Python environments that allow you to manage project-specific dependencies separately from your system-wide Python installation.

## 📋 Table of Contents

- [What are Virtual Environments?](#what-are-virtual-environments)
- [Why Use Virtual Environments?](#why-use-virtual-environments)
- [Types of Virtual Environments](#types-of-virtual-environments)
- [Creating Virtual Environments](#creating-virtual-environments)
- [Activating Virtual Environments](#activating-virtual-environments)
- [Managing Dependencies](#managing-dependencies)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## What are Virtual Environments?

A **virtual environment** is an isolated Python environment that contains its own Python installation and packages. Think of it as a separate workspace for each project.

### Key Components
- **Independent Python**: Has its own `python` executable
- **Package Manager**: Uses `pip` specific to this environment
- **Site-packages**: Stores third-party libraries
- **Activation Script**: Sets up environment-specific paths

## Why Use Virtual Environments?

### 🚫 Avoid Version Conflicts
Different projects may require different versions of the same library:

```python
# Project A needs Flask 1.0
# Project B needs Flask 2.0
# Virtual environments solve this conflict
```

### 🧹 Clean Project Setup
- **No system pollution**: Don't clutter your main Python installation
- **Easy cleanup**: Delete the environment folder when done
- **Reproducible**: Share exact dependencies with others
- **Professional workflow**: Industry-standard practice

### 💼 Project Isolation
- **Version control friendly**: Only commit requirements.txt, not dependencies
- **Deployment consistency**: Match development and production environments
- **Team collaboration**: Everyone uses the same dependency versions

## Types of Virtual Environments

### 1. venv (Built-in)
- **Included** with Python 3.3+
- **Lightweight** and simple
- **Fast** to create and use
- **Recommended** for most projects

### 2. virtualenv (Third-party)
- **More features** than venv
- **Cross-platform** compatibility
- **Legacy projects** may still use it
- **Less commonly used** today

### 3. conda
- **Anaconda/Miniconda** package manager
- **Manages** both Python and non-Python dependencies
- **Scientific computing** friendly
- **Larger footprint** than venv

## Creating Virtual Environments

### Using venv (Recommended)

```bash
# Navigate to your project directory
cd /workspaces/Python_Framework

# Create virtual environment named 'venv'
python -m venv venv

# Alternative names (choose one)
python -m venv env           # 'env' is common
python -m venv .venv        # Hidden folder on Unix
python -m venv myenv        # Custom name
```

### Using virtualenv

```bash
# Install virtualenv first
pip install virtualenv

# Create virtual environment
virtualenv venv

# Specify Python version
virtualenv -p python3.9 venv
```

### Using conda

```bash
# Create conda environment
conda create -n myproject python=3.9

# Create with specific packages
conda create -n myproject python=3.9 flask=2.0
```

## Activating Virtual Environments

### On Windows

```cmd
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

### On macOS/Linux

```bash
# Bash, Zsh, or other shells
source venv/bin/activate

# Short version (if in PATH)
. venv/bin/activate
```

### Checking Activation

```bash
# Check if activated
which python  # Should show venv path
where python  # On Windows

# Check Python version
python --version

# Check installed packages
pip list
```

### Deactivating

```bash
# Simple deactivation
deactivate
```

## Managing Dependencies

### Installing Packages

```bash
# While environment is active
pip install flask
pip install flask==2.0.3
pip install "flask>=2.0,<3.0"

# Install from requirements.txt
pip install -r requirements.txt
```

### Creating requirements.txt

```bash
# Generate requirements file
pip freeze > requirements.txt

# Example requirements.txt
Flask==2.0.3
requests==2.26.0
Jinja2==3.0.1
```

### Installing from requirements.txt

```bash
# Fresh environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Best Practices

### 📁 Project Structure

```
my_project/
├── venv/                 # Virtual environment
├── requirements.txt     # Dependencies
├── app.py               # Your code
├── tests/               # Test files
└── README.md            # Documentation
```

### 🚫 What to Ignore in Version Control

Add to `.gitignore`:

```gitignore
# Virtual environments
venv/
env/
.venv/
myenv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Jupyter Notebook
.ipynb_checkpoints
```

### 🔄 Workflow Best Practices

1. **Create early**: Set up virtual environment at project start
2. **Activate always**: Remember to activate before working
3. **Document dependencies**: Keep requirements.txt updated
4. **Test in clean environment**: Verify with fresh venv
5. **Use consistent names**: `venv` is a good default

### 📦 Advanced Package Management

```bash
# Install specific version
pip install "package-name==1.2.3"

# Install range of versions
pip install "package-name>=1.0,<2.0"

# Install from git
pip install git+https://github.com/user/repo.git

# Install in development mode
pip install -e .
```

## Troubleshooting

### Common Issues

#### "python: command not found"
```bash
# Try python3 instead
python3 -m venv venv

# Check Python installation
which python3
python3 --version
```

#### Permission denied (macOS/Linux)
```bash
# May need to adjust permissions
chmod +x venv/bin/activate

# Or use sudo sparingly (not recommended)
sudo pip install package-name
```

#### Activation fails (Windows)
```powershell
# If PowerShell execution policy blocks scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use Command Prompt instead
cmd
venv\Scripts\activate.bat
```

#### Pip not found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Update pip
python -m pip install --upgrade pip

# Reinstall pip if needed
python -m ensurepip --upgrade
```

### Environment Issues

#### Wrong Python version
```bash
# Check Python version
python --version

# Create with specific version
python3.9 -m venv venv

# Verify correct version
which python
python --version
```

#### Corrupted environment
```bash
# Delete and recreate
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recreate environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🛠️ Integration with IDEs

### VSCode

1. **Open project folder**
2. **Select interpreter**: Ctrl+Shift+P → "Python: Select Interpreter"
3. **Choose**: `./venv/bin/python` or `venv\Scripts\python.exe`
4. **Configure terminal**: Set default shell to use activated environment

### PyCharm

1. **File → Settings** (Windows/Linux) or **PyCharm → Preferences** (macOS)
2. **Project: Your Project** → **Python Interpreter**
3. **Click gear icon** → **Add**
4. **Existing environment** → Browse to `venv/bin/python`
5. **Check "Make available to all projects"**

## 📈 Advanced Topics

### Multiple Environments

```bash
# Development environment
python -m venv venv-dev
source venv-dev/bin/activate
pip install -r requirements-dev.txt

# Production environment
python -m venv venv-prod
source venv-prod/bin/activate
pip install -r requirements-prod.txt
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

CMD ["python", "app.py"]
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Create virtual environment
      run: python -m venv venv
    - name: Activate and install
      run: |
        source venv/bin/activate
        pip install -r requirements.txt
        pip install pytest
    - name: Run tests
      run: |
        source venv/bin/activate
        pytest
```

## 🎯 Summary

Virtual environments are essential for professional Python development:

- **Isolate dependencies** per project
- **Avoid version conflicts** between projects
- **Enable reproducible** setups
- **Facilitate collaboration** and deployment
- **Maintain clean** development environments

With virtual environments mastered, you're ready to move on to **VSCode Setup** for optimal Flask development!

*Next: [VSCode Flask Setup](./12howtorunflaskinvscode.md)*

*Previous: [Templates](./08-templates.md)*
