APC Database Web Interface
A Flask-based web application for managing the Arlington Physicians' Center database system. Developed as part of DB1 Project Phase 3B.

Quick Start
Prerequisites
Python 3.7 or higher

MySQL Server

APC database from previous phases

Installation Steps
Extract or Clone the Project

bash
# If using git
git clone https://github.com/yourusername/APC_WEB.git
cd APC_WEB
Install Dependencies

bash
pip install -r requirements.txt
Configure Database Connection

Edit config.py with your MySQL credentials:

python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'apc_database',
    'user': 'root',      # Change if different
    'password': '',      # Change if different
    'port': 3306
}
Run the Application

bash
python app.py
Access the Web Interface
Open your browser and go to: http://127.0.0.1:5000

Required Database Tables
The application expects these tables to exist in your apc_database:

Hospital

Physician

Patient

Speciality

Insurance

Consultation

Hospital_Location

Physician_Speciality

Available Operations
Main Operations
Q1: Hospital Expansion - Add Pediatrics specialty, Dr. Emily White, and patient Timmy Jones

Q2: Patient Insurance Details - Display all patients with insurance information

Q3: Update Consultation - Update follow-up time for John Smith

Q4: Delete Hospital Location - Remove location from St. Jude's Hospital

View-Based Queries
QV1: Hospitals in Cityville

QV2: Patients Over 30 Years Old

QV3: Physician with Most Specialties

QV4: Average Patient Age

Project Structure
text
APC_WEB/
├── app.py                 # Main Flask application
├── config.py              # Database configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── honor_code.txt         # Signed honor code
├── templates/
│   └── index.html         # Web interface template
└── static/
    └── style.css          # CSS styling
Dependencies
Flask==2.3.3

mysql-connector-python==8.1.0

Troubleshooting
Common Issues
Database Connection Error

Verify MySQL server is running

Check credentials in config.py

Ensure apc_database exists

Module Not Found Errors

Run: pip install -r requirements.txt

Check Python version (requires 3.7+)

Port Already in Use

Change port in app.py: app.run(port=5001)

Or kill existing process using port 5000

Testing the Application
Start the application: python app.py

Open browser to http://127.0.0.1:5000

Try running Q2 first to test database connection

Execute other operations as needed

File Descriptions
app.py: Contains all Flask routes and database operations

config.py: Database connection settings

requirements.txt: Python package dependencies

templates/index.html: Main web interface

static/style.css: Styling for the web interface

Database Views Created
The application automatically creates these views when needed:

HospitalLocationSummary

PatientAgeDistribution

PhysicianSpecialityCount

Team Information
[Your Name] - [Your Student ID]

[Teammate Name] - [Teammate Student ID] (if applicable)

Course Information
Course: DB1

Project: Phase 3B

Due Date: Nov 21st 2025

Institution: UT Arlington

Support
For issues with the application:

Check that all database tables exist

Verify MySQL server is running

Ensure Python dependencies are installed

Check the console for error messages

License
This project is for academic purposes as part of UT Arlington DB1 course.

take away the honor codde
APC Database Web Interface
A Flask-based web application for managing the Arlington Physicians' Center database system. Developed as part of DB1 Project Phase 3B.

Quick Start
Prerequisites
Python 3.7 or higher

MySQL Server

APC database from previous phases

Installation Steps
Extract or Clone the Project

bash
# If using git
git clone https://github.com/yourusername/APC_WEB.git
cd APC_WEB
Install Dependencies

bash
pip install -r requirements.txt
Configure Database Connection

Edit config.py with your MySQL credentials:

python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'apc_database',
    'user': 'root',      # Change if different
    'password': '',      # Change if different
    'port': 3306
}
Run the Application

bash
python app.py
Access the Web Interface
Open your browser and go to: http://127.0.0.1:5000

Required Database Tables
The application expects these tables to exist in your apc_database:

Hospital

Physician

Patient

Speciality

Insurance

Consultation

Hospital_Location

Physician_Speciality

Available Operations
Main Operations
Q1: Hospital Expansion - Add Pediatrics specialty, Dr. Emily White, and patient Timmy Jones

Q2: Patient Insurance Details - Display all patients with insurance information

Q3: Update Consultation - Update follow-up time for John Smith

Q4: Delete Hospital Location - Remove location from St. Jude's Hospital

View-Based Queries
QV1: Hospitals in Cityville

QV2: Patients Over 30 Years Old

QV3: Physician with Most Specialties

QV4: Average Patient Age

Project Structure
text
APC_WEB/
├── app.py                 # Main Flask application
├── config.py              # Database configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface template
└── static/
    └── style.css          # CSS styling
Dependencies
Flask==2.3.3

mysql-connector-python==8.1.0

Troubleshooting
Common Issues
Database Connection Error

Verify MySQL server is running

Check credentials in config.py

Ensure apc_database exists

Module Not Found Errors

Run: pip install -r requirements.txt

Check Python version (requires 3.7+)

Port Already in Use

Change port in app.py: app.run(port=5001)

Or kill existing process using port 5000

Testing the Application
Start the application: python app.py

Open browser to http://127.0.0.1:5000

Try running Q2 first to test database connection

Execute other operations as needed

File Descriptions
app.py: Contains all Flask routes and database operations

config.py: Database connection settings

requirements.txt: Python package dependencies

templates/index.html: Main web interface

static/style.css: Styling for the web interface
