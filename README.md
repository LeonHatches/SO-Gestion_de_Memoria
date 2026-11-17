# Gestor de memoria principal

Simulador educativo de RAM con Python 3. Ejecuta desde esta carpeta:

    python main.py

El menú permite cargar un proceso, consultar la RAM y terminar procesos.
En la opción 1, indica el identificador y cuatro tamaños en el orden
código, datos, heap y stack. Si pulsas Enter, cada segmento mide 2.
La opción 2 muestra el mapa y las bases de los bloques. Un punto es una
posición libre y una letra identifica al proceso que ocupa esa posición.
La opción 4 libera todos los segmentos de un proceso.

La opción 3 simula una solicitud de la CPU. Carga A con tamaños 2 2 2 2,
elige el segmento datos y pide la posición lógica 1. La base de datos
es 2 y la dirección física que calcula el menú es 3. Selecciona T
para traducir, L para leer o E para escribir un valor entero.

Código tiene permiso R (lectura). Datos, heap y stack tienen RW
(lectura y escritura). Prueba escribir 42 en A / datos / 1 y léelo.
Luego intenta escribir en A / codigo / 0 y observa el rechazo.

El espacio empieza con 32 posiciones y se puede cambiar con:

    python main.py --capacidad 16

Para verificar la RAM, la carga, la traducción y la protección:

    python -m unittest pruebas -v
