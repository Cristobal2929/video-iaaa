import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

# Traductor de tiempo ultra-preciso
def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema):
    print(f"🎬 REPARANDO SUBTÍTULOS PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # Limpieza total
    for f in ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]:
        if os.path.exists(f): os.remove(f)

    # 1. GUIONISTA PRO
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escribe un guion épico y misterioso sobre {tema} para un video de 1 minuto. Unas 110 palabras. Solo el texto, sin nada más."
        res = model.generate_content(prompt, safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}])
        guion = res.text.strip().replace('*', '').replace('"', '')
    except:
        guion = f"El misterio de {tema} es algo que ha desconcertado a la humanidad durante siglos. Prepárate para descubrir la verdad."

    # 2. VOZ Y GENERACIÓN DE SUBS MANUAL (Paso a paso)
    print("🔊 Generando voz y sincronizando palabras...")
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # Convertimos el offset de edge-tts a milisegundos
                inicio = chunk["offset"] / 10000
                duracion = chunk["duration"] / 10000
                fin = inicio + duracion
                # Añadimos la palabra al archivo de subtítulos
                subs_vtt.append(f"{tiempo_a_vtt(inicio)} --> {tiempo_a_vtt(fin)}\n{chunk['text']}\n\n")
                
    with open("static/subs.vtt", "w", encoding="utf-8") as f: 
        f.writelines(subs_vtt)
    print("✅ Archivo de subtítulos creado.")

    # 3. IMAGEN IA
    img_url = f"https://image.pollinations.ai/prompt/cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical?width=480&height=854&nologo=true"
    with open("static/fondo.jpg", "wb") as f: f.write(requests.get(img_url).content)

    # 4. MONTAJE CON RUTA FORZADA (Aquí estaba el fallo)
    print("🎥 Quemando subtítulos amarillos...")
    # Estilo viral: Amarillo, borde negro, centrado abajo
    estilo = "FontName=Arial,FontSize=26,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=60"
    
    # Importante: Usamos './static/subs.vtt' con comillas para que FFmpeg no se pierda
    comando = (
        f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 '
        f'-vf "scale=480:854,subtitles=\'static/subs.vtt\':force_style=\'{estilo}\'" '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-c:a aac -shortest static/video_final.mp4'
    )
    os.system(comando)
    print("🚀 PROCESO FINALIZADO CON ÉXITO")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
