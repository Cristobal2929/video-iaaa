import os, json, subprocess, base64, requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") # Se configura en los Secrets de GitHub
TALLER = "." # Se ejecuta directamente en la carpeta workspace

def validar_fotograma(ruta_img, keyword):
    if not GEMINI_API_KEY: return True
    try:
        with open(ruta_img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [
                {"text": f"Responde solo SI o NO. ¿Esta imagen representa: {keyword}?"},
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded_string}}
            ]}]
        }
        res = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        return "SI" in res.json()['candidates'][0]['content']['parts'][0]['text'].strip().upper()
    except:
        return True

if __name__ == "__main__":
    print("⚡ Iniciando procesamiento en la nube...")
    
    with open("paquete.json", "r") as f:
        datos = json.load(f)

    frases = [escena["frase"] for escena in datos["escenas"]]
    guion_completo = ". ".join(frases) + "."
    
    print("🎙️ Generando voz neuronal...")
    os.system(f'edge-tts --voice es-ES-AlvaroNeural --text "{guion_completo}" --write-media voz.mp3')
    dur_audio = float(subprocess.check_output('ffprobe -i voz.mp3 -show_entries format=duration -v quiet -of csv=p=0', shell=True).decode().strip())
    dur_escena = dur_audio / len(datos["escenas"])

    clips_list = []
    
    print("👁️ Validando y editando escenas...")
    for escena in datos["escenas"]:
        raw = escena["archivo"]
        frame = f"frame_{escena['id']}.jpg"
        ready = f"ready_{escena['id']}.mp4"
        
        # Saca un fotograma y valida
        os.system(f'ffmpeg -y -i {raw} -ss 00:00:01 -vframes 1 {frame} > /dev/null 2>&1')
        
        if validar_fotograma(frame, escena["keyword"]):
            print(f"✅ Clip {escena['id']} validado por IA.")
        else:
            print(f"⚠️ Clip {escena['id']} no tiene sentido visual. Se usará igual pero necesita revisión.")
            
        # Edición pesada de FFmpeg (la hace el servidor de GitHub, no tu móvil)
        os.system(f'ffmpeg -y -i {raw} -t {dur_escena} -vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30" -c:v libx264 -preset fast -an {ready} > /dev/null 2>&1')
        clips_list.append(ready)

    # Generar subtítulos
    with open("subs.srt", "w", encoding="utf-8") as f:
        for idx, frase in enumerate(frases, start=1):
            start, end = (idx - 1) * dur_escena, idx * dur_escena
            def f_time(s): return f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{int(s%60):02d},{int((s%1)*1000):03d}"
            f.write(f"{idx}\n{f_time(start)} --> {f_time(end)}\n{frase}\n\n")

    print("🎬 Ensamblando vídeo final...")
    with open("list.txt", "w") as f:
        for c in clips_list: f.write(f"file '{c}'\n")

    estilo = "FontName=Arial,Bold=1,FontSize=28,PrimaryColour=&H00FFFF,OutlineColour=&H000000,BorderStyle=1,Outline=4,Shadow=2,Alignment=2,MarginV=130"
    os.system(f'ffmpeg -y -f concat -safe 0 -i list.txt -i voz.mp3 -vf "subtitles=subs.srt:force_style=\'{estilo}\'" -c:v libx264 -crf 23 -c:a aac -shortest VIDEO_FINAL.mp4')
    print("🏆 Renderización completa.")
