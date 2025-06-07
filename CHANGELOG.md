# 📓 Changelog

Todas las versiones importantes del proyecto Turna, ordenadas cronológicamente.

---

## [v1.1] - 2025-06-07

### Agregado
- Tabla `servicios` relacionada con `profesionales` en SQLite
- Inserción de datos de prueba para `servicios`
- Endpoint `/profesionales/<id>/servicios` en Flask
- Restricción `UNIQUE` en campo `email` para evitar duplicados
- Mejora en `init_db.py` con `INSERT OR IGNORE`

---

## [v1.0] - 2025-04-16

### Inicial
- Estructura base del proyecto en Flask
- Clases iniciales: `Profesional`, `Cliente`, `Servicio`, `Turno`
- Creación del repositorio y primer versionado (`v1.0`)