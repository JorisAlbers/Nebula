import threading
import socket
import select

class Server(threading.Thread):
    def __init__(self, ip,port):
        self.ip = ip
        self.port = port
        self.connections = []

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
            # Get the list sockets which are ready to be read through select
            print("Server main loop")
            read_sockets,write_sockets,error_sockets = select.select(self.connections,[],[])

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
                            #TODO Parse message and call correct callback
                            pass
                                          
                    except:
                        # The client is no longer connected
                        # TODO do stuff on connection cloesed
                        print "Client (%s, %s) is offline" % addr
                        sock.close()
                        self.connections.remove(sock)
                        continue

        #Cleanup
        self.server_socket.shutdown()
        self.server_socket.close()
        

    def broadcast(self,message):
        """
        Send a message to all connected clients
        """
        for socket in self.connections:
            if socket != self.server_socket:
                self.sendToSocket(socket,message)

    def sendToSocket(self,socket, message):
        """
        Send a message to a socket
        """
        try:
            socket.send(message)
        except:
            # Broken socket
            print("Connection with {0} closed. Removing from list of active connections.".format(socket.getpeername()))
            socket.close()
            self.connections.remove(socket)

    def stop(self):
        """Stop the server controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the server is stopping"""
        return self.stop_event.is_set()
