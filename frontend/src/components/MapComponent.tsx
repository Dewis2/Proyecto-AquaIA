'use client';

import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Zone, Alert } from '@/types';

function getColor(level?: Alert['nivel']) {
  if (level === 'critica') return '#dc2626';
  if (level === 'alta') return '#f97316';
  if (level === 'media') return '#facc15';
  return '#16a34a';
}

export default function MapComponent({ zones, alerts }: { zones: Zone[]; alerts: Alert[] }) {
  return (
    <MapContainer center={[-11.1586, -75.9926]} zoom={10} style={{ height: 380, width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {zones.map((zone) => {
        const critical = alerts.find((a) => a.zona_id === zone.id && a.nivel === 'critica' && a.estado === 'activa');
        return (
          <CircleMarker key={zone.id} center={[zone.latitud, zone.longitud]} radius={10} pathOptions={{ color: getColor(critical?.nivel) }}>
            <Popup>
              <strong>{zone.nombre}</strong>
              <p>{zone.tipo}</p>
              <p>{critical ? '⚠ Alerta crítica activa' : 'Sin alerta crítica'}</p>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
