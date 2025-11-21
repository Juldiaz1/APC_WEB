from flask import Flask, render_template, request, jsonify, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'apc_secret_key_2025'

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="apc_database"
    )

@app.route("/")
def home():
    return render_template("index.html")

def create_views():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        CREATE OR REPLACE VIEW HospitalLocationSummary AS
        SELECT 
            H.HName AS HospitalName,
            GROUP_CONCAT(HL.Location ORDER BY HL.Location SEPARATOR ', ') AS Locations
        FROM Hospital H
        LEFT JOIN Hospital_Location HL 
            ON H.HId = HL.HId
        GROUP BY H.HId, H.HName;
    """)

    cur.execute("""
        CREATE OR REPLACE VIEW PatientAgeDistribution AS
        SELECT 
            P.PName AS PatientName,
            TIMESTAMPDIFF(YEAR, P.DateOfBirth, CURDATE()) AS Age
        FROM Patient P;
    """)

    cur.execute("""
        CREATE OR REPLACE VIEW PhysicianSpecialityCount AS
        SELECT 
            CONCAT(Ph.FName, ' ', Ph.LName) AS FullName,
            COUNT(PS.SName) AS NumSpecialities
        FROM Physician Ph
        LEFT JOIN PHYSICIAN_SPECIALITY PS
            ON Ph.PId = PS.PId
        GROUP BY Ph.PId, Ph.FName, Ph.LName;
    """)

    db.commit()

@app.route("/q1_hospital_expansion")
def q1_hospital_expansion():
    return render_template("q1.html")

@app.route("/q2_patient_insurance")
def q2_patient_insurance():
    return render_template("q2.html")

@app.route("/q3_update_consultation")
def q3_update_consultation():
    return render_template("q3.html")

@app.route("/q4_remove_location")
def q4_remove_location():
    return render_template("q4.html")

@app.route("/create_views")
def create_views_page():
    return render_template("create_views.html")

@app.route("/view_queries")
def view_queries_page():
    return render_template("view_queries.html")

@app.route("/database_status")
def database_status():
    return render_template("database_status.html")

@app.route("/test_connection")
def test_connection():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT DATABASE()")
        db_name = cur.fetchone()[0]
        return f"SUCCESS: Connected to database: {db_name}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route("/q1", methods=['GET', 'POST'])
def q1():
    if request.method == 'GET':
        return render_template("q1.html")
    
    db = get_db()
    cur = db.cursor()

    queries = [
        "INSERT INTO Speciality (SName) VALUES ('Pediatrics');",
        "INSERT INTO Physician (PId, FName, LName, MInitial, HId) VALUES (601, 'Emily', 'White', 'C', 1);",
        "INSERT INTO PHYSICIAN_SPECIALITY (PId, SName) VALUES (601, 'Pediatrics');",
        "INSERT INTO PATIENT (PSSN, PName, Sex, Address, DateOfBirth, PId, PoId) VALUES ('22233445566', 'Timmy Jones', 'M', 'Unknown', '2020-01-15', 601, NULL);"
    ]

    try:
        for query in queries:
            cur.execute(query)
        
        db.commit()
        return jsonify({
            "status": "success", 
            "message": "Q1 Completed Successfully",
            "queries": queries
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error: {e}",
            "queries": queries
        })

@app.route("/q2", methods=['GET'])
def q2():
    query = """
        SELECT P.PName AS PatientName,
        CP.PoName AS PolicyName,
        CP.PoType AS PolicyType,
        P.DateOfBirth
        FROM Patient P
        LEFT JOIN CoveragePolicy CP ON P.PoId = CP.PoId;
    """

    db = get_db()
    cur = db.cursor(dictionary=True)
    
    try:
        cur.execute(query)
        results = cur.fetchall()
        return jsonify({
            "status": "success",
            "data": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/q3", methods=['GET', 'POST'])
def q3():
    if request.method == 'GET':
        return render_template("q3.html")
    
    query = """
        UPDATE CONSULTATION
        SET FDate = '2025-08-01', FTime= '11:00:00'
        WHERE PSSN = '111-22-3333'
          AND CDate = '2025-08-01' AND CTime= '06:00:00';
    """

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(query)
        db.commit()
        return jsonify({
            "status": "success", 
            "message": "Consultation Updated Successfully",
            "query": query
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/q4", methods=['GET', 'POST'])
def q4():
    if request.method == 'GET':
        return render_template("q4.html")
    
    query = """
        DELETE FROM Hospital_Location
        WHERE HId = 301 AND Location = '1000 Hospital Dr, Cityville';
    """

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(query)
        db.commit()
        return jsonify({
            "status": "success", 
            "message": "Location removed successfully",
            "query": query
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/qv1")
def qv1():
    query = """
        SELECT *
        FROM HospitalLocationSummary
        WHERE Locations LIKE '%Cityville%';
    """
    
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(query)
        results = cur.fetchall()
        return jsonify({
            "status": "success",
            "data": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/qv2")
def qv2():
    query = """
        SELECT *
        FROM PatientAgeDistribution
        WHERE Age > 30;
    """
    
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(query)
        results = cur.fetchall()
        return jsonify({
            "status": "success",
            "data": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/qv3")
def qv3():
    query = """
        SELECT FullName
        FROM PhysicianSpecialityCount
        ORDER BY NumSpecialities DESC
        LIMIT 1;
    """
    
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(query)
        results = cur.fetchall()
        return jsonify({
            "status": "success",
            "data": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {e}",
            "query": query
        })

@app.route("/qv4")
def qv4():
    query = """
        SELECT AVG(Age) AS AverageAge
        FROM PatientAgeDistribution;
    """
    
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(query)
        results = cur.fetchall()
        return jsonify({
            "status": "success",
            "data": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {e}",
            "query": query
        })

@app.before_first_request
def initialize():
    create_views()

if __name__ == "__main__":
    app.run(debug=True)
