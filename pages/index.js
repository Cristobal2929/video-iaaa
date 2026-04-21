import { useState } from 'react';

export default function Home() {
  const [tema, setTema] = useState('');
  const [loading, setLoading] = useState(false);

  const generarVideo = async () => {
    setLoading(true);
    alert("🚀 ¡Orden recibida! El motor Fénix está trabajando en: " + tema);
    setLoading(false);
  };

  return (
    <div style={{backgroundColor: 'black', color: 'white', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: 'sans-serif'}}>
      <h1 style={{fontSize: '3rem', fontWeight: 'bold', marginBottom: '10px', background: 'linear-gradient(to right, #facc15, #ef4444)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>
        Viral AI Generator
      </h1>
      <p style={{color: '#9ca3af', marginBottom: '30px', textAlign: 'center', maxWidth: '400px'}}>
        Crea vídeos verticales virales con un solo click.
      </p>
      
      <div style={{width: '100%', maxWidth: '400px', backgroundColor: '#18181b', padding: '30px', borderRadius: '15px', border: '1px solid #27272a'}}>
        <label style={{display: 'block', fontSize: '0.875rem', marginBottom: '10px', color: '#d1d5db'}}>Tema del vídeo</label>
        <input 
          type="text" 
          placeholder="Ej: Curiosidades del espacio..." 
          style={{width: '100%', padding: '15px', borderRadius: '10px', backgroundColor: 'black', border: '1px solid #3f3f46', color: 'white', marginBottom: '20px', outline: 'none'}}
          value={tema}
          onChange={(e) => setTema(e.target.value)}
        />
        
        <button 
          onClick={generarVideo}
          disabled={!tema || loading}
          style={{width: '100%', backgroundColor: '#eab308', color: 'black', fontWeight: 'bold', padding: '15px', borderRadius: '10px', border: 'none', cursor: 'pointer', opacity: (!tema || loading) ? 0.5 : 1}}
        >
          {loading ? "PROCESANDO..." : "GENERAR VÍDEO VIRAL"}
        </button>
      </div>
      <footer style={{marginTop: '50px', color: '#525252', fontSize: '0.75rem'}}>
        Potenciado por Motor Fénix V300 • © 2026
      </footer>
    </div>
  );
}
