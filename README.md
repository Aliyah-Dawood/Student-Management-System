STUDENT MANAGEMENT SYSTEM
=========================

A web-based student management application built with Flask. It allows administrators to manage student records, course enrollments, and predict students' career aspirations using a machine learning classifier.

Live Demo:
https://student-management-system-lyc7.onrender.com


REPOSITORY STRUCTURE
---------------------
Student-Management-System/
│
├── src/                  → Source code and assets
│   ├── static/           → CSS, JavaScript, etc.
│   ├── templates/        → HTML templates
│   ├── models/           → Trained ML classifier and scaler
│   ├── app.py            → Main Flask application
│   ├── config.py         → App configuration
│
├── exe/                  → Optional: packaged executables
│   └── StudentManagement.exe
│
├── requirements.txt      → Python dependencies
├── README.txt            → Project overview and instructions


PREREQUISITES
-------------
- Python 3.6 or later
- pip
- Git
- (Optional) virtualenv for isolated environments


GETTING STARTED (SOURCE CODE SETUP)
-----------------------------------

1. Clone the repository:
   git clone https://github.com/Aliyah-Dawood/Student-Management-System.git
   cd Student-Management-System

2. Create a virtual environment:

   On Windows:
   python -m venv venv
   venv\Scripts\activate

   On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Install required packages:
   pip install -r requirements.txt

4. Ensure ML model files are present in src/models/:
   - aspiration_classifier.pkl
   - scaler.pkl

5. Run the Flask app:
   cd src
   python app.py

6. Open your browser and go to:
   http://127.0.0.1:5000/


OPTIONAL: RUNNING PRE-BUILT EXECUTABLE (WINDOWS)
------------------------------------------------
1. Download StudentManagement.exe from the exe/ folder or the GitHub Releases page
2. Double-click the file to launch the app
3. Your default web browser should open the app automatically


CONFIGURATION
-------------
Edit the file at src/config.py to update:
- Secret key
- Debug mode
- Database URI (SQLite by default)


TROUBLESHOOTING
---------------
- If you get ModuleNotFoundError: run 'pip install -r requirements.txt' again
- If the port is already in use: run 'python app.py --port 5001'
- If model files aren't found: make sure aspiration_classifier.pkl and scaler.pkl are in src/models/
- If app isn't loading: make sure you're running from inside the src/ directory


LICENSE
-------
This project is licensed under the MIT License. See LICENSE file for more information.


ACKNOWLEDGEMENTS
----------------
Thanks to all contributors and learners who use this project as a reference for Flask, SQLite, and machine learning integrations in web apps.

