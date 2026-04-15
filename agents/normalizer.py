import anthropic
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.supabase_client import supabase

client = anthropic.Anthropic()

def normalizar_producto(raw_scrape):
    print(f"Normalizando: {raw_scrape['raw_name']}")

    prompt = f"""
    Eres un experto en productos de retail chileno.
    
    Analiza este producto scrapeado de {raw_scrape['store']} y extrae la información limpia.
    
    Producto raw: {raw_scrape['raw_name']}
    Precio: {raw_scrape['raw_price']}
    URL: {raw_scrape['raw_url']}
    
    Responde SOLO con un JSON con esta estructura exacta, sin texto adicional:
    {{
        "name": "nombre limpio del producto",
        "brand": "marca",
        "category": "categoría general",
        "slug": "nombre-en-minusculas-con-guiones"
    }}
    """

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    respuesta = message.content[0].text

    try:
        producto = json.loads(respuesta)

        # Guardar en tabla products
        result = supabase.table("products").insert(producto).execute()
        product_id = result.data[0]["id"]

        # Marcar raw_scrape como procesado
        supabase.table("raw_scrapes").update(
            {"processed": True}
        ).eq("id", raw_scrape["id"]).execute()

        # Guardar precio en historial
        supabase.table("price_history").insert({
            "product_id": product_id,
            "store": raw_scrape["store"],
            "price": raw_scrape["raw_price"],
            "url": raw_scrape["raw_url"]
        }).execute()

        print(f"Listo: {producto['name']} guardado en products y price_history")
        return product_id

    except Exception as e:
        print(f"Error procesando: {e}")
        return None

def procesar_pendientes():
    # Busca todos los raw_scrapes que no han sido procesados
    pendientes = supabase.table("raw_scrapes").select("*").eq(
        "processed", False
    ).execute()

    print(f"{len(pendientes.data)} productos pendientes de normalizar")

    for scrape in pendientes.data:
        normalizar_producto(scrape)

if __name__ == "__main__":
    procesar_pendientes()
