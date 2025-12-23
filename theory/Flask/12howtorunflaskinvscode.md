# 🛠️ VSCode Flask Setup Guide

A comprehensive guide for setting up Visual Studio Code for optimal Flask development with Python, including extensions, configuration, and debugging.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installing VSCode](#installing-vscode)
- [Essential Extensions](#essential-extensions)
- [Python Environment Setup](#python-environment-setup)
- [Flask Project Configuration](#flask-project-configuration)
- [Debugging Setup](#debugging-setup)
- [Code Formatting and Linting](#code-formatting-and-linting)
- [Integrated Terminal](#integrated-terminal)
- [Git Integration](#git-integration)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Productivity Tips](#productivity-tips)

## Prerequisites

Before setting up VSCode for Flask development, ensure you have:

- **Python 3.8+** installed and accessible
- **Basic familiarity** with command line operations
- **Git** installed (optional but recommended)

### Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Verify pip installation
pip --version
# or
python3 -m pip --version
```

## Installing VSCode

### Download and Install

1. **Visit** [Visual Studio Code](https://code.visualstudio.com/)
2. **Download** for your operating system
3. **Install** following platform-specific instructions

### Initial Launch Setup

1. **Launch** VSCode
2. **Complete** the welcome tour (optional)
3. **Sign in** to Microsoft account (optional but recommended for sync)

## Essential Extensions

The right extensions transform VSCode into a powerful Flask development environment.

### 🎯 Must-Have Extensions

#### 1. Python Extension Pack

```bash
# Install via Extensions tab or Command Palette
Ctrl+Shift+P → "Extensions: Install Extensions"
```

**Features:**
- IntelliSense and code completion
- Debugging support
- Code formatting
- Linting and error detection
- Interactive Python REPL

#### 2. Python Debugger

```bash
# Provides advanced debugging features
# Install alongside Python Extension Pack
```

**Features:**
- Variable inspection
- Call stack viewing
- Conditional breakpoints
- Logpoints
- Multi-thread debugging

#### 3. Python Docstring Generator

```bash
# Automatically generates docstrings
pip install pydocstring
```

**Usage:**
```python
def my_function():
    """Place cursor on function and press Enter"""
```

#### 4. Flask Snippets

```bash
# Provides Flask-specific code snippets
# Search for "Flask" in extensions
```

**Benefits:**
- Quick Flask route creation
- Template snippets
- Common patterns
- Blueprint snippets

### 🔧 Recommended Extensions

#### Code Formatting
- **Black Formatter**: Code formatting with Black
- **autopep8**: Alternative formatting tool
- **Prettier**: General code formatting

#### Linting
- **Pylance**: Advanced Python language server
- **Flake8**: Python linting tool
- **MyPy**: Static type checking

#### Git Integration
- **GitLens**: Enhanced Git capabilities
- **Git Graph**: Visual Git history
- **Gitmoji**: Git commit emojis

#### Web Development
- **Live Server**: Local development server
- **Auto Rename Tag**: HTML tag editing
- **Bracket Pair Colorizer**: Code readability

### Installing Extensions

#### Method 1: Extensions Tab
1. **Click** Extensions icon (4 squares) in sidebar
2. **Search** for extension name
3. **Click** Install
4. **Reload** VSCode when prompted

#### Method 2: Command Palette
1. **Press** `Ctrl+Shift+P`
2. **Type** "Extensions: Install Extensions"
3. **Search** and install desired extensions

#### Method 3: Command Line

```bash
# Install VSCode command line tool
# macOS
sudo ln -s /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code /usr/local/bin/code

# Windows (usually installed automatically)
# Restart terminal after installation

# Linux
sudo snap install --classic code
```

## Python Environment Setup

### 1. Create Virtual Environment

```bash
# Navigate to your project
cd /workspaces/Python_Framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Select Python Interpreter

1. **Open** your Flask project in VSCode
2. **Press** `Ctrl+Shift+P`
3. **Type** "Python: Select Interpreter"
4. **Choose** your virtual environment:
   - `venv/Scripts/python.exe` (Windows)
   - `venv/bin/python` (macOS/Linux)

### 3. Verify Environment

```python
# Create test file: test_env.py
import sys
import flask
print(f"Python: {sys.version}")
print(f"Flask: {flask.__version__}")
```

**Run the test:**
```bash
# In integrated terminal
python test_env.py
```

### 4. Configure Python Path

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true
}
```

## Flask Project Configuration

### 1. Create Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask: Run",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/code/flask_app/app.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "FLASK_APP": "code/flask_app/app.py",
                "FLASK_ENV": "development"
            },
            "args": ["--host=0.0.0.0", "--port=5000"],
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Flask: Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/code/flask_app/app.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "FLASK_APP": "code/flask_app/app.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": ["--host=0.0.0.0", "--port=5000"],
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### 2. Create Workspace Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88"],
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.associations": {
        "*.html": "html"
    },
    "emmet.includeLanguages": {
        "jinja2": "html"
    }
}
```

### 3. Flask-Specific Settings

```json
{
    "python.analysis.extraPaths": ["./code/flask_app"],
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/__pycache__/**": true,
        "**/.venv/**": true,
        "**/venv/**": true
    }
}
```

## Debugging Setup

### 1. Flask Debug Configuration

```json
{
    "name": "Flask Debug",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "code/flask_app/app.py",
        "FLASK_ENV": "development"
    },
    "args": ["run"],
    "console": "integratedTerminal",
    "justMyCode": false
}
```

### 2. Breakpoints

**Types of Breakpoints:**
- **Line Breakpoints**: Stop at specific lines
- **Conditional Breakpoints**: Stop when conditions are met
- **Logpoints**: Log without stopping
- **Exception Breakpoints**: Stop on exceptions

**Setting Breakpoints:**
1. **Click** in the gutter (left of line numbers)
2. **Right-click** breakpoint for options
3. **Use** F9 to toggle

### 3. Debugging Workflow

```python
# app.py - Example for debugging
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Set breakpoint here to inspect variables
    name = "Flask Developer"  # Debug this line
    return render_template("index.html", name=name)

if __name__ == "__main__":
    # Set breakpoint here to see app configuration
    app.run(debug=True)
```

**Debug Steps:**
1. **Set** breakpoints in your code
2. **Press** F5 or go to Run → Start Debugging
3. **Choose** "Flask Debug" configuration
4. **Inspect** variables in the Variables panel
5. **Step** through code with F10, F11, Shift+F11

## Code Formatting and Linting

### 1. Black Formatter Setup

```bash
# Install Black
pip install black

# Configure in settings.json
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"]
}
```

### 2. Flake8 Linting

```bash
# Install Flake8
pip install flake8

# Configure in settings.json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length=88",
        "--select=E,W,F"
    ]
}
```

### 3. Import Sorting

```bash
# Install isort
pip install isort

# Configure in settings.json
{
    "python.sortImports.args": [
        "--profile", "black",
        "--multi-line=3",
        "--trailing-comma"
    ]
}
```

### 4. Auto-formatting on Save

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Integrated Terminal

### 1. Terminal Setup

1. **Open** integrated terminal: `Ctrl+`` (backtick)
2. **Select** your shell:
   - **Windows**: PowerShell, Command Prompt, Git Bash
   - **macOS**: zsh, bash
   - **Linux**: bash, zsh, fish

### 2. Activate Virtual Environment

```bash
# In VSCode terminal
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Verify activation
which python
python --version
```

### 3. Terminal Configuration

```json
// settings.json
{
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "terminal.integrated.env.linux": {
        "PYTHONPATH": "${workspaceFolder}"
    }
}
```

### 4. Terminal Tasks

Create `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Flask App",
            "type": "shell",
            "command": "${command:python.interpreterPath}",
            "args": ["code/flask_app/app.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

## Git Integration

### 1. Initialize Git Repository

```bash
# In integrated terminal
git init
git add .
git commit -m "Initial commit: Flask project setup"
```

### 2. GitLens Extension

**Features:**
- Visual blame annotations
- Repository insights
- History visualization
- Comparison views

### 3. Git Configuration

```json
// settings.json
{
    "git.enableSmartCommit": true,
    "git.autofetch": true,
    "git.confirmSync": false,
    "scm.diffDecorations": "all"
}
```

### 4. Git Ignore Setup

Create `.gitignore`:

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

# VSCode
.vscode/settings.json
.vscode/launch.json

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db
```

## Advanced Configuration

### 1. Workspace-specific Settings

Create `.vscode/settings.json` in project root:

```json
{
    "python.analysis.autoSearchPaths": true,
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.extraPaths": ["./code/flask_app"],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests/"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/venv": true
    },
    "search.exclude": {
        "**/venv": true,
        "**/__pycache__": true
    }
}
```

### 2. Testing Setup

Create `tests/test_app.py`:

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask' in response.data
```

### 3. Snippets Configuration

Create `.vscode/python.json`:

```json
{
    "Flask Route": {
        "prefix": "route",
        "body": [
            "@app.route('${1:/}', methods=['${2|GET,POST|}'])",
            "def ${3:function_name}():",
            "    ${4:# Function implementation}",
            "    return ${5:render_template('${6:template.html}')}"
        ],
        "description": "Create Flask route"
    },
    "Flask Template": {
        "prefix": "template",
        "body": [
            "{% extends 'base.html' %}",
            "",
            "{% block content %}",
            "    <h1>${1:Page Title}</h1>",
            "    ${2:<!-- Template content -->}",
            "{% endblock %}"
        ],
        "description": "Create Flask template"
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Python Interpreter Not Found

**Symptoms:**
- "Python not found" errors
- No IntelliSense suggestions
- Linting not working

**Solutions:**
1. **Check** Python installation: `python --version`
2. **Select** correct interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
3. **Set** interpreter path in settings.json

#### 2. Virtual Environment Not Activated

**Symptoms:**
- Wrong Python version
- Packages not found
- Import errors

**Solutions:**
```bash
# Manually activate in terminal
source venv/bin/activate

# Set interpreter path
Ctrl+Shift+P → "Python: Select Interpreter" → Browse to venv/bin/python
```

#### 3. Flask Debug Not Working

**Symptoms:**
- Breakpoints not hit
- Debug console not opening
- Flask app doesn't restart on changes

**Solutions:**
1. **Check** launch.json configuration
2. **Verify** FLASK_APP environment variable
3. **Set** `FLASK_ENV=development`

#### 4. Extension Not Working

**Symptoms:**
- Features not available
- Extensions greyed out
- Commands not found

**Solutions:**
1. **Reload** VSCode window: Ctrl+Shift+P → "Developer: Reload Window"
2. **Check** extension is installed
3. **Disable/enable** extension
4. **Restart** VSCode completely

### Performance Issues

#### Slow Startup
```json
{
    "python.analysis.linting.enabled": false,
    "python.analysis.typeCheckingMode": "basic",
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true
    }
}
```

#### Memory Usage
- **Disable** unused extensions
- **Exclude** large folders from workspace
- **Clear** IntelliSense cache: Ctrl+Shift+P → "Python: Restart Language Server"

## Productivity Tips

### 1. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+`` | Toggle Terminal |
| `F5` | Start Debugging |
| `Ctrl+F5` | Run without Debugging |
| `Ctrl+S` | Save (triggers auto-format) |
| `Ctrl+/` | Toggle Comment |
| `Alt+Shift+F` | Format Document |
| `F9` | Toggle Breakpoint |
| `F10` | Step Over |
| `F11` | Step Into |
| `Shift+F11` | Step Out |

### 2. Code Navigation

- **Go to Definition**: F12
- **Go to Declaration**: Ctrl+F12
- **Find All References**: Shift+F12
- **Peek Definition**: Alt+F12
- **Go to Symbol**: Ctrl+Shift+O
- **Command Palette**: Ctrl+Shift+P

### 3. Multi-cursor Editing

- **Add cursor**: Alt+Click
- **Add cursor above/below**: Ctrl+Alt+Up/Down
- **Select next occurrence**: Ctrl+D
- **Select all occurrences**: Ctrl+Shift+L

### 4. Snippets Usage

1. **Type** snippet prefix (e.g., "route")
2. **Press** Tab to expand
3. **Navigate** between placeholders with Tab/Shift+Tab

### 5. Terminal Tips

- **Split terminal**: Ctrl+Shift+`
- **New terminal**: Ctrl+Shift+`
- **Clear terminal**: Ctrl+L
- **Navigate command history**: Up/Down arrows

### 6. Git Integration

- **Stage changes**: Ctrl+Shift+G → Stage All
- **Commit**: Ctrl+Shift+G → Commit
- **View diff**: Click on changed file
- **Branches**: Status bar (bottom left)

### 7. Live Share (Optional)

Install **Live Share** extension for:
- **Pair programming**
- **Code reviews**
- **Debugging sessions**
- **Voice chat integration**

## 🎯 Summary

VSCode provides an excellent environment for Flask development:

- **Extensions** enhance productivity and functionality
- **Debugger** enables efficient troubleshooting
- **Integrated terminal** keeps workflow smooth
- **Git integration** supports version control
- **Customization** allows personalized setup

With VSCode properly configured, you're ready for **Virtual Environment Creation** to manage your Flask project dependencies!

*Next: [Virtual Environment Creation](./13create_virtual_enviroment.md)*

*Previous: [Virtual Environments](./11virtualenviroment.md)*
