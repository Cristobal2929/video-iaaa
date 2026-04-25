import re

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# El prompt definitivo para que la IA estudie el libro y cree el Software
nuevo_prompt_pdf = """
        prompt_sistema = (
            "Eres un Desarrollador Frontend Senior, experto en Inteligencia Artificial y Algoritmos. Tu misión es leer, analizar y comprender profundamente este libro/PDF sobre misticismo y numerología: "
            f"'{texto[:6000]}'.\\n\\n"
            "REGLAS OBLIGATORIAS PARA EL CÓDIGO:\\n"
            "1. Devuelve un HTML5 completo con Tailwind CSS (<script src=\\"https://cdn.tailwindcss.com\\"></script>).\\n"
            "2. Diseña una interfaz mística, premium y espectacular (fondos oscuros, destellos cósmicos o dorados, tipografía elegante).\\n"
            "3. LA HERRAMIENTA VIVA (MOTOR TESHUÁ): Tienes que programar en JavaScript un motor interactivo que HAGA EXACTAMENTE LO QUE ENSEÑA EL PDF.\\n"
            "4. Crea un formulario moderno donde el usuario escriba su Nombre Completo y su Fecha de Nacimiento.\\n"
            "5. El JavaScript debe procesar esos datos al instante aplicando las fórmulas del libro:\\n"
            "   - Calcular la Numerología (reduciendo números) y simular la Guematría.\\n"
            "   - Desglosar las fases del alma (Manifestación, Prueba, Liberación, Servicio).\\n"
            "   - Mostrar el Número del Destino, Número del Alma y los Arquetipos que le corresponden (Elías, José, Cristo, etc.).\\n"
            "6. Muestra los resultados como un 'Mensaje del Alma' personalizado y revelador, igual que lo hace el autor en el libro.\\n"
            "7. Usa JavaScript para crear animaciones suaves cuando aparezcan los resultados.\\n"
            "DEVUELVE ÚNICAMENTE EL CÓDIGO HTML PURO."
        )
"""

# Reemplazamos el prompt anterior del PDF por este nuevo súper-prompt
codigo = re.sub(
    r'prompt_sistema = \(\s*"Eres un Diseñador Web Experto.*?DEVUELVE ÚNICAMENTE EL HTML PURO."\s*\)',
    nuevo_prompt_pdf.strip(),
    codigo,
    flags=re.DOTALL
)

with open('api/main.py', 'w', encoding='utf-8') as f:
    f.write(codigo)

print("✅ IA configurada para estudiar el PDF y crear la Herramienta Viva.")
