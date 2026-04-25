import os
import glob

def download_videos(query, max_videos=5):

    os.makedirs("storage/clips", exist_ok=True)

    cmd = f'yt-dlp --ignore-errors "ytsearch{max_videos}:{query}" -o "storage/clips/video_%(autonumber)s.%(ext)s"'
    os.system(cmd)

    clips = glob.glob("storage/clips/video_*")

    # 🔥 SI FALLA TODO → usar cualquier clip existente en el sistema
    if len(clips) == 0:
        clips = glob.glob("storage/*.mp4")

    # 🔥 SI AÚN FALLA → NO CRASHEAR
    if len(clips) == 0:
        print("⚠️ No hay vídeos reales → creando placeholder seguro")
        placeholder = "storage/placeholder.txt"
        with open(placeholder, "w") as f:
            f.write("no video")
        return [placeholder]

    return clips[:max_videos]
