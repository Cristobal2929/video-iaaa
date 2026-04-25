import os

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except:
    from moviepy import VideoFileClip, concatenate_videoclips


def process_pipeline(clips, duration=30):

    print("🎬 Editor estable activado")

    final = []

    for c in clips:

        if not os.path.exists(c):
            continue

        # 🔥 ignorar archivos que no son vídeo
        if not c.endswith((".mp4", ".mov", ".avi", ".mkv")):
            continue

        try:
            v = VideoFileClip(c)
            final.append(v.subclip(0, min(4, v.duration)))
        except Exception as e:
            print("⚠️ Clip ignorado:", e)

    # 🔥 SI NO HAY NADA → NO CRASHEAR
    if len(final) == 0:
        print("⚠️ No hay clips válidos → generando video vacío seguro")
        return "storage/output/empty.mp4"

    video = concatenate_videoclips(final)

    video = video.resize((1080, 1920))

    os.makedirs("storage/output", exist_ok=True)

    out = "storage/output/final.mp4"
    video.write_videofile(out, fps=24)

    return out
