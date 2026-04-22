import argparse, os, asyncio, google.generativeai as genai, edge_tts, requests

async def fabricar_video(tema):
    print(f"🎨 INICIANDO CREADOR DE ARTE IA para: {tema}")
    os.makedirs("static", exist_ok=True)
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ ERROR: Falta GEMINI_API_KEY")
        return

    # --- 1. GUION Y PROMPT VISUAL CON GEMINI ---
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Le pedimos el dato y una descripción para la IA de imagen
        prompt_ia = f"Dame un dato curioso corto sobre {tema}. Y luego, una frase en inglés que describa una imagen cinematográfica y épica sobre eso."
        res = model.generate_content(prompt_ia)
        texto_completo = res.text.strip().split('\n')
        guion = texto_completo[0]
        # Si Gemini nos da una descripción, la usamos; si no, inventamos una
        prompt_imagen = texto_completo[-1] if len(texto_completo) > 1 else f"Cinematic epic photography of {tema}, 8k, highly detailed"
        print(f"📝 Guion: {guion}")
    except Exception as e:
        guion = f"Hablemos sobre {tema}. Es un tema increible."
        prompt_imagen = f"Epic cinematic {tema}"
        print(f"⚠️ Error Gemini: {e}")

    # --- 2. VOZ ---
    print("🔊 Generando voz...")
    await edge_tts.Communicate(guion, "es-ES-AlvaroNeural").save("static/voz.mp3")

    # --- 3. GENERACIÓN DE ARTE IA (Pollinations) ---
    print(f"🖼️ Creando Arte IA único para el fondo...")
    # Limpiamos el prompt para la URL
    prompt_url = prompt_imagen.replace(" ", "%20")
    img_url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=720&height=1280&model=flux&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("static/fondo_ia.jpg", "wb") as f:
            f.write(img_data)
        print("✅ Imagen IA generada.")
    except Exception as e:
        print(f"❌ Falló la IA de imagen: {e}")
        return

    # --- 4. MONTAJE CINEMÁTICO (FFmpeg) ---
    print("🎥 Animando imagen y montando video...")
    # Aplicamos un efecto de "Zoom suave" (Ken Burns) a la imagen para que parezca video
    ffmpeg_cmd = (
        f'ffmpeg -y -loop 1 -i static/fondo_ia.jpg -i static/voz.mp3 '
        f'-vf "zoompan=z=\'zoom+0.001\':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=300:s=720x1280" '
        f'-c:v libx264 -preset ultrafast -tune stillimage -c:a copy -shortest static/video_final.mp4'
    )
    os.system(ffmpeg_cmd)
    
    if os.path.exists("static/video_final.mp4"):
        print("🚀 ¡OBRA DE ARTE TERMINADA!")
    else:
        print("❌ Error en el montaje final.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str)
    args = parser.parse_args()
    asyncio.run(fabricar_video(args.tema))
