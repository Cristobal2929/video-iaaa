import argparse
import os
import google.generativeai as genai
import yt_dlp

def descargar_video_fondo(busqueda):
    print(f"🎬 Buscando fondo en YouTube: {busqueda}")
    # Configuración para descargar un video corto y ligero
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'default_search': 'ytsearch1:', # Busca el primer resultado
        'max_filesize': 50 * 1024 * 1024, # Máximo 50MB
        'outtmpl': 'background.mp4',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"vertical gameplay {busqueda} no copyright"])
        print("✅ Fondo descargado correctamente.")
        return "background.mp4"
    except Exception as e:
        print(f"❌ Error al descargar de YouTube: {e}")
        return None

def generar_video(tema):
    print(f"🚀 Motor Fénix activado para: '{tema}'")
    if not os.path.exists("static"): os.makedirs("static")

    # 1. EL CEREBRO (Gemini)
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Haz un guion de TikTok de 15 segundos sobre: {tema}. Solo el texto."
    respuesta = model.generate_content(prompt)
    guion = respuesta.text
    print(f"✅ GUION:\n{guion}")

    # 2. LOS OJOS (YouTube)
    # Buscamos algo genérico que pegue con todo como Minecraft o Parkour
    archivo_fondo = descargar_video_fondo("minecraft parkour")

    # 3. EL MONTAJE (Moviepy)
    # Por ahora, para no fallar, guardamos el fondo descargado como el video final
    if archivo_fondo and os.path.exists(archivo_fondo):
        os.rename(archivo_fondo, "static/video_final.mp4")
        print("✅ Video de YouTube listo para descargar en la web.")
    else:
        print("⚠️ No hubo fondo, creando video de emergencia...")
        from moviepy.editor import ColorClip
        clip = ColorClip(size=(1080, 1920), color=(30, 30, 30), duration=5)
        clip.write_videofile("static/video_final.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str, required=True)
    args = parser.parse_args()
    generar_video(args.tema)
