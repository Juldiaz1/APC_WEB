# app.py
from flask import Flask, render_template, request, flash
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'apc_phase3_secret_2025'

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Q1: Hospital Expansion Operations
@app.route('/q1', methods=['GET', 'POST'])
def q1_hospital_expansion():
    results = []
    sql_queries = []
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # Q1 Operations
                queries = [
                    # 1. Add new specialty "Pediatrics"
                    "INSERT IGNORE INTO Speciality (SName) VALUES ('Pediatrics')",
                    
                    # 2. Add new physician Dr. Emily White
                    "INSERT IGNORE INTO Physician (PId, FName, LName, MInitial, HId) VALUES (601, 'Emily', 'White', 'C', 1)",
                    
                    # 3. Link physician to specialty
                    "INSERT IGNORE INTO Physician_Speciality (PId, SName) VALUES (601, 'Pediatrics')",
                    
                    # 4. Add new patient Timmy Jones
                    "INSERT IGNORE INTO Patient (PSSN, PName, Sex, DateOfBirth, PId, PoId) VALUES ('22233445566', 'Timmy Jones', 'M', '2020-01-15', 601, 1)",
                    
                    # 5. Create consultation (assign patient to physician)
                    "INSERT IGNORE INTO Consultation (PSSN, PId, CDate, CTime) VALUES ('22233445566', 601, CURDATE(), CURTIME())"
                ]
                
                for query in queries:
                    sql_queries.append(query)
                    cursor.execute(query)
                
                conn.commit()
                results.append("SUCCESS: All Q1 operations completed successfully!")
                
                # Verification
                verification_queries = [
                    ("SELECT SName FROM Speciality WHERE SName = 'Pediatrics'", "Pediatrics specialty"),
                    ("SELECT * FROM Physician WHERE PId = 601", "Dr. Emily White"),
                    ("SELECT * FROM Patient WHERE PSSN = '22233445566'", "Timmy Jones patient"),
                    ("SELECT * FROM Physician_Speciality WHERE PId = 601 AND SName = 'Pediatrics'", "Physician-Specialty link")
                ]
                
                for v_query, desc in verification_queries:
                    cursor.execute(v_query)
                    if cursor.fetchone():
                        results.append(f"VERIFIED: {desc} added successfully")
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            results.append(f"ERROR: {str(e)}")
    
    return render_template('q1.html', results=results, sql_queries=sql_queries)

# Q2: Patient Insurance Details
@app.route('/q2')
def q2_patient_insurance():
    sql_query = """
    SELECT 
        p.PName AS PatientName,
        cp.PoName AS CoveragePolicy,
        cp.PoType AS CoverageType,
        p.DateOfBirth AS DateOfBirth
    FROM Patient p
    JOIN CoveragePolicy cp ON p.PoId = cp.PoId
    ORDER BY p.PName
    """
    
    patients = []
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql_query)
            patients = cursor.fetchall()
            cursor.close()
            conn.close()
    except Exception as e:
        flash(f"Error retrieving patient insurance data: {str(e)}")
    
    return render_template('q2.html', patients=patients, sql_query=sql_query)

# Q3: Update Consultation Follow-up
@app.route('/q3', methods=['GET', 'POST'])
def q3_update_consultation():
    result = None
    sql_query = """
    UPDATE Consultation 
    SET FDate = '2025-08-01', FTime = '11:00:00'
    WHERE PSSN = '111-22-3333' 
    AND CDate = '2025-08-01' 
    AND CTime = '06:00:00'
    """
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # First, check if the consultation exists
                check_query = """
                SELECT * FROM Consultation 
                WHERE PSSN = '111-22-3333' 
                AND CDate = '2025-08-01' 
                AND CTime = '06:00:00'
                """
                cursor.execute(check_query)
                
                if not cursor.fetchone():
                    # Create the consultation if it doesn't exist
                    create_query = """
                    INSERT IGNORE INTO Consultation (PSSN, PId, CDate, CTime, FDate, FTime) 
                    VALUES ('111-22-3333', 1, '2025-08-01', '06:00:00', '2025-08-01', '09:00:00')
                    """
                    cursor.execute(create_query)
                    flash("Note: Consultation didn't exist. Created it first, then updating...")
                
                # Now update the follow-up time
                cursor.execute(sql_query)
                conn.commit()
                
                # Verify the update
                cursor.execute("SELECT FDate, FTime FROM Consultation WHERE PSSN = '111-22-3333' AND CDate = '2025-08-01' AND CTime = '06:00:00'")
                updated = cursor.fetchone()
                
                if updated and updated[0] == '2025-08-01' and str(updated[1]) == '11:00:00':
                    result = "SUCCESS: Consultation follow-up time successfully updated to 2025-08-01 at 11:00:00!"
                else:
                    result = "WARNING: Update executed but verification failed"
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            result = f"ERROR: {str(e)}"
    
    return render_template('q3.html', result=result, sql_query=sql_query)

