# Gestor de memoria principal

Simulador educativo de RAM con Python 3. Ejecuta desde esta carpeta:

    python main.py

El menú permite cargar un proceso, consultar la RAM y terminar procesos.
En la opción 1, indica el identificador y cuatro tamaños en el orden
código, datos, heap y stack. Si pulsas Enter, cada segmento mide 2.
La opción 2 muestra el mapa y las bases de los bloques. Un punto es una
posición libre y una letra identifica al proceso que ocupa esa posición.
La opción 4 libera todos los segmentos de un proceso.

El espacio empieza con 32 posiciones y se puede cambiar con:

    python main.py --capacidad 16

Para verificar la RAM y la carga de procesos:

    python -m unittest pruebas -v
