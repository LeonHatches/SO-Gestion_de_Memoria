import unittest

from gestor import Gestor, NOMBRES_SEGMENTOS
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


def tamanos(codigo=2, datos=2, heap=2, stack=2):
    return dict(zip(NOMBRES_SEGMENTOS, (codigo, datos, heap, stack)))


class PruebasGestor(unittest.TestCase):
    def setUp(self):
        self.gestor = Gestor(Memoria(32))

    def test_carga_cuatro_segmentos_y_reusa_el_hueco(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.cargar("B", tamanos())
        self.assertEqual(self.gestor.ram.mapa(), "A" * 8 + "B" * 8 + "." * 16)
        self.gestor.terminar("A")
        self.gestor.cargar("C", tamanos())
        self.assertEqual(self.gestor.procesos["C"]["codigo"].base, 0)

    def test_carga_fallida_devuelve_las_reservas_parciales(self):
        self.gestor.cargar("A", tamanos())
        anterior = self.gestor.ram.mapa()
        with self.assertRaises(ValueError):
            self.gestor.cargar("D", tamanos(datos=28))
        self.assertEqual(self.gestor.ram.mapa(), anterior)
        self.assertNotIn("D", self.gestor.procesos)

    def test_rechaza_un_proceso_duplicado(self):
        self.gestor.cargar("A", tamanos())
        with self.assertRaises(ValueError):
            self.gestor.cargar("A", tamanos(datos=4))

    def test_la_misma_posicion_logica_tiene_bases_distintas(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.cargar("B", tamanos())
        self.assertEqual(self.gestor.traducir("A", "datos", 1), 3)
        self.assertEqual(self.gestor.traducir("B", "datos", 1), 11)

    def test_proceso_y_segmento_deben_existir(self):
        self.gestor.cargar("A", tamanos())
        with self.assertRaises(ValueError):
            self.gestor.traducir("A", "otro", 0)
        with self.assertRaises(ValueError):
            self.gestor.traducir("B", "datos", 0)

    def test_limites_de_un_segmento_de_dos_posiciones(self):
        self.gestor.cargar("A", tamanos())
        self.assertEqual(self.gestor.traducir("A", "datos", 0), 2)
        self.assertEqual(self.gestor.traducir("A", "datos", 1), 3)
        for invalida in (-1, 2, 1.5):
            with self.subTest(posicion=invalida):
                with self.assertRaises(ValueError):
                    self.gestor.traducir("A", "datos", invalida)

    def test_codigo_es_de_solo_lectura(self):
        self.gestor.cargar("A", tamanos())
        self.assertEqual(self.gestor.leer("A", "codigo", 0), (0, 0))
        with self.assertRaisesRegex(ValueError, "permisos R"):
            self.gestor.escribir("A", "codigo", 0, 61)
        self.assertEqual(self.gestor.leer("A", "codigo", 0), (0, 0))

    def test_escribir_datos_no_modifica_otro_proceso(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.cargar("B", tamanos())
        self.assertEqual(self.gestor.escribir("A", "datos", 1, 42), 3)
        self.assertEqual(self.gestor.leer("A", "datos", 1), (3, 42))
        self.assertEqual(self.gestor.leer("B", "datos", 1), (11, 0))

    def test_un_desbordamiento_no_modifica_el_segmento_vecino(self):
        self.gestor.cargar("A", tamanos())
        with self.assertRaisesRegex(ValueError, "fuera del segmento"):
            self.gestor.escribir("A", "datos", 2, 42)
        self.assertEqual(self.gestor.leer("A", "heap", 0), (4, 0))

    def test_compactar_une_huecos_y_preserva_el_acceso_logico(self):
        for proceso in "ABC":
            self.gestor.cargar(proceso, tamanos())
        self.gestor.escribir("C", "datos", 1, 42)
        self.gestor.terminar("B")
        mapa = self.gestor.ram.mapa()
        self.assertEqual(mapa, "AAAAAAAA........CCCCCCCC........")
        self.assertEqual(self.gestor.ram.libres(), 16)
        self.assertEqual(self.gestor.ram.mayor_hueco(), 8)
        with self.assertRaises(ValueError):
            self.gestor.cargar("D", tamanos(datos=10))
        self.assertEqual(self.gestor.ram.mapa(), mapa)
        self.assertEqual(self.gestor.leer("C", "datos", 1), (19, 42))

        self.assertEqual(self.gestor.compactar(), 4)
        self.assertEqual(self.gestor.ram.mayor_hueco(), 16)
        self.assertEqual(self.gestor.leer("C", "datos", 1), (11, 42))
        self.gestor.cargar("D", tamanos(datos=10))
        self.assertEqual(self.gestor.ram.libres(), 0)

    def test_compactar_una_ram_vacia(self):
        self.assertEqual(self.gestor.compactar(), 0)
        self.assertEqual(self.gestor.ram.mayor_hueco(), 32)

    def test_recupera_el_proceso_con_los_mismos_valores_en_otra_base(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.escribir("A", "datos", 1, 57)
        self.gestor.enviar("A")
        self.assertEqual(self.gestor.ram.libres(), 32)
        with self.assertRaises(ValueError):
            self.gestor.cargar("A", tamanos())
        self.gestor.cargar("B", tamanos())
        self.gestor.recuperar("A")
        self.assertEqual(self.gestor.leer("A", "datos", 1), (11, 57))
        self.assertNotIn("A", self.gestor.intercambio)

    def test_recuperacion_sin_espacio_conserva_el_proceso_en_intercambio(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.escribir("A", "datos", 1, 55)
        self.gestor.enviar("A")
        self.gestor.cargar("B", tamanos(datos=25))
        antes = self.gestor.ram.mapa()
        with self.assertRaises(ValueError):
            self.gestor.recuperar("A")
        self.assertEqual(self.gestor.ram.mapa(), antes)
        self.assertNotIn("A", self.gestor.procesos)
        self.assertEqual(self.gestor.intercambio["A"]["datos"], [0, 55])

    def test_terminar_un_proceso_suspendido_libera_su_identificador(self):
        self.gestor.cargar("A", tamanos())
        self.gestor.enviar("A")
        self.gestor.terminar("A")
        self.gestor.cargar("A", tamanos())
        self.assertNotIn("A", self.gestor.intercambio)
