import argparse
import os
import asyncio
import google.generativeai as genai
import yt_dlp
import edge_tts
from edge_tts import SubMaker

# 1. Función para la Voz y Subtítulos (Boca y Texto)
async def generar_voz_y_subtitulos(texto, archivo_audio, archivo_subs):
    print("🗣️ Generando voz y tiempos de subtítulos...")
    VOICE = "es-ES-AlvaroNeural"
    communicate = edge_tts.Communicate(texto, VOICE)
    submaker = edge_tts.SubMaker()
    
    with open(archivo_audio, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open(archivo_subs, "w", encoding="utf-8") as f:
        f.write(submaker.generate_subs())
    print("✅ Audio y Subtítulos generados.")

# 2. Función para descargar fondo (Ojos)
def descargar_fondo():
    print("🎬 Descargando fondo de YouTube...")
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'default_search': 'ytsearch1:',
        'outtmpl': 'background.mp4',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["vertical parkour gameplay no copyright"])
    return "background.mp4"

def generar_video(tema):
    print(f"🚀 MOTOR FÉNIX: Creando vídeo viral sobre '{tema}'")
    if not os.path.exists("static"): os.makedirs("static")

    # A. Gemini hace el guion
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content(f"Escribe un dato curioso y viral sobre {tema}. Solo el texto, 15 segundos.")
    guion = res.text.strip()
    print(f"📜 Guion: {guion}")

    # B. Generar Voz y SRT
    asyncio.run(generar_voz_y_subtitulos(guion, "voz.mp3", "subs.srt"))

    # C. Descargar Fondo
    descargar_fondo()

    # D. EL MONTAJE MAESTRO CON FFMPEG (Quemar subtítulos)
    # Este comando une audio, video y pone los subtítulos amarillos en el centro
    print("🏗️ Ensamblando todo con FFmpeg...")
    comando = (
        'ffmpeg -y -i background.mp4 -i voz.mp3 '
        '-vf "subtitles=subs.srt:force_style=\'Alignment=10,FontSize=20,PrimaryColour=&H00FFFF,OutlineColour=&H000000,BorderStyle=3\'" '
        '-map 0:v:0 -map 1:a:0 -shortest -c:v libx264 -pix_fmt yuv420p static/video_final.mp4'
    )
    os.system(comando)
    print("✅ ¡VÍDEO FINAL COMPLETADO!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str, required=True)
    args = parser.parse_args()
    generar_video(args.tema)
