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
