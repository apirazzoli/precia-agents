import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.supabase_client import supabase

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def scrape_product(url):
    print(f"Scrapeando: {url}")
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error al acceder: {response.status_code}")
        return None

    # Buscar datos del producto en el HTML
    html = response.text
    
    # Extraer precio actual
    precio = None
    if '"price":' in html:
        try:
            start = html.find('"price":') + 8
            end = html.find(',', start)
            precio = int(float(html[start:end].strip()))
        except:
            pass

    # Extraer nombre
    nombre = None
    if '<title>' in html:
        try:
            start = html.find('<title>') + 7
            end = html.find('</title>')
            nombre = html[start:end].strip()
        except:
            pass

    if not precio or not nombre:
        print("No se pudieron extraer datos básicos")
        return None

    data = {
        "store": "falabella",
        "raw_name": nombre,
        "raw_price": precio,
        "raw_url": url,
        "processed": False
    }

    # Guardar en Supabase
    result = supabase.table("raw_scrapes").insert(data).execute()
    print(f"Guardado: {nombre} - ${precio}")
    return result

if __name__ == "__main__":
    url = input("Pega la URL del producto de Falabella: ")
    scrape_product(url)
