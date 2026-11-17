"""Representación de la memoria física del simulador."""


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
        return "".join("." if celda is None else celda for celda in self.celdas)

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
