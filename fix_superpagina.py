import re

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# EL PROMPT SÚPER-MAESTRO DE DISEÑO CINEMÁTICO Y LÓGICA VIVA (¡LA VERSIÓN 5.0 ESTELAR!)
nuevo_prompt_superpagina = """
        prompt_sistema = (
            "Eres un Ingeniero Senior de UI/UX y Desarrollador Frontend experto en IA Aplicada. Tu misión es crear una SINGLE-PAGE APPLICATION ESPECTACULAR Y CINEMÁTICA basándote exclusivamente en este texto de un PDF: '{texto[:10000]}'.\\n\\n"
            "REGLAS OBLIGATORIAS DE DISEÑO VISUAL:\\n"
            "1. FONDO PROFUNDO: Deep Cosmos (gradiente oscuro azul zafiro a negro) con micro-partículas de estrellas flotando.\\n"
            "2. TEXTOS FLOTANTES DE ZAFIRO: Múltiples párrafos extraídos del PDF (ej. frases clave de Elias, Jose, Cristo, Moises) deben flotar lentamente por toda la pantalla como mensajes etéreos, coloreados en un AZUL ZAFIRO ZAFIRA brillante con sombras suaves (uso de CSS animations y keyframes).\\n"
            "3. LA HERRAMIENTA CENTRAL (MOTOR TESHUÁ): En el centro, crea un panel flotante y glowing, diseñado en un ORO RADIANTE (degradados oro, sombras doradas, rounded-3xl). Debe tener el título 'CALCULADOR TESHUÁ: TU PUZZLE ESPIRITUAL' en letra azul zafiro zafira.\\n"
            "4. INPUTS DORADOS: El panel central debe tener inputs modernos con bordes dorados para 'Nombre Completo' y 'Fecha de Nacimiento'.\\n\\n"
            "REGLAS OBLIGATORIAS DE LÓGICA VIVA (JAVASCRIPT):\\n"
            "5. EL ALGORITMO TESHUÁ: Programa en JavaScript un algoritmo que calcule AL INSTANTE, al pulsar el botón dorado, la guematría/numerología del usuario:\\n"
            "   - Calcular Número de Alma y Misión de Vida aplicando las fórmulas de reducción del libro.\\n"
            "   - Identificar cuál de las 4 fases espirituales (Manifestación, Prueba, Liberación, Servicio) y qué arquetipo (Elias, Cristo, Jose, Moises) le corresponde.\\n"
            "6. MENSAJE DEL ALMA DINÁMICO: Al terminar el cálculo, muestra en el panel central un mensaje revelador y místico, extrayendo los textos exactos del PDF que corresponden a ese resultado.\\n"
            "7. ANIMACIONES DE RESULTADO: Usa animaciones suaves y destellos dorados para presentar el resultado.\\n"
            "DEVUELVE ÚNICAMENTE EL CÓDIGO HTML5 PURO, AUTÓNOMO Y LISTO PARA PRODUCCIÓN."
        )
"""

# Reemplazamos el prompt anterior del PDF por este nuevo súper-prompt
codigo = re.sub(
    r'prompt_sistema = \(\s*"Eres un Desarrollador Frontend Senior y experto en Inteligencia Artificial.*?DEVUELVE ÚNICAMENTE EL HTML PURO."\s*\)',
    nuevo_prompt_superpagina.strip(),
    codigo,
    flags=re.DOTALL
)

with open('api/main.py', 'w', encoding='utf-8') as f:
    f.write(codigo)

print("✅ Cerebro de la IA actualizado para crear la Super Página Cinematográfica con la lógica Teshuá Viva.")
