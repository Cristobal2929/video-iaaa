with open('main.py', 'r') as f:
    code = f.read()

new_func = """def generar_guion_ia(tema):
    print("⚡ GENERANDO GUION PROFESIONAL CON LLAMA-3.3-70B...")
    prompt = (
        f"Actúa como el Copywriter Principal de Digital Riders (digitalriders.com), una agencia de marketing digital premium y vanguardista. "
        f"Tu misión es crear el guion para un video corto (Reel/TikTok/Short) altamente viral y profesional sobre el tema: '{tema}'. "
        f"REGLAS VITALES:\n"
        f"1. ESTRUCTURA: Un gancho inicial impactante en el primer segundo, desarrollo directo de alto valor, y un CTA claro.\n"
        f"2. FORMATO: Devuelve entre 6 y 10 frases. CADA FRASE EN UNA LÍNEA NUEVA.\n"
        f"3. ESTILO: Persuasivo, moderno, seguro y experto. Frases de máximo 12 palabras para que la voz de IA suene perfecta, respire de forma natural y mantenga la retención del usuario.\n"
        f"4. PROHIBIDO: Usar emojis, comillas, hashtags, numeraciones o texto de relleno (como 'Aquí tienes el guion').\n"
        f"5. CIERRE: La última frase DEBE ser obligatoriamente: 'Lleva tu negocio al siguiente nivel. Link en el perfil.'"
    )
    if GROQ_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {"model": "llama-3.3-70b-versatile", "temperature": 0.6, "messages": [{"role": "system", "content": prompt}]}
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            return [l.strip() for l in r.json()["choices"][0]["message"]["content"].split('\n') if l.strip() and not l.startswith("Aquí")]
        except: pass
    return ["La inteligencia artificial está cambiando las reglas del juego.", "En Digital Riders sabemos cómo aprovecharla para escalar tus ventas.", "Lleva tu negocio al siguiente nivel. Link en el perfil."]"""

# Reemplazamos la función antigua por la nueva con precisión quirúrgica
if "def generar_guion_ia(tema):" in code and "async def crear_audio_alvaro" in code:
    parte1 = code.split("def generar_guion_ia(tema):")[0]
    parte2 = "async def crear_audio_alvaro" + code.split("async def crear_audio_alvaro")[1]
    
    with open('main.py', 'w') as f:
        f.write(parte1 + new_func + "\n\n" + parte2)
    print("✅ Cerebro de Copywriting de Digital Riders activado.")
else:
    print("❌ No se encontró la función. El código ya estaba modificado.")
