import os
import asyncio
import argparse
import requests
import google.generativeai as genai
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Configuración de APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
PEXELS_API = os.getenv("PEXELS_API_KEY")

async def generar_guion_y_keywords(tema):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Escribe una historia de terror de 15 segundos sobre {tema}. Devuelve SOLO este formato: GUION: (texto corto) | KEYWORDS: (4 palabras en ingles separadas por comas)"
    response = model.generate_content(prompt).text
    guion = response.split("GUION:")[1].split("|")[0].strip()
    keywords = response.split("KEYWORDS:")[1].strip().split(",")
    return guion, [k.strip() for k in keywords]

async def texto_a_voz(texto):
    communicate = edge_tts.Communicate(texto, "es-ES-AlvaroNeural")
    await communicate.save("voz.mp3")

def descargar_clips(keywords):
    paths = []
    headers = {"Authorization": PEXELS_API}
    for i, k in enumerate(keywords):
        url = f"https://api.pexels.com/videos/search?query={k}&per_page=1&orientation=portrait"
        res = requests.get(url, headers=headers).json()
        video_url = res['videos'][0]['video_files'][0]['link']
        path = f"clip_{i}.mp4"
        with open(path, "wb") as f:
            f.write(requests.get(video_url).content)
        paths.append(path)
    return paths

def montar_video(guion, clips_paths):
    audio = AudioFileClip("voz.mp3")
    duracion_por_clip = audio.duration / len(clips_paths)
    
    final_clips = []
    for p in clips_paths:
        # Cortamos y ajustamos cada clip a la pantalla del móvil (vertical)
        clip = VideoFileClip(p).resize(height=1920).set_duration(duracion_por_clip).set_fps(30)
        final_clips.append(clip)
    
    video = concatenate_videoclips(final_clips).set_audio(audio)
    
    # Subtítulos automáticos centrados
    txt = TextClip(guion, fontsize=50, color='yellow', font='Arial', method='caption', 
                   size=(video.w*0.8, None)).set_duration(audio.duration).set_position('center')
    
    result = CompositeVideoClip([video, txt])
    result.write_videofile("video_final.mp4", codec="libx264", audio_codec="aac", fps=30)

async def ejecutar_todo(tema):
    print(f"🎬 Iniciando producción: {tema}")
    guion, keywords = await generar_guion_y_keywords(tema)
    await texto_a_voz(guion)
    paths = descargar_clips(keywords)
    montar_video(guion, paths)
    print("✅ Vídeo terminado con éxito.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tema', type=str)
    parser.add_argument('--id', type=str) # Recibimos el ID aunque no lo usemos en el nombre interno
    args = parser.parse_args()
    asyncio.run(ejecutar_todo(args.tema))
