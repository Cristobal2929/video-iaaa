#!/bin/bash
git add .
git commit -m "🚦 Sistema de cola VIP activado"
git pull origin main --rebase
git push origin main
echo "✅ ¡Subida completada con éxito sin chocar con el robot!"
