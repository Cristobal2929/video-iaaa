import argparse, os, asyncio, edge_tts, requests, random
from google import genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 EFECTO ZOOM INFINITO: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz, f_subs = "voz_temp.mp3", "subs_temp.vtt"
    f_final = f"static/{video_id}.mp4"

    # 1. GUIONISTA GEMINI
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt_guion = f"Escribe un guion épico de misterio sobre {tema}. Unas 110 palabras. Solo el texto."
    
    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt_guion)
        guion = response.text.strip().replace('*', '').replace('"', '')
    except:
        guion = f"El misterio de {tema} es insondable. Prepárate para viajar al corazón de lo desconocido."

    # 2. VOZ Y SUBS
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    with open(f_voz, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio = chunk["offset"] / 10000
                fin = (chunk["offset"] + chunk["duration"]) / 10000
                subs_vtt.append(f"{tiempo_a_vtt(inicio)} --> {tiempo_a_vtt(fin)}\n{chunk['text']}\n\n")
    with open(f_subs, "w", encoding="utf-8") as f: f.writelines(subs_vtt)

    # 3. LAS 3 IMÁGENES (Lejos, Cerca, Muy Cerca)
    niveles = ["wide cinematic shot", "detailed medium shot", "extreme close up macro"]
    for i, nivel in enumerate(niveles, 1):
        seed = random.randint(1, 99999)
        # Añadimos el nivel de zoom al prompt de la imagen
        prompt_img = f"{nivel}%20{tema.replace(' ', '%20')}%208k%20vertical%20cinematic"
        url = f"https://image.pollinations.ai/prompt/{prompt_img}?width=720&height=1280&nologo=true&seed={seed}"
        with open(f"img{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        print(f"✅ Imagen {i} ({nivel}) lista.")

    # 4. MONTAJE DE ZOOM DINÁMICO
    estilo = "FontName=Arial,FontSize=30,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=80"
    
    # Filtro complejo: Cada imagen tiene su propio zoom y se funden entre sí
    filtro_v = (
        "[0:v]scale=1280:2275,zoompan=z='min(zoom+0.0012,1.5)':d=1:s=720x1280,fade=t=out:st=14:d=1[v1]; "
        "[1:v]scale=1280:2275,zoompan=z='min(zoom+0.0012,1.5)':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=14:d=1[v2]; "
        "[2:v]scale=1280:2275,zoompan=z='min(zoom+0.0012,1.5)':d=1:s=720x1280,fade=t=in:st=0:d=1[v3]; "
        f"[v1][v2][v3]concat=n=3:v=1:a=0,subtitles='{f_subs}':force_style='{estilo}'[v]"
    )
    
    ffmpeg_cmd = (
        f'ffmpeg -y -loop 1 -t 15 -i img1.jpg -loop 1 -t 15 -i img2.jpg -loop 1 -t 15 -i img3.jpg -i {f_voz} '
        f'-filter_complex "{filtro_v}" -map "[v]" -map 3:a -c:v libx264 -pix_fmt yuv420p '
        f'-profile:v baseline -level 3.0 -movflags +faststart -shortest {f_final}'
    )
    os.system(ffmpeg_cmd)
    
    # Limpieza
    for i in range(1, 4): os.remove(f"img{i}.jpg")
    os.remove(f_voz); os.remove(f_subs)
    print("🚀 VIDEO TERMINADO CON ÉXITO")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str); parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args(); asyncio.run(fabricar_video(args.tema, args.id))
