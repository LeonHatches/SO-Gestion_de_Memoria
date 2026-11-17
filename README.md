# Gestor de memoria principal por segmentos

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

## Compactación

En la opción 5, los segmentos se desplazan juntos hacia el inicio. El
gestor actualiza sus bases. Los permisos, las posiciones lógicas y los
valores de cada segmento se conservan.

Para ensayar un caso listo para usar:

    python main.py --practica

1. Elige 2 y observa el mapa. A y C están en RAM y el hueco de B quedó libre.
2. Elige 1, escribe D, y pide 2 10 2 2. Hay 16 libres repartidas en huecos de 8.
3. Elige 5. El mayor hueco pasa de 8 a 16 sin cambiar el total libre.
4. Elige 1 y vuelve a cargar D con 2 10 2 2. La carga se completa.

## Intercambio

En la opción 6, E copia los valores de un proceso al almacenamiento
simulado y libera sus segmentos en RAM. R vuelve a cargar el proceso y
restaura sus valores. Si la RAM no alcanza, el proceso sigue guardado.
Si hay huecos dispersos, puedes compactar antes de recuperar el proceso.
El almacenamiento se guarda en memoria durante la ejecución del menú.

## Pruebas

Para verificar la RAM, carga, traducción, permisos, compactación e intercambio:

    python -m unittest pruebas -v
