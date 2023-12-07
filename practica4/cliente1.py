import paho.mqtt.client as mqtt
import basura
import json
import time

# Variables globales
ip_broker = "localhost" # ip broker
puerto_broker = 1883    # Puerto del broker
topic = "juego-user1"   # topico al que me suscribo para recibir mensajes
topic_contrario = "juego-user2" # topico al que me suscribo para enviar mensajes
tablero = [[None, None, None], [None, None, None], [None, None, None]]  # tablero vacío para empezar juegos
fin_del_juego = False   # Para terminar el hilo
marca = "X" # Como se rellena el tablero

# Sobreescribir el método de conexión
def on_connect(client, userdata, flags, rc):
    print(f"Soy el cliente {client._client_id.decode()} y me voy a suscribir al tópico --> {topic}")
    client.subscribe(topic)

# Método sobreescrito que reacciona una vez llega una publicación al topic suscrito
def on_message(client, userdata, msg):
    global tablero, fin_del_juego
    print(f"Acabo de recibir --> \n   {msg.payload.decode()}")  # Imprimir el mensaje por pantalla
    time.sleep(0.5)
    # Decodificar el mensaje enviado en formato json
    mensaje = json.loads(msg.payload.decode())
    # En el caso de que sea una lista se tratará de parte del juego, en caso contrario
    # tratamos el mensaje como que alguien ha enviado un mensaje al topic en el que estoy y
    # le envio un tablero con el primer movimiento para que empiece el juego
    if not isinstance(mensaje, list):
        casilla = basura.generar_casilla()  # Genero la casilla
        basura.modificar_tablero(tablero, casilla, marca)   # Modifico el tablero
        print("Lo modifico --> \n")
        basura.pintar_tablero(tablero)
        # Lo envio
        mensaje = json.dumps(tablero)
        client.publish(topic_contrario, mensaje)
    # Si recibo un tablero de juego siempre realizaré el siguiente movimeinto (de manera
    # aletoria) sobre el tablero y envio el nuevo tablero al topic suscrito
    else:
        tablero = mensaje   # Cambio el valor de mi variable global
        basura.pintar_tablero(tablero)
        # Comprobamos que el tablero no sea una combinación terminante
        if basura.victoria(tablero):
            print("He perdido")
            fin_del_juego = True
        elif basura.tablas(tablero):
            print("No quedan movimientos")
            fin_del_juego = True
        else:   # No es una combinación terminante, se sigue jugando
            casilla = basura.generar_casilla()  # Genero una casilla
            # Las sigo generando hasta que sean casillas validas
            while not basura.casilla_valida(tablero, casilla):
                casilla = basura.generar_casilla();
            basura.modificar_tablero(tablero, casilla, marca)   # Modifico el tablero
            print("Lo modifico --> \n")
            basura.pintar_tablero(tablero)#Lo envio
            client.publish(topic_contrario, json.dumps(tablero))
            # Vuelvo a comprobar que sean terminantes para poder terminar el hilo
            if basura.victoria(tablero):
                print("He ganado")
                time.sleep(1)
                fin_del_juego = True
            elif basura.tablas(tablero):
                print("No quedan movivimientos despúes del mio")
                time.slep(1)
                fin_del_juego = True

# Inicializamos al cliente MQTT
client1 = mqtt.Client(client_id = "user-1")
# Sobreescribimos sus métodos
client1.on_connect = on_connect
client1.on_message = on_message
# Conectar al broker (IP de la máquina donde se ejecuta, puerto en el que esta el broker, T de espera)
client1.connect(ip_broker, puerto_broker, 60)
# Iniciar el bucle de red
client1.loop_start()
# Saludamos nada más entrar
client1.publish(topic_contrario, json.dumps(f"Saludos, soy {client1._client_id.decode()}, espero algún contrincante"))

while not fin_del_juego:
    pass