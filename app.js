async function cargarVideo() {
  const status = document.getElementById("status");

  try {
    const res = await fetch(
      "https://raw.githubusercontent.com/Cristobal2929/video-iaaa/main/public_url.txt?cache=" + Date.now()
    );

    const url = await res.text();

    if (!url.includes("http")) {
      status.innerText = "Sin vídeo aún...";
      return;
    }

    document.getElementById("video").src = url.trim();
    status.innerText = "Vídeo listo ✔";

  } catch (e) {
    status.innerText = "Error cargando vídeo";
  }
}

async function generar() {
  const tema = document.getElementById("idea").value;
  const status = document.getElementById("status");

  if (!tema) {
    status.innerText = "Escribe una idea";
    return;
  }

  status.innerText = "Generando vídeo... ⏳";

  await fetch("https://video-iaaa.vercel.app/api/generar", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      tema: tema,
      codigo: "VIP-FENIX"
    })
  });

  setTimeout(cargarVideo, 25000);
}

// auto load
window.onload = cargarVideo;
