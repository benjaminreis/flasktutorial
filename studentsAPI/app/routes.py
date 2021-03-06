from app import app
import pyodbc
import json
from flask import (request)
from models import Student
from flask_cors import CORS

server = 'localhost' 
database = 'Training' 
conn = pyodbc.connect('DRIVER=SQL Server;SERVER='+server+';DATABASE='+database+';Trusted_Connection=True;')
cursor = conn.cursor()


@app.route('/')
@app.route('/index')
def index():
    # cursor.execute("select * FROM dbo.Students")
    # for row in cursor.fetchall():
    #     print(row)
    return "completed"

#SQL parameters for pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Getting-started#parameters
def Call_Database(query):
    raw = cursor.execute(query)
    return raw 

def Students_JSON(raw_data):
    items = []
    for row in raw_data:
        items.append({'ID': row[0], 'FirstName': row[1], 'LastName': row[2], 'GraduationDate': row[3], 'LoanBalance': str(row[4]), 'Servicer': row[5], 'SchoolName': row[6], 'StudentID': row[7], 'Status': row[8]})
    return json.dumps(items)

@app.route('/Students')
def All():
    query = "Select * from dbo.students"
    raw = Call_Database(query)
    return Students_JSON(raw)

@app.route('/Students/<int:student_ID>', methods=['GET'])
def get(student_ID):
    query = "SELECT * FROM dbo.[STUDENTS] WHERE ID = ?"
    cursor.execute(query, student_ID)
    raw = cursor.fetchall()
    student = Student.Student(raw[0])
    students = [student]
    return json.dumps([student.__dict__ for student in students])

@app.route('/Students', methods=['POST'])
def create():
    if request.method == 'POST':
        query = "INSERT INTO dbo.[STUDENTS] (FirstName, LastName, GraduationDate, LoanBalance, Servicer, SchoolName, StudentID, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        json = request.get_json(force=True)
        FirstName = json['FirstName']
        LastName = json['LastName']
        GraduationDate = json['GraduationDate']
        LoanBalance = None
        if 'LoanBalance' in json:
            LoanBalance = json['LoanBalance']
        Servicer = None
        if 'Servicer' in json:
            Servicer = json['Servicer']
        SchoolName = json['SchoolName']
        
        StudentID = None
        if 'StudentID' in json:
            StudentID = json['StudentID']
        Status = json['Status']
        cursor.execute(query, FirstName, LastName, GraduationDate, LoanBalance, Servicer, SchoolName, StudentID, Status)
        cursor.commit()
    return "success"

@app.route('/Students/<int:student_ID>', methods=['PUT'])
def edit(student_ID):
    query = "UPDATE DBO.[STUDENTS] SET "
    params = []
    json = request.get_json(force=True)
    if ((json['FirstName'] != None) or (json['FirstName'] != '')):
        params.append(json['FirstName'])
        query += "FirstName = ?,"
    if ((json['LastName'] != None) or (json['LastName'] != '')):
        params.append(json['LastName'])
        query += "LastName = ?,"
    if ((json['GraduationDate'] != None) or (json['GraduationDate'] != '')):
        params.append(json['GraduationDate'])
        query += "GraduationDate = ?,"  
    if 'LoanBalance' in json:        
        if ((json['LoanBalance'] != None) or (json['LoanBalance'] != '')):
            params.append(json['LoanBalance'])
            query += "LoanBalance = ?,"
    if 'Servicer' in json:
        if ((json['Servicer'] != None) or (json['Servicer'] != '')):
            params.append(json['Servicer'])
            query += "Servicer = ?,"
    if ((json['SchoolName'] != None) or (json['SchoolName'] != '')):
        params.append(json['SchoolName'])
        query += "SchoolName = ?,"
    if 'StudentID' in json:
        if ((json['StudentID'] != None) or (json['StudentID'] != '')):
            params.append(json['StudentID'])
            query += "StudentID = ?,"
    if ((json['Status'] != None) or (json['Status'] != '')):
        params.append(json['Status'])
        query += "Status = ?," 

    query = query[:-1]
    query += " WHERE ID = ?"
    params.append(student_ID)
    cursor.execute(query, params)
    cursor.commit()
    return "success"