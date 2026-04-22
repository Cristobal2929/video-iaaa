import argparse, os, asyncio, edge_tts, requests, random, subprocess
import google.generativeai as genai

def tiempo_a_ass(segundos):
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

async def fabricar_video(tema, video_id):
    print(f"🔱 MODO LEYENDA ACTIVADO: {tema}")
    os.makedirs("static", exist_ok=True)
    f_voz, f_subs, f_raw, f_music, f_final = "voz.mp3", "subs.ass", "raw.mp4", "music.mp3", f"static/{video_id}.mp4"

    # 1. GUIONISTA GEMINI (120 palabras)
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Crea un guion cinematográfico para un video de 60 segundos sobre {tema}. Estilo oscuro, frases impactantes de máximo 6 palabras. Sin asteriscos. Empieza con un secreto que nadie sepa."
    try:
        res = model.generate_content(prompt)
        guion = res.text.strip().replace("*", "").replace('"', '')
    except:
        guion = f"El misterio de {tema} es algo que desafía la realidad. Prepárate para descubrir la verdad oculta."

    # 2. VOZ + SUBS KARAOKE
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_data = []
    with open(f_voz, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio, fin = chunk["offset"]/10000000, (chunk["offset"]+chunk["duration"])/10000000
                palabra = chunk["text"].upper()
                subs_data.append(f"Dialogue: 0,{tiempo_a_ass(inicio)},{tiempo_a_ass(fin)},Default,,0,0,0,,{{\\c&H00FFFFFF&\\bord5\\shad3\\b1}}{palabra}")

    with open(f_subs, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BorderStyle, Outline, Shadow, Alignment\nStyle: Default,Arial,45,&H00FFFFFF,&H00000000,1,5,2,2\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        f.write("\n".join(subs_data))

    # 3. PEXELS (Metraje Real)
    pex_key = os.environ.get("PEXELS_API_KEY")
    headers = {"Authorization": pex_key}
    try:
        r = requests.get(f"https://api.pexels.com/videos/search?query={tema}&per_page=1&orientation=portrait", headers=headers).json()
        video_url = r['videos'][0]['video_files'][0]['link']
    except:
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-stars-in-the-deep-space-34554-large.mp4"
    with open(f_raw, "wb") as f: f.write(requests.get(video_url).content)

    # 4. MÚSICA
    music_url = "https://cdn.pixabay.com/download/audio/2022/10/19/audio_suspense.mp3"
    with open(f_music, "wb") as f: f.write(requests.get(music_url).content)

    # 5. RENDER CINEMATOGRÁFICO (El toque que vuela la cabeza)
    cmd = (
        f'ffmpeg -y -i {f_raw} -i {f_voz} -i {f_music} '
        f'-filter_complex "[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,'
        f'unsharp=5:5:1.0:5:5:0.0,curves=preset=darker,noise=alls=12:allf=t+u,vignette=PI/4,'
        f'subtitles={f_subs}[v];[1:a]volume=1.5[a1];[2:a]volume=0.15[a2];[a1][a2]amix=inputs=2[a]" '
        f'-map "[v]" -map "[a]" -c:v libx264 -pix_fmt yuv420p -b:v 5000k -shortest {f_final}'
    )
    os.system(cmd)
    
    # Limpiar temporales
    for f in [f_voz, f_subs, f_raw, f_music]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
