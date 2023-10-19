# AA_Practica_1
En la carpeta se encuentran los archivos que resuelven la primera práctica de AA

### MODO DE USO:
  - Abrir en la terminal la carpeta "Practica_1"
  - Utilizar el comando "python salaEspera.py" para abrir el serversocket
  - Según el valor de la variable "jugadoresMaximos" en "salaEspera" abrir tantas terminales como haga falta
  - Ejecutar el archivo python "clienteSalaEspera.py" en las terminales e ir visualizando el resultado

### PEQUEÑA EXPLICACIÓN:
  - El server va avisando a los jugadores en la sala de espera de la cantidad de jugadores que hay en la sala
y de la cantidad de jugadores que faltan. Una vez el máximo de jugadores es alcanzado se muestra un mensaje
para indicar que "va a empezar la partida" y simplemente los hilos acaban su función dentro del server y
acaban su ejecución. El servidor sigue funcionando de fondo pero habrá que apagarlo y volverlo a encender
para que vuelva a hacer el recuento.
