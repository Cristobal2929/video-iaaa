from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Tu llave maestra (Se configura en Vercel, no aquí)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "Cristobal2929"
REPO_NAME = "video-iaaa"

# Lista de códigos de acceso que tú vendes a tus clientes
CODIGOS_VALIDOS = ["PRO-2026-X", "VIP-FENIX", "CLIENTE-01"]

@app.route('/api/generar', methods=['POST'])
def generar_video():
    data = request.json
    tema = data.get("tema")
    id_video = data.get("id")
    codigo = data.get("codigo")

    # 1. Verificamos el código de acceso
    if codigo not in CODIGOS_VALIDOS:
        return jsonify({"error": "Código de acceso inválido"}), 403

    # 2. Ordenamos a GitHub que fabrique el vídeo
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "event_type": "generar_video_viral",
        "client_payload": {"tema": tema, "id": id_video}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        return jsonify({"status": "¡Vídeo en camino! Tu orden ha sido procesada."}), 200
    else:
        return jsonify({"error": "Error al conectar con el motor de cine"}), 500

if __name__ == "__main__":
    app.run()
