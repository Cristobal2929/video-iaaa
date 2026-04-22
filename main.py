import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 REPARANDO SUPER-PRODUCCIÓN: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz = f"static/voz_{video_id}.mp3"
    f_subs = f"static/subs_{video_id}.vtt"
    f_img = f"static/fondo_{video_id}.jpg"
    f_final = f"static/{video_id}.mp4"

    # 1. GUION ROBUSTO
    guion_reserva = f"El misterio de {tema} ha permanecido oculto durante demasiado tiempo. Muchos han intentado descubrir la verdad, pero pocos han regresado con respuestas claras. Hoy exploramos las sombras de este fenómeno fascinante que desafía toda lógica conocida."
    
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escribe un guion épico y misterioso sobre {tema}. Unas 100 palabras. Solo texto."
        res = model.generate_content(prompt)
        guion = res.text.strip().replace('*', '').replace('"', '')
        if len(guion.split()) < 20: guion = guion_reserva
    except:
        guion = guion_reserva

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

    # 3. IMAGEN IA
    img_url = f"https://image.pollinations.ai/prompt/epic%20cinematic%20{tema.replace(' ', '%20')}%208k%20vertical?width=720&height=1280&nologo=true"
    with open(f_img, "wb") as f: f.write(requests.get(img_url).content)

    # 4. MONTAJE ESTABILIZADO (Zoom suave + Subtítulos)
    print("🎥 Montando vídeo final...")
    estilo = "FontName=Arial,FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=80"
    
    # Filtro zoompan simplificado para evitar errores de memoria
    filtro_video = (
        f"scale=1280:2275,zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':s=720x1280,"
        f"subtitles='{f_subs}':force_style='{estilo}'"
    )
    
    comando = (
        f'ffmpeg -y -loop 1 -i {f_img} -i {f_voz} '
        f'-vf "{filtro_video}" '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-c:a aac -shortest {f_final}'
    )
    
    os.system(comando)
    
    # Limpieza
    for temp in [f_voz, f_subs, f_img]:
        if os.path.exists(temp): os.remove(temp)
    print(f"✅ Proceso finalizado: {f_final}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
