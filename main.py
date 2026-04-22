import os, argparse, asyncio, google.generativeai as genai, yt_dlp, edge_tts

async def generar_todo(tema):
    print(f"--- INICIO DEPURACIÓN ---")
    if not os.path.exists("static"): 
        os.makedirs("static")
        print("📁 Carpeta static creada.")
    
    # Cerebro
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content(f"Dato corto sobre {tema}")
    guion = res.text.strip()
    print(f"📝 Guion listo: {guion[:20]}...")

    # Voz
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")
    print("🔊 Audio guardado en static/voz.mp3")

    # Fondo (Simulado rápido para asegurar que el archivo existe)
    print("🎬 Creando archivo de video...")
    comando_emergencia = 'ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=5 -vf "drawtext=text=\'PROCESANDO...\':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2" -c:v libx264 static/video_final.mp4'
    os.system(comando_emergencia)
    
    if os.path.exists("static/video_final.mp4"):
        size = os.path.getsize("static/video_final.mp4")
        print(f"✅ VIDEO CREADO: static/video_final.mp4 ({size} bytes)")
    else:
        print("❌ ERROR: El video no se creó.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(generar_todo(args.tema))
