import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

# Nuestro propio traductor de tiempo (indestructible)
def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema):
    print(f"🛠️ GENERANDO VIDEO TURBO PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # Limpieza
    for f in ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]:
        if os.path.exists(f): os.remove(f)

    # 1. GUION GEMINI
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"El misterio de {tema} es algo asombroso."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Dato curioso muy corto sobre {tema}. Maximo 15 palabras.")
        guion = res.text.strip()
    except: pass

    # 2. VOZ Y SUBTÍTULOS (MÉTODO PROPIO SIN ERRORES)
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # Convertimos las medidas a milisegundos y creamos los subtítulos a mano
                inicio_ms = chunk["offset"] / 10000
                fin_ms = (chunk["offset"] + chunk["duration"]) / 10000
                subs_vtt.append(f"{tiempo_a_vtt(inicio_ms)} --> {tiempo_a_vtt(fin_ms)}\n{chunk['text']}\n\n")
                
    with open("static/subs.vtt", "w", encoding="utf-8") as f: 
        f.writelines(subs_vtt)

    # 3. IMAGEN IA LIGERA
    prompt_ia = f"cinematic%20{tema.replace(' ', '%20')}%20vertical"
    img_data = requests.get(f"https://image.pollinations.ai/prompt/{prompt_ia}?width=480&height=854&nologo=true").content
    with open("static/fondo.jpg", "wb") as f: f.write(img_data)

    # 4. MONTAJE WEB-FASTSTART
    estilo = "FontName=Arial,FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=50"
    comando = (
        f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-vf "scale=480:854,subtitles=static/subs.vtt:force_style=\'{estilo}\'" '
        f'-c:a aac -shortest static/video_final.mp4'
    )
    os.system(comando)
    print("✅ Video listo para la web")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
