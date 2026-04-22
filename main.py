import argparse, os, asyncio, edge_tts, requests, random, subprocess, re
import google.generativeai as genai

def tiempo_a_ass(ms):
s, ms = divmod(int(ms), 1000)
m, s = divmod(s, 60)
h, m = divmod(m, 60)
return f"{h}:{m:02d}:{s:02d}.{int(ms/10):02d}"

=========================

DETECTAR FRASES

=========================

def dividir_frases(texto):
frases = re.split(r'[.!?]+', texto)
return [f.strip() for f in frases if len(f.strip()) > 10][:3]  # max 3 escenas

async def fabricar_video(tema, video_id):
print(f"🧠 MODO INTELIGENTE: {tema}")
os.makedirs("static", exist_ok=True)

f_voz = "voz.mp3"
f_subs = "subs.ass"
f_final = f"static/{video_id}.mp4"
f_music = "music.mp3"

# =========================
# 1. GUION INTELIGENTE
# =========================
api_key = os.environ.get("GEMINI_API_KEY")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Crea un guion viral sobre {tema}.
    Usa frases cortas.
    Mucho impacto emocional.
    """

    res = model.generate_content(prompt)
    guion = res.text.strip().replace("*", "")

except:
    guion = f"No deberías ignorar esto sobre {tema}..."

frases = dividir_frases(guion)

# =========================
# 2. VOZ + SUBS DINÁMICOS
# =========================
communicate = edge_tts.Communicate(guion, "es-ES-AlvaroNeural")

subs = []
with open(f_voz, "wb") as f:
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            f.write(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            inicio = tiempo_a_ass(chunk["offset"]/10000)
            fin = tiempo_a_ass((chunk["offset"]+chunk["duration"])/10000)
            palabra = chunk["text"]

            # 🎯 palabras importantes
            if len(palabra) > 6:
                estilo = "{\\fs70\\c&H0000FF&\\bord4}"
            else:
                estilo = "{\\fs60\\c&H00FFFF&\\bord3}"

            subs.append(
                f"Dialogue: 0,{inicio},{fin},Default,,0,0,0,,{estilo}{palabra}"
            )

with open(f_subs, "w", encoding="utf-8") as f:
    f.write("""[Script Info]

ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BorderStyle, Outline, Shadow, Alignment
Style: Default,Arial,60,&H00FFFF00,&H00000000,1,3,0,2

[Events]
Format: Layer, Start, End, Style, Text
""")
f.write("\n".join(subs))

# =========================
# 3. IMÁGENES POR ESCENA
# =========================
imgs = []
for i, frase in enumerate(frases):
    seed = random.randint(1,999999)
    prompt_img = f"cinematic dramatic {frase} 8k vertical"
    url = f"https://image.pollinations.ai/prompt/{prompt_img.replace(' ','%20')}?width=720&height=1280&seed={seed}"

    nombre = f"img{i}.jpg"
    with open(nombre,"wb") as f:
        f.write(requests.get(url).content)

    imgs.append(nombre)

# =========================
# 4. MÚSICA
# =========================
music_url = "https://cdn.pixabay.com/download/audio/2022/10/19/audio_suspense.mp3"
with open(f_music,"wb") as f:
    f.write(requests.get(music_url).content)

# =========================
# 5. EFECTOS INTELIGENTES
# =========================
fps = 30
dur = float(os.popen(f"ffprobe -i {f_voz} -show_entries format=duration -v quiet -of csv=p=0").read())
dur_img = dur / len(imgs)
frames = int(dur_img * fps)

filtros = []
for i in range(len(imgs)):
    # zoom dinámico aleatorio
    zoom_type = random.choice([
        "1.0+0.003*on",
        "1.2-0.002*on",
        "1.0+0.004*sin(on/10)"
    ])

    filtros.append(
        f"[{i}:v]scale=1280:2275,"
        f"zoompan=z='{zoom_type}':d={frames}:s=720x1280:fps={fps},"
        f"eq=contrast=1.2:brightness=0.05,"
        f"fade=t=in:st=0:d=0.5,fade=t=out:st={dur_img-0.5}:d=0.5[v{i}]"
    )

concat = "".join([f"[v{i}]" for i in range(len(imgs))])

filtro_final = (
    "; ".join(filtros) +
    f"; {concat}concat=n={len(imgs)}:v=1:a=0,"
    f"subtitles={f_subs},fps=30[v]"
)

# =========================
# 6. RENDER FINAL PRO
# =========================
inputs = " ".join([f"-loop 1 -t {dur_img} -i {img}" for img in imgs])

cmd = f"""
ffmpeg -y {inputs} -i {f_voz} -i {f_music} \
-filter_complex "{filtro_final}; \
[{len(imgs)}:a]volume=1.2[a1]; \
[{len(imgs)+1}:a]volume=0.25[a2]; \
[a1][a2]amix=inputs=2:duration=shortest[a]" \
-map "[v]" -map "[a]" \
-c:v libx264 -pix_fmt yuv420p \
-shortest \
{f_final}
"""

subprocess.run(cmd, shell=True)

# =========================
# CLEAN
# =========================
for img in imgs:
    os.remove(img)

os.remove(f_voz)
os.remove(f_music)
os.remove(f_subs)

print(f"🎬 VIDEO INTELIGENTE: {f_final}")

if name == "main":
parser = argparse.ArgumentParser()
parser.add_argument("--tema", type=str)
parser.add_argument("--id", type=str, required=True)

args = parser.parse_args()
asyncio.run(fabricar_video(args.tema, args.id))

