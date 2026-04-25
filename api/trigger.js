export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    const { tema } = req.body;

    if (!tema) {
        return res.status(400).json({ error: 'Falta tema' });
    }

    try {
        const response = await fetch(
            'https://api.github.com/repos/Cristobal2929/video-iaaa/dispatches',
            {
                method: 'POST',
                headers: {
                    'Authorization': `token ${process.env.GITHUB_TOKEN}`,
                    'Accept': 'application/vnd.github.v3+json'
                },
                body: JSON.stringify({
                    event_type: 'hacer_video',
                    client_payload: { tema }
                })
            }
        );

        if (response.status === 204) {
            return res.status(200).json({ ok: true });
        } else {
            const text = await response.text();
            return res.status(500).json({ error: text });
        }

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
}
