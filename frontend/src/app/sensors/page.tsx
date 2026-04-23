'use client';
import { LayoutShell } from '@/modules/shared/LayoutShell';
import { apiFetch } from '@/services/api';
import { Sensor } from '@/types';
import { useEffect, useState } from 'react';

export default function SensorsPage() {
  const [sensors, setSensors] = useState<Sensor[]>([]);
  useEffect(() => { apiFetch<Sensor[]>('/sensors').then(setSensors).catch(() => setSensors([])); }, []);
  return <LayoutShell><h2>Gestión de sensores</h2><pre>{JSON.stringify(sensors, null, 2)}</pre></LayoutShell>;
}
