import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

async def fabricar_video(tema):
    print(f"🛠️ REPARANDO VIDEO PARA: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # Limpieza previa
    for f in ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]:
        if os.path.exists(f): os.remove(f)

    # 1. GEMINI BLINDADO
    api_key = os.environ.get("GEMINI_API_KEY")
    guion = f"El misterio de {tema} es algo que te dejara sin palabras."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Dato curioso impactante y corto sobre {tema}. Solo texto.", safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}])
        guion = res.text.strip()
    except: print("⚠️ Usando guion de reserva.")

    # 2. VOZ Y SUBTÍTULOS
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    submaker = edge_tts.SubMaker()
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary": submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    with open("static/subs.vtt", "w", encoding="utf-8") as f: f.write(submaker.generate_subs())

    # 3. IMAGEN IA
    prompt_ia = f"cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical"
    img_data = requests.get(f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true").content
    with open("static/fondo.jpg", "wb") as f: f.write(img_data)

    # 4. MONTAJE ULTRA-COMPATIBLE (Perfil Baseline + Tune Stillimage)
    print("🎥 Montando en formato universal...")
    estilo = "FontName=Arial,FontSize=28,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=60"
    
    # Comando FFmpeg optimizado para móviles antiguos y nuevos
    os.system(f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p -vf "scale=720:1280,subtitles=static/subs.vtt:force_style=\'{estilo}\'" -c:a aac -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"): print("✅ REPARACIÓN EXITOSA")
    else: exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
