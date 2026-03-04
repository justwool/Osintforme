import React, { useState, useEffect, useMemo } from 'react';
import { Terminal, Globe, Search, RefreshCw, ExternalLink, Clock, Shield, AlertTriangle, Radio, Navigation } from 'lucide-react';

const DATA_URL = "https://raw.githubusercontent.com/justwool/Osintforme/refs/heads/main/data.json";

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const fetchIntel = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${DATA_URL}?t=${Date.now()}`);
      if (!response.ok) throw new Error("Awaiting GitHub Action data sync...");
      const jsonData = await response.json();
      setData(jsonData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIntel();
    const interval = setInterval(fetchIntel, 60000);
    return () => clearInterval(interval);
  }, []);

  const filteredData = useMemo(() => {
    return data.filter(item => {
      const category = item.category?.toLowerCase() || '';
      const platform = item.platform?.toLowerCase() || '';
      const text = item.text?.toLowerCase() || '';
      const source = item.source?.toLowerCase() || '';

      const matchesFilter = filter === 'all' || 
                            category === filter || 
                            platform === filter ||
                            (filter === 'alerts' && (category.includes('alert') || source.includes('bno')));
      
      const matchesSearch = text.includes(searchTerm.toLowerCase()) || 
                            source.includes(searchTerm.toLowerCase());
      
      return matchesFilter && matchesSearch;
    });
  }, [data, filter, searchTerm]);

  return (
    <div className="min-h-screen bg-[#020202] text-slate-400 font-sans selection:bg-emerald-500/30">
      {/* HUD Header */}
      <nav className="sticky top-0 z-50 bg-[#020202]/90 backdrop-blur-xl border-b border-white/5 px-4 py-3">
        <div className="max-w-2xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute -inset-1 bg-emerald-500/20 blur-sm rounded-full animate-pulse"></div>
              <Radio size={18} className="text-emerald-500 relative" />
            </div>
            <div>
              <h1 className="text-[11px] font-black tracking-[0.3em] text-white uppercase leading-none">STRAT_INTEL_V2</h1>
              <div className="flex items-center gap-2 mt-1">
                <span className="flex items-center gap-1 text-[8px] text-emerald-500/80 font-mono font-bold uppercase tracking-widest">
                  <div className="w-1 h-1 bg-emerald-500 rounded-full animate-ping"></div> Live_Feed
                </span>
                <span className="text-[8px] text-white/20 font-mono tracking-widest">[{data.length}_RECORDS]</span>
              </div>
            </div>
          </div>
          <button onClick={fetchIntel} className="p-2.5 bg-white/5 rounded-xl border border-white/5 active:scale-90 transition-all">
            <RefreshCw size={14} className={`${loading ? 'animate-spin text-emerald-400' : 'text-slate-500'}`} />
          </button>
        </div>
      </nav>

      <main className="px-4 py-6 max-w-2xl mx-auto space-y-5 pb-24">
        {/* Search Control */}
        <div className="relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within:text-emerald-400 transition-colors" size={14} />
          <input 
            type="text" 
            placeholder="Intercept keywords..." 
            className="w-full bg-[#080808] border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-emerald-500/40 focus:bg-[#0a0a0a] transition-all placeholder:text-slate-700 font-medium"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        {/* Signal Filters */}
        <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar scroll-smooth">
          {[
            {id: 'all', label: 'All Signals'},
            {id: 'alerts', label: 'Priority Alerts', icon: <AlertTriangle size={10}/>},
            {id: 'analysis', label: 'Analysis'},
            {id: 'naval', label: 'Naval Assets', icon: <Navigation size={10}/>},
            {id: 'bluesky', label: 'BSky Hub'},
            {id: 'rss', label: 'RSS Nodes'}
          ].map(t => (
            <button 
              key={t.id} 
              onClick={() => setFilter(t.id)} 
              className={`flex items-center gap-2 whitespace-nowrap px-5 py-2.5 rounded-xl text-[10px] uppercase font-black tracking-tight border transition-all ${
                filter === t.id 
                ? 'bg-emerald-600 border-emerald-400 text-white shadow-[0_4px_20px_rgba(5,150,105,0.3)]' 
                : 'bg-[#0a0a0a] border-white/5 text-slate-500 hover:border-white/20 active:bg-white/5'
              }`}
            >
              {t.icon} {t.label}
            </button>
          ))}
        </div>

        {/* Intelligence Stream */}
        <div className="space-y-4">
          {filteredData.length > 0 ? filteredData.map((item, i) => (
            <article key={i} className="group relative bg-[#080808] border border-white/5 rounded-2xl overflow-hidden hover:border-white/20 transition-all active:scale-[0.99]">
              {/* Highlight Bar for Alerts */}
              {(item.category?.includes('alert') || item.source?.includes('BNO')) && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500/80 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></div>
              )}

              <div className="p-5">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-2.5">
                    <div className={`p-1.5 rounded-lg ${item.platform === 'bluesky' ? 'bg-sky-500/10 text-sky-500' : 'bg-orange-500/10 text-orange-500'}`}>
                      {item.platform === 'bluesky' ? <Radio size={12} /> : <Shield size={12} />}
                    </div>
                    <div>
                      <h2 className="text-[12px] font-black text-white leading-none mb-1">{item.source}</h2>
                      <span className="text-[9px] text-slate-600 font-mono uppercase tracking-widest">{item.platform || 'System'} Node</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 text-[9px] text-slate-500 font-mono bg-white/5 px-2.5 py-1 rounded-lg border border-white/5">
                    <Clock size={10} className="text-emerald-500/50" /> 
                    {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>

                <p className="text-[14px] text-slate-200 leading-[1.6] mb-5 font-medium">
                  {item.text}
                </p>

                <div className="flex justify-between items-center pt-4 border-t border-white/5">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-500/80 uppercase tracking-tighter bg-emerald-500/5 px-2 py-1 rounded-md">
                      <Globe size={11} /> {item.region || 'Global'}
                    </div>
                    <div className="text-[9px] font-bold text-slate-700 uppercase tracking-widest">
                      {item.category || 'Intercept'}
                    </div>
                  </div>
                  <a 
                    href={item.url} 
                    target="_blank" 
                    rel="noreferrer" 
                    className="flex items-center gap-2 text-[10px] font-black text-white uppercase bg-white/5 hover:bg-emerald-600 hover:text-white px-4 py-2 rounded-xl transition-all border border-white/5 hover:border-emerald-400"
                  >
                    Details <ExternalLink size={10} />
                  </a>
                </div>
              </div>
            </article>
          )) : (
            <div className="flex flex-col items-center justify-center py-32 border-2 border-dashed border-white/5 rounded-[2.5rem] opacity-40">
              <Terminal size={32} className="mb-4 text-slate-700" />
              <p className="text-xs text-slate-600 font-mono tracking-widest italic uppercase">Zero_Signal_Matches</p>
            </div>
          )}
        </div>
      </main>

      {/* Decorative Scraper Overlay */}
      <div className="fixed inset-0 pointer-events-none border-[12px] border-[#020202] opacity-50 shadow-[inset_0_0_100px_rgba(0,0,0,0.8)]"></div>
    </div>
  );
}
