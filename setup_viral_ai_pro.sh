#!/bin/bash

echo "🚀 Creando Sistema Viral IA Pro..."

mkdir -p core engine storage/clips storage/output

# SCRIPT IA
cat << 'EOT' > core/script_ai.py
import random

def generate_script(topic, duration=30):

    hooks = [
        f"Nadie te cuenta esto sobre {topic}...",
        f"Lo que vas a ver de {topic} te va a sorprender...",
        f"{topic}: la verdad oculta detrás de esto...",
    ]

    story = [
        "Todo empezó normal...",
        "Pero algo cambió de forma inesperada...",
        "El misterio empezó a crecer...",
        "El final nadie lo esperaba..."
    ]

    return random.choice(hooks) + "\n\n" + "\n".join(story)
EOT

# VOZ
cat << 'EOT' > core/voice.py
import os

def generate_voice(text):
    os.makedirs("storage/output", exist_ok=True)
    path = "storage/output/voice.txt"
    with open(path, "w") as f:
        f.write(text)
    return path
EOT

# SUBTITULOS
cat << 'EOT' > core/subtitles.py
import os

def generate_subtitles(script):
    os.makedirs("storage/output", exist_ok=True)
    lines = script.split("\n")

    srt = []
    t = 0

    for line in lines:
        if line.strip():
            srt.append(f"{t} --> {t+3}\n{line}\n")
            t += 3

    path = "storage/output/subs.srt"
    with open(path, "w") as f:
        f.write("\n".join(srt))

    return path
EOT

# DOWNLOADER
cat << 'EOT' > core/downloader.py
import os
import glob

def download_videos(query, max_videos=5):

    os.makedirs("storage/clips", exist_ok=True)

    cmd = f'yt-dlp --ignore-errors "ytsearch{max_videos}:{query}" -o "storage/clips/video_%(autonumber)s.%(ext)s"'
    os.system(cmd)

    files = glob.glob("storage/clips/video_*")

    if not files:
        return ["storage/fallback.mp4"]

    return files[:max_videos]
EOT

# EDITOR
cat << 'EOT' > core/editor.py
import os

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except:
    from moviepy import VideoFileClip, concatenate_videoclips

def process_pipeline(clips, duration=30):

    final = []

    for c in clips:
        if not os.path.exists(c):
            continue

        try:
            v = VideoFileClip(c)
            final.append(v.subclip(0, min(4, v.duration)))
        except:
            pass

    if not final:
        raise Exception("No clips")

    video = concatenate_videoclips(final)
    video = video.resize((1080, 1920))

    os.makedirs("storage/output", exist_ok=True)
    out = "storage/output/final.mp4"
    video.write_videofile(out, fps=24)

    return out
EOT

# ORCHESTRATOR
cat << 'EOT' > engine/orchestrator.py
from core.script_ai import generate_script
from core.downloader import download_videos
from core.editor import process_pipeline
from core.voice import generate_voice
from core.subtitles import generate_subtitles

def run(topic, duration=30):

    print("🚀 SISTEMA VIRAL IA PRO")

    script = generate_script(topic, duration)
    print("\n🧠 SCRIPT:\n", script)

    clips = download_videos(topic)
    video = process_pipeline(clips, duration)

    generate_voice(script)
    generate_subtitles(script)

    print("\n✅ VIDEO FINAL:", video)
    return video

if __name__ == "__main__":
    topic = input("📌 Tema: ")
    duration = int(input("⏱️ Duración: "))
    run(topic, duration)
EOT

chmod +x setup_viral_ai_pro.sh

echo "✅ Sistema creado. Ejecuta:"
echo "python -m engine.orchestrator"
