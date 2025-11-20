from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_operation', methods=['POST'])
def execute_operation():
    operation = request.form.get('operation')
    result = ""
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'})
    
    try:
        cursor = connection.cursor()
        
        if operation == 'q1':
            result = execute_hospital_expansion(cursor, connection)
        
        elif operation == 'q2':
            result = get_patient_insurance_details(cursor)
        
        elif operation == 'q3':
            result = update_consultation(cursor, connection)
        
        elif operation == 'q4':
            result = delete_hospital_location(cursor, connection)
        
        elif operation == 'qv1':
            result = get_hospitals_in_cityville(cursor)
        
        elif operation == 'qv2':
            result = get_patients_over_30(cursor)
        
        elif operation == 'qv3':
            result = get_physician_most_specialties(cursor)
        
        elif operation == 'qv4':
            result = get_average_patient_age(cursor)
        
        else:
            result = "Invalid operation"
            
    except Error as e:
        result = f"Error: {e}"
    finally:
        cursor.close()
        connection.close()
    
    return jsonify({'result': result})

def execute_hospital_expansion(cursor, connection):
    """Q1: Hospital Expansion Operations"""
    try:
        # Add new specialty
        cursor.execute("INSERT INTO Speciality (SName, SDescription) VALUES ('Pediatrics', 'Child healthcare services')")
        
        # Add new physician
        cursor.execute("INSERT INTO Physician (PId, PFName, PMInit, PLName, HId) VALUES (601, 'Emily', 'C', 'White', 1)")
        
        # Link physician to specialty
        cursor.execute("INSERT INTO Physician_Speciality (PId, SId) VALUES (601, (SELECT SId FROM Speciality WHERE SName = 'Pediatrics'))")
        
        # Add new patient
        cursor.execute("INSERT INTO Patient (PSSN, PFName, PLName, PDoB, PGender) VALUES ('22233445566', 'Timmy', 'Jones', '2020-01-15', 'Male')")
        
        # Assign patient to physician
        cursor.execute("INSERT INTO Consultation (PSSN, PId, ConsultationDate) VALUES ('22233445566', 601, CURDATE())")
        
        connection.commit()
        return "Q1: Hospital expansion completed successfully!\n- Pediatrics specialty added\n- Dr. Emily White hired\n- Timmy Jones admitted and assigned to Dr. White"
    
    except Error as e:
        connection.rollback()
        return f"Error in Q1: {e}"

def get_patient_insurance_details(cursor):
    """Q2: Patient Insurance Details"""
    try:
        query = """
        SELECT 
            CONCAT(P.PFName, ' ', P.PLName) AS PatientName,
            I.IName AS InsuranceName,
            I.IType AS InsuranceType,
            P.PDoB AS DateOfBirth
        FROM Patient P
        JOIN Insurance I ON P.PSSN = I.PSSN
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            return "No insurance data found"
        
        output = "Q2: Patient Insurance Details:\n"
        output += "-" * 80 + "\n"
        output += f"{'Patient Name':<20} {'Insurance Name':<20} {'Type':<15} {'Date of Birth':<15}\n"
        output += "-" * 80 + "\n"
        
        for row in results:
            output += f"{row[0]:<20} {row[1]:<20} {row[2]:<15} {str(row[3]):<15}\n"
        
        return output
    
    except Error as e:
        return f"Error in Q2: {e}"

def update_consultation(cursor, connection):
    """Q3: Update Consultation Follow-up"""
    try:
        query = """
        UPDATE Consultation 
        SET FollowUpDate = '2025-08-01 11:00:00'
        WHERE PSSN = '111-22-3333' 
        AND ConsultationDate = '2025-08-01' 
        AND ConsultationTime = '06:00:00'
        """
        cursor.execute(query)
        connection.commit()
        
        if cursor.rowcount > 0:
            return "Q3: Consultation follow-up updated successfully for John Smith"
        else:
            return "Q3: No matching consultation found to update"
    
    except Error as e:
        connection.rollback()
        return f"Error in Q3: {e}"

def delete_hospital_location(cursor, connection):
    """Q4: Delete Hospital Location"""
    try:
        query = """
        DELETE FROM Hospital_Location 
        WHERE HId = 301 
        AND HLocation = '1000 Hospital Dr, Cityville'
        """
        cursor.execute(query)
        connection.commit()
        
        if cursor.rowcount > 0:
            return "Q4: Hospital location deleted successfully"
        else:
            return "Q4: No matching hospital location found to delete"
    
    except Error as e:
        connection.rollback()
        return f"Error in Q4: {e}"

def get_hospitals_in_cityville(cursor):
    """QV1: Hospitals in Cityville"""
    try:
        create_view_query = """
        CREATE OR REPLACE VIEW HospitalLocationSummary AS
        SELECT 
            H.HName AS HospitalName,
            GROUP_CONCAT(HL.HLocation SEPARATOR ', ') AS Locations
        FROM Hospital H
        LEFT JOIN Hospital_Location HL ON H.HId = HL.HId
        GROUP BY H.HId, H.HName
        """
        cursor.execute(create_view_query)
        
        query = """
        SELECT HospitalName, Locations 
        FROM HospitalLocationSummary 
        WHERE Locations LIKE '%Cityville%'
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        output = "QV1: Hospitals in Cityville:\n"
        output += "-" * 50 + "\n"
        
        for row in results:
            output += f"Hospital: {row[0]}\nLocations: {row[1]}\n"
        
        return output if results else "No hospitals found in Cityville"
    
    except Error as e:
        return f"Error in QV1: {e}"

