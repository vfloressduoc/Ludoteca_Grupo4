# context_processors.py

import requests

def valor_dolar(request):
    url = "https://mindicador.cl/api"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        dolar_value = data.get('dolar', {}).get('valor')
        dolar_formateado = f"${dolar_value:.2f}" if dolar_value is not None else "N/A"
    except requests.RequestException as e:
        print(f"Error: {e}")
        dolar_formateado = "Error"

    return {'valor_dolar_hoy': dolar_formateado}