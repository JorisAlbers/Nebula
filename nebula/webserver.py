from BaseHTTPServer import HTTPServer
from config import *
from repositories.animation_reader import AnimationReader
from config import Config
from web_app.http_server import NebulaHTTPServer
from web_app.routes import *
import threading


class WebServer(threading.Thread):
    def __init__(self,ip,port,animationReader):
        if not isinstance(ip,str):
            raise ValueError("The ip must be a string")
        if not isinstance(port,int):
            raise ValueError("The port must be an int")
        if not isinstance(animationReader,AnimationReader):
            raise ValueError("The animation reader must be an animationReader")
        self.ip = ip
        self.port = port
        self.animationReader = animationReader
        self.server = NebulaHTTPServer((ip, port), MyRequestHandler, animationReader)
        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def start(self):
        try:
            while not self.stop_event.is_set():
                self.server.httpd.serve_forever(1) # 1 to allow polling

        except Exception, e:
            print("Webserver failed. shutting down. Exception ({0}) - {1}".format(type(e),e.message))
        finally:
            # Cleanup



            try:
                self.server.socket.close()
            except Exception, e:
                print("Webserver closing failed. Exception ({0}) - {1}".format(type(e), e.message))

    def stop(self):
        """Stop the webserver"""
        self.stop_event.set()

    def stopped(self):
        """Check if the webserver is stopping"""
        return self.stop_event.is_set()


if __name__ == '__main__':
    """
    For testing purposes
    """
    ip = "localhost"
    port = 8080
    animationReader = AnimationReader('./../resources')
    webserver = WebServer(animationReader)
    webserver.start()
    webserver.join()