# Q4: Remove Hospital Location
@app.route('/q4', methods=['GET', 'POST'])
def q4_remove_location():
    result = None
    sql_query = """
    DELETE FROM Hospital_Location 
    WHERE Location = '1000 Hospital Dr, Cityville' 
    AND HId = 301
    """
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # First, check if the location exists
                check_query = """
                SELECT * FROM Hospital_Location 
                WHERE Location = '1000 Hospital Dr, Cityville' 
                AND HId = 301
                """
                cursor.execute(check_query)
                
                if cursor.fetchone():
                    cursor.execute(sql_query)
                    conn.commit()
                    result = "SUCCESS: Hospital location '1000 Hospital Dr, Cityville' successfully removed!"
                else:
                    result = "NOTE: Location '1000 Hospital Dr, Cityville' for St. Jude's Hospital (HId=301) was not found in the database"
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            result = f"ERROR: {str(e)}"
    
    return render_template('q4.html', result=result, sql_query=sql_query)

# Create Views
@app.route('/create_views', methods=['GET', 'POST'])
def create_views():
    results = []
    view_queries = []
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # View creation queries
                views = {
                    'HospitalLocationSummary': """
                    CREATE OR REPLACE VIEW HospitalLocationSummary AS
                    SELECT 
                        H.HName AS HospitalName,
                        GROUP_CONCAT(HL.Location SEPARATOR ', ') AS Locations
                    FROM Hospital H
                    LEFT JOIN Hospital_Location HL ON H.HId = HL.HId
                    GROUP BY H.HId, H.HName
                    """,
                    
                    'PatientAgeDistribution': """
                    CREATE OR REPLACE VIEW PatientAgeDistribution AS
                    SELECT 
                        PName AS PatientName,
                        TIMESTAMPDIFF(YEAR, DateOfBirth, CURDATE()) AS Age
                    FROM Patient
                    """,
                    
                    'PhysicianSpecialityCount': """
                    CREATE OR REPLACE VIEW PhysicianSpecialityCount AS
                    SELECT 
                        CONCAT(FName, ' ', LName) AS PhysicianName,
                        COUNT(PS.SName) AS SpecialityCount
                    FROM Physician P
                    LEFT JOIN Physician_Speciality PS ON P.PId = PS.PId
                    GROUP BY P.PId, P.FName, P.LName
                    """
                }
                
                for view_name, query in views.items():
                    view_queries.append(query)
                    cursor.execute(query)
                    results.append(f"SUCCESS: {view_name} view created successfully!")
                
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            results.append(f"ERROR: {str(e)}")
    
    return render_template('create_views.html', results=results, view_queries=view_queries)

# View Queries
@app.route('/view_queries')
def view_queries():
    queries_results = {}
    view_sql_queries = {
        'qv1': "SELECT HospitalName, Locations FROM HospitalLocationSummary WHERE Locations LIKE '%Cityville%'",
        'qv2': "SELECT PatientName FROM PatientAgeDistribution WHERE Age > 30",
        'qv3': "SELECT PhysicianName, SpecialityCount FROM PhysicianSpecialityCount ORDER BY SpecialityCount DESC LIMIT 1",
        'qv4': "SELECT ROUND(AVG(Age), 2) AS AverageAge FROM PatientAgeDistribution"
    }
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            for query_name, sql_query in view_sql_queries.items():
                cursor.execute(sql_query)
                queries_results[query_name] = {
                    'data': cursor.fetchall(),
                    'sql': sql_query
                }
            
            cursor.close()
            conn.close()
    except Exception as e:
        flash(f"Error executing view queries: {str(e)}")
    
    return render_template('view_queries.html', results=queries_results)

# Database Status
@app.route('/database_status')
def database_status():
    status = {}
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Check tables
            tables = ['Hospital', 'Physician', 'Patient', 'Speciality', 'Physician_Speciality', 
                     'CoveragePolicy', 'Consultation', 'Hospital_Location', 'Diagnosis']
            
            for table in tables:
                cursor.execute(f"SHOW TABLES LIKE '{table}'")
                status[table] = "EXISTS" if cursor.fetchone() else "MISSING"
            
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            status['database'] = f"Connected to: {db_name}"
            
            # Count records
            cursor.execute("SELECT COUNT(*) as count FROM Hospital")
            status['hospital_records'] = f"{cursor.fetchone()['count']} records"
            
            cursor.execute("SELECT COUNT(*) as count FROM Physician")
            status['physician_records'] = f"{cursor.fetchone()['count']} records"
            
            cursor.execute("SELECT COUNT(*) as count FROM Patient")
            status['patient_records'] = f"{cursor.fetchone()['count']} records"
            
            cursor.close()
            conn.close()
        else:
            status['connection'] = "Failed to connect to database"
    except Exception as e:
        status['error'] = f"Database error: {str(e)}"
    
    return render_template('database_status.html', status=status)

@app.route('/test_connection')
def test_connection():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return f"SUCCESS: Database connection successful! Connected to: {db_name}"
        else:
            return "ERROR: Database connection failed!"
    except Exception as e:
        return f"ERROR: Database connection error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
