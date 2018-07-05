from config import Config, readConfig
from repositories.animation_reader import AnimationReader
from animation.animation_controller import AnimationController
from light.led_controller import LedController
from light.led_strip import NeoPixelLedStrip
from networking.server import Server
from networking.client import Client
import Timing

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
        if(len(list_of_animations < 1)):
            print("No animations found!")
            return

        self.server.start()
        while True:
            #TODO add try/except
            option = self.getTerminalInput()
            if option == 1:
                print("Manual stop event set.")
            elif option == 2:
                animation_to_start = self.getTerminalAnimationInput(list_of_animations)
                if animation_to_start is not None:
                    self.animationReader.loadAnimation(animation_to_start,self.config.client_id)
                    start_at = Timing.unix_timestamp() + 2 # Add 2 secs sync buffer time
                    self.server.sendStartAnimimation(animation_to_start,start_at)

    def getTerminalInput(self):
        print("1 - Stop")
        print("2 - Start an animation")
        return int(raw_input())

    def getTerminalAnimationInput(self,animations):
        for x in range(0,len(animations)):
            print("{0} - {1}".format(x+1,animations[x]))
        i = int(raw_input())
        if i > 0 and i < len(animations)+1:
            return animations[i]
        else:
            return None
    

def main(config_path):
    config = readConfig(config_path)
    animationReader = AnimationReader(config.animation.resourcePath)
    motionController = None
    ledstrip = NeoPixelLedStrip(config.light.length, config.light.pinPWM, config.light.freq, config.light.dma_channel, config.light.invert)
    ledController = LedController(ledstrip, config.light.led_sections)
    animationController = AnimationController(ledController,motionController)

    print("Starting animationController")
    animationController.start()

    if config.isMaster:
        print("I'm the master. My client id is {0}".format(config.client_id))
        server = Server(config.networking.ip, config.networking.port)
        master = NebulaMaster(config,animationReader,animationController,server)
        master.start()
       
    else:
        print("I'm a slave with client id {0}".format(config.client_id))
        client = Client(config.networking.server_ip, config.networking.server_port,config.client_id)
        #TODO init callbacks
        
if __name__ == "__main__":
    import sys
    config_path = None

    for i in range(1,len(sys.argv)):
        command = sys.argv[i]
        if command == "-h":
            print("NEBULA")
            print("commands:")
            print("-c <config_file_path>")
            sys.exit(0)
        elif command == "-c":
            i += 1
            config_path = sys.argv[i]
        elif command == "-r":
            i += 1
            resource_dir_path = sys.argv[i]
        else:
            print("Unknown command ({0}). Use -h to print the help.".format(sys.argv[i]))
        
    if  config_path is not None:
        main(config_path)



