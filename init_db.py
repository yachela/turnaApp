import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS profesionales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especialidad TEXT NOT NULL
    );
''')

profesionales = [
    ('Ailen Kiroz', 'Psicología'),
    ('Agustin Morales', 'Nutrición'),
    ('Juan Cueva', 'Kinesiología')
]

conn.executemany("INSERT INTO profesionales (nombre, especialidad) VALUES (?, ?)", profesionales)

conn.commit()
conn.close()

conn.execute('''
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        duracion INTEGER NOT NULL, -- en minutos
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

conn.executemany('''
    INSERT INTO servicios (nombre, duracion, precio, profesional_id)
    VALUES (?, ?, ?, ?)
''', servicios)