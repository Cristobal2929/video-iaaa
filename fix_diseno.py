import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# 1. Mejoramos el prompt del generador normal
nuevo_prompt_web = """
        prompt_sistema = (
            f"Eres un Diseñador Web y Desarrollador Frontend Experto. Crea una Landing Page premium, moderna y espectacular sobre: '{prompt_usuario}'.\\n"
            "REGLAS OBLIGATORIAS:\\n"
            "1. Devuelve un documento HTML5 completo con <html>, <head> y <body>.\\n"
            "2. En el <head>, incluye OBLIGATORIAMENTE el CDN de Tailwind: <script src=\\"https://cdn.tailwindcss.com\\"></script>\\n"
            "3. Añade tipografía de Google Fonts (ej. Poppins o Inter) para que se vea elegante.\\n"
            "4. Escribe CSS personalizado dentro de una etiqueta <style> para animaciones o sombras especiales.\\n"
            "5. Escribe JavaScript dentro de una etiqueta <script> al final del body para hacer el menú interactivo o añadir efectos de scroll.\\n"
            f"6. Usa obligatoriamente estas imágenes como fondos espectaculares o elementos visuales: {imgs_str}.\\n"
            "7. Diseño profesional: usa gradientes, bordes redondeados (rounded-2xl), tarjetas (cards) y una sección Hero impactante.\\n"
            "DEVUELVE ÚNICAMENTE EL CÓDIGO HTML PURO, sin texto extra."
        )
"""

# 2. Mejoramos el prompt del generador por PDF (el que has usado)
nuevo_prompt_pdf = """
        prompt = (
            "Eres un Diseñador Web Experto. Crea una Landing Page premium y moderna BASADA EXCLUSIVAMENTE en este texto de un PDF: "
            f"'{texto[:3000]}'.\\n\\n"
            "REGLAS OBLIGATORIAS:\\n"
            "1. Devuelve un documento HTML5 completo.\\n"
            "2. En el <head>, incluye el CDN de Tailwind: <script src=\\"https://cdn.tailwindcss.com\\"></script> y Google Fonts.\\n"
            "3. Estructura el texto del PDF para que no sea aburrido: usa tarjetas (cards), secciones con fondos de colores (bg-gray-50, gradientes oscuros), y un menú de navegación superior.\\n"
            "4. Escribe JavaScript dentro de una etiqueta <script> para darle interactividad a la página (ej. botones que hagan algo).\\n"
            "5. Añade estilos extra en una etiqueta <style>.\\n"
            "DEVUELVE ÚNICAMENTE EL CÓDIGO HTML PURO, listo para producción."
        )
"""

# Reemplazamos en el código (buscamos las cadenas antiguas y ponemos las nuevas)
import re

# Actualizar el de web normal
codigo = re.sub(
    r'prompt_sistema = \(f"Eres Desarrollador Senior.*?DEVUELVE SOLO HTML."\)',
    nuevo_prompt_web.strip(),
    codigo,
    flags=re.DOTALL
)

# Actualizar el de PDF
codigo = re.sub(
    r'prompt = f"Crea una Landing Page basada en este texto de un PDF: \'{texto\[:3000\]}\'\. Usa Tailwind CSS, incluye menú y footer\. DEVUELVE SOLO HTML\."',
    nuevo_prompt_pdf.strip(),
    codigo,
    flags=re.DOTALL
)

with open('api/main.py', 'w', encoding='utf-8') as f:
    f.write(codigo)

print("✅ Instrucciones Premium inyectadas. La IA ahora usará CSS y JavaScript obligatorio.")
