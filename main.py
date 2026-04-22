import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tema', type=str, required=True)
    parser.add_argument('--id', type=str, required=True)
    args = parser.parse_args()

    print(f"🎬 Arrancando motor para: {args.tema}")
    
    # REVISIÓN DE LLAVES
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("❌ ERROR: No encuentro la PEXELS_API_KEY en los secretos de GitHub")
        return

    print("✅ Llave de Pexels detectada. Conectando...")

    # AQUÍ ES DONDE SUELE FALLAR
    try:
        # Simulamos la creación para ver si el flujo de guardado funciona
        # En tu código real, aquí es donde Pexels descarga.
        # Vamos a forzar un error si el tema es "miedo" para ver qué pasa
        if "miedo" in args.tema.lower():
             print("⚠️ Pexels no devolvió resultados para este tema.")
        
        # CREAMOS UN ARCHIVO DE PRUEBA REAL (No vacío)
        with open("video_final.mp4", "w") as f:
            f.write("Este es un archivo de video simulado para probar el sistema de guardado.")
        
        print(f"✅ Archivo creado con éxito para el ID: {args.id}")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")

if __name__ == "__main__":
    main()
