#!/bin/bash
#
# Medication Health Reminder - Setup Script (Unix/macOS/Linux)
# This script creates a virtual environment and installs all dependencies.
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo -e "${BLUE}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}${BOLD}║                                                              ║${NC}"
echo -e "${BLUE}${BOLD}║   💊  Medication Health Reminder - Setup                     ║${NC}"
echo -e "${BLUE}${BOLD}║                                                              ║${NC}"
echo -e "${BLUE}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
echo -e "${BLUE}[1/4]${NC} Checking Python version..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}✗ Python 3.10+ required. You have Python $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"

# Create virtual environment
echo -e "${BLUE}[2/4]${NC} Creating virtual environment..."

if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists. Skipping creation.${NC}"
else
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Virtual environment created at ./venv${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}[3/4]${NC} Installing dependencies..."

pip install --upgrade pip --quiet
pip install -r requirements.txt

echo -e "${GREEN}✓ All dependencies installed successfully${NC}"

# Completion message
echo -e "${BLUE}[4/4]${NC} Setup complete!"
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║                    Setup Complete! 🎉                        ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}To run the application:${NC}"
echo ""
echo -e "  ${YELLOW}Option 1 - Using virtual environment directly:${NC}"
echo "    ./venv/bin/python app.py"
echo ""
echo -e "  ${YELLOW}Option 2 - Activate virtual environment first:${NC}"
echo "    source venv/bin/activate"
echo "    python app.py"
echo ""
echo -e "${BOLD}Quick Start:${NC}"
echo "  1. Run the app"
echo "  2. Click \"Create an Account\" to register"
echo "  3. Sign in and start managing your medications!"
echo ""
echo -e "${BLUE}Enjoy using Medication Health Reminder! 💊${NC}"
echo ""

