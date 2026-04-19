'use client';
import { LayoutShell } from '@/modules/shared/LayoutShell';
import { apiFetch } from '@/services/api';
import { User } from '@/types';
import { useEffect, useState } from 'react';

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  useEffect(() => { apiFetch<User[]>('/users').then(setUsers).catch(() => setUsers([])); }, []);
  return <LayoutShell><h2>Gestión de usuarios (admin)</h2><pre>{JSON.stringify(users, null, 2)}</pre></LayoutShell>;
}
