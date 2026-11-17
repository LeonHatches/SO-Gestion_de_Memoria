"""Gestión de procesos y sus tablas de segmentos."""

from dataclasses import dataclass
from string import ascii_uppercase

NOMBRES_SEGMENTOS = ("codigo", "datos", "heap", "stack")
PERMISOS = {"codigo": "R", "datos": "RW", "heap": "RW", "stack": "RW"}


@dataclass
class Segmento:
    base: int
    tamano: int
    permisos: str

    def direccion(self, desplazamiento):
        if type(desplazamiento) is not int or not 0 <= desplazamiento < self.tamano:
            raise ValueError(f"Posición fuera del segmento. Usa 0 a {self.tamano - 1}.")
        return self.base + desplazamiento


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
                segmentos[nombre] = Segmento(base, tamano, PERMISOS[nombre])
        except ValueError:
            for segmento in segmentos.values():
                self.ram.liberar(segmento.base, segmento.tamano)
            raise
        self.procesos[proceso] = segmentos

    def obtener_proceso(self, proceso):
        if proceso not in self.procesos:
            raise ValueError(f"El proceso {proceso} no está en la RAM.")
        return self.procesos[proceso]

    def terminar(self, proceso):
        segmentos = self.obtener_proceso(proceso)
        for segmento in segmentos.values():
            self.ram.liberar(segmento.base, segmento.tamano)
        del self.procesos[proceso]

    def obtener_segmento(self, proceso, nombre):
        segmentos = self.obtener_proceso(proceso)
        if nombre not in segmentos:
            raise ValueError(f"El proceso {proceso} no tiene un segmento {nombre}.")
        return segmentos[nombre]

    def traducir(self, proceso, nombre, desplazamiento):
        """Convierte un desplazamiento válido en una dirección de RAM."""
        segmento = self.obtener_segmento(proceso, nombre)
        return segmento.direccion(desplazamiento)
