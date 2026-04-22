import os
import sys
import argparse
import requests
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tema', type=str, required=True)
    parser.add_argument('--id', type=str, required=True)
    args = parser.parse_args()

    api_key = os.getenv('PEXELS_API_KEY')
    print(f"🎬 Buscando vídeos para: {args.tema}")

    # Diccionario rápido de traducción para que Pexels siempre encuentre algo
    # Si no está en la lista, usará el tema original
    busqueda = args.tema
    if "miedo" in args.tema.lower(): busqueda = "horror"
    if "gato" in args.tema.lower(): busqueda = "cats"
    if "coche" in args.tema.lower(): busqueda = "cars"
    if "playa" in args.tema.lower(): busqueda = "beach"

    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/videos/search?query={busqueda}&per_page=3&orientation=portrait"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Cogemos el primer vídeo que encontremos
        video_url = data['videos'][0]['video_files'][0]['link']
        print(f"✅ Vídeo encontrado: {video_url}")
        
        # Lo descargamos de verdad
        v_data = requests.get(video_url).content
        with open("video_final.mp4", "wb") as f:
            f.write(v_data)
        
        print("🚀 Vídeo descargado y guardado correctamente.")

    except Exception as e:
        print(f"❌ Error: No se pudo obtener el vídeo. {str(e)}")
        # Creamos un pequeño archivo de error para no dejarlo en 0 bytes
        with open("video_final.mp4", "w") as f:
            f.write("Error: Pexels no encontró resultados.")

if __name__ == "__main__":
    main()
