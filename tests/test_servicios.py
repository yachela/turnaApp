import unittest
from app import app

class TestServicios(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_listar_servicios_profesional_existente(self):
        response = self.client.get('/profesionales/1/servicios')

        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.json, list)

        self.assertGreater(len(response.json), 0)

        self.assertIn('nombre', response.json[0])
        self.assertIn('precio', response.json[0])

    def test_no_insertar_profesional_duplicado(self):
        import sqlite3

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM profesionales")
        count_antes = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO profesionales (nombre, especialidad, email)
            VALUES (?, ?, ?)""", ('Juan Cueva', 'Kinesiología', 'juan@turna.com'))
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM profesionales")
        count_despues = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count_antes, count_despues)
        