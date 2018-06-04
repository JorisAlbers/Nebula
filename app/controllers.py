from Cheetah.Template import Template
import os
from config import *


class Controller(object):
    def __init__(self, server):
        self.__server = server

    @property
    def server(self):
        return self.__server


class ContentController(Controller):
    CONTENT_BASE_PATH = 'app/public/'

    def __init__(self, server):
        Controller.__init__(self, server)

    def showAction(self):
        filename = ContentController.CONTENT_BASE_PATH + self.server.path[9:]
        if os.access(filename, os.R_OK) and not os.path.isdir(filename):
            # TODO: is there any possibility to access files outside the root with ..?
            file = open(filename, "r")
            content = file.read()
            file.close()

            # TODO: set correct content type
            self.server.send_response(200)
            self.server.send_header('Content-type', 'text/html')
            self.server.end_headers()
            self.server.wfile.write(content)
        else:
            print filename
            self.server.send_response(404)
            self.server.end_headers()


class IndexController(Controller):

    def __init__(self, server):
        Controller.__init__(self, server)

    def indexAction(self):
        nameSpace = {'title': 'Nebula', 'config': WebConfig}

        self.server.send_response(200)
        self.server.send_header('Content-type', 'text/html')
        self.server.end_headers()
        self.server.wfile.write(Template(file='app/views/index.tmpl', searchList=[nameSpace]))
        return
