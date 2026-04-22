import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

async def fabricar_video(tema):
    print(f"🛠️ GENERANDO FORMATO WEB SEGURO: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # Limpiar todo rastro de videos viejos
    for f in ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]:
        if os.path.exists(f): os.remove(f)

    # 1. GUION RAPIDO
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"El misterio de {tema} es increible."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Dato curioso muy corto sobre {tema}. Maximo 15 palabras.")
        guion = res.text.strip()
    except: pass

    # 2. VOZ Y SUBS
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    submaker = edge_tts.SubMaker()
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary": submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    with open("static/subs.vtt", "w", encoding="utf-8") as f: f.write(submaker.generate_subs())

    # 3. IMAGEN IA LIGERA
    prompt_ia = f"cinematic%20{tema.replace(' ', '%20')}%20vertical"
    img_data = requests.get(f"https://image.pollinations.ai/prompt/{prompt_ia}?width=480&height=854&nologo=true").content
    with open("static/fondo.jpg", "wb") as f: f.write(img_data)

    # 4. MONTAJE WEB-FASTSTART (El secreto para que no se vea roto)
    # Bajamos la resolución a 480x854 para que cargue volando en el móvil
    estilo = "FontName=Arial,FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=50"
    
    # -movflags +faststart permite que el video empiece a sonar antes de descargarse entero
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
