import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AquaIA PMV1',
  description: 'Monitoreo de agua PMV1',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
