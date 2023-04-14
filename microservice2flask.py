import pyodbc
import requests
from flask import Flask, request, jsonify

server = 'localhost'
database = 'TestBia'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes')


app = Flask(__name__)

@app.route('/postcode')
def get_postcode():
   
    lat = request.args.get('lat')
    lon = request.args.get('lon')

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
        
        
        return jsonify({'postcode': postcode, 'country': country, 'quality': quality, 'eastings': eastings, 'northings': northings, 'nhs_ha': nhs_ha, 'european_electoral_region': european_electoral_region, 'primary_care_trust': primary_care_trust})
    
    
    else:
        return jsonify({'error': 'Error en la solicitud'})


if __name__ == '__main__':
    app.run(debug=True)