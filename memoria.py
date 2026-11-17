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
