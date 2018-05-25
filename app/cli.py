#!/usr/bin/python
from BaseHTTPServer import HTTPServer
from routes import *
from config import WebConfig


def main():
    try:
        httpd = HTTPServer(('', WebConfig.port), MyRequestHandler)
        print 'Server started...'
        httpd.serve_forever()
    except:
        print 'Server shutting down'
        httpd.socket.close()


if __name__ == '__main__':
    main()
