'use client';

import { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('admin@aquaia.local');
  const [password, setPassword] = useState('Admin123!');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1'}/auth/login`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
      window.location.href = '/';
    }
  };

  return (
    <main style={{ maxWidth: 420, margin: '3rem auto', background: '#fff', padding: '1rem', borderRadius: 8 }}>
      <h2>Ingreso AquaIA</h2>
      <form onSubmit={handleSubmit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" style={{ width: '100%', marginBottom: 8 }} />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" style={{ width: '100%', marginBottom: 8 }} />
        <button type="submit">Ingresar</button>
      </form>
    </main>
  );
}
