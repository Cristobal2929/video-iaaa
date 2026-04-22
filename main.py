import argparse, os, asyncio, edge_tts, requests, random
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🔥 INICIANDO MODO DIOS: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz, f_subs = "voz_temp.mp3", "subs_temp.vtt"
    f_final = f"static/{video_id}.mp4"

    # 1. GUIONISTA CINEMATOGRÁFICO
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escribe un guion épico, oscuro y fascinante sobre {tema} para un documental de 1 minuto. Unas 130 palabras. No uses asteriscos. Empieza con un gancho que paralice el corazón."
        res = model.generate_content(prompt)
        guion = res.text.strip().replace('*', '').replace('"', '')
    except:
        guion = f"Imagina un mundo donde {tema} es la única realidad. Un lugar donde los secretos se esconden en cada rincón y la verdad es más extraña que la ficción. Prepárate para descubrir lo imposible."

    # 2. VOZ Y SUBS DE PRECISIÓN
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    with open(f_voz, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio, fin = chunk["offset"]/10000, (chunk["offset"]+chunk["duration"])/10000
                subs_vtt.append(f"{tiempo_a_vtt(inicio)} --> {tiempo_a_vtt(fin)}\n{chunk['text']}\n\n")
    with open(f_subs, "w", encoding="utf-8") as f: f.writelines(subs_vtt)

    # 3. 5 IMÁGENES HYPER-REALISTAS
    prompts = ["masterpiece wide cinematic", "intense dramatic medium shot", "extreme macro detail", "aerial epic perspective", "portrait bokeh focus"]
    for i in range(1, 6):
        seed = random.randint(1, 999999)
        p = f"{prompts[i-1]}%20{tema.replace(' ', '%20')}%20hyperrealistic%20dramatic%20lighting%208k%20vertical"
        url = f"https://image.pollinations.ai/prompt/{p}?width=720&height=1280&nologo=true&seed={seed}"
        with open(f"img{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        print(f"✅ Escena {i} renderizada.")

    # 4. MONTAJE NIVEL "HOLLYWOOD"
    # Subtítulos Amarillos Neón, letra impactante y centrada
    estilo = "FontName=Arial,FontSize=34,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=4,Alignment=2,MarginV=90"
    
    # Efecto: Cada imagen tiene un movimiento distinto (Zoom In, Pan, Zoom Out, Rotate, Zoom Fast)
    filtro_v = (
        "[0:v]scale=1280:2275,zoompan=z='min(zoom+0.0015,1.5)':d=1:s=720x1280,fade=t=out:st=11:d=1[v1]; "
        "[1:v]scale=1280:2275,zoompan=z='1.1':x='x+0.5':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=11:d=1[v2]; "
        "[2:v]scale=1280:2275,zoompan=z='1.5-0.001*in':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=11:d=1[v3]; "
        "[3:v]scale=1280:2275,zoompan=z='1.1':y='y+0.5':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=11:d=1[v4]; "
        "[4:v]scale=1280:2275,zoompan=z='min(zoom+0.002,1.6)':d=1:s=720x1280,fade=t=in:st=0:d=1[v5]; "
        f"[v1][v2][v3][v4][v5]concat=n=5:v=1:a=0,subtitles='{f_subs}':force_style='{estilo}'[v]"
    )
    
    comando = (
        f'ffmpeg -y -loop 1 -t 12 -i img1.jpg -loop 1 -t 12 -i img2.jpg -loop 1 -t 12 -i img3.jpg -loop 1 -t 12 -i img4.jpg -loop 1 -t 12 -i img5.jpg -i {f_voz} '
        f'-filter_complex "{filtro_v}" -map "[v]" -map 5:a -c:v libx264 -pix_fmt yuv420p -b:v 4000k -shortest {f_final}'
    )
    
    os.system(comando)
    
    # Limpieza
    for i in range(1, 6): os.remove(f"img{i}.jpg")
    os.remove(f_voz); os.remove(f_subs)
    print(f"🎬 OBRA MAESTRA FINALIZADA: {f_final}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str); parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args(); asyncio.run(fabricar_video(args.tema, args.id))
