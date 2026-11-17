"""Menú del gestor de memoria principal."""

from memoria import Memoria


def ver_estado(ram):
    mapa = ram.mapa()
    print("Mapa de RAM (un punto por posición libre)")
    for inicio in range(0, ram.capacidad, 16):
        fin = min(inicio + 16, ram.capacidad)
        print(f"  {inicio:02d}-{fin - 1:02d}  {mapa[inicio:fin]}")
    print(f"Libres: {ram.libres()} de {ram.capacidad}. Mayor hueco: {ram.mayor_hueco()}.")


def bucle(ram):
    opciones = {
        "2": ("Ver el mapa de RAM", ver_estado),
    }
    while True:
        print()
        print("GESTOR DE MEMORIA PRINCIPAL")
        for numero, (titulo, _) in opciones.items():
            print(f"{numero}. {titulo}")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        if opcion not in opciones:
            print("Elige una opción del menú.")
            continue
        _, accion = opciones[opcion]
        try:
            accion(ram)
        except ValueError as error:
            print(f"Operación rechazada. {error}")


def main():
    try:
        bucle(Memoria(32))
    except (EOFError, KeyboardInterrupt):
        print()
        print("Fin de la simulación.")


if __name__ == "__main__":
    main()
