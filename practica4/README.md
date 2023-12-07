# AA_Practica_4
En la carpeta se encuentran los archivos que resuelven la segunda práctica de Mosquitto+

### Modo de uso
    - Ejecutar el broker de mosquitto (preferiblemente en el puerto 1883 pero es modificable en el código)
    - Ejecutar los archivos python de manera habitual
    - IMPORTANTE: Siempre ejecutar el "cliente1" antes del "cliente2" debido a que será el cliente 1 el que
    empezará mandando el primer tablero, el cliente 2 no tiene incorporada esta función

### Cosas a tener en cuenta
    - El código referente a los hilos solo esta comentado en el primer cliente ya que el segundo 
    hace exactamente lo mismo o muy parecido
    - El archivo "basura" no es basura, es el nombre que le he puesto y es donde están las 
    funciones relacionadas con la mecánica del juego. Cada vez que se lea "basura" leer en su lugar "tictactoe"
    - Cuando acaban las ejecuciones por algún motivo el segundo no revibe bien el último tablero y no llega a 
    acabar. No he encontrado el motivo de porque sucede esto