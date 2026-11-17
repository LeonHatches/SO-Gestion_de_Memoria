import unittest

from memoria import Memoria


class PruebasMemoria(unittest.TestCase):
    def test_la_ram_empieza_vacia(self):
        ram = Memoria(8)
        self.assertEqual(ram.capacidad, 8)
        self.assertEqual(ram.libres(), 8)
        self.assertEqual(ram.mapa(), "........")
