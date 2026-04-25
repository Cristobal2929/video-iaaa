#!/bin/bash
source .env
pip install python-multipart python-dotenv --quiet
pkill -f uvicorn
rm -f temp_*.mp4
nohup uvicorn api.main:app --host 0.0.0.0 --port 8000 > log.txt 2>&1 &
echo "🚀 Servidor Fenix AI Studio iniciado a prueba de fallos."
echo "Abriendo túnel de Cloudflare..."
sleep 3
npx --yes cloudflared tunnel --url http://localhost:8000 2>&1 | grep -o 'https://[a-zA-Z0-9.-]*\.trycloudflare\.com'
