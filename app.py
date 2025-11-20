# app.py
from flask import Flask, render_template, request, flash
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        flash(f"Database connection error: {e}")
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
                
                # Q1 Queries
                queries = [
                    # Add new specialty
                    "INSERT INTO Speciality (SName) VALUES ('Pediatrics')",
                    
                    # Add new physician
                    "INSERT INTO Physician (PId, PFName, PMInit, PLName, HId) VALUES (601, 'Emily', 'C', 'White', 1)",
                    
                    # Link physician to specialty
                    "INSERT INTO Physician_Speciality (PId, SId) VALUES (601, (SELECT SId FROM Speciality WHERE SName = 'Pediatrics'))",
                    
                    # Add new patient
                    "INSERT INTO Patient (PSSN, PFName, PLName, PDoB, PGender, HId) VALUES ('22233445566', 'Timmy', 'Jones', '2020-01-15', 'M', 1)",
                    
                    # Assign patient to physician
                    "INSERT INTO Consultation (PSSN, PId, CDateTime) VALUES ('22233445566', 601, NOW())"
                ]
                
                for query in queries:
                    sql_queries.append(query)
                    cursor.execute(query)
                
                conn.commit()
                results.append("Q1 Operations completed successfully!")
                cursor.close()
                conn.close()
            
        except Exception as e:
            results.append(f"Error: {str(e)}")
    
    return render_template('q1.html', results=results, sql_queries=sql_queries)

# Q2: Patient Insurance Details
@app.route('/q2')
def q2_patient_insurance():
    patients = []
    sql_query = """
    SELECT 
        CONCAT(P.PFName, ' ', P.PLName) AS PatientName,
        IC.ICName AS CoveragePolicy,
        IC.ICType AS CoverageType,
        P.PDoB AS DateOfBirth
    FROM Patient P
    JOIN Insurance_Coverage IC ON P.PSSN = IC.PSSN
    """
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql_query)
            patients = cursor.fetchall()
            cursor.close()
            conn.close()
            
    except Exception as e:
        flash(f"Error: {str(e)}")
    
    return render_template('q2.html', patients=patients, sql_query=sql_query)

# Q3: Update Consultation Follow-up
@app.route('/q3', methods=['GET', 'POST'])
def q3_update_consultation():
    result = None
    sql_query = """
    UPDATE Consultation 
    SET CFollowUpDateTime = '2025-08-01 11:00:00'
    WHERE PSSN = '111-22-3333' 
    AND CDateTime = '2025-08-01 06:00:00'
    """
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                conn.commit()
                result = "Consultation follow-up time updated successfully!"
                cursor.close()
                conn.close()
            
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template('q3.html', result=result, sql_query=sql_query)

# Q4: Remove Hospital Location
@app.route('/q4', methods=['GET', 'POST'])
def q4_remove_location():
    result = None
    sql_query = """
    DELETE FROM Hospital_Location 
    WHERE HLAddress = '1000 Hospital Dr, Cityville' 
    AND HId = 301
    """
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                conn.commit()
                result = "Hospital location removed successfully!"
                cursor.close()
                conn.close()
            
        except Exception as e:
            result = f"Error: {str(e)}"
    
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
                        GROUP_CONCAT(HL.HLAddress SEPARATOR ', ') AS Locations
                    FROM Hospital H
                    LEFT JOIN Hospital_Location HL ON H.HId = HL.HId
                    GROUP BY H.HId, H.HName
                    """,
                    
                    'PatientAgeDistribution': """
                    CREATE OR REPLACE VIEW PatientAgeDistribution AS
                    SELECT 
                        CONCAT(PFName, ' ', PLName) AS PatientName,
                        TIMESTAMPDIFF(YEAR, PDoB, CURDATE()) AS Age
                    FROM Patient
                    """,
                    
                    'PhysicianSpecialityCount': """
                    CREATE OR REPLACE VIEW PhysicianSpecialityCount AS
                    SELECT 
                        CONCAT(P.PFName, ' ', P.PLName) AS PhysicianName,
                        COUNT(PS.SId) AS SpecialityCount
                    FROM Physician P
                    LEFT JOIN Physician_Speciality PS ON P.PId = PS.PId
                    GROUP BY P.PId, P.PFName, P.PLName
                    """
                }
                
                for view_name, query in views.items():
                    view_queries.append(f"-- {view_name} View\n{query}")
                    cursor.execute(query)
                    results.append(f"{view_name} view created successfully!")
                
                conn.commit()
                cursor.close()
                conn.close()
            
        except Exception as e:
            results.append(f"Error: {str(e)}")
    
    return render_template('create_views.html', results=results, view_queries=view_queries)

# View Queries
@app.route('/view_queries')
def view_queries():
    queries_results = {}
    view_sql_queries = {
        'qv1': """
        SELECT HospitalName, Locations 
        FROM HospitalLocationSummary 
        WHERE Locations LIKE '%Cityville%'
        """,
        'qv2': """
        SELECT PatientName 
        FROM PatientAgeDistribution 
        WHERE Age > 30
        """,
        'qv3': """
        SELECT PhysicianName, SpecialityCount 
        FROM PhysicianSpecialityCount 
        ORDER BY SpecialityCount DESC 
        LIMIT 1
        """,
        'qv4': """
        SELECT AVG(Age) AS AverageAge 
        FROM PatientAgeDistribution
        """
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
        flash(f"Error: {str(e)}")
    
    return render_template('view_queries.html', results=queries_results)

# Database Connection Test
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
            return f"✅ Database connection successful! Connected to: {db_name}"
        else:
            return "❌ Database connection failed!"
    except Exception as e:
        return f"❌ Database connection error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
