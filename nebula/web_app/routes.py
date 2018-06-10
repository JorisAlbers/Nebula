from BaseHTTPServer import BaseHTTPRequestHandler
from controllers import *
import re


class Router(object):

    def __init__(self, server):
        self.__routes = []
        self.__server = server

    def addRoute(self, regexp, controller, action):
        self.__routes.append({'regexp': regexp, 'controller': controller, 'action': action})

    def route(self, path):
        for route in self.__routes:
            if re.search(route['regexp'], path):
                cls = globals()[route['controller']]
                func = cls.__dict__[route['action']]
                obj = cls(self.__server)
                apply(func, (obj,))
                return

        # Not found
        self.__server.send_response(404)
        self.__server.end_headers()


class MyRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        routes = [

            {'regexp': r'^/$', 'controller': 'IndexController', 'action': 'indexAction'},
            {'regexp': r'^/public/', 'controller': 'ContentController', 'action': 'showAction'},
            {'regexp': r'^/update', 'controller': 'UpdateController', 'action': 'indexAction'},

        ]

        self.__router = Router(self)
        for route in routes:
            self.__router.addRoute(route['regexp'], route['controller'], route['action'])

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.__router.route(self.path)
