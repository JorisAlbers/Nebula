import threading
import socket
import select
from message_types import MessageType

class Server(threading.Thread):
    def __init__(self, ip,port):
        self.ip = ip
        self.port = port
        self.connections = []
        self.client_to_socket = {}
        self.socket_to_client = {}

        self.RECV_BUFFER = 4096

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this has no effect, why ?
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        print("Start")
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(10)
        # Add server socket to the list of readable connections
        self.connections.append(self.server_socket)
 
        print("Server started on ip {0}, port {1} ".format(self.ip,self.port))
        while not self.stop_event.is_set():
            # Get the list sockets which are ready to be read through select. Timeout = 1, to keep checking if the stop event is set
            read_sockets,write_sockets,error_sockets = select.select(self.connections,[],[],1)

            for sock in read_sockets:
                #New connection
                if sock == self.server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = self.server_socket.accept()
                    self.connections.append(sockfd)
                    print "Client (%s, %s) connected" % addr

                #Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            print('Message recieved: {0}'.format(data))
                            sock.send("server received the message : {0}".format(data))
                            self.parseMessage(sock,data)
                            pass
                                          
                    except:
                        # TODO do stuff on connection cloesed
                        print("Sending data failed to {0} failed. Closing socket.")
                        sock.close()
                        self.connections.remove(sock)
                        continue
            

        #Cleanup
        self.broadcast(MessageType.DISCONNECT,"Server is shutting down")
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.server_socket.close()
        
    def parseMessage(self,socket,message):
        try:
            split = message.split(';')
            messageType = MessageType(int(split[0]))
            if (messageType == MessageType.CONNECT):# message_type;client_id
                client_id = split[1]
                if client_id in self.client_to_socket: 
                    print("Client with id ({0}) reconnected.".format(client_id))
                    old_socket = self.client_to_socket[client_id]
                    self.closeSocket(old_socket,"A new client with the same id has connected")
                    del self.socket_to_client[old_socket]
                    self.client_to_socket[client_id] = socket
                    self.socket_to_client[socket] = client_id
                else:
                    print("Client with id ({0}) connected for the first time.".format(client_id))
                    self.client_to_socket[client_id] = socket
                    self.socket_to_client[socket] = client_id
                
            elif (messageType == MessageType.DISCONNECT): # message_type;reason
                client_id = self.socket_to_client[socket]
                print("Client {0} is disconnecting".format(client_id))
                self.connections.remove(socket)
                #del self.client_to_socket[client_id]
                #del self.socket_to_client[socket]
        except Exception,e:
            print("Failed to parse message: ({0}), reason: ({1})".format(message,str(e)))

    def broadcast(self,message_type,message):
        """
        Send a message to all connected clients
        """
        for socket in self.connections:
            if socket != self.server_socket:
                self.sendToSocket(socket,message_type,message)

    def sendToSocket(self,socket, message_type, message):
        """
        Send a message to a socket
        """
        try:
            socket.send("{0};{1}".format(int(message_type),message))
        except:
            print("Connection with {0} closed. Removing from list of active connections.".format(socket.getpeername()))
            try:
                if socket in self.connections:
                    self.connections.remove(socket)
            except:
                pass

    def sendToClient(self, client_id, message_type, message):
        """
        Send a message to a specific client by its ID.
        """
        if not client_id in self.client_to_socket:
            raise ValueError("The client with id {} does not exist".format(client_id))
        self.sendToSocket(self.client_to_socket[client_id],message_type,message)

    def closeSocket(self,socket,reason):
        """
        Tell the socket that the connection will be closed and close the socket
        """
        try:
            socket.send("{0};{1}".format(int(MessageType.DISCONNECT),reason))
        except:
            print("can't send close message to socket, was already closed.")
        finally:
            try:
                socket.close()
            except:
                print("Can't close socket, was already closed.")
            finally:
                try:
                    if socket in self.connections:
                        self.connections.remove(socket)
                except Exception,e:
                    print("Socket was already removed from connections.")

    def stop(self):
        """Stop the server controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the server is stopping"""
        return self.stop_event.is_set()
