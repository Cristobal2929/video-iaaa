import os

with open('main.py', 'r') as f:
    code = f.read()

old_func = """def obtener_video_contextual(frase, duracion):
    if not PEXELS_API_KEY: return ColorClip(size=(720, 1280), color=(10, 10, 15), duration=duracion)
    palabras_filtro = ["el", "la", "un", "una", "de", "con", "en", "para", "por", "link", "perfil", "es", "son", "y", "que", "te", "tu", "se", "pero", "más", "los", "las", "a", "su"]
    keywords = [w for w in frase.lower().replace(".", "").replace(",", "").split() if w.isalpha() and w not in palabras_filtro]
    query = keywords[0] if keywords else "business"
    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
        r = requests.get(url, headers={"Authorization": PEXELS_API_KEY}).json()
        if not r.get("videos"):
            r = requests.get("https://api.pexels.com/videos/search?query=office&per_page=10&orientation=portrait", headers={"Authorization": PEXELS_API_KEY}).json()
        video_data = random.choice(r["videos"])
        link = video_data['video_files'][0]['link']
        temp_name = f"temp_{random.randint(0,99999)}.mp4"
        with open(temp_name, "wb") as f: f.write(requests.get(link).content)
        clip_original = VideoFileClip(temp_name)
        scale_factor = max(720/clip_original.w, 1280/clip_original.h)
        clip_scaled = clip_original.resize(scale_factor)
        final_clip = clip_scaled.crop(x_center=clip_scaled.w/2, y_center=clip_scaled.h/2, width=720, height=1280)
        if final_clip.duration < duracion:
            veces = int(duracion/final_clip.duration) + 1
            final_clip = concatenate_videoclips([final_clip] * veces, method="compose")
        return final_clip.subclip(0, duracion)
    except: return ColorClip(size=(720, 1280), color=(10, 10, 15), duration=duracion)"""

new_func = """def obtener_video_contextual(frase, duracion):
    if not PEXELS_API_KEY: return ColorClip(size=(720, 1280), color=(20, 20, 30), duration=duracion)
    
    # Extraer palabras clave reales
    limpiar = "".join([c for c in frase if c.isalnum() or c==" "])
    palabras = [w for w in limpiar.lower().split() if len(w) > 3]
    
    # Intentar varias búsquedas
    search_queries = palabras[:2] + ["business", "abstract", "nature", "technology"]
    
    for query in search_queries:
        try:
            print(f"🔍 Buscando video en Pexels para: {query}...")
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=20&orientation=portrait"
            r = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=10).json()
            
            if r.get("videos") and len(r["videos"]) > 0:
                video_data = random.choice(r["videos"])
                link = next(f['link'] for f in video_data['video_files'] if f['width'] >= 720)
                temp_name = f"temp_{random.randint(0,99999)}.mp4"
                
                with open(temp_name, "wb") as f: 
                    f.write(requests.get(link).content)
                
                clip = VideoFileClip(temp_name)
                # Ajuste de pantalla completa
                scale = max(720/clip.w, 1280/clip.h)
                clip = clip.resize(scale).crop(x_center=clip.resize(scale).w/2, y_center=clip.resize(scale).h/2, width=720, height=1280)
                
                if clip.duration < duracion:
                    clip = concatenate_videoclips([clip] * (int(duracion/clip.duration)+1)).subclip(0, duracion)
                else:
                    clip = clip.subclip(0, duracion)
                
                os.remove(temp_name) # Limpiar basura
                return clip
        except Exception as e:
            print(f"❌ Error buscando {query}: {e}")
            continue

    return ColorClip(size=(720, 1280), color=(30, 30, 40), duration=duracion)"""

# Reemplazo manual por si las sangrías fallan
if "def obtener_video_contextual" in code:
    # Esta es una forma bruta pero efectiva de asegurar el cambio
    start_marker = "def obtener_video_contextual(frase, duracion):"
    end_marker = "def generar_guion_ia(tema):"
    parts = code.split(start_marker)
    pre = parts[0]
    post = parts[1].split(end_marker)[1]
    final_code = pre + new_func + "\n\n" + end_marker + post
    with open('main.py', 'w') as f:
        f.write(final_code)
    print("✅ Motor de Pexels actualizado.")
else:
    print("❌ No se encontró la función original.")
