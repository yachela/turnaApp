import unittest
from app import app

class TestDisponibilidades(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_listar_disponibilidades(self):
        """GET /profesionales/1/disponibilidades debe devolver lista (200)."""
        resp = self.client.get('/profesionales/1/disponibilidades')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

    def test_crear_disponibilidad(self):
        """POST /profesionales/1/disponibilidades crea una franja (201)."""
        nuevo = {
            "dia_semana": "Martes",
            "fecha_especifica": None,
            "hora_inicio": "14:00",
            "hora_fin": "16:00"
        }
        resp = self.client.post('/profesionales/1/disponibilidades', json=nuevo)
        self.assertEqual(resp.status_code, 201)
        data = resp.json
        self.assertEqual(data["dia_semana"], "Martes")
        self.assertEqual(data["hora_inicio"], "14:00")
        self.assertEqual(data["hora_fin"], "16:00")
        self.assertEqual(data["profesional_id"], 1)
        self.assertIsInstance(data["id"], int)