import argparse
import os
import google.generativeai as genai
import yt_dlp
import asyncio
import edge_tts

# Función para convertir el guion en audio (La Boca)
async def generar_voz(texto, archivo_audio):
    print("🗣️ Generando voz en off...")
    # Usamos una voz viral (Alvaro o Jorge suelen ser las de TikTok)
    VOICE = "es-ES-AlvaroNeural" 
    communicate = edge_tts.Communicate(texto, VOICE)
    await communicate.save(archivo_audio)
    print(f"✅ Audio guardado en: {archivo_audio}")

def descargar_video_fondo(busqueda):
    print(f"🎬 Buscando fondo en YouTube: {busqueda}")
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'default_search': 'ytsearch1:',
        'outtmpl': 'background.mp4',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"vertical gameplay {busqueda} no copyright"])
        return "background.mp4"
    except:
        return None

def generar_video(tema):
    print(f"🚀 Motor Fénix activado para: '{tema}'")
    if not os.path.exists("static"): os.makedirs("static")

    # 1. EL CEREBRO (Gemini)
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    respuesta = model.generate_content(f"Haz un guion corto de 15 segundos para TikTok sobre: {tema}. Solo el texto del narrador.")
    guion = respuesta.text
    print(f"✅ GUION: {guion}")

    # 2. LA BOCA (Voz en off)
    archivo_audio = "voz.mp3"
    asyncio.run(generar_voz(guion, archivo_audio))

    # 3. LOS OJOS (Fondo de YouTube)
    archivo_fondo = descargar_video_fondo("minecraft parkour")

    # 4. EL MONTAJE FINAL (Moviepy)
    # Aquí es donde unimos la voz con el video
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video = VideoFileClip(archivo_fondo).subclip(0, 15) # Cogemos 15 segundos
        audio = AudioFileClip(archivo_audio)
        
        video_final = video.set_audio(audio)
        video_final.write_videofile("static/video_final.mp4", fps=24, codec="libx264")
        print("✅ ¡VÍDEO CON VOZ GENERADO!")
    except Exception as e:
        print(f"⚠️ Error en montaje: {e}. Guardando fondo como emergencia.")
        if archivo_fondo: os.rename(archivo_fondo, "static/video_final.mp4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str, required=True)
    args = parser.parse_args()
    generar_video(args.tema)
