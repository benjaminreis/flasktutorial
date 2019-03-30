import pyodbc

class Student:

   def __init__(self, jsonRow):
       print(jsonRow[0])
       print("hey yo!")
       self.id = jsonRow[0]
       self.FirstName = jsonRow[1]
       self.LastName = jsonRow[2]
       self.GraduationDate = jsonRow[3]
       self.LoanBalance = jsonRow[4]
       self.Servicer = jsonRow[5]
       self.StudentID = jsonRow[6]
       self.Status = jsonRow[7]
