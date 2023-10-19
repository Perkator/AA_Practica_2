import socket
# Client side

import sys

host, port = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((host, port))

    # Receive data from the server
    while True:
        received = str(sock.recv(1024), "utf-8") #decoding
        if received == "":
            break
        print("Received: {}".format(received))