import os
import asyncio
import argparse
import requests
import google.generativeai as genai
import edge_tts

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

# =========================
# CONFIGURACIÓN SEGURA
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API = os.getenv("PEXELS_API_KEY")

if not GEMINI_API_KEY or not PEXELS_API:
    raise Exception("❌ Faltan API keys en variables de entorno")

genai.configure(api_key=GEMINI_API_KEY)

# 🔥 FIX CRÍTICO (tu error 404)
model = genai.GenerativeModel("gemini-1.5-flash")


# =========================
# 1. GUION + KEYWORDS
# =========================
async def generar_guion_y_keywords(tema):
    prompt = f"""
    Crea una historia corta de terror de 15 segundos sobre: {tema}

    FORMATO OBLIGATORIO:
    GUION: texto corto
    KEYWORDS: palabra1, palabra2, palabra3, palabra4 (en inglés)
    """

    response = model.generate_content(prompt).text

    try:
        guion = response.split("GUION:")[1].split("KEYWORDS:")[0].strip()
        keywords_raw = response.split("KEYWORDS:")[1].strip()
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

        if len(keywords) < 1:
            keywords = ["horror", "dark", "night", "fear"]

        return guion, keywords

    except Exception as e:
        raise Exception(f"❌ Error parseando Gemini: {response}") from e


# =========================
# 2. TEXTO A VOZ
# =========================
async def texto_a_voz(texto):
    communicate = edge_tts.Communicate(texto, "es-ES-AlvaroNeural")
    await communicate.save("voz.mp3")


# =========================
# 3. PEXELS SAFE DOWNLOAD
# =========================
def descargar_clips(keywords):
    clips = []
    headers = {"Authorization": PEXELS_API}

    for i, k in enumerate(keywords[:4]):
        try:
            url = f"https://api.pexels.com/videos/search?query={k}&per_page=1&orientation=portrait"
            res = requests.get(url, headers=headers).json()

            videos = res.get("videos", [])
            if not videos:
                continue

            video_url = videos[0]["video_files"][0]["link"]

            path = f"clip_{i}.mp4"
            with open(path, "wb") as f:
                f.write(requests.get(video_url).content)

            clips.append(path)

        except Exception as e:
            print(f"⚠️ Error con keyword {k}: {e}")

    if not clips:
        raise Exception("❌ No se pudieron descargar clips de Pexels")

    return clips


# =========================
# 4. MONTAJE DE VIDEO
# =========================
def montar_video(guion, clips_paths):
    audio = AudioFileClip("voz.mp3")
    duracion = audio.duration / len(clips_paths)

    clips_finales = []

    for p in clips_paths:
        clip = (
            VideoFileClip(p)
            .resize(height=1920)
            .set_duration(duracion)
            .set_fps(30)
        )
        clips_finales.append(clip)

    video = concatenate_videoclips(clips_finales, method="compose")
    video = video.set_audio(audio)

    # Subtítulos
    subtitulos = TextClip(
        guion,
        fontsize=50,
        color='yellow',
        font='Arial',
        method='caption',
        size=(video.w * 0.8, None)
    ).set_duration(audio.duration).set_position('center')

    final = CompositeVideoClip([video, subtitulos])

    final.write_videofile(
        "video_final.mp4",
        codec="libx264",
        audio_codec="aac",
        fps=30
    )


# =========================
# PIPELINE PRINCIPAL
# =========================
async def ejecutar_todo(tema):
    print(f"🎬 Iniciando producción: {tema}")

    guion, keywords = await generar_guion_y_keywords(tema)
    print("🧠 Guion:", guion)
    print("🔑 Keywords:", keywords)

    await texto_a_voz(guion)
    clips = descargar_clips(keywords)

    montar_video(guion, clips)

    print("✅ VIDEO GENERADO CON ÉXITO")


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str, required=True)
    parser.add_argument("--id", type=str)

    args = parser.parse_args()

    asyncio.run(ejecutar_todo(args.tema))
