# Decisiones técnicas PMV1

- FastAPI + SQLAlchemy por simplicidad y mantenibilidad.
- Arquitectura por capas para crecer a PMV2/PMV3 sin reescritura.
- JWT stateless con expiración configurable.
- Detección de anomalías por regla de umbral (sin modelos predictivos PMV2).
- Frontend Next.js con módulos por dominio y servicio HTTP central.
