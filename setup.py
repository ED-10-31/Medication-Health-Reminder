#!/usr/bin/env python3
"""
Medication Health Reminder - Setup Script
Cross-platform setup script to create virtual environment and install dependencies.
"""

import subprocess
import sys
import os
import platform

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Print setup header"""
    print(f"""
{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   💊  Medication Health Reminder - Setup                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")

def print_step(step, message):
    """Print a step message"""
    print(f"{Colors.BLUE}[{step}]{Colors.END} {message}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    print_step("1/4", "Checking Python version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print_error(f"Python 3.10+ required. You have Python {version_str}")
        print("Please install Python 3.8 or higher from https://python.org")
        return False
    
    print_success(f"Python {version_str} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    print_step("2/4", "Creating virtual environment...")
    
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
    
    if os.path.exists(venv_path):
        print_warning("Virtual environment already exists. Skipping creation.")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created at ./venv")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def get_pip_path():
    """Get the path to pip in the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")

def get_python_path():
    """Get the path to python in the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def install_dependencies():
    """Install required dependencies"""
    print_step("3/4", "Installing dependencies...")
    
    pip_path = get_pip_path()
    
    if not os.path.exists(pip_path):
        print_error("pip not found in virtual environment")
        return False
    
    try:
        # Upgrade pip first
        subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], 
                      check=True)
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def print_completion():
    """Print completion message with instructions"""
    python_cmd = get_python_path()
    
    if platform.system() == "Windows":
        activate_cmd = ".\\venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print_step("4/4", "Setup complete!")
    print()
    print(f"""{Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                    Setup Complete! 🎉                        ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}To run the application:{Colors.END}

  {Colors.YELLOW}Option 1 - Using virtual environment directly:{Colors.END}
    {python_cmd} app.py

  {Colors.YELLOW}Option 2 - Activate virtual environment first:{Colors.END}
    {activate_cmd}
    python app.py

{Colors.BOLD}Quick Start:{Colors.END}
  1. Run the app
  2. Click "Create an Account" to register
  3. Sign in and start managing your medications!

{Colors.BLUE}Enjoy using Medication Health Reminder! 💊{Colors.END}
""")

def main():
    """Main setup function"""
    print_header()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 4: Print completion message
    print_completion()

if __name__ == "__main__":
    main()

