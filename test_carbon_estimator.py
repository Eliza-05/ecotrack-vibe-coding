"""Pruebas de carbon_estimator.py usando unittest (librería estándar).

Ejecutar con: python -m unittest test_carbon_estimator.py -v
"""

import unittest

from carbon_estimator import estimar_huella


class TestCasosPrevios(unittest.TestCase):
    """Casos que ya funcionaban antes de esta corrección; no deben romperse."""

    def test_ejemplo_base_carne_y_bus(self):
        total, actividades = estimar_huella("Hoy comí carne y viajé 20 km en bus")
        self.assertEqual(total, 8.0)
        descripciones = {a.descripcion for a in actividades}
        self.assertIn("20 km en bus", descripciones)
        self.assertIn("Comida: carne", descripciones)

    def test_texto_vacio(self):
        self.assertEqual(estimar_huella(""), (0.0, []))

    def test_texto_solo_espacios(self):
        self.assertEqual(estimar_huella("   "), (0.0, []))

    def test_sin_actividades_reconocibles(self):
        total, actividades = estimar_huella("Fui a dormir temprano")
        self.assertEqual(total, 0)
        self.assertEqual(actividades, [])

    def test_multiples_alimentos_sin_verbo_conducir(self):
        # "caminé" no es un verbo de conducir y no hay "en <medio>", así que
        # el tramo en km no debe generar una actividad de transporte.
        total, actividades = estimar_huella("Comí pollo y pescado, y caminé 5 km")
        descripciones = {a.descripcion for a in actividades}
        self.assertIn("Comida: pollo", descripciones)
        self.assertIn("Comida: pescado", descripciones)
        self.assertEqual(len(actividades), 2)
        self.assertEqual(total, 2.6)


class TestCorreccionesReportadas(unittest.TestCase):
    """Casos reportados como fallando; deben quedar corregidos."""

    def test_caso_1_dos_medios_de_transporte_en_una_frase(self):
        total, actividades = estimar_huella(
            "Hoy comí pollo, viajé 10 km en carro y 5 km en bus"
        )
        descripciones = {a.descripcion: a.co2e_kg for a in actividades}

        self.assertIn("10 km en carro", descripciones)
        self.assertAlmostEqual(descripciones["10 km en carro"], 1.9)

        self.assertIn("5 km en bus", descripciones)
        self.assertAlmostEqual(descripciones["5 km en bus"], 0.5)

        self.assertIn("Comida: pollo", descripciones)
        self.assertEqual(len(actividades), 3)
        self.assertAlmostEqual(total, 3.5)

    def test_caso_2_verbo_manejar_sin_en_medio(self):
        total, actividades = estimar_huella("Hoy manejé 15 km y comí pescado")
        descripciones = {a.descripcion: a.co2e_kg for a in actividades}

        self.assertIn("15 km en carro", descripciones)
        self.assertAlmostEqual(descripciones["15 km en carro"], 2.85)
        self.assertIn("Comida: pescado", descripciones)
        self.assertEqual(len(actividades), 2)
        self.assertAlmostEqual(total, 4.35)

    def test_verbo_conducir_pretérito(self):
        total, actividades = estimar_huella("Ayer conduje 15 km")
        self.assertEqual(len(actividades), 1)
        self.assertEqual(actividades[0].descripcion, "15 km en carro")
        self.assertAlmostEqual(total, 2.85)


if __name__ == "__main__":
    unittest.main()
