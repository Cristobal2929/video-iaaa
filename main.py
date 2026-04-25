import PIL.Image
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
import os, time, random, glob, requests, textwrap, asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, concatenate_audioclips, concatenate_videoclips, CompositeAudioClip
from dotenv import load_dotenv

# FORZAMOS A PYTHON A LEER TUS LLAVES SECRETAS
load_dotenv() 

OUTPUT_FOLDER = "docs/videos"
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

def obtener_video_contextual(frase, duracion):
    if not PEXELS_API_KEY: 
        print("❌ AVISO: No se encontró la llave de Pexels.")
        return ColorClip(size=(720, 1280), color=(20, 20, 30), duration=duracion)
    
    limpiar = "".join([c for c in frase if c.isalnum() or c==" "])
    palabras = [w for w in limpiar.lower().split() if len(w) > 3]
    search_queries = palabras[:2] + ["business", "success", "technology", "abstract"]
    
    for query in search_queries:
        try:
            print(f"🔍 Buscando fondo Pexels: {query}...")
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
            r = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=10)
            
            if r.status_code != 200:
                print(f"❌ Error API Pexels: {r.status_code}")
                continue
                
            data = r.json()
            if data.get("videos") and len(data["videos"]) > 0:
                video_data = random.choice(data["videos"])
                link = next((f['link'] for f in video_data['video_files'] if f['width'] >= 720), video_data['video_files'][0]['link'])
                temp_name = f"temp_{random.randint(0,99999)}.mp4"
                
                with open(temp_name, "wb") as f: 
                    f.write(requests.get(link).content)
                
                clip = VideoFileClip(temp_name)
                scale = max(720/clip.w, 1280/clip.h)
                clip = clip.resize(scale).crop(x_center=clip.resize(scale).w/2, y_center=clip.resize(scale).h/2, width=720, height=1280)
                
                if clip.duration < duracion:
                    clip = concatenate_videoclips([clip] * (int(duracion/clip.duration)+1)).subclip(0, duracion)
                else:
                    clip = clip.subclip(0, duracion)
                
                return clip
        except Exception as e:
            print(f"❌ Excepción Pexels: {e}")
            continue
            
    print("⚠️ No se encontró vídeo en Pexels, usando fondo negro por seguridad.")
    return ColorClip(size=(720, 1280), color=(30, 30, 40), duration=duracion)

def generar_guion_ia(tema):
    print("⚡ GENERANDO GUION PROFESIONAL CON IA...")
    prompt = (
        "Actúa como el Copywriter Principal de Digital Riders (digitalriders.com), agencia de marketing digital premium. "
        f"Crea un guion para un Reel viral sobre: '{tema}'. "
        "REGLAS: "
        "1. Gancho inicial, valor directo y CTA claro. "
        "2. Devuelve entre 6 y 10 frases. CADA FRASE EN UNA LÍNEA NUEVA. "
        "3. Persuasivo y seguro. Máximo 12 palabras por frase. "
        "4. Cero emojis, cero comillas. "
        "5. La última frase debe ser obligatoriamente: 'Lleva tu negocio al siguiente nivel. Link en el perfil.'"
    )
    if GROQ_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {"model": "llama-3.3-70b-versatile", "temperature": 0.6, "messages": [{"role": "system", "content": prompt}]}
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            return [l.strip() for l in r.json()["choices"][0]["message"]["content"].split('\n') if l.strip() and not l.startswith("Aquí")]
        except: pass
    return ["Domina el marketing digital hoy.", "Lleva tu negocio al siguiente nivel. Link en el perfil."]

async def crear_audio_ia(texto, archivo_salida):
    voz_elegida = os.getenv("VOZ_VIDEO", "Alvaro")
    voz_codigo = f"es-ES-{voz_elegida}Neural"
    await edge_tts.Communicate(texto, voz_codigo).save(archivo_salida)

def generar_video():
    tema_video = os.getenv("TEMA_VIDEO", "Emprendimiento")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    frases = generar_guion_ia(tema_video)
    clips_voz, clips_video, clips_texto = [], [], []
    t_actual = 0
    
    for i, texto in enumerate(frases):
        if not texto: continue
        temp_audio = f"voz_{i}.mp3"
        asyncio.run(crear_audio_ia(texto, temp_audio))
        voz = AudioFileClip(temp_audio)
        clips_voz.append(voz)
        
        v_clip = obtener_video_contextual(texto, voz.duration)
        clips_video.append(v_clip.set_start(t_actual))
        
        txt_wrapped = "\n".join(textwrap.wrap(texto, width=22))
        txt = TextClip(txt=txt_wrapped, fontsize=58, color='white', font=FONT_PATH, stroke_color='black', stroke_width=4, method='label', align='center').set_position(('center', 800)).set_start(t_actual).set_duration(voz.duration)
        clips_texto.append(txt)
        t_actual += voz.duration
        
    voz_completa = concatenate_audioclips(clips_voz)
    video_fondo = concatenate_videoclips(clips_video, method="compose")
    audio_final = voz_completa
    
    canciones = glob.glob("música/negocio/*.mp3") + glob.glob("musica/negocio/*.mp3")
    if canciones:
        bg_music = AudioFileClip(random.choice(canciones))
        if bg_music.duration < voz_completa.duration:
            bg_music = concatenate_audioclips([bg_music] * (int(voz_completa.duration / bg_music.duration) + 1))
        bg_music = bg_music.subclip(0, voz_completa.duration).volumex(0.15)
        audio_final = CompositeAudioClip([bg_music, voz_completa])
        
    final = CompositeVideoClip([video_fondo.set_audio(audio_final)] + clips_texto, size=(720, 1280))
    nombre = f"{OUTPUT_FOLDER}/viral_dr_{int(time.time())}.mp4"
    final.write_videofile(nombre, fps=24, codec="libx264", audio_codec="aac", threads=2)
    # Limpiamos basurilla
    for f in glob.glob("voz_*.mp3"): os.remove(f)
    print("✅ VÍDEO PANTALLA COMPLETA LISTO.")

if __name__ == "__main__":
    generar_video()
