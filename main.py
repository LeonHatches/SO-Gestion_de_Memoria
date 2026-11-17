"""Menú del gestor de memoria principal."""

import argparse

from gestor import Gestor, NOMBRES_SEGMENTOS
from memoria import Memoria


def ver_estado(gestor):
    ram = gestor.ram
    mapa = ram.mapa()
    print("Mapa de RAM (un punto por posición libre)")
    for inicio in range(0, ram.capacidad, 16):
        fin = min(inicio + 16, ram.capacidad)
        print(f"  {inicio:02d}-{fin - 1:02d}  {mapa[inicio:fin]}")
    print(f"Libres: {ram.libres()} de {ram.capacidad}. Mayor hueco: {ram.mayor_hueco()}.")
    print("Cada letra identifica un proceso.")
    if gestor.procesos:
        print("  PID  Segmento  Base  Tamaño  Rango lógico")
        for proceso, segmentos in sorted(gestor.procesos.items()):
            for nombre, segmento in segmentos.items():
                print(f"  {proceso:>3}  {nombre:<8}  {segmento.base:>4}  "
                      f"{segmento.tamano:>6}  0-{segmento.tamano - 1}")
    else:
        print("No hay procesos en RAM.")


def cargar_proceso(gestor):
    proceso = input("Proceso (A-Z): ").strip().upper()
    entrada = input("Tamaños de codigo datos heap stack [2 2 2 2]: ").split()
    tamanos = [int(valor) for valor in entrada] if entrada else [2] * 4
    if len(tamanos) != len(NOMBRES_SEGMENTOS):
        raise ValueError("Escribe cuatro tamaños separados por espacios.")
    gestor.cargar(proceso, dict(zip(NOMBRES_SEGMENTOS, tamanos)))
    print(f"Proceso {proceso} cargado.")


def pedir_direccion():
    proceso = input("Proceso: ").strip().upper()
    nombre = input("Segmento (codigo/datos/heap/stack): ").strip().lower()
    desplazamiento = int(input("Posición lógica: "))
    return proceso, nombre, desplazamiento


def consultar_direccion(gestor):
    modo = input("CPU: [T]raducir, [L]eer o [E]scribir: ").strip().lower()
    if modo not in ("t", "l", "e"):
        raise ValueError("Elige T, L o E.")
    proceso, nombre, desplazamiento = pedir_direccion()
    if modo == "t":
        fisica = gestor.traducir(proceso, nombre, desplazamiento)
        base = gestor.obtener_segmento(proceso, nombre).base
        print(f"{proceso}/{nombre}: base {base} + posición {desplazamiento} = física {fisica}.")
    elif modo == "l":
        fisica, valor = gestor.leer(proceso, nombre, desplazamiento)
        print(f"Lectura en la posición física {fisica}: {valor}.")
    else:
        valor = int(input("Valor entero: "))
        fisica = gestor.escribir(proceso, nombre, desplazamiento, valor)
        print(f"Se escribió {valor} en la posición física {fisica}.")


def terminar_proceso(gestor):
    proceso = input("Proceso que termina: ").strip().upper()
    gestor.terminar(proceso)
    print(f"Proceso {proceso} terminado. Sus posiciones quedaron libres.")


def bucle(gestor):
    opciones = {
        "1": ("Cargar un proceso", cargar_proceso),
        "2": ("Ver RAM y tabla de segmentos", ver_estado),
        "3": ("Traducir, leer o escribir una dirección lógica", consultar_direccion),
        "4": ("Terminar un proceso", terminar_proceso),
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
            accion(gestor)
        except ValueError as error:
            print(f"Operación rechazada. {error}")


def main():
    parser = argparse.ArgumentParser(description="Gestor de memoria principal")
    parser.add_argument("--capacidad", type=int, default=32, help="posiciones de RAM (32 por defecto)")
    args = parser.parse_args()
    if args.capacidad < 1:
        parser.error("la capacidad debe ser positiva")
    try:
        bucle(Gestor(Memoria(args.capacidad)))
    except (EOFError, KeyboardInterrupt):
        print()
        print("Fin de la simulación.")


if __name__ == "__main__":
    main()
