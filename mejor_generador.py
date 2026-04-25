import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# Definimos el nuevo prompt ultra-profesional
nuevo_prompt_sistema = """prompt_sistema = (
            "Eres el Desarrollador Frontend Senior de una agencia de élite. "
            f"Diseña una Landing Page premium, completa y moderna sobre: '{prompt_usuario}'. \\n\\n"
            "ESTRUCTURA OBLIGATORIA:\\n"
            "1. NAVIGATION: Menú superior moderno, logo a la izquierda, enlaces a la derecha (Inicio, Servicios, Contacto) con efectos hover.\\n"
            "2. HERO SECTION: Cabecera impactante con título gigante, subtítulo persuasivo y un botón principal. Usa una de las fotos de Pexels como fondo con un 'overlay' oscuro para que el texto se lea bien.\\n"
            "3. SERVICES: Una cuadrícula (grid) de 3 o 4 columnas con iconos y descripciones, usando bordes redondeados y sombras suaves.\\n"
            "4. CONTENT SECTION: Una sección de 'Sobre nosotros' o 'Por qué elegirnos' con texto a un lado e imagen al otro.\\n"
            "5. FOOTER: Pie de página profesional con fondo oscuro, enlaces rápidos y copyright.\\n\\n"
            "REGLAS TÉCNICAS:\\n"
            "- Usa Tailwind CSS puro vía CDN.\\n"
            "- Tipografía moderna (inter o sans-serif).\\n"
            f"- Usa estas imágenes reales de Pexels: {imgs_str}.\\n"
            "- Todo en un solo archivo HTML. DEVUELVE SOLO EL CÓDIGO HTML."
        )"""

# Reemplazamos el bloque del prompt antiguo por el nuevo
if 'prompt_sistema = (' in codigo:
    partes = codigo.split('prompt_sistema = (')
    # Buscamos el final del prompt antiguo (la siguiente línea de headers)
    parte_final = partes[1].split('headers = {')[1]
    
    codigo_actualizado = partes[0] + nuevo_prompt_sistema + "\n        headers = {" + parte_final
    
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(codigo_actualizado)
    print("🚀 ¡El mejor generador del mundo ha sido activado!")
else:
    print("❌ No pude localizar el prompt antiguo para actualizarlo.")
