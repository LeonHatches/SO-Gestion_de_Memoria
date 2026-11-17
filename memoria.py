"""Representación de la memoria física del simulador."""

from dataclasses import dataclass


@dataclass
class Celda:
    proceso: str
    valor: int = 0


class Memoria:
    def __init__(self, capacidad):
        if capacidad < 1:
            raise ValueError("La capacidad debe ser positiva.")
        self.celdas = [None] * capacidad

    @property
    def capacidad(self):
        return len(self.celdas)

    def libres(self):
        return self.celdas.count(None)

    def mapa(self):
        return "".join("." if celda is None else celda.proceso for celda in self.celdas)

    def mayor_hueco(self):
        mayor = 0
        actual = 0
        for celda in self.celdas:
            if celda is None:
                actual += 1
                mayor = max(mayor, actual)
            else:
                actual = 0
        return mayor

    def buscar_hueco(self, tamano):
        if tamano <= 0:
            raise ValueError("El tamaño debe ser positivo.")
        libres = 0
        for indice, celda in enumerate(self.celdas):
            libres = libres + 1 if celda is None else 0
            if libres == tamano:
                return indice - tamano + 1
        raise ValueError(f"No hay un hueco contiguo de {tamano} posiciones.")

    def ocupar(self, base, tamano, proceso):
        fin = base + tamano
        if not 0 <= base < fin <= self.capacidad:
            raise ValueError("El bloque está fuera de la RAM.")
        if any(celda is not None for celda in self.celdas[base:fin]):
            raise ValueError("El bloque contiene posiciones ocupadas.")
        self.celdas[base:fin] = [Celda(proceso) for _ in range(tamano)]

    def liberar(self, base, tamano):
        self.celdas[base:base + tamano] = [None] * tamano
