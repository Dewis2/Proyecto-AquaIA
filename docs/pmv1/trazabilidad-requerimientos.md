# Trazabilidad PMV1

| HU | RF | Backend endpoint | Frontend pantalla | BD |
|---|---|---|---|---|
| HU-01 | RF-01/RF-06 | `GET /zones`, `GET /readings` | `/` | `zona`, `lectura_sensor` |
| HU-02 | RF-04/RF-07 | `POST /readings` | `/alerts` | `lectura_sensor`, `alerta` |
| HU-03 | RF gestión sensores | `CRUD /sensors` | `/sensors` | `sensor` |
| HU-09 | RF-07/RF-08 | `GET /alerts`, `GET /dashboard/summary` | `/alerts`, `/` | `alerta` |
| HU-10 | RF historial | `POST /alerts/{id}/resolve` | `/alerts` | `alerta`, `audit_log` |
| HU-12 | RF-09 | `POST /auth/login`, `GET /users` | `/login`, `/users` | `usuario` |
| HU-14 | RF gestión zonas | `CRUD /zones` | `/zones`, `/` | `zona`, `sensor` |
