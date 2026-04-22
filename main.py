import os
import asyncio
import requests
import edge_tts
from moviepy.editor import *

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ Falta GROQ_API_KEY")

if not PEXELS_API_KEY:
    raise Exception("❌ Falta PEXELS_API_KEY")

# =========================
# IA GROQ
# =========================
def generar_guion_y_keywords(tema):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": f"Crea un guion viral de 15 segundos sobre {tema}. Formato: GUION: ... KEYWORDS: 4 palabras en inglés"}
        ],
        "temperature": 0.9
    }

    r = requests.post(url, headers=headers, json=data)

    if r.status_code != 200:
        raise Exception(r.text)

    res = r.json()

    if "choices" not in res:
        raise Exception(res)

    text = res["choices"][0]["message"]["content"]

    guion = text.split("GUION:")[1].split("KEYWORDS:")[0].strip()
    keywords = text.split("KEYWORDS:")[1].strip().split(",")

    return guion, [k.strip() for k in keywords]

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

        videos = r.get("videos", [])
        if not videos:
            continue

        video_url = videos[0]["video_files"][0]["link"]

        path = f"clip_{i}.mp4"
        with open(path, "wb") as f:
            f.write(requests.get(video_url).content)

        clips.append(path)

    if not clips:
        raise Exception("No clips found")

    return clips

# =========================
# VIDEO
# =========================
def montar_video(guion, clips):
    audio = AudioFileClip("voz.mp3")
    dur = audio.duration / len(clips)

    videos = []

    for c in clips:
        clip = VideoFileClip(c).resize(height=1920).set_duration(dur)
        videos.append(clip)

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

    await texto_a_voz(guion)

    clips = descargar_clips(keywords)

    montar_video(guion, clips)

    print("✅ VIDEO LISTO")

if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "terror"
    asyncio.run(run(tema))
