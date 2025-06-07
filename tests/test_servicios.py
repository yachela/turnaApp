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
