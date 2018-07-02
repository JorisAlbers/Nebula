import socket
import select
import threading
from message_types import MessageType
#from .. import Timing
import time
 
class Client(threading.Thread):
    def __init__(self,server_ip,server_port):
        self.server_ip = server_ip
        self.server_port = server_port 
        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.reconnect_wait_ms = 500
        self.connected = False

        #CallBacks
        self.startAnimationCallback = None
    
    def init_callbacks(self,startAnimationCallback):
        self.startAnimationCallback = startAnimationCallback

    def run(self):
        # A quick inital connection for logging purposes
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        if(self.tryConnectToServer(self.server_ip,self.server_port)):
            print("Connected to server")
        else:
            print("Inital connect to server failed. Will retry every {0} miliseconds".format(self.reconnect_wait_ms))

        while not self.stop_event.is_set():
            if self.connected:
                # Get the list sockets which are readable. Timeout = 1 to keep checking if the stop event has been set.
                socket_list = [self.socket]
                read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [],1)
                for sock in read_sockets:
                    #incoming message from remote server
                    print("Reading message")
                    if sock == self.socket:
                        data = sock.recv(4096)
                        if not data :
                            print("Server connection failed")
                            self.connected = False
                            self.socket.close()
                        else :
                            self.parseMessage(sock,data)
                            
            if not self.connected:
                # The server is disconnected. Try to reconnect
                if(self.tryConnectToServer(self.server_ip,self.server_port)):
                    print("Connected to server")
                else:
                    time.sleep(1)

        #Cleanup
        try:
            self.sendToServer(MessageType.DISCONNECT,"Stop event was set")
        except:
            pass
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def parseMessage(self,socket,message):
        split = message.split(';')
        messageType = MessageType(int(split[0]))
        if (messageType == MessageType.DISCONNECT): # message_type;reason
            print("Server send disconnect signal, reason: {0}".format(split[1]))
            self.connected = False
            self.socket.close()
        if messageType == MessageType.START_ANIMATION: # mt;animation_key;start_at
            print("Server wants me to start animation ({0}) at UNIX : {1}".format(split[1],split[2]))
            # TODO add value checks and send to server if incorrect
            if self.startAnimationCallback is not None:
                self.startAnimationCallback(split[1],float(split[2]))
            else:
                print("Can't start animation, callback was not set.")

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

    def tryConnectToServer(self,ip,port):
        """
        Try to connect to the server. Returns true if connected
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(2)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            return True
        except Exception,e:
            return False

    def stop(self):
        """Stop the client"""
        self.stop_event.set()

    def stopped(self):
        """Check if the client is stopping"""
        return self.stop_event.is_set()

