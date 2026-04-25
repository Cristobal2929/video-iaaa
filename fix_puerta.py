import os

with open('api/main.py', 'r', encoding='utf-8') as f:
    codigo = f.read()

# 1. Añadimos el modelo de datos correcto para que FastAPI no se queje
nuevo_modelo = """
class PromptData(BaseModel):
    prompt: str
"""

if "class PromptData" not in codigo:
    codigo = codigo.replace("class WebData(BaseModel):", nuevo_modelo + "\nclass WebData(BaseModel):")

# 2. Arreglamos la puerta de entrada del generador web
codigo = codigo.replace("async def api_generate_web(data: dict):", "async def api_generate_web(data: PromptData):")
codigo = codigo.replace("prompt_usuario = data.get(\"prompt\")", "prompt_usuario = data.prompt")

with open('api/main.py', 'w', encoding='utf-8') as f:
    f.write(codigo)

print("✅ Puerta de entrada reparada. Adiós al Error 422.")
