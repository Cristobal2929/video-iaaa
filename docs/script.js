function generarVideo() {

  const tema = "negocio digital";

  const url =
    "https://github.com/Cristobal2929/video-iaaa/actions/workflows/video.yml";

  window.open(url, "_blank");

  document.getElementById("status").innerText =
    "📡 Abriendo GitHub Actions...";

  document.getElementById("btn").innerText = "⏳ Abre Actions";
}
