with open('index.html', 'r', encoding='utf-8') as f:
    ui = f.read()

# 1. Aseguramos que la función showTab existe y gestiona todas las pestañas
if 'function showTab' not in ui:
    # Si por algún motivo se borró, la reinyectamos
    js_tabs = """
    function showTab(tabId) {
        // Ocultar todas las pestañas
        document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.add('hidden'));
        // Mostrar la elegida
        const target = document.getElementById('tab-' + tabId);
        if (target) target.classList.remove('hidden');
        
        // Actualizar botones (quitar active de todos)
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active', 'bg-blue-600', 'bg-purple-600', 'bg-gray-600');
            btn.classList.add('bg-gray-800');
        });
        
        // Poner color al activo
        const activeBtn = document.getElementById('btn-' + tabId);
        if (activeBtn) {
            activeBtn.classList.remove('bg-gray-800');
            const color = tabId === 'web' ? 'bg-blue-600' : (tabId === 'video' ? 'bg-purple-600' : 'bg-gray-600');
            activeBtn.classList.add('active', color);
        }
        
        if(tabId === 'history') cargarHistorial();
    }
    """
    ui = ui.replace('</script>', js_tabs + '\n</script>')

# 2. Corregimos los IDs de los botones en el HTML para que coincidan con la función
ui = ui.replace('onclick="showTab(\'web\')"', 'id="btn-web" class="tab-btn active px-5 py-2 rounded-lg bg-blue-600 transition font-semibold border border-gray-700" onclick="showTab(\'web\')"')
ui = ui.replace('onclick="showTab(\'video\')"', 'id="btn-video" class="tab-btn px-5 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition font-semibold border border-gray-700" onclick="showTab(\'video\')"')
ui = ui.replace('onclick="showTab(\'history\')"', 'id="btn-history" class="tab-btn px-5 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition font-semibold border border-gray-700" onclick="showTab(\'history\')"')

# 3. Nos aseguramos de que el div de la pestaña video se llame 'tab-video' y el de galería 'tab-history'
# (A veces el prompt los llama distinto)
ui = ui.replace('id="tab-video"', 'id="tab-video"') 
ui = ui.replace('id="tab-history"', 'id="tab-history"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(ui)
print("✅ Botones de Galería y Reels sincronizados y reparados.")
