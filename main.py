import argparse, os, asyncio, edge_tts, requests, random
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 INICIANDO MONTAJE MULTI-IMAGEN: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz = f"static/voz_{video_id}.mp3"
    f_subs = f"static/subs_{video_id}.vtt"
    f_final = f"static/{video_id}.mp4"

    # 1. GUION LARGO Y POTENTE
    api_key = os.environ.get("GEMINI_API_KEY")
    guion_base = f"El misterio de {tema} es algo que desafía toda lógica. Durante décadas, se han ocultado pruebas que sugieren una realidad mucho más oscura de lo que nos han contado. ¿Estamos preparados para la verdad?"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escribe un guion de misterio conspiranoico sobre {tema}. Unas 120 palabras. Empieza con un gancho fuerte. Solo el texto."
        res = model.generate_content(prompt)
        guion = res.text.strip().replace('*', '').replace('"', '')
        if len(guion.split()) < 30: guion = guion_base
    except: guion = guion_base

    # 2. VOZ Y SUBS (Manual para que no fallen)
    print("🔊 Generando voz y mapa de palabras...")
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

    # 3. GENERAR 3 IMÁGENES PARA EL MOVIMIENTO
    print("🖼️ Generando secuencia de 3 imágenes...")
    for i in range(1, 4):
        seed = random.randint(1, 9999) # Cambiamos la semilla para que sean distintas
        url = f"https://image.pollinations.ai/prompt/cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical?width=720&height=1280&nologo=true&seed={seed}"
        with open(f"static/img{i}_{video_id}.jpg", "wb") as f:
            f.write(requests.get(url).content)
        print(f"✅ Imagen {i} lista.")

    # 4. MONTAJE ÉPICO (3 Imágenes + Transiciones + Zoom + Subs)
    print("🎥 Montando secuencia cinematográfica...")
    # Estilo de subtítulos: Amarillo neón, más grandes y centrados
    estilo = "FontName=Arial,FontSize=28,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=70"
    
    # Este comando une las 3 fotos, les da movimiento y fundido (crossfade)
    comando = (
        f'ffmpeg -y '
        f'-loop 1 -t 15 -i static/img1_{video_id}.jpg '
        f'-loop 1 -t 15 -i static/img2_{video_id}.jpg '
        f'-loop 1 -t 15 -i static/img3_{video_id}.jpg '
        f'-i {f_voz} '
        f'-filter_complex "[0:v]scale=1280:2275,zoompan=z=\'1.03+0.0005*in\':d=1:s=720x1280,fade=t=out:st=14:d=1[v1]; '
        f'[1:v]scale=1280:2275,zoompan=z=\'1.03+0.0005*in\':d=1:s=720x1280,fade=t=in:st=0:d=1,fade=t=out:st=14:d=1[v2]; '
        f'[2:v]scale=1280:2275,zoompan=z=\'1.03+0.0005*in\':d=1:s=720x1280,fade=t=in:st=0:d=1[v3]; '
        f'[v1][v2][v3]concat=n=3:v=1:a=0,subtitles=\'{f_subs}\':force_style=\'{estilo}\'[v]" '
        f'-map "[v]" -map 3:a -c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart -shortest {f_final}'
    )
    
    os.system(comando)
    
    # Limpieza de archivos temporales
    for i in range(1, 4): os.remove(f"static/img{i}_{video_id}.jpg")
    os.remove(f_voz)
    print(f"🚀 VIDEO TERMINADO: {f_final}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
