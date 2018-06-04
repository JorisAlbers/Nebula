#!/usr/bin/python
from BaseHTTPServer import HTTPServer
from routes import *
from config import web_config


def main():
    try:
        httpd = HTTPServer(('', web_config.port), MyRequestHandler)
        print 'Server started...'
        httpd.serve_forever()
    except:
        print 'Server shutting down'
        httpd.socket.close()


if __name__ == '__main__':
    main()
