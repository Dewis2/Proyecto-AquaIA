'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { PropsWithChildren } from 'react';

const items = [
  // Menú principal PMV1 (puede filtrarse por rol en una siguiente iteración).
  { href: '/', label: 'Dashboard' },
  { href: '/alerts', label: 'Alertas' },
  { href: '/zones', label: 'Zonas' },
  { href: '/sensors', label: 'Sensores' },
  { href: '/users', label: 'Usuarios' },
];

export function LayoutShell({ children }: PropsWithChildren) {
  const pathname = usePathname();
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>AquaIA PMV1</h1>
        <nav>
          {items.map((item) => (
            <Link key={item.href} href={item.href} className={pathname === item.href ? 'active' : ''}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main>{children}</main>
    </div>
  );
}
