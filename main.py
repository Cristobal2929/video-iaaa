import argparse
import os
import google.generativeai as genai

def generar_video(tema):
    print(f"🚀 Iniciando motor con Gemini para: '{tema}'")
    if not os.path.exists("static"):
        os.makedirs("static")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: No hay API Key.")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Haz un guion de TikTok de 20 segundos sobre: {tema}. Solo el texto del narrador."
        respuesta = model.generate_content(prompt)
        print(f"✅ GUION GENERADO:\n{respuesta.text}")
    except Exception as e:
        print(f"❌ Error en Gemini: {e}")

    # Video negro temporal
    try:
        from moviepy.editor import ColorClip
        clip = ColorClip(size=(1080, 1920), color=(20, 20, 20), duration=3)
        clip.write_videofile("static/video_final.mp4", fps=24, codec="libx264", logger=None)
        print("✅ Archivo de video listo.")
    except:
        print("⚠️ Error con moviepy.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", type=str, required=True)
    args = parser.parse_args()
    generar_video(args.tema)
