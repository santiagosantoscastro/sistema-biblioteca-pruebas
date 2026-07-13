"""
Pruebas unitarias sobre el Sistema de Gestión de Biblioteca.
Tipo de prueba: Pruebas Funcionales / Unitarias.

Casos de prueba:
CP-01: Préstamo exitoso de un libro con ejemplares disponibles.
CP-02: Intento de préstamo de un libro sin ejemplares disponibles.
CP-03: Cálculo correcto de la multa por retraso en la devolución.
"""

import unittest
from library_system import (
    Biblioteca,
    SinEjemplaresDisponiblesError,
    LibroNoEncontradoError,
)


class TestSistemaBiblioteca(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba: crea una biblioteca limpia
        y registra un libro de prueba con 1 solo ejemplar disponible."""
        self.biblioteca = Biblioteca()
        self.biblioteca.registrar_libro(
            isbn="978-0134685991",
            titulo="Effective Java",
            autor="Joshua Bloch",
            cantidad=1,
        )

    # ------------------------------------------------------------------
    # CP-01: Préstamo exitoso
    # ------------------------------------------------------------------
    def test_cp01_prestamo_exitoso(self):
        resultado = self.biblioteca.prestar_libro(
            isbn="978-0134685991", usuario="jperez"
        )
        libro = self.biblioteca.buscar_libro("978-0134685991")

        self.assertTrue(resultado)
        self.assertEqual(libro.cantidad_disponible, 0)
        self.assertIn(("978-0134685991", "jperez"), self.biblioteca.prestamos_activos)

    # ------------------------------------------------------------------
    # CP-02: Préstamo sin ejemplares disponibles (caso negativo)
    # ------------------------------------------------------------------
    def test_cp02_prestamo_sin_ejemplares_disponibles(self):
        # Se agota el único ejemplar disponible
        self.biblioteca.prestar_libro(isbn="978-0134685991", usuario="jperez")

        # Un segundo usuario intenta prestar el mismo libro -> debe fallar
        with self.assertRaises(SinEjemplaresDisponiblesError):
            self.biblioteca.prestar_libro(isbn="978-0134685991", usuario="mrodriguez")

    # ------------------------------------------------------------------
    # CP-03: Cálculo de multa por retraso
    # ------------------------------------------------------------------
    def test_cp03_calculo_multa_por_retraso(self):
        multa_5_dias = self.biblioteca.calcular_multa(5)
        multa_sin_retraso = self.biblioteca.calcular_multa(0)
        multa_negativa = self.biblioteca.calcular_multa(-3)

        self.assertEqual(multa_5_dias, 2500)   # 5 días x 500
        self.assertEqual(multa_sin_retraso, 0)
        self.assertEqual(multa_negativa, 0)     # nunca debe ser negativa

    # ------------------------------------------------------------------
    # búsqueda de un libro inexistente
    # ------------------------------------------------------------------
    def test_busqueda_libro_inexistente(self):
        with self.assertRaises(LibroNoEncontradoError):
            self.biblioteca.buscar_libro("000-0000000000")


if __name__ == "__main__":
    unittest.main(verbosity=2)
