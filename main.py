import argparse, os, asyncio, edge_tts, requests
import google.generativeai as genai

# Nuestro traductor de tiempo (indestructible)
def tiempo_a_vtt(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

async def fabricar_video(tema):
    print(f"🎬 MODO SUPER-PRODUCCIÓN INICIADO: {tema}")
    os.makedirs("static", exist_ok=True)
    
    for f in ["static/voz.mp3", "static/subs.vtt", "static/fondo.jpg", "static/video_final.mp4"]:
        if os.path.exists(f): os.remove(f)

    # --- 1. GUIONISTA EXPERTO (Largo y Viral) ---
    api_key = os.environ.get("GEMINI_API_KEY")
    guion_reserva = f"¿Crees que lo sabes todo sobre {tema}? Prepárate para descubrir un secreto que cambiará tu forma de verlo."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Le damos instrucciones precisas para un video de ~1 minuto
        prompt = f"""Escribe un guion épico y misterioso para un video viral corto sobre: {tema}. 
        Debe tener unas 100 a 120 palabras. 
        Estructura: 
        1. Empieza con un gancho brutal que haga que la gente se quede a mirar.
        2. Cuenta un secreto, leyenda o dato fascinante y poco conocido.
        3. Termina con una frase impactante. 
        IMPORTANTE: Escribe SOLO el texto que se va a narrar, sin emojis, sin corchetes y sin texto entre asteriscos."""
        
        res = model.generate_content(prompt, safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ])
        
        # Limpiamos posibles asteriscos que a veces pone la IA para negritas
        if res.text: 
            guion = res.text.strip().replace('*', '').replace('"', '')
        else:
            guion = guion_reserva
            
    except Exception as e: 
        print("⚠️ Error Gemini:", e)
        guion = guion_reserva

    # --- 2. VOZ Y SUBS ---
    print("🔊 Grabando narración...")
    communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")
    subs_vtt = ["WEBVTT\n\n"]
    
    with open("static/voz.mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                inicio = chunk["offset"] / 10000
                fin = (chunk["offset"] + chunk["duration"]) / 10000
                subs_vtt.append(f"{tiempo_a_vtt(inicio)} --> {tiempo_a_vtt(fin)}\n{chunk['text']}\n\n")
                
    with open("static/subs.vtt", "w", encoding="utf-8") as f: 
        f.writelines(subs_vtt)

    # --- 3. IMAGEN IA ---
    print("🖼️ Creando arte...")
    prompt_ia = f"epic%20cinematic%20{tema.replace(' ', '%20')}%208k%20vertical"
    img_data = requests.get(f"https://image.pollinations.ai/prompt/{prompt_ia}?width=480&height=854&nologo=true").content
    with open("static/fondo.jpg", "wb") as f: f.write(img_data)

    # --- 4. MONTAJE ---
    print("🎥 Montando película...")
    # Ajusté un pelín el tamaño de la letra para que quepan bien las frases largas
    estilo = "FontName=Arial,FontSize=25,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=50"
    comando = (
        f'ffmpeg -y -loop 1 -i static/fondo.jpg -i static/voz.mp3 '
        f'-c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart '
        f'-vf "scale=480:854,subtitles=static/subs.vtt:force_style=\'{estilo}\'" '
        f'-c:a aac -shortest static/video_final.mp4'
    )
    os.system(comando)
    print("✅ PRODUCCION TERMINADA")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
