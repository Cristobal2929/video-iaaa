import argparse, os, asyncio, google.generativeai as genai, edge_tts, requests

async def fabricar_video(tema):
    print(f"🎨 Iniciando Arte IA para: {tema}")
    os.makedirs("static", exist_ok=True)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 1. GUION
    guion = f"El misterio de {tema} es algo que te dejara sin palabras."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Dato curioso muy corto sobre {tema}. Solo texto.")
        guion = res.text.strip()
    except: print("⚠️ IA falló, usando guion de reserva.")

    # 2. VOZ
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")

    # 3. IMAGEN IA
    print("🖼️ Generando Imagen Única...")
    prompt_ia = f"cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical"
    img_url = f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true"
    
    img_data = requests.get(img_url).content
    with open("static/fondo.jpg", "wb") as f:
        f.write(img_data)

    # 4. MONTAJE (Aumentamos un poco el tiempo para que FFmpeg respire)
    print("🎥 Montando video final...")
    os.system('ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=720:1280" -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"):
        # Verificamos el tamaño para estar seguros
        size = os.path.getsize("static/video_final.mp4")
        print(f"✅ ¡VÍDEO CREADO! Tamaño: {size} bytes")
    else:
        print("❌ EL VÍDEO NO SE CREÓ")
        exit(1) # Forzamos error si no hay video

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