def get_patients_over_30(cursor):
    """QV2: Patients Over 30 Years Old"""
    try:
        create_view_query = """
        CREATE OR REPLACE VIEW PatientAgeDistribution AS
        SELECT 
            CONCAT(PFName, ' ', PLName) AS PatientName,
            TIMESTAMPDIFF(YEAR, PDoB, CURDATE()) AS Age
        FROM Patient
        """
        cursor.execute(create_view_query)
        
        query = "SELECT PatientName, Age FROM PatientAgeDistribution WHERE Age > 30"
        cursor.execute(query)
        results = cursor.fetchall()
        
        output = "QV2: Patients Over 30 Years Old:\n"
        output += "-" * 40 + "\n"
        
        for row in results:
            output += f"Patient: {row[0]}, Age: {row[1]}\n"
        
        return output if results else "No patients over 30 years old found"
    
    except Error as e:
        return f"Error in QV2: {e}"

def get_physician_most_specialties(cursor):
    """QV3: Physician with Most Specialties"""
    try:
        create_view_query = """
        CREATE OR REPLACE VIEW PhysicianSpecialityCount AS
        SELECT 
            CONCAT(P.PFName, ' ', P.PLName) AS PhysicianName,
            COUNT(PS.SId) AS SpecialityCount
        FROM Physician P
        LEFT JOIN Physician_Speciality PS ON P.PId = PS.PId
        GROUP BY P.PId, P.PFName, P.PLName
        """
        cursor.execute(create_view_query)
        
        query = """
        SELECT PhysicianName, SpecialityCount 
        FROM PhysicianSpecialityCount 
        ORDER BY SpecialityCount DESC 
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return f"QV3: Physician with most specialties:\n{result[0]} with {result[1]} specialties"
        else:
            return "QV3: No physician data found"
    
    except Error as e:
        return f"Error in QV3: {e}"

def get_average_patient_age(cursor):
    """QV4: Average Patient Age"""
    try:
        create_view_query = """
        CREATE OR REPLACE VIEW PatientAgeDistribution AS
        SELECT 
            CONCAT(PFName, ' ', PLName) AS PatientName,
            TIMESTAMPDIFF(YEAR, PDoB, CURDATE()) AS Age
        FROM Patient
        """
        cursor.execute(create_view_query)
        
        query = "SELECT AVG(Age) FROM PatientAgeDistribution"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result[0]:
            return f"QV4: Average patient age: {result[0]:.2f} years"
        else:
            return "QV4: No patient age data found"
    
    except Error as e:
        return f"Error in QV4: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
