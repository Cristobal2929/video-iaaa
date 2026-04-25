import os
import re
import fitz
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TESHUÁ - Fenix AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def clean_ai_response(text: str) -> str:
    match = re.search(r'(<div.*>.*</div>|<article.*>.*</article>|<h[1-6]>.*)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    text = re.sub(r'^```html\s*', '', text)
    text = re.sub(r'```$', '', text)
    return text.strip()

def extract_pdf_context(path: str) -> str:
    try:
        if not os.path.exists(path):
            return "El Código 650 es la clave unificada que conecta Yesod, Jojmá y el despertar."
        doc = fitz.open(path)
        return "".join([page.get_text() for page in doc[:15]])
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
async def ver_portal():
    ruta_html = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "app", "templates", "editor.html")
    if os.path.exists(ruta_html):
        return FileResponse(ruta_html)
    return {"mensaje": "El lienzo de TESHUÁ aún no se encuentra en la ruta especificada."}

@app.get("/generar-portal")
async def generar_portal(nombre: str, fecha: str):
    contexto = extract_pdf_context("../TESHUA_El_Puzzle_Espiritual.pdf")
    
    prompt_maestro = f"""
    Actúa como un Artista de Arte Sacro y Oráculo. Basado en TESHUÁ: {contexto[:2000]}...
    Genera un reporte místico para el buscador '{nombre}' nacido el '{fecha}'. Relaciónalo con el Código 650.
    REGLAS: Solo responde con HTML puro usando Tailwind CSS (text-[#BF953F]). Usa font-cinzel para títulos y font-playfair para textos. NADA DE EXPLICACIONES EXTRAS.
    """
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_maestro}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=3000,
        )
        return {"html": clean_ai_response(chat.choices[0].message.content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
