import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')

conn.execute('''
    DROP TABLE IF EXISTS usuarios;
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        rol TEXT DEFAULT 'cliente'
    );
''')

admin_pw = generate_password_hash("adminmailar")
maria_pw = generate_password_hash("mariamailar")
juan_pw = generate_password_hash("juanmailar")

usuarios = [
    ("Admin", "admin@mail.ar", admin_pw, "admin"),
    ('María', 'maria@mail.ar', maria_pw, 'cliente'),
    ('Juan', 'juan@mail.ar', juan_pw, 'cliente')
]

conn.executemany(
    "INSERT OR IGNORE INTO usuarios (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)",
    usuarios
)

# hashed_pw = generate_password_hash("adminmailar")
# conn.execute('''
#     INSERT INTO usuarios (nombre, email, contrasena, rol)
#     VALUES (?, ?, ?, ?)
# ''', ("Admin", "admin@mail.ar", hashed_pw, "admin"),)

conn.execute('''
    DROP TABLE IF EXISTS profesionales;
''')

conn.execute('''
   CREATE TABLE IF NOT EXISTS profesionales (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre TEXT NOT NULL,
     especialidad TEXT NOT NULL,
     email TEXT NOT NULL UNIQUE
   );
''')

profesionales = [
    ('Ailen Kiroz', 'Psicología', 'ailen@turna.com'),
    ('Agustin Morales', 'Nutrición', 'agustin@turna.com'),
    ('Juan Cueva', 'Kinesiología', 'juan@turna.com'),
    ('María Pérez', 'Dermatología', 'maria@turna.com'),
    ('Lucas García', 'Fisioterapia', 'lucas@turna.com'),
    ('Sofía Martínez', 'Cardiología', 'sofia@turna.com'),
    ('Carlos López', 'Odontología', 'carlos@turna.com')
]

conn.executemany(
    "INSERT OR IGNORE INTO profesionales (nombre, especialidad, email) VALUES (?, ?, ?)",
    profesionales
)

conn.execute('''
    DROP TABLE IF EXISTS servicios;
''')


conn.execute('''
    CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    duracion INTEGER NOT NULL,
    precio REAL NOT NULL,
    profesional_id INTEGER NOT NULL,
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
    );
''')

servicios = [
    ('Consulta inicial', 60, 4000, 1),
    ('Terapia breve', 45, 3500, 1),
    ('Plan nutricional', 30, 3000, 2),
    ('Rehabilitación postural', 60, 4500, 3),
    ('Consulta inicial', 60, 4000, 4),
    ('Consulta inicial', 60, 4000, 5),
    ('Consulta inicial', 60, 4000, 6),
    ('Consulta dermatológica', 30, 5000, 4),
    ('Tratamiento facial', 45, 6000, 4),
    ('Consulta de fisioterapia', 60, 4500, 5),
    ('Terapia manual', 30, 4000, 5),
    ('Chequeo cardiológico', 30, 5000, 6),
    ('Electrocardiograma', 30, 5500, 6),
    ('Limpieza dental', 45, 7000, 7),
    ('Ortodoncia básica', 60, 8000, 7)
]

conn.executemany(
    'INSERT OR IGNORE INTO servicios (nombre, duracion, precio, profesional_id) VALUES (?, ?, ?, ?)',
    servicios
)

conn.execute('''
    DROP TABLE IF EXISTS turnos;
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesional_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    );
''')

# Seed initial turnos (appointments)
turnos = [
    (1, 2, 1, '2025-06-20', '09:00', 'pendiente'),
    (1, 3, 2, '2025-06-21', '10:30', 'pendiente'),
    (2, 2, 3, '2025-06-22', '11:00', 'pendiente'),
    (3, 3, 4, '2025-06-23', '14:00', 'pendiente')
]
conn.executemany(
    'INSERT OR IGNORE INTO turnos (profesional_id, cliente_id, servicio_id, fecha, hora, estado) VALUES (?, ?, ?, ?, ?, ?)',
    turnos
)

conn.execute('''
    CREATE TABLE IF NOT EXISTS disponibilidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profesional_id INTEGER NOT NULL,
        dia_semana INTEGER,       -- 0=domingo, 1=lunes, ..., 6=sábado
        fecha_especifica TEXT,    -- YYYY-MM-DD para excepciones
        hora_inicio TEXT NOT NULL,-- HH:MM
        hora_fin TEXT NOT NULL,   -- HH:MM
        FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
    );
''')

disponibilidades = [

    (1, 1, None, '08:00', '12:00'),
    (1, 3, None, '14:00', '18:00'),
    (2, 2, None, '09:00', '13:00'),

    (3, None, '2025-06-25', '10:00', '15:00')
]
conn.executemany(
    'INSERT OR IGNORE INTO disponibilidades (profesional_id, dia_semana, fecha_especifica, hora_inicio, hora_fin) VALUES (?, ?, ?, ?, ?)',
    disponibilidades
)

conn.commit()
conn.close()
