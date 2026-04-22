import argparse, os, asyncio, edge_tts, requests, random, subprocess
import google.generativeai as genai

def tiempo_a_ass(ms):
s, ms = divmod(int(ms), 1000)
m, s = divmod(s, 60)
h, m = divmod(m, 60)
return f"{h}:{m:02d}:{s:02d}.{int(ms/10):02d}"

async def fabricar_video(tema, video_id):
print(f"🔥 MODO VIRAL ACTIVADO: {tema}")
os.makedirs("static", exist_ok=True)

f_voz = "voz.mp3"
f_subs = "subs.ass"
f_final = f"static/{video_id}.mp4"
f_music = "music.mp3"

# =========================
# 1. GUION ULTRA VIRAL
# =========================
api_key = os.environ.get("GEMINI_API_KEY")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Crea un guion extremadamente adictivo sobre: {tema}.
    Estilo: TikTok viral.
    Frases cortas.
    Mucho suspenso.
    Gancho brutal en 3 segundos.
    """

    res = model.generate_content(prompt)
    guion = res.text.strip().replace("*", "")

except:
    guion = f"No deberías estar viendo esto sobre {tema}..."

# =========================
# 2. VOZ + SUBS KARAOKE
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

            subs.append(
                f"Dialogue: 0,{inicio},{fin},Default,,0,0,0,,{{\\fs60\\c&H00FFFF&\\bord3\\shad1}}{palabra}"
            )

# ASS HEADER (ESTILO TIKTOK)
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
# 3. IMÁGENES PRO
# =========================
estilos = [
    "dark cinematic horror lighting",
    "epic dramatic face shadow",
    "hyper realistic macro fear",
    "aerial apocalyptic view",
    "emotional portrait tears"
]

for i in range(1, 6):
    seed = random.randint(1,999999)
    prompt_img = f"{estilos[i-1]} {tema} 8k vertical"
    url = f"https://image.pollinations.ai/prompt/{prompt_img.replace(' ','%20')}?width=720&height=1280&seed={seed}"

    with open(f"img{i}.jpg","wb") as f:
        f.write(requests.get(url).content)

# =========================
# 4. MÚSICA VIRAL
# =========================
music_url = "https://cdn.pixabay.com/download/audio/2022/10/19/audio_suspense.mp3"
with open(f_music,"wb") as f:
    f.write(requests.get(music_url).content)

# =========================
# 5. EFECTOS PRO
# =========================
fps = 30
dur = float(os.popen(f"ffprobe -i {f_voz} -show_entries format=duration -v quiet -of csv=p=0").read())
dur_img = dur / 5
frames = int(dur_img * fps)

filtros = []
for i in range(5):
    filtros.append(
        f"[{i}:v]scale=1280:2275,"
        f"zoompan=z='1.0+0.004*on':d={frames}:s=720x1280:fps={fps},"
        f"eq=contrast=1.2:brightness=0.05,"
        f"fade=t=in:st=0:d=0.5,fade=t=out:st={dur_img-0.5}:d=0.5[v{i}]"
    )

concat = "".join([f"[v{i}]" for i in range(5)])

filtro_final = (
    "; ".join(filtros) +
    f"; {concat}concat=n=5:v=1:a=0,"
    f"subtitles={f_subs},"
    f"fps=30[v]"
)

# =========================
# 6. RENDER FINAL
# =========================
cmd = f"""
ffmpeg -y \
-loop 1 -t {dur_img} -i img1.jpg \
-loop 1 -t {dur_img} -i img2.jpg \
-loop 1 -t {dur_img} -i img3.jpg \
-loop 1 -t {dur_img} -i img4.jpg \
-loop 1 -t {dur_img} -i img5.jpg \
-i {f_voz} -i {f_music} \
-filter_complex "{filtro_final}" \
-map "[v]" -map 5:a -map 6:a \
-filter:a "[5:a]volume=1.2[a1];[6:a]volume=0.3[a2];[a1][a2]amix=inputs=2" \
-c:v libx264 -pix_fmt yuv420p \
-shortest \
{f_final}
"""

subprocess.run(cmd, shell=True)

# =========================
# CLEAN
# =========================
for i in range(1,6):
    os.remove(f"img{i}.jpg")

os.remove(f_voz)
os.remove(f_music)
os.remove(f_subs)

print(f"🎬 VIDEO VIRAL CREADO: {f_final}")

if name == "main":
parser = argparse.ArgumentParser()
parser.add_argument("--tema", type=str)
parser.add_argument("--id", type=str, required=True)

args = parser.parse_args()
asyncio.run(fabricar_video(args.tema, args.id))

