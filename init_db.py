import sqlite3

conn = sqlite3.connect('database.db')

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
    ('Rehabilitación postural', 60, 4500, 3)
]

conn.executemany(
    'INSERT OR IGNORE INTO servicios (nombre, duracion, precio, profesional_id) VALUES (?, ?, ?, ?)',
    servicios
)
conn.execute('''
    CREATE TABLE IF NOT EXISTS turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesional_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    );
''')

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

conn.commit()
conn.close()
