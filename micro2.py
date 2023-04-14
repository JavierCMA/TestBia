import pyodbc
import requests

#ConnectionSQLLocal JAV

server = 'localhost'
database = 'TestBia'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes')


cursor = cnxn.cursor()


query = "SELECT id, lat, lon FROM BiaTable;"
cursor.execute(query)
rows = cursor.fetchall()

# API CALL, iterar filas csv micro 1. Revisar!
for row in rows:
    
    id = row[0]
    lat = row[1]
    lon = row[2]
    
    
    url = f'https://api.postcodes.io/postcodes?lon={lon}&lat={lat}'
    response = requests.get(url)
    
    
    if response.status_code == 200:
        data = response.json()
        if data['result']:
            try:
                postcode = data['result'][0]['postcode']
            except (IndexError, KeyError):
                postcode = None
            
            try:
                country = data['result'][0]['country']
            except (IndexError, KeyError):
                country = None
            
            try:
                quality = data['result'][0]['quality']
            except (IndexError, KeyError):
                quality = None

            try:
                eastings = data['result'][0]['eastings']
            except (IndexError, KeyError):
                eastings = None

            try:
                northings = data['result'][0]['northings']
            except (IndexError, KeyError):
                northings = None

            try:
                nhs_ha = data['result'][0]['nhs_ha']
            except (IndexError, KeyError):
                nhs_ha = None

            try:
                european_electoral_region = data['result'][0]['european_electoral_region']
            except (IndexError, KeyError):
                european_electoral_region = None

            try:
                primary_care_trust = data['result'][0]['primary_care_trust']
            except (IndexError, KeyError):
                primary_care_trust = None
        
        #Revisar! Carga muy lenta posible #temptable or API exceed call request 12000 rows
        query = "UPDATE BiaTable SET postcode = ?, country = ?, quality = ?,eastings = ?,northings = ?,nhs_ha = ?,european_electoral_region = ?,primary_care_trust = ? WHERE id = ?;"
        cursor.execute(query, postcode, country,quality,eastings,northings,nhs_ha,european_electoral_region,primary_care_trust, id)
        cnxn.commit()


cursor.close()
cnxn.close()


print('Update Sucess')