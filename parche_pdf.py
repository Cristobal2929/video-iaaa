import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# Inyectamos la librería al inicio
if "import fitz" not in codigo:
    codigo = "import fitz\n" + codigo

# Creamos el nuevo endpoint para PDF
nuevo_endpoint_pdf = """
@app.post("/generate/web-from-pdf")
async def api_generate_web_pdf(file: UploadFile = File(...)):
    try:
        # 1. Leer el PDF
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        texto_extraido = ""
        for page in doc:
            texto_extraido += page.get_text()
        
        # 2. Pedir a la IA que cree la web basada en ese contenido
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        prompt_sistema = (
            "Eres un Desarrollador Senior. Crea una Landing Page profesional BASADA EXCLUSIVAMENTE "
            f"en el siguiente contenido de un PDF: '{texto_extraido[:3000]}'. "
            "Usa Tailwind CSS, estructura limpia con menú, hero y secciones. "
            "Si el PDF menciona servicios o datos de contacto, inclúyelos. DEVUELVE SOLO HTML."
        )
        
        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "temperature": 0.5, "messages": [{"role": "system", "content": prompt_sistema}]}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers).json()
        html_code = r["choices"][0]["message"]["content"].replace("```html", "").replace("```", "").strip()
        
        return {"status": "success", "html": html_code}
    except Exception as e:
        return {"status": "error", "html": str(e)}
"""

# Insertar antes del generador de video para mantener orden
if "@app.post(\"/generate/video\")" in codigo:
    codigo = codigo.replace("@app.post(\"/generate/video\")", nuevo_endpoint_pdf + "\n@app.post(\"/generate/video\")")

with open('api/main.py', 'w', encoding='utf-8') as f:
    f.write(codigo)
print("✅ Motor de lectura de PDF integrado en el Backend.")
