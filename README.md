# Patient-Visit-Tracker
A Streamlit-powered dashboard to track patient visits, diagnoses, and treatment costs in a hospital using an SQLite database. Features include filtering by doctor/diagnosis, visit history and average cost tools being used includesPython, Streamlit, SQLite, Pandas, Matplotlib


Filter visits by Doctor and Diagnosis
Tabular display of all visit records
 View most common diagnosis and average treatment cost
 monthly visit trend chart
Detailed patient visit history lookup
(Optional) Explore visits per doctor or diagnosis

technologies used:
frontend :Streamlit
backend : SQLite3
data handling :pandas
data visualization :malplotlib
DB viewer :SQLite Studio

setup:
- create a virual envirionment in python 
-go the venv folder
-create dataset folder for csv files storing
-create Database.py for all connection,creating tables and queries
-create init_db.py for calling those functions created in Database.py
-excute as python Database.py and init_db.py
-after all succesfull excution  the database is created in folder
-you  can view the data in SQLite studio which is open source  resource for viewing the data of 
 csv along with the datatypes used.
-create main.py file whre your frontend code will go
-run the whole app as "streamlit run main.py"
-the app runs in localhost of ypur browser

 
 
