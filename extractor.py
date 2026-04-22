import os, random, json

TALLER = os.path.abspath("workspace")
os.makedirs(TALLER, exist_ok=True)

class PsychoEngine:
    def __init__(self, tema):
        self.tema = tema.lower().strip()

    def generate_with_keywords(self):  
        return [
            (f"El 99% de la gente entiende MAL el {self.tema}.", f"{self.tema} mystery cinematic"),
            ("Tu cerebro elige siempre el camino fácil.", "frustration mental dark aesthetic"),
            (f"La verdad es que el {self.tema} cambia tu mente.", "epic revelation nature landscape"),
            ("Actúa sin esperar a sentirte listo.", "action running motivation cinematic"),
            ("El cambio duele. La mediocridad te destruye.", "success achievement dark mindset")
        ]

def god_search(query, out):
    print(f"🔎 Descargando clip para: {query}")
    cmd = f'python -m yt_dlp -f "best[ext=mp4]" --match-filter "duration < 180" --no-check-certificate --quiet --no-warnings -o "{out}" "ytsearch1:{query}"'
    os.system(cmd)
    return os.path.exists(out)

if __name__ == "__main__":
    tema = input("🧠 Tema del vídeo: ").strip()
    
    engine = PsychoEngine(tema)
    guion_mapeado = engine.generate_with_keywords()
    
    paquete_datos = {"tema": tema, "escenas": []}

    print("🔪 Iniciando extracción en YouTube...")
    for i, (frase, busqueda) in enumerate(guion_mapeado):
        raw_video = os.path.join(TALLER, f"raw_{i}.mp4")
        if god_search(busqueda, raw_video):
            paquete_datos["escenas"].append({
                "id": i,
                "frase": frase,
                "keyword": busqueda,
                "archivo": f"raw_{i}.mp4"
            })

    # Guardamos el mapa de datos para que GitHub sepa qué hacer
    with open(os.path.join(TALLER, "paquete.json"), "w") as f:
        json.dump(paquete_datos, f, indent=4)

    print("🚀 Sincronizando con GitHub...")
    os.system(f'cd {TALLER} && git add . && git commit -m "Nuevos clips: {tema}" && git push origin main')
    print("✅ Extracción terminada. GitHub asume el control.")
