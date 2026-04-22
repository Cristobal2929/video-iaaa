import os
import asyncio
import argparse
import requests
import edge_tts

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# =========================
# CONFIGURACIÓN GROQ
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API = os.getenv("PEXELS_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ Falta GROQ_API_KEY")

# =========================
# IA (GROQ)
# =========================
def generar_guion_y_keywords(tema):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Crea un guion viral de 15-20 segundos sobre: {tema}

    FORMATO:
    GUION: texto corto emocional
    KEYWORDS: 4 palabras en inglés separadas por comas
    """

    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }

    r = requests.post(url, headers=headers, json=data)
    text = r.json()["choices"][0]["message"]["content"]

    guion = text.split("GUION:")[1].split("KEYWORDS:")[0].strip()
    keywords = text.split("KEYWORDS:")[1].strip().split(",")

    return guion, [k.strip() for k in keywords]


# =========================
# TTS
# =========================
async def texto_a_voz(texto):
    communicate = edge_tts.Communicate(texto, "es-ES-AlvaroNeural")
    await communicate.save("voz.mp3")


# =========================
# PEXELS
# =========================
def descargar_clips(keywords):
    clips = []
    headers = {"Authorization": PEXELS_API}

    for i, k in enumerate(keywords[:4]):
        url = f"https://api.pexels.com/videos/search?query={k}&per_page=1&orientation=portrait"

        r = requests.get(url, headers=headers).json()
        videos = r.get("videos", [])

        if not videos:
            continue

        video_url = videos[0]["video_files"][0]["link"]

        path = f"clip_{i}.mp4"
        with open(path, "wb") as f:
            f.write(requests.get(video_url).content)

        clips.append(path)

    if not clips:
        raise Exception("❌ No clips found")

    return clips


# =========================
# VIDEO
# =========================
def montar_video(guion, clips_paths):
    audio = AudioFileClip("voz.mp3")
    duracion = audio.duration / len(clips_paths)

    clips_finales = []

    for p in clips_paths:
        clip = VideoFileClip(p).resize(height=1920).set_duration(duracion).set_fps(30)
        clips_finales.append(clip)

    video = concatenate_videoclips(clips_finales, method="compose")
    video = video.set_audio(audio)

    subtitulos = TextClip(
        guion,
        fontsize=50,
        color="yellow",
        method="caption",
        size=(video.w * 0.8, None)
    ).set_duration(audio.duration).set_position("center")

    final = CompositeVideoClip([video, subtitulos])

    final.write_videofile("video_final.mp4", codec="libx264", audio_codec="aac", fps=30)


# =========================
# MAIN
# =========================
async def ejecutar_todo(tema):
    print("🎬 Tema:", tema)

    guion, keywords = generar_guion_y_keywords(tema)

    print("🧠 Guion:", guion)
    print("🔑 Keywords:", keywords)

    await texto_a_voz(guion)

    clips = descargar_clips(keywords)

    montar_video(guion, clips)

    print("✅ VIDEO GENERADO")


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "terror"
    asyncio.run(ejecutar_todo(tema))
