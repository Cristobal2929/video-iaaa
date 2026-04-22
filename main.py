import argparse, os, asyncio, google.generativeai as genai, edge_tts, requests

async def fabricar_video(tema):
    print(f"🎬 INICIO: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # 1. GUION
    guion = f"El tema de hoy es {tema}. Es realmente impresionante."
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Dato curioso muy corto sobre {tema}. Solo texto.")
        guion = res.text.strip()
        print("✅ Guion OK")
    except: print("⚠️ Guion reserva")

    # 2. VOZ
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")
    print("✅ Voz OK")

    # 3. IMAGEN IA
    print("🖼️ Generando Imagen...")
    prompt_ia = f"cinematic%20{tema.replace(' ', '%20')}%208k%20vertical"
    img_url = f"https://image.pollinations.ai/prompt/{prompt_ia}?width=720&height=1280&nologo=true"
    with open("static/fondo.jpg", "wb") as f:
        f.write(requests.get(img_url).content)
    print("✅ Imagen OK")

    # 4. MONTAJE (FFmpeg con formato universal)
    print("🎥 Montando...")
    # Forzamos el archivo video_final.mp4
    os.system('ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=720:1280" -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"):
        print(f"🚀 EXITO TOTAL: Archivo creado ({os.path.getsize('static/video_final.mp4')} bytes)")
    else:
        print("❌ ERROR: No se creo el video")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
