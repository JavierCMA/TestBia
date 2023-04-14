from flask import Flask, request, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)


server = 'localhost'
database = 'TestBia'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes')

cursor = cnxn.cursor()

@app.route('/cargar_csv', methods=['POST'])
def cargar_csv():
    try:
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
                
        query = "INSERT INTO BiaTable (Lat, Lon) VALUES (?, ?);"
        cursor.executemany(query, df[['lat', 'lon']].values.tolist())
        
        cnxn.commit()

        return jsonify({'status': 'success', 'message': 'Carga Success'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

if __name__ == '__main__':
    app.run()