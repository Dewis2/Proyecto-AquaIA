'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '@/services/api';

interface Summary {
  active_alerts: number;
  critical_alerts: number;
  total_sensors: number;
  active_sensors: number;
  zones_count: number;
  last_hour_readings: number;
}

export function DashboardView() {
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    const tick = () => apiFetch<Summary>('/dashboard/summary').then(setSummary).catch(() => setSummary(null));
    tick();
    const interval = setInterval(tick, 60000);
    return () => clearInterval(interval);
  }, []);

  if (!summary) return <p>Cargando resumen...</p>;

  return (
    <section>
      <h2>Dashboard PMV1</h2>
      <div className="grid">
        {Object.entries(summary).map(([k, v]) => (
          <article key={k} className="card">
            <p>{k.replaceAll('_', ' ')}</p>
            <strong>{v}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}
