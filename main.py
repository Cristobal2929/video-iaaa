import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 HISTORIA ÚNICA: {tema} [{video_id}]")
    os.makedirs("static", exist_ok=True)
    
    # Nombres de archivo 100% únicos
    f_voz = f"static/voz_{video_id}.mp3"
    f_subs = f"static/subs_{video_id}.vtt"
    f_img = f"static/fondo_{video_id}.jpg"
    f_final = f"static/{video_id}.mp4"

    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Escribe un guion épico sobre {tema} para un video de 1 minuto. Unas 110 palabras. Solo texto, sin asteriscos ni corchetes."
        res = model.generate_content(prompt, safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}])
        guion = res.text.strip().replace('*', '').replace('"', '')
    except:
        guion = f"El misterio de {tema} es algo asombroso. Prepárate para descubrir la verdad oculta."

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

    img_url = f"https://image.pollinations.ai/prompt/cinematic%20epic%20{tema.replace(' ', '%20')}%208k%20vertical?width=480&height=854&nologo=true"
    with open(f_img, "wb") as f: f.write(requests.get(img_url).content)

    estilo = "FontName=Arial,FontSize=26,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=60"
    comando = (
        f'ffmpeg -y -loop 1 -i {f_img} -i {f_voz} '
        f'-vf "scale=480:854,subtitles=\'{f_subs}\':force_style=\'{estilo}\'" '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-c:a aac -shortest {f_final}'
    )
    os.system(comando)
    
    # Borramos los archivos intermedios para no colapsar la memoria, nos quedamos solo con el MP4
    for temp in [f_voz, f_subs, f_img]:
        if os.path.exists(temp): os.remove(temp)
    print("✅ Guardado en el historial con éxito")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
