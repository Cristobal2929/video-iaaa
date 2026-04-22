import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

async def fabricar_video(tema):
    print(f"🚀 INICIANDO MODO PRO (LIMPIEZA TOTAL) PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # --- 0. LIMPIEZA DE CACHÉ LOCAL (Agresiva) ---
    # Borramos los archivos viejos antes de empezar la nueva generación
    files_to_clean = ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]
    for f in files_to_clean:
        if os.path.exists(f):
            os.remove(f)
            print(f"🗑️ Caché limpiado: {f}")

    # --- 1. GEMINI BLINDADO ---
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"Hablemos sobre {tema}. Es un tema fascinante."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Apagamos los filtros de seguridad molestos para que no falle
        res = model.generate_content(
            f"Escribe un dato curioso, impactante y muy corto sobre {tema}. Máximo 20 palabras. Directo al grano.",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        guion = res.text.strip()
        print("✅ Gemini 100% Operativo.")
    except Exception as e:
        print(f"⚠️ Aviso Gemini: {e}")

    # --- 2. VOZ Y SUBTÍTULOS MILIMÉTRICOS ---
    print("🔊 Creando voz y mapa de subtítulos...")
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    submaker = edge_tts.SubMaker()
    
    # Guardamos el audio y al mismo tiempo cazamos el tiempo exacto de cada palabra
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
    # Guardamos los subtítulos en un archivo .vtt
    with open("static/subs.vtt", "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())
    print("✅ Audio y subtítulos creados.")

    # --- 3. ARTE IA PREMIUM ---
    print("🖼️ Generando Arte...")
    # Mejoramos el prompt visual para asegurar un estilo cinematográfico épico
    # We use a static reference to the desired cinematic style created previously
    prompt_ia = f"cinematic%20epic%20deep%20space%20photography%208k%20vertical%20{tema.replace(' ', '%20')}"
    img_url = f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("static/fondo.jpg", "wb") as f:
            f.write(img_data)
        print("✅ Imagen generada.")
    except Exception as e:
        print(f"❌ Falló Pollinations: {e}")
        return

    # --- 4. MONTAJE CON TEXTO QUEMADO (Efecto Viral) ---
    print("🎥 Quemando subtítulos amarillos en el video final...")
    
    # Estilo: Letra amarilla brillante, tamaño grande, borde negro muy grueso, centrada
    # PrimaryColour: Blue channel is 00 (no blue), Green is FF (full green), Red is FF (full red) -> Yellow
    estilo = "FontName=Arial,FontSize=30,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=50"
    
    # FFmpeg command to loop the image, burn subtitles, scale correctly, and use dynamic bitrate
    ffmpeg_cmd = (
        f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 '
        f'-c:v libx264 -pix_fmt yuv420p -b:v 3M '
        f'-vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,subtitles=static/subs.vtt:force_style=\'{estilo}\'" '
        f'-c:a aac -b:a 128k -shortest static/video_final.mp4'
    )
    os.system(ffmpeg_cmd)
    
    if os.path.exists("static/video_final.mp4"):
        print("🚀 ¡VÍDEO PRO CON LIMPIEZA TERMINADO!")
    else:
        print("❌ Error crítico en el montaje final")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
