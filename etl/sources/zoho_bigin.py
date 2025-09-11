import requests

def obtener_datos_zoho_bigin(token):
    base_url = "https://www.zohoapis.com/bigin/v1/"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    modulos = {
        "Tratos": "Deals",
        "Empresas": "Accounts",
        "Contactos": "Contacts"
    }
    resultados = {}
    for nombre, endpoint in modulos.items():
        url = f"{base_url}{endpoint}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resultados[nombre] = resp.json().get("data", [])
        else:
            resultados[nombre] = []
    return resultados