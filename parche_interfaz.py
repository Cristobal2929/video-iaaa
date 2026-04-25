with open('index.html', 'r', encoding='utf-8') as f:
    codigo = f.read()

# 1. Arreglamos el botón y lo ponemos Verde
codigo = codigo.replace(
    '<button onclick="toggleEditor()" class="text-xs text-gray-400 hover:text-white bg-gray-700 px-3 py-1 rounded">Ver Código (Avanzado)</button>',
    '<button onclick="toggleEditor()" class="text-sm bg-green-600 hover:bg-green-500 text-white font-bold px-4 py-2 rounded shadow-lg flex items-center gap-2"><span>💻</span> Ver Código (Avanzado)</button>'
)

# 2. Arreglamos la función del botón para que haga scroll hacia el código
nueva_funcion_toggle = """function toggleEditor() { 
            const panel = document.getElementById('code-editor-panel');
            panel.classList.toggle('hidden'); 
            if(!panel.classList.contains('hidden')) {
                panel.scrollIntoView({behavior: "smooth"});
            }
        }"""
codigo = codigo.replace("function toggleEditor() { document.getElementById('code-editor-panel').classList.toggle('hidden'); }", nueva_funcion_toggle)

# 3. Arreglamos el historial para que muestre Webs y Videos
nuevo_historial = """async function cargarHistorial() { 
            const res = await fetch("/api/history"); 
            const data = await res.json(); 
            const grid = document.getElementById("history-grid");
            grid.innerHTML = data.items.map(v => {
                if(v.tipo === "video") {
                    return `<div class="bg-gray-900 p-4 rounded-xl border border-gray-700 shadow-lg"><div class="flex items-center gap-2 mb-2 text-purple-400 font-bold"><span>🎬</span> Video Reel</div><video controls class="w-full h-40 object-cover rounded mb-3"><source src="${v.url}"></video><a href="${v.url}" download class="text-sm bg-gray-800 text-white px-3 py-2 rounded block text-center hover:bg-gray-700">⬇️ Descargar MP4</a></div>`;
                } else {
                    return `<div class="bg-gray-900 p-4 rounded-xl border border-gray-700 shadow-lg"><div class="flex items-center gap-2 mb-2 text-blue-400 font-bold"><span>🌐</span> Proyecto Web</div><div class="h-40 bg-white rounded overflow-hidden mb-3 relative border border-gray-600"><iframe src="${v.url}" class="w-full h-full pointer-events-none transform scale-[0.6] origin-top-left" style="width: 166%; height: 166%;"></iframe></div><div class="flex gap-2"><a href="${v.url}" target="_blank" class="flex-1 text-center text-sm bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-500 font-bold">👁️ Abrir</a><a href="${v.url}" download class="flex-1 text-center text-sm bg-orange-600 text-white px-3 py-2 rounded hover:bg-orange-500 font-bold">⬇️ HTML</a></div></div>`;
                }
            }).join(""); 
        }"""
        
# Reemplazamos la función vieja del historial
import re
codigo = re.sub(r'async function cargarHistorial\(\).*?\}\s*</script>', nuevo_historial + '\n    </script>', codigo, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(codigo)
print("✅ Interfaz actualizada: Botón verde arreglado e Historial de Webs activo.")
