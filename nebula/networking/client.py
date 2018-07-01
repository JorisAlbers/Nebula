import socket
import select
import threading
from message_types import MessageType
 
class Client(threading.Thread):
    def __init__(self,server_ip,server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
         # connect to remote host
        try :
            self.socket.connect((self.server_ip, self.server_port))
            print("Connected to server")
        except :
            print("Unable to connect to server")
            return
        
        while not self.stop_event.is_set():
            # Get the list sockets which are readable. Timeout = 1 to keep checking if the stop event has been set.
            socket_list = [self.socket]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [],1)
            for sock in read_sockets:
                #incoming message from remote server
                if sock == self.socket:
                    data = sock.recv(4096)
                    if not data :
                        print("Server disconnected")
                        #TODO try to reconnect
                        return
                    else :
                        # TODO parse message and call callback
                        print("Message received from server: {0}".format(data))
                        pass
        
        #Cleanup
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def sendToServer(self,message_type,message):
        if not isinstance(message_type, MessageType):
            raise ValueError("The message_type must be an MessageType!")
        if not isinstance(message,str):
            raise ValueError("The message must be of type string!")
        try:
            self.socket.send("{0};{1}".format(int(message_type),message))
        except:
            raise Exception("Server connection lost")
            #TODO handle this, try to reconnect for x tries or something

    def stop(self):
        """Stop the client"""
        self.stop_event.set()

    def stopped(self):
        """Check if the client is stopping"""
        return self.stop_event.is_set()

