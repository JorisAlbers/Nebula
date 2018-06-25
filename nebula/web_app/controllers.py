from Cheetah.Template import Template
from config import *
import subprocess
import sys
import os

from animation.animation_reader import AnimationReader
# from nebula.config import animation_config


class Controller(object):
    def __init__(self, server):
        self.__server = server

    @property
    def server(self):
        return self.__server


class ContentController(Controller):
    CONTENT_BASE_PATH = '/public/'

    def __init__(self, server):
        Controller.__init__(self, server)

    def showAction(self):
        filename = self.server.path[1:]
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
        ar = self.server.animationReader
        animations = ar.get_animations()
        nameSpace = {'title': 'Nebula', 'config': web_config, 'animationList': animations}

        self.server.send_response(200)
        self.server.send_header('Content-type', 'text/html')
        self.server.end_headers()
        self.server.wfile.write(Template(file='web_app/views/index.tmpl', searchList=[nameSpace]))
        return


class UpdateController(Controller):

    def __init__(self, server):
        Controller.__init__(self, server)

    def indexAction(self):
        print subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()

        self.server.send_response(307)
        self.server.send_header('Location', self.server.headers.get('Host') + self.server.path)
        self.server.end_headers()

        # os.execv(sys.executable, ['python'] + sys.argv)
        proc = subprocess.Popen('python update.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        sys.exit()
