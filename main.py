import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Database import *

#setting the page

st.set_page_config(layout="wide")

# setting title

st.title("Patient Visit Tracker Dashboard")

#loading data from db to var and creating dataframe using pandas 

allVisits = AllVisitDetails() #load from the database to all visits var
VisitsDataframe= pd.DataFrame(allVisits, columns=["Visit ID", "Patient", "Doctor", "Date", "Diagnosis", "Cost"])


# sidebar creation  and filtering
st.sidebar.header(" Apply Filters")
doctors =VisitsDataframe["Doctor"].unique().tolist()#to list is a python list 
diagnosis = VisitsDataframe["Diagnosis"].unique().tolist()

selectedDoctor = st.sidebar.selectbox("Select Doctor", ["All"] + doctors)
selectedDiagnosis = st.sidebar.selectbox("Select Diagnosis", ["All"] + diagnosis)
# copying the actual dataframe to another var for not being messy
filteredDataFrame = VisitsDataframe.copy()
# applying filters on dataframe with sidebar 
if selectedDoctor != "All":
   filteredDataFrame = filteredDataFrame[filteredDataFrame["Doctor"] == selectedDoctor]
if selectedDiagnosis != "All":
    filteredDataFrame= filteredDataFrame[filteredDataFrame["Diagnosis"] == selectedDiagnosis]


#2nd feature of project  visits table
st.subheader("Visit Records")
st.dataframe(filteredDataFrame, use_container_width=True) #takes the sidebar input and filtred data is shown in the table

#metrics  and common disease and average cost
st.subheader("Top Diagnosis & Avg. Cost")
column1,column2=st.columns(2) # divides the page into two cols

with column1:
  DiagnoisedDisease=CommonDiagnosis()#commkon disease of all the data
  st.metric(label="Most Common Diagnosied Disease",value=DiagnoisedDisease[0][0])
with column2:
  AvgTreamentCostvist=AverageCost()# avg cost is stord in var as one value
  st.metric(label="Average cost per Visit (₹)",value=AvgTreamentCostvist[0][0])

#3rd segment of project line cahrt of monthly visits

st.subheader("Monthly Visits")
 
monthsData=MonthlyVisits()# monthsdata stored data from the query of all grouped months  it returnds a tuple of"2023-3"

monthlyData_DataFrame=pd.DataFrame(monthsData,columns=["Month","count of visits"])

#ploting the map
fig,ax=plt.subplots(figsize=(5, 3))#figure holds the complete dta and and you can draw on axis
ax.plot(monthlyData_DataFrame["Month"],monthlyData_DataFrame["count of visits"],marker="o",linestyle="-")
ax.set_xlabel("Month")
ax.set_ylabel("Number of Visits")
plt.xticks(rotation=45,ha="right")
plt.tight_layout()
plt.grid(True,alpha=0.3)
st.pyplot(fig)


#4th segment of project patient details as per  patient id

st.subheader("Patient History")
patientId=st.text_input("Enter Patient ID: ")# takes patient i as input stored in patientid var

if patientId: #if patientid is there in records
  try:
     PatientHistory=VisitsByPatients(int(patientId)) # takes the patient details from sql query and convert it into integer
     if PatientHistory:# if patient history found
       historyDataFrame=pd.DataFrame(PatientHistory,columns=["Date", "Doctor", "Diagnosis", "Cost"])
       st.success(f"History of the patient for the ID {patientId}")
       st.dataframe(historyDataFrame,use_container_width=True)
     else:
       st.info("No visits found of patient")
  except ValueError:
    st.error("please enter a Valid numeric id")


# Doctor view

st.subheader("Doctors History")
doctorId=st.text_input("Enter doctor ID:")
if doctorId:
  try:
    historyDoctor=VisitsByDoctor(int(doctorId))
    if historyDoctor:
      doctorDataframe=pd.DataFrame(historyDoctor,columns=["Date", "Patient", "Diagnosis", "Cost"])
      st.success(f"History of the Doctor for the ID {doctorId}")
      st.dataframe(doctorDataframe,use_container_width=True)
    else:
        st.info("No visits found of doctor")
  except ValueError:
    st.error("please enter a Valid numeric id")

# diagnosis view

st.subheader("Diagnosis History")
DiagnosisiView=st.selectbox("chooose diagnosis to view visits",["None"]+diagnosis)
if DiagnosisiView!="None":
  diagnosisData=NoOfVisitsDiagnosis(DiagnosisiView)
  if diagnosisData:
    diagnosisDataFrame=pd.DataFrame(diagnosisData,columns=["Visit ID", "Patient ID", "Doctor ID", "Date", "Diagnosis", "Cost"])
    st.dataframe(diagnosisDataFrame,use_container_width=True)
  else:    
    st.info("No visits found of diagnosis")



       
   
  



