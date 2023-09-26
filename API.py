from urllib import reponse
import requests

api_key = 'marioyeahs'

base_url = 'http://api.geonames.org/countryCodeJSON'
params = {
    'lat': '47.0',
    'lng': '10.2',
    'username': api_key
}

response = requests.get(base_url,params=params)

if reponse.status_code == 200:
    data = reponse.json()
    country_code = data['countryCode']
    print(f"El código de tu país para la ubicación proporcionada es: {country_code}")
else:
    print(f"Error en la solicitud HTTP. Código de estado: {reponse.status_code}")