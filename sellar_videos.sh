#!/bin/bash

# Este script busca todos los mp4 y les pega el sello R21
for video in videos_crudos/*.mp4; do
    # Sacamos el nombre del archivo
    nombre=$(basename "$video")
    echo "🦈 Procesando: $nombre..."
    
    # El comando mágico de FFmpeg (pega el sello.png arriba a la derecha)
    ffmpeg -y -i "$video" -i sello.png -filter_complex "overlay=W-w-30:30" -codec:a copy "videos_listos/$nombre"
    
    echo "✅ Listo: videos_listos/$nombre"
done

echo "🔥 ¡Todos los vídeos tienen su acceso verificado!"
