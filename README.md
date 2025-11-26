# 💊 Medication Health Reminder

A modern, user-friendly desktop application to help you track your medications, monitor stock levels, and never miss a dose.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **User Authentication** - Secure login and registration system
- **Medication Management** - Add, view, and track all your medications
- **Smart Refill Alerts** - Automatic warnings when stock is running low (< 3 days)
- **Daily Progress Tracking** - See how many doses you've taken today vs. your daily requirement
- **Medication History** - Complete log of all medication intakes with timestamps
- **PDF Export** - Generate professional PDF reports of your medication history
- **Modern Dark UI** - Beautiful, eye-friendly dark theme interface
- **Multilingual Support** - Switch between English and Chinese (中文) with one click

## 📸 Screenshots

The app features:
- Split-screen login/register pages
- Dashboard with sidebar navigation
- Medication cards with progress indicators
- History view with export functionality

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Quick Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Medication-Health-Reminder.git
   cd Medication-Health-Reminder
   ```

2. **Run the setup script**

   **macOS/Linux:**
   ```bash
   ./setup.sh
   ```
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   **Cross-platform (Python):**
   ```bash
   python setup.py
   ```

3. **Run the application**
   ```bash
   # Using virtual environment directly
   ./venv/bin/python app.py      # macOS/Linux
   .\venv\Scripts\python app.py  # Windows
   
   # Or activate venv first
   source venv/bin/activate      # macOS/Linux
   .\venv\Scripts\activate       # Windows
   python app.py
   ```

### Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Medication-Health-Reminder.git
   cd Medication-Health-Reminder
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📦 Dependencies

- `customtkinter` - Modern UI framework for Python
- `fpdf` - PDF generation library

## 🎯 How to Use

### Getting Started
1. Launch the app with `python app.py`
2. Click **"Create an Account"** to register
3. Enter a username and password (minimum 3 characters each)
4. Sign in with your credentials

### Managing Medications
1. Click **"➕ Add Medication"** in the sidebar
2. Enter the medication name, total pills in stock, and daily dosage
3. Click **"Add Medication"** to save

### Taking Medications
1. Go to **"📋 My Medications"**
2. View your daily progress for each medication
3. Click **"💊 Take Dose"** to record taking a pill
4. The progress bar updates automatically

### Viewing History & Reports
1. Click **"📜 History"** in the sidebar
2. See all your medication intake records
3. Click **"📄 Export PDF"** to generate a report


## 🔧 Technical Details

- **Database**: Local JSON file (`med_data.json`) for simple, portable data storage
- **GUI Framework**: CustomTkinter for modern, cross-platform UI
- **Architecture**: Modular design with separate backend logic

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

Created as part of INF452 Final Project

---

**Stay healthy, never miss a dose! 💊**
