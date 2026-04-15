import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.scraper_falabella import scrape_product
from agents.normalizer import procesar_pendientes

def correr_pipeline(urls):
    print("="*50)
    print("PRECIA - Pipeline iniciado")
    print("="*50)

    # Paso 1: Scrapear todas las URLs
    print(f"\nPaso 1: Scrapeando {len(urls)} productos...")
    for url in urls:
        scrape_product(url)

    # Paso 2: Normalizar con Claude
    print("\nPaso 2: Normalizando con Claude...")
    procesar_pendientes()

    print("\n" + "="*50)
    print("Pipeline completado")
    print("="*50)

if __name__ == "__main__":
    # Aqui van las URLs que quieres scrapear
    urls = [
        "https://www.falabella.com/falabella-cl/product/881951127/Smart-TV-Samsung-55-QLED-4K",
    ]
    
    correr_pipeline(urls)
