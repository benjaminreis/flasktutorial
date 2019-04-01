import pyodbc

class Student:

   def __init__(self, jsonRow):
       self.id = jsonRow[0]
       self.FirstName = jsonRow[1]
       self.LastName = jsonRow[2]
       self.GraduationDate = jsonRow[3]
       self.LoanBalance = str(jsonRow[4])
       self.Servicer = jsonRow[5]
       self.SchoolName = jsonRow[6]
       self.StudentID = jsonRow[7]
       self.Status = jsonRow[8]
