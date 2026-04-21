"use client";
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
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 font-sans">
      <h1 className="text-5xl font-extrabold mb-4 bg-gradient-to-r from-yellow-400 to-red-500 bg-clip-text text-transparent">
        Viral AI Generator
      </h1>
      <p className="text-gray-400 mb-8 text-center max-w-md">
        Crea vídeos verticales virales con un solo click. IA real, resultados reales.
      </p>
      
      <div className="w-full max-w-md bg-zinc-900 p-8 rounded-2xl border border-zinc-800 shadow-2xl">
        <label className="block text-sm font-medium mb-2 text-gray-300">Tema del vídeo</label>
        <input 
          type="text" 
          placeholder="Ej: Curiosidades del espacio..." 
          className="w-full p-4 rounded-xl bg-black border border-zinc-700 focus:border-yellow-500 outline-none mb-6 transition-all text-white"
          value={tema}
          onChange={(e) => setTema(e.target.value)}
        />
        
        <button 
          onClick={generarVideo}
          disabled={!tema || loading}
          className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-4 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "PROCESANDO..." : "GENERAR VÍDEO VIRAL"}
        </button>
      </div>

      <footer className="mt-12 text-zinc-600 text-sm italic">
        Potenciado por Motor Fénix V300 • © 2026
      </footer>
    </div>
  );
}
