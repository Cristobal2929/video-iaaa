import argparse, os, asyncio, google.generativeai as genai, yt_dlp, edge_tts

async def fabricar_video(tema):
    print(f"🎬 Iniciando motor para: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # 1. Comprobar Llave
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: No se encuentra la GEMINI_API_KEY en los Secrets de GitHub.")
        return

    # 2. Guion
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Escribe un dato curioso y muy corto sobre {tema}. Solo el dato.")
        guion = res.text.strip()
        print(f"📝 Guion generado: {guion[:30]}...")
    except Exception as e:
        print(f"❌ ERROR en Gemini: {e}")
        return

    # 3. Voz
    print("🔊 Generando voz...")
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")

    # 4. Fondo
    print("📥 Descargando fondo...")
    ydl_opts = {'format': 'best[ext=mp4]', 'default_search': 'ytsearch1:', 'outtmpl': 'bg.mp4', 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download(["minecraft parkour no copyright"])
    except Exception as e:
        print(f"❌ ERROR en descarga: {e}")
        return

    # 5. Montaje
    print("🎥 Montando video final...")
    os.system('ffmpeg -y -i bg.mp4 -i static/voz.mp3 -map 0:v -map 1:a -c:v copy -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"):
        print("✅ ¡VÍDEO TERMINADO CON ÉXITO!")
    else:
        print("❌ ERROR: El archivo final no se creó.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
