import random

def generate_script(topic, duration=30):

    hooks = [
        f"Nadie te cuenta esto sobre {topic}...",
        f"Lo que vas a ver de {topic} te va a sorprender...",
        f"{topic}: la verdad oculta detrás de esto...",
    ]

    story = [
        "Todo empezó normal...",
        "Pero algo cambió de forma inesperada...",
        "El misterio empezó a crecer...",
        "El final nadie lo esperaba..."
    ]

    return random.choice(hooks) + "\n\n" + "\n".join(story)
