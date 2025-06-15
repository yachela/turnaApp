# Turna

**Turna** es un sistema web de gestión de turnos orientado a profesionales independientes  
(psicólogos, nutricionistas, kinesiólogos, coaches, etc.), diseñado para optimizar agendas,  
reducir ausencias y mejorar la experiencia de reserva de citas.

---

## Estado actual del proyecto

### Backend (Flask + SQLite)
- API REST con Flask 2.x y CORS habilitado para los orígenes del frontend.  
- Endpoints CRUD para:
  - **Profesionales** (`/profesionales`, `/profesionales/<id>`)  
  - **Servicios** (`/profesionales/<id>/servicios`, `/servicios/<id>`)  
  - **Turnos** (`/turnos`, `/turnos/<id>`)  
  - **Disponibilidades** (`/profesionales/<id>/disponibilidades`, `/disponibilidades/<id>`, `/profesionales/<id>/disponibilidades_libres`)  
- Base de datos SQLite con tablas: `profesionales`, `servicios`, `turnos`, `disponibilidades`.  
- Script `init_db.py` para crear y poblar la BBDD con datos de ejemplo.  
- Tests unitarios en `tests/` para servicios, turnos y disponibilidades.

### Frontend (React + Vite + Bootstrap)
- SPA en React 18 con Vite como bundler y servidor de desarrollo.  
- Navegación declarativa con React Router v6.  
- UI basada en Bootstrap 5 + React-Bootstrap y componentes propios:  
  - **HeroSection**, **FeaturesSection**, **CustomNavbar**  
  - **ProfesionalesList**, **ProfessionalDetail**, **ServiciosList**, **DisponibilidadesList**, **TurnosList**  
- Axios para consumir la API y gestionar estados de carga y errores.

---

## Próximos pasos

1. **Autenticación y roles** (JWT para profesionales y clientes).  
2. **Migraciones de BBDD** con Alembic para SQLite/Postgres.  
3. **Notificaciones** por email/SMS (SendGrid, Twilio).  
4. **Pruebas de integración** en frontend con React Testing Library.  
5. **CI/CD y despliegue** (GitHub Actions, Heroku/Netlify, Vercel).

---

## Tecnologías

- **Backend:** Python 3.x, Flask, flask_cors, SQLite3  
- **Frontend:** Node.js, Vite, React 18, React Router, React-Bootstrap, Axios  
- **Herramientas:** Git, GitHub, Trello, unittest, ESLint  

---

## Autor

Laura Belén Yachelini – Proyecto académico para la materia **Análisis y Metodologías de Software**