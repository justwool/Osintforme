import React, { useState, useEffect } from 'react';

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  // GET THIS LINK FROM YOUR GITHUB AFTER THE SCRIPT RUNS
  const DATA_URL = "https://raw.githubusercontent.com/justwool/Osintforme/refs/heads/main/data.json";

  useEffect(() => {
    fetch(DATA_URL).then(res => res.json()).then(d => {
      setData(d);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  return (
    <div style={{background:'#050505', color:'#ccc', minHeight:'100vh', padding:'15px', fontFamily:'sans-serif'}}>
      <h2 style={{color:'#fff', fontSize:'14px', letterSpacing:'2px'}}>OSINT FEED</h2>
      {loading ? <p>Loading...</p> : data.map((item, i) => (
        <div key={i} style={{background:'#111', padding:'15px', borderRadius:'10px', marginBottom:'10px', border:'1px solid #222'}}>
          <div style={{display:'flex', justifyContent:'space-between', marginBottom:'5px'}}>
            <b style={{color:'#fff', fontSize:'12px'}}>{item.source}</b>
            <small style={{color:'#555'}}>{item.region}</small>
          </div>
          <p style={{fontSize:'14px', margin:'5px 0'}}>{item.text}</p>
          <a href={item.url} style={{color:'#10b981', fontSize:'12px', textDecoration:'none'}}>Source Link →</a>
        </div>
      ))}
    </div>
  );
}
