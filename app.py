from flask import Flask, render_template, request, jsonify
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

@app.post("/q1")
def q1():
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO Speciality (SName) VALUES ('Pediatrics');")
        cur.execute("INSERT INTO Physician (PId, FName, LName, MInitial, HId) VALUES (601, 'Emily', 'White', 'C', 1);")
        cur.execute("INSERT INTO PHYSICIAN_SPECIALITY (PId, SName) VALUES (601, 'Pediatrics');")
        cur.execute("INSERT INTO PATIENT (PSSN, PName, Sex, Address, DateOfBirth, PId, PoId) VALUES ('22233445566', 'Timmy Jones', 'M', 'Unknown', '2020-01-15', 601, NULL);")
        
        db.commit()
        return jsonify({"status": "success", "message": "Q1 Completed Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"})

@app.get("/q2")
def q2():
    db = get_db()
    cur = db.cursor(dictionary=True)

    query = """
        SELECT P.PName AS PatientName,
        CP.PoName AS PolicyName,
        CP.PoType AS PolicyType,
        P.DateOfBirth
        FROM Patient P
        LEFT JOIN CoveragePolicy CP ON P.PoId = CP.PoId;
    """

    cur.execute(query)
    return jsonify(cur.fetchall())

@app.post("/q3")
def q3():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE CONSULTATION
        SET FDate = '2025-08-01', FTime= '11:00:00'
        WHERE PSSN = '111-22-3333'
          AND CDate = '2025-08-01' AND CTime= '06:00:00';
    """)

    db.commit()
    return jsonify({"status": "success", "message": "Consultation Updated Successfully"})

@app.post("/q4")
def q4():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        DELETE FROM Hospital_Location
        WHERE HId = 301 AND Location = '1000 Hospital Dr, Cityville';
    """)

    db.commit()
    return jsonify({"status": "success", "message": "Location removed successfully"})

@app.get("/qv1")
def qv1():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT HospitalName, Locations
        FROM HospitalLocationSummary
        WHERE Locations LIKE '%Cityville%';
    """)

    return jsonify(cur.fetchall())

@app.get("/qv2")
def qv2():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT PatientName
        FROM PatientAgeDistribution
        WHERE Age > 30;
    """)

    return jsonify(cur.fetchall())

@app.get("/qv3")
def qv3():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT FullName
        FROM PhysicianSpecialityCount
        ORDER BY NumSpecialities DESC
        LIMIT 1;
    """)

    return jsonify(cur.fetchall())

@app.get("/qv4")
def qv4():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT AVG(Age) AS AverageAge
        FROM PatientAgeDistribution;
    """)

    return jsonify(cur.fetchall())

if __name__ == "__main__":
    create_views()
    app.run(debug=True)
