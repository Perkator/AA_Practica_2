import socketserver
import threading

# Variables globales
jugadores = 0
jugadoresMaximos = 3

# The server based on threads for each connection
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # DOC: ThreadingMixIn define un atributo daemon_threads, que indica si el servidor debe esperar o no la terminación del hilo

    daemon_threads = True
    allow_reuse_address = True

class PlayerHandler(socketserver.StreamRequestHandler):
    def handle(self): # A new message come
        print(f"Connected: {self.client_address} on {threading.current_thread().name}")
        try:
            self.initialize()
            self.espera()
        except Exception as e:
            print(e)
        
    def send(self, message):
        self.wfile.write((f"{message}\n").encode('utf-8'))

    def initialize(self):
        global jugadores, jugadoresMaximos
        jugadores = jugadores + 1
        self.send(f"WELCOME PLAYER {jugadores}")
        if jugadores == jugadoresMaximos:
            self.send("¡Ya estais todos!")
        else:
            self.send('Sois %d/%d jugadores, ¡Esperando al resto!'%(jugadores,jugadoresMaximos))
    
    def espera(self):
        global jugadores, jugadoresMaximos
        jugadoresActuales = jugadores
        if jugadores < jugadoresMaximos:
            while jugadores < jugadoresMaximos:
                if jugadoresActuales != jugadores:
                    jugadoresActuales = jugadoresActuales + 1
                    self.send(f'Sois {jugadores}/{jugadoresMaximos} jugadores, ¡Esperando al resto!')
                pass
        self.send("La partida va a empezar")

server = ThreadedTCPServer(('', 9999), PlayerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()