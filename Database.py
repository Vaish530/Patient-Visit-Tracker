import sqlite3
import pandas as pd
conn=sqlite3.connect("Hospital.db")
c=conn.cursor()
print("db created")
def create_tables():
  conn=sqlite3.connect("Hospital.db")
  c=conn.cursor()
  c.execute('DROP TABLE IF EXISTS Patients')
  c.execute('DROP TABLE IF EXISTS Doctors')
  c.execute('DROP TABLE IF EXISTS Visits')
  c.execute('''
        CREATE TABLE Patients (
            p_id INTEGER PRIMARY KEY AUTOINCREMENT,
            p_name TEXT,
            p_age INTEGER
        )
    ''') 
  c.execute('''
        CREATE TABLE Doctors (
            d_id INTEGER PRIMARY KEY AUTOINCREMENT,
            d_name TEXT,
            specialization TEXT
        )
    ''')
  c.execute('''
        CREATE TABLE  Visits (
            v_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            date TEXT,
            diagnosis TEXT,
            cost REAL,
            FOREIGN KEY (patient_id) REFERENCES patients(p_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(d_id)
        )
    ''')
  print("tables are created")
  conn.commit()
  conn.close()
def load_dataset():
   conn=sqlite3.connect("Hospital.db")
   c=conn.cursor()
   pat=pd.read_csv("C:/Users/91628/OneDrive/Documents/_My_projects _Vaishnavi/PatientVisitTracker/dataset/patients_updated.csv")
   doc=pd.read_csv("C:/Users/91628/OneDrive/Documents/_My_projects _Vaishnavi/PatientVisitTracker/dataset/doctors_updated.csv")
   vis=pd.read_csv("C:/Users/91628/OneDrive/Documents/_My_projects _Vaishnavi/PatientVisitTracker/dataset/visits_updated.csv")
   pat.to_sql("Patients",conn,if_exists="replace",index=False)
   doc.to_sql("Doctors",conn,if_exists="replace",index=False)
   vis.to_sql("Visits",conn,if_exists="replace",index=False)
   print("loading dataset is done")
   conn.commit()
   conn.close()
def executeQuery(query,params=()):
   conn=sqlite3.connect("Hospital.db")
   c=conn.cursor()
   c.execute(query,params)
   res=c.fetchall()
   conn.close()
   return res
def NoOfVisitsDoctor(doctor_id):
   query="SELECT * FROM Visits WHERE doctor_id=?;"
   return executeQuery(query,(doctor_id,))
def NoOfVisitsDiagnosis(diagnosis):
   query="SELECT * FROM Visits WHERE diagnosis=?;"
   return executeQuery(query,(diagnosis,))
def AllVisitDetails():
   query=""" SELECT v.v_id,p.p_name,d.d_name,v.date,v.diagnosis,v.cost
   FROM Visits v
   JOIN Patients p ON v.patient_id=p.p_id
   JOIN Doctors d ON  v.doctor_id=d.d_id
   ORDER BY v.date DESC;"""
   return executeQuery(query)
def VisitsByPatients(patient_id):
   query="""SELECT v.date,d.d_name AS doctor,v.diagnosis,v.cost
    FROM Visits  v
    JOIN Doctors d ON v.doctor_id=d.d_id
    WHERE v.patient_id= ?
    ORDER BY v.date;"""
   return executeQuery(query,(patient_id,))
def VisitsByDoctor(doctor_id):
   query=""" SELECT v.date,p.p_name AS patient ,v.diagnosis,v.cost
   FROM Visits v
   JOIN Patients p ON v.patient_id=p.p_id
   WHERE v.doctor_id=?
   ORDER BY v.date;"""
   return executeQuery(query,(doctor_id,))
def CommonDiagnosis():
   query=""" SELECT diagnosis,COUNT(*) AS frequency
   FROM Visits
   GROUP BY diagnosis
   ORDER BY frequency DESC
   LIMIT 1;"""
   return executeQuery(query)
def AverageCost():
   query="SELECT ROUND(AVG(cost),2) as avgTreatment FROM  Visits;"
   return executeQuery(query)
def MonthlyVisits():
   query=""" SELECT strftime('%Y-%m', date) AS month,COUNT(*) AS count
   FROM Visits
   GROUP BY month
   ORDER BY month; """
   return executeQuery(query)

    

 
    
  
