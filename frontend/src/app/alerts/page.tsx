'use client';

import { useEffect, useState } from 'react';
import { LayoutShell } from '@/modules/shared/LayoutShell';
import { apiFetch } from '@/services/api';
import { Alert } from '@/types';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    apiFetch<Alert[]>('/alerts').then(setAlerts).catch(() => setAlerts([]));
  }, []);

  const resolveAlert = async (id: number) => {
    const note = prompt('Nota de resolución (obligatoria):');
    if (!note || note.length < 5) return;
    await apiFetch(`/alerts/${id}/resolve`, { method: 'POST', body: JSON.stringify({ resolucion_notas: note }) });
    setAlerts((prev) => prev.map((a) => (a.id === id ? { ...a, estado: 'resuelta', resolucion_notas: note } : a)));
  };

  return (
    <LayoutShell>
      <h2>Alertas activas y resueltas</h2>
      <table>
        <thead><tr><th>ID</th><th>Nivel</th><th>Descripción</th><th>Estado</th><th>Acción</th></tr></thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.id}>
              <td>{a.id}</td>
              <td><span className={`badge ${a.nivel}`}>{a.nivel}</span></td>
              <td>{a.descripcion}</td>
              <td>{a.estado}</td>
              <td>{a.estado === 'activa' ? <button onClick={() => resolveAlert(a.id)}>Resolver</button> : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </LayoutShell>
  );
}
