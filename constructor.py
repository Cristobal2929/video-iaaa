import os, requests, zipfile, json

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()

def buscar_fotos(query):
    if not PEXELS_API_KEY: return []
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=3"
    r = requests.get(url, headers={"Authorization": PEXELS_API_KEY}).json()
    return [img['src']['large'] for img in r.get('photos', [])]

def generar_landing():
    descripcion = os.getenv("DESCRIPCION_WEB", "Negocio Digital")
    print(f"🚀 Iniciando construcción de: {descripcion}")
    
    # 1. Groq diseña la estructura
    prompt = f"""
    Eres un Senior Web Designer. Crea una Landing Page profesional y moderna sobre: {descripcion}.
    Usa HTML5 y Tailwind CSS.
    IMPORTANTE: Deja espacios para 3 imágenes usando etiquetas <img> con el id 'foto1', 'foto2' y 'foto3'.
    Incluye secciones de: Hero, Beneficios, Testimonios y un Call to Action brillante.
    Devuelve ÚNICAMENTE el código HTML completo, sin explicaciones.
    """
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": prompt}]
    }
    
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    html_raw = r.json()['choices'][0]['message']['content']

    # 2. Buscamos fotos reales para el tema
    fotos = buscar_fotos(descripcion)
    for i, url in enumerate(fotos):
        html_raw = html_raw.replace(f'id="foto1"' if i==0 else f'id="foto{i+1}"', f'src="{url}"')

    # 3. Guardamos los archivos
    os.makedirs("docs/webs", exist_ok=True)
    nombre_archivo = f"web_{int(time.time())}.html"
    path_html = f"docs/webs/{nombre_archivo}"
    
    with open(path_html, "w") as f:
        f.write(html_raw)
        
    # 4. Creamos el ZIP descargable
    zip_path = f"docs/webs/proyecto_{int(time.time())}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(path_html, "index.html")

    print(f"✅ Web construida: {nombre_archivo}")

if __name__ == "__main__":
    import time
    generar_landing()
