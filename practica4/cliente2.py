import paho.mqtt.client as mqtt
import basura
import json
import time
# Variables globales
ip_broker = "localhost" # ip broker
puerto_broker = 1883    # Puerto del broker
topic = "juego-user2"
topic_contrario = "juego-user1"
fin_del_juego = False
marca = "O"

def on_connect(client, userdata, flags, rc):
    print(f"Soy el cliente {client._client_id.decode()} y me voy a suscribir al tópico --> {topic}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global fin_del_juego
    print(f"Acabo de recibir --> \n   {msg.payload.decode()}")
    mensaje = json.loads(msg.payload.decode())
    basura.pintar_tablero(mensaje)
    if basura.victoria(mensaje):
        print("He perdido")
        fin_del_juego = True
    elif basura.tablas(mensaje):
        print("No quedan movimientos")
        fin_del_juego = True
    else:
        casilla = basura.generar_casilla()
        while not basura.casilla_valida(mensaje, casilla):
            casilla = basura.generar_casilla();
        basura.modificar_tablero(mensaje, casilla, marca)
        print("Lo modifico --> \n")
        basura.pintar_tablero(mensaje)
        #Lo envio
        client.publish(topic_contrario, json.dumps(mensaje))
        # Vuelvo a comprobar que sean terminantes para poder terminar el hilo
        if basura.victoria(mensaje):
            print("He ganado")
            time.sleep(1)
            fin_del_juego = True
        if basura.tablas(mensaje):
            print("No quedan movivimientos despúes del mio")
            time.sleep(1)
            fin_del_juego = True

# Inicializamos al cliente MQTT
client2 = mqtt.Client(client_id = "user-2")
# Sobreescribimos sus métodos
client2.on_connect = on_connect
client2.on_message = on_message
# Conectar al broker (IP de la máquina donde se ejecuta, puerto en el que esta el broker, T de espera)
client2.connect(ip_broker, puerto_broker, 60)
# Iniciar el bucle de red
client2.loop_start()
# Saludamos nada más entrar
client2.publish(topic_contrario, json.dumps(f"Saludos, soy {client2._client_id.decode()}"))

while not fin_del_juego:
    pass