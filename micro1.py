import pyodbc
import pandas as pd

#Intentar def 
#ConnectionSQLLocal JAV
server = 'localhost'
database = 'TestBia'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes')

cursor = cnxn.cursor()

csv_file_path = r'C:\Users\jcuel\Downloads\postcodesgeo.csv'
df = pd.read_csv(csv_file_path)
    

query = "INSERT INTO BiaTable (Lat, Lon) VALUES (?, ?);"
cursor.executemany(query, df[['lat', 'lon']].values.tolist())

cnxn.commit()
cursor.close()
cnxn.close()

print('Carga Success')