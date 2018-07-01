import threading
import socket
import select

class Server(threading.Thread):
    """
    The server acts as a receiving client. 
    """
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
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(10)
        # Add server socket to the list of readable connections
        self.connections.append(self.server_socket)
 
        print("Server started on ip {0}, port {1} ".format(self.ip,self.port))
        while not self.stop_event.is_set():
            # Get the list sockets which are ready to be read through select
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
        self.server_socket.close()