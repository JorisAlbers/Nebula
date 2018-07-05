from nebula.config import Config, readConfig
from nebula.repositories.animation_reader import AnimationReader
from nebula.animation.animation_controller import AnimationController
from nebula.light.led_controller import LedController
from nebula.light.led_strip import NeoPixelLedStrip
from nebula.networking.server import Server
from nebula.networking.client import Client
import nebula.Timing
import os

class NebulaMaster(object):
    def __init__(self,config,animationReader,animationController,server):
        if not isinstance(config,Config):
            raise ValueError("The config must be of type Config")
        if not isinstance(animationReader, AnimationReader):
            raise ValueError("The animationReader must be of type AnimationReader!")
        if not isinstance(animationController,AnimationController):
            raise ValueError("The animationContoller must be of type AnimationController!")
        if not isinstance(server,Server):
            raise ValueError("The server must be of type server!")

        self.config = config
        self.animationReader = animationReader
        self.animationContoller = animationController
        self.server = server

    def start(self):
        # TODO init callbacks
        list_of_animations = self.animationReader.listAnimations()
        if(len(list_of_animations) < 1):
            print("No animations found!")
            return

        self.server.start()
        while True:
            try:
                option = self.getTerminalInput()
                if option == 1:
                    print("Manual stop event set.")
                    break
                elif option == 2:
                    animation_to_start = self.getTerminalAnimationInput(list_of_animations)
                    if animation_to_start is not None:
                        self.animationReader.loadAnimation(animation_to_start,self.config.client_id)
                        start_at = Timing.unix_timestamp() + 2 # Add 2 secs sync buffer time
                        self.server.sendStartAnimimation(animation_to_start,start_at)
            except KeyboardInterrupt:
                print("Manual stop event set.")
            except Exception,e:
                print("ERROR : {0}".format(type(e)))
                print("MESSAGE: {0}".format(e.message))
        self.server.stop()
        self.animationContoller.stop()
        print("END of nebula master")

    def getTerminalInput(self):
        self.clearTerminal()
        print("1 - Stop")
        print("2 - Start an animation")
        return int(raw_input())

    def getTerminalAnimationInput(self,animations):
        self.clearTerminal()
        for x in range(0,len(animations)):
            print("{0} - {1}".format(x+1,animations[x]))
        i = int(raw_input())
        if i > 0 and i < len(animations)+1:
            return animations[i-1]
        else:
            return None

    def clearTerminal(self):
        os.system("clear")

    

def main(config_path):
    config = readConfig(config_path)
    animationReader = AnimationReader(config.animation.resourcePath)
    motionController = None
    ledstrip = NeoPixelLedStrip(config.light.strip_length, config.light.pwm_pin, config.light.pwm_freq, config.light.dma_channel, config.light.inverse)
    ledController = LedController(ledstrip, config.light.strip_sections)
    animationController = AnimationController(ledController,motionController)

    print("Starting animationController")
    animationController.start()

    if config.isMaster:
        print("I'm the master. My client id is {0}".format(config.client_id))
        server = Server(config.networking.server_ip, config.networking.server_port)
        master = NebulaMaster(config,animationReader,animationController,server)
        master.start()
       
    else:
        print("I'm a slave with client id {0}".format(config.client_id))
        client = Client(config.networking.server_ip, config.networking.server_port,config.client_id)
        #TODO init callbacks


def print_help():
    print("NEBULA")
    print("commands:")
    print("-c <config_file_path>")
     
if __name__ == "__main__":
    import sys
    config_path = None

    for i in range(1,len(sys.argv)):
        command = sys.argv[i]
        if command == "-h":
            print_help()
            sys.exit(0)
        elif command == "-c":
            i += 1
            config_path = os.path.abspath(sys.argv[i])
        elif command == "-r":
            i += 1
            resource_dir_path = sys.argv[i]
        else:
            print("Unknown command ({0}). Use -h to print the help.".format(sys.argv[i]))
        
    if  config_path is not None:
        main(config_path)
    else:
        print("Please set the config file path. Type -h to print the help.")



