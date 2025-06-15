import unittest
from app import app

class TestTurnos(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_listar_turnos(self):
        """GET /turnos debe devolver una lista (200)."""
        resp = self.client.get('/turnos')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

    def test_crear_turno(self):
        """POST /turnos con datos válidos crea un turno (201)."""
        nuevo = {
            "profesional_id": 1,
            "cliente_id": 1,
            "servicio_id": 1,
            "fecha": "2025-07-01",
            "hora": "10:30"
        }
        resp = self.client.post('/turnos', json=nuevo)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json.get("status"), "ok")