import select
from copy import deepcopy
from threading import Thread
import utils
from message import Message
import json
import config

class NodeServer(Thread):
    def __init__(self, node):
        Thread.__init__(self)
        self.node = node
        #On initialization
        self.state = config.released
        self.queueNodes = []
        self.voted = False
        self.replied = 0
    
    def run(self):
        self.update()

    def update(self):
        self.connection_list = []
        self.server_socket = utils.create_server_socket(self.node.port)
        self.connection_list.append(self.server_socket)

        while self.node.daemon:
            (read_sockets, write_sockets, error_sockets) = select.select(
                self.connection_list, [], [], 5)
            if not (read_sockets or write_sockets or error_sockets):
                print('NS%i - Timed out'%self.node.id) #force to assert the while condition 
            else:
                for read_socket in read_sockets:
                    if read_socket == self.server_socket:
                        (conn, addr) = read_socket.accept()
                        self.connection_list.append(conn)
                    else:
                        try:
                            msg_stream = read_socket.recvfrom(4096)
                            for msg in msg_stream:
                                try:
                                    ms = json.loads(str(msg,"utf-8"))
                                    self.process_message(ms)
                                except:
                                    None
                        except:
                            read_socket.close()
                            self.connection_list.remove(read_socket)
                            continue
        
        self.server_socket.close()

    def set_state(self, state):
        self.state = state
    
    def process_message(self, msg):
        global queuenodes
        new_msg = deepcopy(msg)
        # On receipt of a release from pi at pj 
        if new_msg.get_msgtype == "release":
            if not queueNodes.clear:
                self.queueNodes.pop()
                #Send reply to pk
                message = Message(msg_type="reply",
                            src=self.id,
                            data="Hola, this is Node_%i _ counter:%i"%(self.id,self.wakeupcounter))
                self.node.client.multicast(message, self.queueNodes)
                self.voted = True
            else:
                self.voted = False
        #On receipt of a request from pi at pj
        elif msg.get_msgtype == "accessSc":
            if self.state == config.held or not self.voted:
                self.queueNodes.append(new_msg.get_source)
            else:
                reply = Message(msg_type="reply",
                            src=self.id)
                self.node.client.send_message(reply,new_msg.get_source)
                self.voted = True
        elif smg.get_msgtype == "reply": #reply
            self.replied += 1
                
        print("Node_%i receive msg: %s"%(self.node.id,new_msg))
