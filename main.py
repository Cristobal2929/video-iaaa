import argparse, os, asyncio, edge_tts, requests, random
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 RENDER ESTABLE: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz, f_subs = "voz_temp.mp3", "subs_temp.vtt"
    f_final = f"static/{video_id}.mp4"

    # 1. GUIONISTA
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Escribe un guion épico y misterioso sobre {tema}. Unas 110 palabras. Solo texto.")
        guion = res.text.strip().replace('*', '').replace('"', '')
    except: guion = f"El misterio de {tema} es algo que desafía la realidad. Prepárate para el viaje."

    # 2. VOZ Y SUBS
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    with open(f_voz, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio, fin = chunk["offset"]/10000, (chunk["offset"]+chunk["duration"])/10000
                subs_vtt.append(f"{tiempo_a_vtt(inicio)} --> {tiempo_a_vtt(fin)}\n{chunk['text']}\n\n")
    with open(f_subs, "w", encoding="utf-8") as f: f.writelines(subs_vtt)

    # 3. 3 IMÁGENES
    for i in range(1, 4):
        seed = random.randint(1, 99999)
        url = f"https://image.pollinations.ai/prompt/cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical?width=720&height=1280&nologo=true&seed={seed}"
        with open(f"img{i}.jpg", "wb") as f: f.write(requests.get(url).content)

    # 4. MONTAJE CINE (Zoom suave + Transiciones)
    estilo = "FontName=Arial,FontSize=30,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=80"
    
    # Filtro optimizado: Zoom suave hacia adelante en las 3 fotos con fundido
    filtro_v = (
        "[0:v]scale=1280:2275,zoompan=z='min(zoom+0.001,1.5)':d=1:s=720x1280,fade=t=out:st=14:d=1[v1]; "
        "[1:v]scale=1280:2275,zoompan=z='min(zoom+0.001,1.5)':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=14:d=1[v2]; "
        "[2:v]scale=1280:2275,zoompan=z='min(zoom+0.001,1.5)':d=1:s=720x1280,fade=t=in:st=0:d=1[v3]; "
        f"[v1][v2][v3]concat=n=3:v=1:a=0,subtitles='{f_subs}':force_style='{estilo}'[v]"
    )
    
    os.system(f'ffmpeg -y -loop 1 -t 15 -i img1.jpg -loop 1 -t 15 -i img2.jpg -loop 1 -t 15 -i img3.jpg -i {f_voz} -filter_complex "{filtro_v}" -map "[v]" -map 3:a -c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart -shortest {f_final}')
    
    for i in range(1, 4): os.remove(f"img{i}.jpg")
    os.remove(f_voz); os.remove(f_subs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str); parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args(); asyncio.run(fabricar_video(args.tema, args.id))
