import argparse, os, asyncio, google.generativeai as genai, yt_dlp, edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

async def generar_video(tema):
    print(f"🚀 Fabricando: {tema}")
    if not os.path.exists("static"): os.makedirs("static")
    
    # Cerebro (Guion)
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    guion = model.generate_content(f"Dato viral corto sobre {tema}. Solo texto.").text
    
    # Boca (Audio)
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")
    
    # Ojos (Video de fondo)
    ydl_opts = {'format': 'best[ext=mp4]', 'default_search': 'ytsearch1:', 'outtmpl': 'background.mp4', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download(["minecraft parkour no copyright"])
    
    # Montaje
    video = VideoFileClip("background.mp4").subclip(0, 15)
    audio = AudioFileClip("static/voz.mp3")
    video.set_audio(audio).write_videofile("static/video_final.mp4", codec="libx264")
    print("✅ ¡VÍDEO GUARDADO EN STATIC!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(generar_video(args.tema))
