import argparse, os, asyncio, edge_tts, requests, random, subprocess
import google.generativeai as genai

# Ayudante para el tiempo de los subtítulos .ass
def tiempo_a_ass(segundos):
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

async def fabricar_video(tema, video_id):
    print(f"🔥 RENDERIZANDO MODO BESTIA: {tema}")
    os.makedirs("static", exist_ok=True)

    voz = "voz_temp.mp3"
    subs = "subs_temp.ass"
    salida = f"static/{video_id}.mp4"
    music = "music_temp.mp3"

    # 1. GUIONISTA GEMINI (Adicción Pura)
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Crea un guion corto de 100 palabras para TikTok sobre el misterio de {tema}. Estilo oscuro, frases cortas, gancho inicial brutal. Sin asteriscos."
        res = model.generate_content(prompt)
        guion = res.text.strip().replace("*", "").replace('"', '')
    except:
        guion = f"No deberías estar viendo esto sobre {tema}. Lo que descubrirás a continuación ha sido ocultado por años. Prepárate."

    # 2. VOZ + SUBTÍTULOS KARAOKE
    print("🔊 Generando voz y subtítulos dinámicos...")
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_data = []
    
    with open(voz, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio = chunk["offset"]/10000000 # Convertir a segundos
                duracion = chunk["duration"]/10000000
                fin = inicio + duracion
                palabra = chunk["text"]
                # Estilo: Amarillo Neón (\c&H00FFFF&), borde negro (\bord4)
                subs_data.append(
                    f"Dialogue: 0,{tiempo_a_ass(inicio)},{tiempo_a_ass(fin)},Default,,0,0,0,,{{\\c&H00FFFF&\\bord4\\shad2}}{palabra}"
                )

    with open(subs, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BorderStyle, Outline, Shadow, Alignment\nStyle: Default,Arial,36,&H00FFFFFF,&H00000000,1,4,1,2\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        f.write("\n".join(subs_data))

    # 3. 3 IMÁGENES CINEMÁTICAS
    print("🖼️ Generando imágenes de alto impacto...")
    estilos = ["epic wide shot", "dramatic medium", "extreme macro detail"]
    for i in range(3):
        seed = random.randint(1, 999999)
        url = f"https://image.pollinations.ai/prompt/cinematic%20dark%20{tema.replace(' ','%20')}%20{estilos[i]}%208k%20vertical?width=720&height=1280&seed={seed}"
        with open(f"img{i}.jpg", "wb") as f:
            f.write(requests.get(url).content)

    # 4. MÚSICA DE SUSPENSE
    print("🎵 Sincronizando audio...")
    music_url = "https://cdn.pixabay.com/download/audio/2022/10/19/audio_suspense.mp3"
    with open(music, "wb") as f:
        f.write(requests.get(music_url).content)

    # 5. CÁLCULO DE DURACIÓN
    dur = float(os.popen(f"ffprobe -i {voz} -show_entries format=duration -v quiet -of csv=p=0").read())
    dur_img = dur / 3

    # 6. RENDERIZADO FINAL (Zoompan + Audio Mix + Subs)
    print("🎥 Iniciando render final en la nube...")
    cmd = f"""
    ffmpeg -y \
    -loop 1 -t {dur_img} -i img0.jpg \
    -loop 1 -t {dur_img} -i img1.jpg \
    -loop 1 -t {dur_img} -i img2.jpg \
    -i {voz} -i {music} \
    -filter_complex "
    [0:v]scale=1280:2275,zoompan=z='min(zoom+0.0015,1.5)':d=1:s=720x1280,fade=t=out:st={dur_img-0.5}:d=0.5[v0];
    [1:v]scale=1280:2275,zoompan=z='1.2-0.001*on':d=1:s=720x1280,fade=t=in:st=0:d=0.5,fade=t=out:st={dur_img-0.5}:d=0.5[v1];
    [2:v]scale=1280:2275,zoompan=z='min(zoom+0.001,1.5)':d=1:s=720x1280,fade=t=in:st=0:d=0.5[v2];
    [v0][v1][v2]concat=n=3:v=1:a=0,subtitles={subs}[v];
    [3:a]volume=1.5[a1];
    [4:a]volume=0.2[a2];
    [a1][a2]amix=inputs=2[a]
    " \
    -map "[v]" -map "[a]" \
    -c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart -shortest {salida}
    """

    subprocess.run(cmd, shell=True)

    # Limpieza
    for i in range(3): os.remove(f"img{i}.jpg")
    os.remove(voz); os.remove(subs); os.remove(music)
    print(f"🔥 VÍDEO FINALIZADO CON ÉXITO: {salida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
