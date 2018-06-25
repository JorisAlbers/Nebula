from BaseHTTPServer import HTTPServer


class NebulaHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, animationReader, bind_and_activate=True, ):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.animationReader = animationReader
