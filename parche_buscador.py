import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

marcador_inicio = "def obtener_imagenes_pexels_web(tema):"
marcador_fin = "app = FastAPI()"

if marcador_inicio in codigo and marcador_fin in codigo:
    parte_arriba = codigo.split(marcador_inicio)[0]
    parte_abajo = codigo.split(marcador_fin)[1]
    
    nueva_funcion = """def obtener_imagenes_pexels_web(tema):
    import requests, os
    key = os.getenv("PEXELS_API_KEY", "").strip()
    default_imgs = [
        "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg",
        "https://images.pexels.com/photos/3182773/pexels-photo-3182773.jpeg"
    ]
    if not key: return default_imgs
    try:
        # Filtramos palabras de relleno para sacar la esencia
        basura = ["crea", "haz", "una", "un", "el", "la", "los", "las", "landing", "page", "pagina", "web", "para", "de", "del", "sobre", "quiero", "sitio", "mi", "tu"]
        limpio = "".join([c for c in tema if c.isalnum() or c==" "])
        palabras = [w for w in limpio.lower().split() if w not in basura and len(w) > 2]
        
        # Cogemos las 2 palabras más importantes (ej. "restaurante mexicano")
        query = " ".join(palabras[:2]) if palabras else "business"
        
        # Obligamos a Pexels a buscar EN ESPAÑOL
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=10&locale=es-ES"
        r = requests.get(url, headers={"Authorization": key}, timeout=5).json()
        
        if "photos" in r and len(r["photos"]) > 0:
            return [p["src"]["large"] for p in r["photos"]]
    except Exception as e: 
        print("Error Pexels Web:", e)
        pass
    return default_imgs

app = FastAPI()"""

    codigo_final = parte_arriba + nueva_funcion + parte_abajo
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(codigo_final)
    print("✅ Buscador Inteligente en Español activado.")
else:
    print("❌ Error: No encontré la función antigua.")
