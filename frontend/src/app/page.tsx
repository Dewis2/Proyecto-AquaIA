'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { LayoutShell } from '@/modules/shared/LayoutShell';
import { DashboardView } from '@/modules/dashboard/DashboardView';
import { apiFetch } from '@/services/api';
import { Alert, Zone } from '@/types';

const MapComponent = dynamic(() => import('@/components/MapComponent'), { ssr: false });

export default function HomePage() {
  const [zones, setZones] = useState<Zone[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    const tick = () => {
      apiFetch<Zone[]>('/zones').then(setZones).catch(() => setZones([]));
      apiFetch<Alert[]>('/alerts?estado=activa').then(setAlerts).catch(() => setAlerts([]));
    };
    tick();
    const interval = setInterval(tick, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <LayoutShell>
      <DashboardView />
      <h3>Mapa de zonas (actualiza cada 60s)</h3>
      <MapComponent zones={zones} alerts={alerts} />
    </LayoutShell>
  );
}
