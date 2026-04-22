import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

async def fabricar_video(tema):
    print(f"🚀 MODO PRO INICIADO PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # --- 1. GEMINI BLINDADO (Sin censura y más creativo) ---
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"¿Sabías esto sobre {tema}? Es algo que te dejará con la boca abierta."
    
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
    print("✅ Subtítulos creados.")

    # --- 3. ARTE IA PREMIUM ---
    print("🖼️ Generando Arte...")
    prompt_ia = f"cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical"
    img_url = f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true"
    with open("static/fondo.jpg", "wb") as f:
        f.write(requests.get(img_url).content)

    # --- 4. MONTAJE CON TEXTO QUEMADO (Efecto Viral) ---
    print("🎥 Quemando subtítulos en el video...")
    # Estilo: Letra amarilla brillante, tamaño grande, borde negro muy grueso, centrada
    estilo = "FontName=Arial,FontSize=30,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=30"
    
    os.system(f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 -c:v libx264 -pix_fmt yuv420p -vf "scale=720:1280,subtitles=static/subs.vtt:force_style=\'{estilo}\'" -c:a copy -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"):
        print("🚀 ¡VÍDEO PRO TERMINADO!")
    else:
        print("❌ Error en el montaje final")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
