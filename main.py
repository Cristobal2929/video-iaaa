import argparse, os, asyncio, google.generativeai as genai, yt_dlp, edge_tts

async def fabricar_video(tema):
    print(f"🎬 Iniciando: {tema}")
    os.makedirs("static", exist_ok=True)
    
    # 1. Guion
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    guion = model.generate_content(f"Dato corto y viral sobre {tema}. Solo el texto.").text.strip()
    
    # 2. Voz
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")
    
    # 3. Fondo
    ydl_opts = {'format': 'best[ext=mp4]', 'default_search': 'ytsearch1:', 'outtmpl': 'bg.mp4', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download(["minecraft parkour no copyright"])
    
    # 4. Montaje con FFmpeg (el más fiable)
    print("🎥 Montando...")
    os.system('ffmpeg -y -i bg.mp4 -i static/voz.mp3 -map 0:v -map 1:a -c:v copy -shortest static/video_final.mp4')
    print("✅ ¡VÍDEO TERMINADO!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
