import unittest

from memoria import Memoria


class PruebasMemoria(unittest.TestCase):
    def test_la_ram_empieza_vacia(self):
        ram = Memoria(8)
        self.assertEqual(ram.capacidad, 8)
        self.assertEqual(ram.libres(), 8)
        self.assertEqual(ram.mapa(), "........")

    def test_el_mayor_hueco_ocupa_toda_la_ram_inicial(self):
        self.assertEqual(Memoria(16).mayor_hueco(), 16)

    def test_rechaza_una_capacidad_invalida(self):
        with self.assertRaises(ValueError):
            Memoria(0)
