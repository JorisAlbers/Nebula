from BaseHTTPServer import HTTPServer
from config import *
from animation.animation_reader import AnimationReader
from config import *
from web_app.http_server import NebulaHTTPServer
from web_app.routes import *


def main():
    try:
        animationReader = AnimationReader(animation_config.resourcePath)
        # If master then:
        if True:
            httpd = NebulaHTTPServer(('', web_config.port), MyRequestHandler, animationReader)
            print 'Server started...'
            httpd.serve_forever()
            print "Running server as master"
    except:
        print "Shutting down"
        # If master then:
        if True:
            httpd.socket.close()


if __name__ == '__main__':
    main()
