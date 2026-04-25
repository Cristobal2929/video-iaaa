export default function handler(req, res) {
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(`
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reto 21 Días</title>
    <style>
        body { font-family: Arial, sans-serif; background: #040914; color: white; text-align: center; padding: 20px; margin: 0; }
        .container { max-width: 500px; margin: 0 auto; }
        .highlight { color: #2563eb; font-weight: bold; }
        video { width: 100%; border: 2px solid #2563eb; border-radius: 15px; margin: 20px 0; box-shadow: 0 0 20px rgba(37,99,235,0.5); }
        .timer { font-size: 45px; color: #ff4757; font-weight: bold; margin: 20px 0; font-family: monospace; }
        .btn { display: block; background: #2563eb; color: white; padding: 22px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 20px; animation: pulse 1.5s infinite; text-transform: uppercase; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lanza tu negocio en <span class="highlight">21 días</span></h1>
        <video src="/static/vid_1776897727.mp4" controls autoplay muted playsinline></video>
        <div class="timer" id="timer">15:00</div>
        <a href="https://go.hotmart.com/M105511113V" class="btn">👉 QUIERO EMPEZAR YA 👈</a>
    </div>
    <script>
        let t = 900;
        setInterval(() => {
            let m = Math.floor(t / 60), s = t % 60;
            document.getElementById('timer').innerText = m + ":" + (s < 10 ? "0" : "") + s;
            if(t > 0) t--;
        }, 1000);
    </script>
</body>
</html>
    `);
}
