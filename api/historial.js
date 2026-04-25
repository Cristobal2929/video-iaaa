import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
    const staticDir = path.join(process.cwd(), 'static');
    
    if (!fs.existsSync(staticDir)) {
        return res.status(200).json([]);
    }

    try {
        const files = fs.readdirSync(staticDir);
        // Filtramos para que solo salgan archivos .mp4
        const videos = files
            .filter(file => file.endsWith('.mp4'))
            .map(file => `/static/${file}`)
            .reverse(); // El más nuevo primero

        res.status(200).json(videos);
    } catch (e) {
        res.status(500).json([]);
    }
}
