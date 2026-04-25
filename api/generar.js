export default async function handler(req, res) {
    const { tema } = req.body;
    
    try {
        const response = await fetch("https://api.github.com/repos/Cristobal2929/video-iaaa/dispatches", {
            method: "POST",
            headers: {
                "Authorization": `token ${process.env.GITHUB_TOKEN}`,
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                event_type: "generar_video_viral",
                client_payload: { tema: tema }
            })
        });

        if (response.ok) {
            res.status(200).json({ success: true });
        } else {
            res.status(500).json({ success: false });
        }
    } catch (error) {
        res.status(500).json({ success: false });
    }
}
