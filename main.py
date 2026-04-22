import argparse, os, asyncio, google.generativeai as genai, yt_dlp, edge_tts

async def fabricar_video(tema):
    print(f"🎬 Iniciando motor para: {tema}")
    os.makedirs("static", exist_ok=True)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: No hay GEMINI_API_KEY")
        return

    # CAMBIO AQUÍ: Usamos un nombre de modelo más estándar
    try:
        genai.configure(api_key=api_key)
        # Probamos con el nombre base que suele ser el más compatible
        model = genai.GenerativeModel('gemini-1.5-flash') 
        res = model.generate_content(f"Escribe un dato curioso, corto y viral sobre {tema}. Solo el texto, sin títulos.")
        guion = res.text.strip()
        print(f"📝 Guion: {guion[:30]}...")
    except Exception as e:
        print(f"⚠️ Falló gemini-1.5-flash, intentando gemini-pro...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"Dato curioso corto sobre {tema}")
            guion = res.text.strip()
        except Exception as e2:
            print(f"❌ ERROR CRÍTICO Gemini: {e2}")
            return

    # Voz
    print("🔊 Generando voz...")
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")

    # Fondo
    print("📥 Descargando fondo...")
    ydl_opts = {'format': 'mp4', 'default_search': 'ytsearch1:', 'outtmpl': 'bg.mp4', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download(["minecraft parkour no copyright"])

    # Montaje
    print("🎥 Montando video final...")
    # Añadimos filtros para asegurar que el video sea vertical (9:16) y se vea bien en móvil
    os.system('ffmpeg -y -i bg.mp4 -i static/voz.mp3 -vf "crop=ih*(9/16):ih,scale=1080:1920" -map 0:v -map 1:a -c:v libx264 -preset ultrafast -shortest static/video_final.mp4')
    
    if os.path.exists("static/video_final.mp4"):
        print("✅ ¡VÍDEO TERMINADO CON ÉXITO!")
    else:
        print("❌ ERROR: El archivo final no se creó.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
