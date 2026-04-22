async function generarVideo() {

    const tema = document.getElementById("tema").value;
    const licencia = document.getElementById("licencia").value;

    document.getElementById("status").innerText = "⏳ Generando video...";

    const res = await fetch("/api/generar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            tema,
            codigo: licencia,
            id: Date.now()
        })
    });

    const data = await res.json();

    if (data.success) {

        document.getElementById("status").innerText = "✅ Video listo";

        const url = data.url || "video_final.mp4";

        document.getElementById("video").src = url;
        document.getElementById("url").innerText = url;
        document.getElementById("url").href = url;

    } else {
        document.getElementById("status").innerText = "❌ Error: " + data.error;
    }
}
