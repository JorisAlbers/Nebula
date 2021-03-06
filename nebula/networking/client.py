import socket
import select
import threading
from message_types import MessageType
#from .. import Timing
import time
 
class Client(threading.Thread):
    def __init__(self, server_ip, server_port, client_id):
        """
        string server_ip - the ip adress of the server.\n
        int server_port - the port of the server.\n
        string client_id - the id of the client. Should be unique for each client.
        """
        if not isinstance(server_ip,str):
            raise ValueError("The server_ip must be of type string")
        if not isinstance(server_port,int):
            raise ValueError("The server_port must be of type int")
        if not isinstance(client_id,str):
            raise ValueError("The client_id must be of type string")
        self.server_ip = server_ip
        self.server_port = server_port 
        self.client_id = client_id
        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.reconnect_wait_ms = 500
        self.connected = False

        #CallBacks
        self.startAnimationCallback = None
        self.clearCallback = None
        self.setBrightnessCallback = None
    
    def init_callbacks(self,startAnimationCallback, clearCallback, brightnessCallback):
        self.startAnimationCallback = startAnimationCallback
        self.clearCallback = clearCallback
        self.setBrightnessCallback = brightnessCallback

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
        try:
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
            if messageType == MessageType.CLEAR:
                print("Server wants me to clear")
                if self.clearCallback is not None:
                    self.clearCallback()
                else:
                    print("Can't clear, callback was not set.")
            if messageType == MessageType.SET_BRIGHTNESS:
                brightness = int(split[1])
                print("Server wants me to set the brightness to {0}".format(brightness))
                if self.setBrightnessCallback is not None:
                    self.setBrightnessCallback()
            else:
                raise ValueError("Unknown or not implemented message type ({0})".format(messageType))
        except Exception,e:
            print("Failed to parse message: ({0}), reason: ([{1}] {2} )".format(message,type(e), e.message))


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
            self.sendToServer(MessageType.CONNECT,self.client_id)
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

