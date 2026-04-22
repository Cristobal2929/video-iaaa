import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

async def fabricar_video(tema):
    print(f"🚀 INICIANDO MODO LIMPIEZA TOTAL PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # --- 0. 🧹 LIMPIEZA DE CACHÉ ZOMBI (Nuevo) 🧹 ---
    # Borramos todos los archivos viejos antes de empezar
    archivos_a_borrar = [
        "static/voz.mp3", 
        "static/subs.vtt", 
        "static/fondo.jpg", 
        "static/video_final.mp4"
    ]
    for archivo in archivos_a_borrar:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"🗑️ Borrado archivo viejo: {archivo}")
    print("✅ Caché local limpio.")

    # --- 1. GEMINI BLINDADO ---
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"Hablemos sobre {tema}. Es un tema fascinante."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Filtros relajados para datos curiosos
        res = model.generate_content(
            f"Escribe un dato curioso, impactante y corto sobre {tema}. Máximo 20 palabras. Directo al grano.",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        guion = res.text.strip()
        print(f"📝 Guion Gemini: {guion}")
    except Exception as e:
        print(f"⚠️ Aviso Gemini: {e}")

    # --- 2. VOZ Y SUBTÍTULOS MILIMÉTRICOS ---
    print("🔊 Creando voz...")
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    submaker = edge_tts.SubMaker()
    
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
    with open("static/subs.vtt", "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())
    print("✅ Audio y subs creados.")

    # --- 3. ARTE IA PREMIUM ---
    print("🖼️ Generando Arte...")
    # Mejoramos el prompt para agujeros negros
    estilo_visual = "cinematic%20epic%20space%20photography%208k%20vertical"
    prompt_ia = f"{estilo_visual}%20{tema.replace(' ', '%20')}"
    img_url = f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("static/fondo.jpg", "wb") as f:
            f.write(img_data)
        print("✅ Imagen generada.")
    except:
        print("❌ Error generando imagen.")
        return

    # --- 4. MONTAJE CON TEXTO QUEMADO ---
    print("🎥 Montando video final con subtítulos virales...")
    # Estilo: Letra amarilla grande, borde negro grueso, centrada abajo
    estilo = "FontName=Arial,FontSize=30,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=50"
    
    # Forzamos reescalado y formato compatible
    comando_ffmpeg = (
        f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 '
        f'-c:v libx264 -pix_fmt yuv420p -b:v 2M '
        f'-vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,subtitles=static/subs.vtt:force_style=\'{estilo}\'" '
        f'-c:a aac -b:a 128k -shortest static/video_final.mp4'
    )
    os.system(comando_ffmpeg)
    
    if os.path.exists("static/video_final.mp4"):
        print("🚀 ¡VÍDEO PRO TERMINADO!")
    else:
        print("❌ Error crítico en el montaje final")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
