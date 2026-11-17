"""Gestión de procesos y sus tablas de segmentos."""

from dataclasses import dataclass
from string import ascii_uppercase

NOMBRES_SEGMENTOS = ("codigo", "datos", "heap", "stack")


@dataclass
class Segmento:
    base: int
    tamano: int


class Gestor:
    def __init__(self, ram):
        self.ram = ram
        self.procesos = {}

    def cargar(self, proceso, tamanos):
        if len(proceso) != 1 or proceso not in ascii_uppercase:
            raise ValueError("Identifica el proceso con una letra entre A y Z.")
        if proceso in self.procesos:
            raise ValueError(f"El proceso {proceso} ya está cargado.")
        if set(tamanos) != set(NOMBRES_SEGMENTOS):
            raise ValueError("Indica los tamaños de código, datos, heap y stack.")
        if any(type(tamano) is not int or tamano <= 0 for tamano in tamanos.values()):
            raise ValueError("Los cuatro tamaños deben ser enteros positivos.")

        segmentos = {}
        try:
            for nombre in NOMBRES_SEGMENTOS:
                tamano = tamanos[nombre]
                base = self.ram.buscar_hueco(tamano)
                self.ram.ocupar(base, tamano, proceso)
                segmentos[nombre] = Segmento(base, tamano)
        except ValueError:
            for segmento in segmentos.values():
                self.ram.liberar(segmento.base, segmento.tamano)
            raise
        self.procesos[proceso] = segmentos
