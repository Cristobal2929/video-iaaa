export default async function handler(req, res) {
  const { tema, id, codigo } = req.body;

  if (codigo !== "VIP-FENIX") {
    return res.status(401).json({ error: "Licencia inválida" });
  }

  // ¡AQUÍ ESTÁ EL CABLEADO!
  const response = await fetch('https://api.github.com/repos/Cristobal2929/video-iaaa/dispatches', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      event_type: 'generar_video_viral',
      client_payload: { tema, id }
    })
  });

  if (response.ok) {
    res.status(200).json({ success: true });
  } else {
    const errorText = await response.text();
    res.status(500).json({ error: errorText });
  }
}
