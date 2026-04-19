'use client';
import { LayoutShell } from '@/modules/shared/LayoutShell';
import { apiFetch } from '@/services/api';
import { Zone } from '@/types';
import { useEffect, useState } from 'react';

export default function ZonesPage() {
  const [zones, setZones] = useState<Zone[]>([]);
  useEffect(() => { apiFetch<Zone[]>('/zones').then(setZones).catch(() => setZones([])); }, []);
  return <LayoutShell><h2>Gestión de zonas</h2><pre>{JSON.stringify(zones, null, 2)}</pre></LayoutShell>;
}
