import argparse
import os

def generar_video(tema):
    print(f"🚀 Iniciando motor Fénix para el tema: '{tema}'")

    # Crear carpeta 'static' si no existe
    if not os.path.exists("static"):
        os.makedirs("static")
        print("📁 Carpeta 'static' creada correctamente.")

    ruta_salida = "static/video_final.mp4"

    print(f"🧠 Procesando guion e imágenes para: {tema}...")
    print("🎬 Renderizando vídeo en formato vertical...")

    try:
        from moviepy.editor import ColorClip
        
        # Clip vertical de color negro de 3 segundos para probar la tubería
        clip = ColorClip(size=(1080, 1920), color=(15, 15, 15), duration=3)
        clip.write_videofile(ruta_salida, fps=24, codec="libx264", logger=None)
        print(f"✅ ¡ÉXITO! Vídeo guardado y listo en: {ruta_salida}")

    except ImportError:
        print("⚠️ No se encontró 'moviepy'. Instalalo en requirements.txt.")
        with open(ruta_salida, "w") as f:
            f.write("Este es un archivo de video simulado.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor de generación de vídeos")
    parser.add_argument("--tema", type=str, required=True, help="Tema desde la web")
    args = parser.parse_args()

    generar_video(args.tema)
