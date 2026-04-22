import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema, video_id):
    print(f"🎬 SUPER-PRODUCCIÓN CON EFECTOS: {tema}")
    os.makedirs("static", exist_ok=True)
    
    f_voz = f"static/voz_{video_id}.mp3"
    f_subs = f"static/subs_{video_id}.vtt"
    f_img = f"static/fondo_{video_id}.jpg"
    f_final = f"static/{video_id}.mp4"

    # 1. GUION INQUEBRANTABLE (Largo siempre, pase lo que pase)
    guion_reserva = f"¿Alguna vez te has preguntado sobre el oscuro misterio de {tema}? Durante décadas, expertos de todo el mundo han intentado descifrar la verdad oculta detrás de este fenómeno. Muchos creen que es solo una simple leyenda urbana, pero los descubrimientos recientes apuntan a algo mucho más grande, aterrador y fascinante. Los documentos secretos revelan que quienes se acercan demasiado a la verdad terminan enfrentándose a lo impensable. La humanidad siempre ha temido a lo desconocido, pero la curiosidad nos empuja inevitablemente a seguir buscando respuestas en las sombras. ¿Estamos realmente preparados para descubrir lo que se esconde detrás del telón? Comparte este video si crees que nos ocultan la verdad y síguenos para explorar más misterios sin resolver."
    
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Escribe un guion épico y muy misterioso sobre {tema} para un video de TikTok. Mínimo 100 palabras. No uses corchetes, ni asteriscos.")
        guion = res.text.strip().replace('*', '').replace('"', '')
        # Si Gemini nos da un guion muy corto por error, forzamos la historia larga
        if len(guion.split()) < 30: 
            guion = guion_reserva
    except:
        guion = guion_reserva

    # 2. VOZ Y SUBTÍTULOS (Precisión milimétrica)
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

    # 3. IMAGEN ALTA CALIDAD (HD 720x1280)
    img_url = f"https://image.pollinations.ai/prompt/epic%20cinematic%20{tema.replace(' ', '%20')}%208k%20vertical?width=720&height=1280&nologo=true"
    with open(f_img, "wb") as f: f.write(requests.get(img_url).content)

    # 4. EFECTOS ESPECIALES DE CÁMARA (ZoomPan) Y SUBTÍTULOS
    print("🎥 Aplicando efecto de cámara lenta y quemando subtítulos...")
    estilo = "FontName=Arial,FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=80"
    
    # Hemos añadido un filtro "zoompan" que acerca la imagen lentamente al centro
    comando = (
        f'ffmpeg -y -loop 1 -i {f_img} -i {f_voz} '
        f'-vf "scale=720:1280,zoompan=z=\'1.02+0.0002*in\':x=\'iw/2-(iw/zoom)/2\':y=\'ih/2-(ih/zoom)/2\':d=3000:s=720x1280,subtitles=\'{f_subs}\':force_style=\'{estilo}\'" '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-c:a aac -shortest {f_final}'
    )
    os.system(comando)
    
    # Limpiamos basura
    for temp in [f_voz, f_subs, f_img]:
        if os.path.exists(temp): os.remove(temp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema, args.id))
