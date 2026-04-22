import os
import asyncio
import requests
import re
import edge_tts
from moviepy.editor import *

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ Falta GROQ_API_KEY")

if not PEXELS_API_KEY:
    raise Exception("❌ Falta PEXELS_API_KEY")


# =========================
# IA (ROBUSTA)
# =========================
def generar_guion_y_keywords(tema):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Crea un vídeo viral de 15 segundos sobre: {tema}

DEVUELVE EXACTAMENTE:

GUION: texto corto emocional
KEYWORDS: palabra1, palabra2, palabra3, palabra4

NO EXPLICACIONES, NO FORMATO EXTRA
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }

    r = requests.post(url, headers=headers, json=data)

    if r.status_code != 200:
        raise Exception(f"❌ Groq error: {r.text}")

    text = r.json()["choices"][0]["message"]["content"]

    # =========================
    # PARSER INTELIGENTE (NO ROMPE)
    # =========================
    guion_match = re.search(r"GUION:\s*(.*)", text)
    key_match = re.search(r"KEYWORDS:\s*(.*)", text)

    if not guion_match or not key_match:
        raise Exception(f"❌ Formato IA inválido:\n{text}")

    guion = guion_match.group(1).strip()
    keywords = [k.strip() for k in key_match.group(1).split(",")]

    return guion, keywords


# =========================
# VOZ
# =========================
async def texto_a_voz(texto):
    tts = edge_tts.Communicate(texto, "es-ES-AlvaroNeural")
    await tts.save("voz.mp3")


# =========================
# PEXELS
# =========================
def descargar_clips(keywords):
    clips = []
    headers = {"Authorization": PEXELS_API_KEY}

    for i, k in enumerate(keywords[:4]):
        url = f"https://api.pexels.com/videos/search?query={k}&per_page=1&orientation=portrait"
        r = requests.get(url, headers=headers).json()

        if not r.get("videos"):
            continue

        video_url = r["videos"][0]["video_files"][0]["link"]

        path = f"clip_{i}.mp4"
        with open(path, "wb") as f:
            f.write(requests.get(video_url).content)

        clips.append(path)

    if not clips:
        raise Exception("❌ No clips encontrados")

    return clips


# =========================
# VIDEO
# =========================
def montar_video(guion, clips):
    audio = AudioFileClip("voz.mp3")
    dur = audio.duration / len(clips)

    videos = [
        VideoFileClip(c).resize(height=1920).set_duration(dur)
        for c in clips
    ]

    final = concatenate_videoclips(videos).set_audio(audio)

    txt = TextClip(
        guion,
        fontsize=50,
        color="yellow",
        method="caption",
        size=(final.w * 0.8, None)
    ).set_duration(audio.duration).set_position("center")

    out = CompositeVideoClip([final, txt])

    out.write_videofile("video_final.mp4", fps=30, codec="libx264", audio_codec="aac")


# =========================
# MAIN
# =========================
async def run(tema):
    print("🎬 Tema:", tema)

    guion, keywords = generar_guion_y_keywords(tema)

    print("🧠 GUION:", guion)
    print("🔑 KEYWORDS:", keywords)

    await texto_a_voz(guion)

    clips = descargar_clips(keywords)

    montar_video(guion, clips)

    print("✅ VIDEO LISTO")


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "terror"
    asyncio.run(run(tema))
