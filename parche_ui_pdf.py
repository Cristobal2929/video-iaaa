with open('index.html', 'r', encoding='utf-8') as f:
    ui = f.read()

# Añadimos el botón de PDF en la UI
boton_pdf = """
            <div class="flex gap-2 mb-3">
                <button onclick="generarWeb()" id="btn-gen-web" class="flex-grow bg-blue-600 py-3 rounded-lg font-bold hover:bg-blue-500 transition shadow-lg text-sm">✨ Crear desde Prompt</button>
                <label class="bg-red-600 hover:bg-red-500 py-3 px-4 rounded-lg font-bold cursor-pointer transition shadow-lg text-sm flex items-center gap-2">
                    <span>📄</span> PDF a Web
                    <input type="file" id="pdf-file" accept=".pdf" class="hidden" onchange="generarDesdePDF(this)">
                </label>
            </div>
"""
ui = ui.replace('<button onclick="generarWeb()" id="btn-gen-web" class="w-full bg-blue-600 py-3 rounded-lg font-bold hover:bg-blue-500 transition shadow-lg">✨ Generar Diseño Inteligente</button>', boton_pdf)

# Añadimos la función JavaScript para manejar el PDF
js_pdf = """
        async function generarDesdePDF(input) {
            if(!input.files[0]) return;
            const status = document.getElementById("web-status");
            status.innerText = "📑 Leyendo PDF y transformando a Web... ⏳";
            status.classList.remove("hidden");
            
            const formData = new FormData();
            formData.append("file", input.files[0]);
            
            try {
                const res = await fetch("/generate/web-from-pdf", { method: "POST", body: formData });
                const data = await res.json();
                if(data.status === "success") {
                    currentHtml = data.html;
                    document.getElementById("web-workspace").classList.remove("hidden");
                    document.getElementById("web-editor").value = currentHtml;
                    cargarGestorContenido();
                    actualizarIframe();
                } else { alert("Error: " + data.html); }
            } catch(e) { alert("Error en la subida."); }
            status.classList.add("hidden");
            status.innerText = "👨‍💻 La IA está diseñando y buscando fotos en Pexels... ⏳";
        }
"""
ui = ui.replace('async function generarWeb() {', js_pdf + '\n        async function generarWeb() {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(ui)
print("✅ Botón de PDF añadido a la interfaz.")
