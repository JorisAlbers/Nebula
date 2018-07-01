import socket
import select
import threading
 
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
        
        while not self.stop_event.isset():
            socket_list = [self.socket]
         
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
            print("Did a select")
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
                        pass