export type Role = 'operador' | 'analista' | 'administrador';

export interface User {
  id: number;
  nombre: string;
  email: string;
  rol: Role;
}

export interface Zone {
  id: number;
  nombre: string;
  descripcion?: string;
  latitud: number;
  longitud: number;
  tipo: string;
  activo: boolean;
}

export interface Sensor {
  id: number;
  zona_id: number;
  tipo: string;
  codigo: string;
  umbral_min: number;
  umbral_max: number;
  estado: string;
}

export interface Alert {
  id: number;
  sensor_id: number;
  zona_id: number;
  tipo: string;
  nivel: 'critica' | 'alta' | 'media' | 'baja';
  valor_detectado: number;
  descripcion: string;
  estado: 'activa' | 'resuelta';
  resolucion_notas?: string;
}
