# APC Database Web Interface - Phase 3

## Project Overview
A comprehensive web interface for managing the Arlington Physicians' Center (APC) database, implementing all Phase 3 requirements with a modern, animated user interface.

## Project Requirements Completed
- **Q1**: Hospital Expansion Operations
- **Q2**: Patient Insurance Details
- **Q3**: Update Consultation Follow-up
- **Q4**: Remove Hospital Location
- **View Creation**: HospitalLocationSummary, PatientAgeDistribution, PhysicianSpecialityCount
- **View Queries**: QV1-QV4 analytical queries

- Technology Stack
- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with animations
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Juldiaz1/APC_WEB.git
cd APC_WEB
```

### Step 2: Install Dependencies
```bash
pip install flask mysql-connector-python
```

### Step 3: Database Configuration
Update the database connection in `app.py`:

```python  you may change on app.py  local host to your host and database to yoyur database personal name 
def get_db():
    return mysql.connector.connect(
        host="localhost",     
        user="root",
        password="your_password",
        database="apc_database"
    )
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```
your local host may be diffrent 

## Project Structure
```
APC_WEB/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard
│   ├── q1.html           # Hospital expansion operations
│   ├── q2.html           # Patient insurance details
│   ├── q3.html           # Update consultation
│   ├── q4.html           # Remove location
│   ├── create_views.html  # View creation page
│   ├── view_queries.html  # View-based queries
│   └── database_status.html # Database status page
└── README.md             # Project documentation
```

## Database Operations

### Q1: Hospital Expansion
- Add 'Pediatrics' specialty
- Hire Dr. Emily White (PId=601)
- Link physician to specialty
- Admit patient Timmy Jones
- Assign patient to physician

### Q2: Patient Insurance
- Display patient names
- Show coverage policies and types
- Include date of birth information

### Q3: Update Consultation
- Update follow-up time for John Smith
- Change from 06:00:00 to 11:00:00
- Specific consultation on 2025-08-01

### Q4: Remove Location
- Delete hospital location record
- Remove '1000 Hospital Dr, Cityville'
- For St. Jude's Hospital (HId=301)

## Database Views

### HospitalLocationSummary
- Hospital names with comma-separated locations
- Used for QV1: Hospitals in Cityville

### PatientAgeDistribution
- Patient names with calculated ages
- Used for QV2: Patients over 30, QV4: Average age

### PhysicianSpecialityCount
- Physician names with specialty counts
- Used for QV3: Physician with most specialties

## View-Based Queries

### QV1: Hospitals in Cityville
Find hospitals with locations in 'Cityville'

### QV2: Patients Over 30
Retrieve patients older than 30 years

### QV3: Physician with Most Specialties
Find physician with highest number of specialties

### QV4: Average Patient Age
Calculate average age of all patients

## Usage Instructions

1. **Home Dashboard**: Navigate between different operations
2. **Q1 Operations**: Execute hospital expansion tasks
3. **Q2 Operations**: View patient insurance data
4. **Q3 Operations**: Update consultation follow-ups
5. **Q4 Operations**: Remove hospital locations
6. **Create Views**: Generate database views (auto-created on startup)
7. **View Queries**: Run analytical queries on views
8. **Database Status**: Check connection and system health

## Error Handling
- Database connection errors are caught and displayed
- SQL execution errors show detailed messages
- Network errors are handled gracefully
- All operations include success/error feedback
