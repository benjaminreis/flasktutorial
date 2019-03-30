from app import app
import pyodbc
import json
from flask import (request)
from models import Student

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
        items.append({'id': row[0], 'FirstName': row[1], 'LastName': row[2], 'GraduationDate': row[3], 'LoanBalance': str(row[4]), 'Servicer': row[5], 'StudentID': row[6], 'Status': row[7]})
    return json.dumps(items)

@app.route('/Students/All')
def All():
    query = "Select * from dbo.students"
    raw = Call_Database(query)
    return Students_JSON(raw)

@app.route('/Students/<int:student_ID>', methods=['GET'])
def get(student_ID):
    query = "SELECT * FROM dbo.[STUDENTS] WHERE ID = ?"
    cursor.execute(query, student_ID)
    raw = cursor.fetchall()
    return Student.Student(raw[0])

@app.route('/Students/Create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        query = "INSERT INTO dbo.[STUDENTS] (FirstName, LastName, GraduationDate, LoanBalance, Servicer, SchoolName, StudentID, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        json = request.get_json(force=True)
        FirstName = json['FirstName']
        LastName = json['LastName']
        GraduationDate = json['GraduationDate']
        LoanBalance = json['LoanBalance']
        Servicer = json['Servicer']
        SchoolName = json['SchoolName']
        StudentID = json['StudentID']
        Status = json['Status']
        cursor.execute(query, FirstName, LastName, GraduationDate, LoanBalance, Servicer, SchoolName, StudentID, Status)
        cursor.commit()
    return "success"