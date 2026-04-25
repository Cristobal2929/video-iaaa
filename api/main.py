from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import re
import os
import requests

app = FastAPI(title="TESHUÁ - Fenix AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_ai_response(text):
    """Extrae únicamente el bloque de código HTML."""
    match = re.search(r'<html>.*</html>', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    return text

def extract_pdf_context(path):
    """Extrae conceptos clave del libro TESHUÁ."""
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text[:5000] # Contexto limitado para la ventana de tokens
    except Exception as e:
        return f"Error al leer PDF: {str(e)}"

@app.get("/generar-portal")
async def generar_portal(nombre: str, fecha: str):
    contexto = extract_pdf_context("TESHUA_El_Puzzle_Espiritual.pdf")
    
    # Aquí se integra la llamada a Groq / Llama 3.3 70B
    # El prompt debe forzar el uso de Cinzel y los hex de oro/marfil
    prompt_sacro = f"""
    Genera un reporte místico basado en: {contexto}.
    Usuario: {nombre}, Nacimiento: {fecha}.
    Estética: #FDFCF0 y #BF953F. 
    Usa Glassmorphism y Tailwind. 
    Responde solo con HTML.
    """
    
    # Simulación de respuesta filtrada
    html_sucio = "```html <html><body>...</body></html> ```" 
    html_puro = clean_ai_response(html_sucio)
    
    return {"html": html_puro}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
