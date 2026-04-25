import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

nuevo_endpoint = """# --- ENDPOINT: GENERADOR WEB ---
@app.post("/generate/web")
async def api_generate_web(data: dict):
    prompt_usuario = data.get("prompt")
    try:
        # 1. Buscamos imágenes premium de Pexels sobre el tema
        imagenes = obtener_imagenes_pexels_web(prompt_usuario)
        imgs_str = ", ".join(imagenes)
        
        # 2. Invocamos al Programador Senior de Digital Riders
        import requests, os
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        
        prompt_sistema = (
            "Eres el Desarrollador Frontend Senior de la agencia 'Digital Riders'. "
            f"Diseña el código HTML5 de una Landing Page premium, moderna y ultra-rápida sobre: '{prompt_usuario}'. "
            "REGLAS VITALES:\\n"
            "1. Todo en un solo archivo (HTML, CSS interno y JS vanilla para animaciones o menús).\\n"
            "2. Usa Tailwind CSS vía CDN (<script src='https://cdn.tailwindcss.com'></script>).\\n"
            "3. Incluye una cabecera (Hero) impactante, sección de servicios/beneficios y un Call to Action (CTA) final.\\n"
            "4. Efectos visuales: Sombras, bordes redondeados, degradados sutiles y efectos 'hover' en botones.\\n"
            f"5. OBLIGATORIO: Usa estas imágenes reales de Pexels para los fondos e ilustraciones: {imgs_str}. "
            "6. DEVUELVE ÚNICAMENTE CÓDIGO HTML PURO. Nada de texto antes ni después (sin markdown)."
        )
        
        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "temperature": 0.6, "messages": [{"role": "system", "content": prompt_sistema}]}
        
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers).json()
        html_code = r["choices"][0]["message"]["content"]
        
        # Limpieza de markdown por si la IA se cuela
        html_code = html_code.replace("```html", "").replace("```", "").strip()
        
        return {"status": "success", "html": html_code}
    except Exception as e:
        return {"status": "error", "html": f"<h3 style='color:red;'>Error de IA: {str(e)}</h3>"}
"""

if "# --- ENDPOINT: GENERADOR WEB ---" in codigo and "# --- ENDPOINT: GENERADOR VIDEO ---" in codigo:
    parte_antes = codigo.split("# --- ENDPOINT: GENERADOR WEB ---")[0]
    parte_despues = codigo.split("# --- ENDPOINT: GENERADOR VIDEO ---")[1]
    
    codigo_final = parte_antes + nuevo_endpoint + "\n# --- ENDPOINT: GENERADOR VIDEO ---" + parte_despues
    
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(codigo_final)
    print("✅ Cerebro Frontend Senior y Pexels instalados al 100%.")
else:
    print("❌ No se encontraron los marcadores en el código.")
