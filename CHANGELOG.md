# 📓 Changelog

Todas las versiones importantes del proyecto Turna, ordenadas cronológicamente.

---

## [v1.3] - 2025-06-15

### Agregado
- Semillas iniciales de `turnos` y `disponibilidades` en `init_db.py` para poblar la base de datos al iniciar.
- Nuevos tests en `tests/test_servicios.py` que verifican la inserción de servicios y previenen profesionales duplicados.
- Se incluyeron datos de ejemplo en `database.db` para demos y pruebas rápidas.

### Mejorado
- Organización de tests: archivo `tests/test_servicios.py` y limpieza de `__pycache__`.
- Actualización del `CHANGELOG.md` con esta sección de seeds y tests.

---

## [v1.2] - 2025-06-08
### Corregido
- Puerto de Flask cambiado a 5001 para evitar conflicto con AirPlay Receiver que ocupa el puerto 5000 en macOS.
- Añadidos headers CORS en Flask (`CORS(app)` y manejador `@after_request`) para permitir peticiones desde el frontend.
- Configuración de proxy en Vite redirigiendo `/profesionales` a `http://localhost:5001` para resolver bloqueos CORS.


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

