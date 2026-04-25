import os, re

try:
    with open('api/main.py', 'r', encoding='utf-8') as f:
        codigo = f.read()

    # 1. Función inyectable para sacar fotos de Pexels
    nueva_funcion = """
def obtener_imagenes_pexels_web(tema):
    import requests, os
    key = os.getenv("PEXELS_API_KEY", "").strip()
    default_imgs = [
        "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg",
        "https://images.pexels.com/photos/3182773/pexels-photo-3182773.jpeg",
        "https://images.pexels.com/photos/1181467/pexels-photo-1181467.jpeg"
    ]
    if not key: return default_imgs
    try:
        q = "".join([c for c in tema if c.isalnum() or c==" "]).split()
        query = q[0] if q else "technology"
        r = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=5", headers={"Authorization": key}, timeout=5).json()
        if "photos" in r and r["photos"]:
            return [p["src"]["large"] for p in r["photos"]]
    except: pass
    return default_imgs
"""
    
    # 2. Inyectamos la función si no existe
    if "def obtener_imagenes_pexels_web" not in codigo:
        partes = codigo.split("\n\n", 1)
        codigo = partes[0] + "\n" + nueva_funcion + "\n\n" + partes[1]

    # 3. Reescribimos el archivo temporalmente para que lo revises
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(codigo)
        
    print("✅ Motor de imágenes de Pexels inyectado en la API.")
    print("⚠️  ATENCIÓN: Como no veo tu código, no puedo inyectar el Prompt seguro.")

except Exception as e:
    print(f"❌ Error al parchear: {e}")
