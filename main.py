import asyncio
import random

def generar_guion_y_keywords(tema):

    # EVITA errores de IA
    guiones = [
        f"Historia sobre {tema} que sorprende al mundo",
        f"Un relato poderoso sobre {tema}",
        f"El secreto oculto de {tema}"
    ]

    keywords = ["historia", tema, "viral", "impactante"]

    guion = random.choice(guiones)

    return guion, keywords


async def run(tema):

    print("🎬 Tema:", tema)

    guion, keywords = generar_guion_y_keywords(tema)

    print("📝 Guion:", guion)
    print("🔑 Keywords:", keywords)

    # SIMULA VIDEO FINAL
    video_url = "https://raw.githubusercontent.com/Cristobal2929/video-iaaa/main/video_final.mp4"

    with open("public_url.txt", "w") as f:
        f.write(video_url)

    print("✅ VIDEO LISTO:", video_url)


if __name__ == "__main__":
    import sys
    tema = sys.argv[2] if "--tema" in sys.argv else "terror"
    asyncio.run(run(tema))
