import os
import json
from ..animation.animation import Animation
from ..animation.animation_loop_mode import LoopMode
from ..light.light_animation import LightAnimation
from ..light.led_drawing import *

class AnimationReader(object):
    ANIMATION_EXTENSION = ".nebula.json"
    def __init__(self,dir_path):
        """
        string dir_path - The location the animations are stored.
        """
        if not isinstance(dir_path,str):
            raise ValueError("The dir path must be a string!")
        if not os.path.isdir(dir_path):
            raise IOError("The dir path does not point to an existing folder!")
        self.dir_path = dir_path

    def listAnimations(self):
        """
        Get a list of the names of all the animations present in the repository
        """
        animations = []
        for file in os.listdir(self.dir_path):
            if file.endswith(self.ANIMATION_EXTENSION):
                animations.append(file.replace(self.ANIMATION_EXTENSION))
        return animations

    def readFile(self,file_name):
        """
        Read the file from the dir_path with the file_name specified in the param.
        """
        path = os.path.join(self.dir_path,file_name)
        if not os.path.isfile(path):
            raise IOError("The animation at {0} does not exist!".format(path))
        try:
            file = open(path,'r')
        except:
            print("AnimationReader : Failed to read file at {0}".format(path))
        else:
            try:
                return file.read()
            except:
                print("AnimationReader: Failed to read lines, filepath = {0}".format(path))
            finally:
                try:
                    file.close()
                except:
                    print("AnimationReader: Failed to close file after reading, filepath = {0}".format(path))

    def loadAnimation(self,name,client_id):
        """
        Load the animation with the name as file prefix (before .extension)
        Only retrieves the animation of the client_id
        """
        if not isinstance(name,str):
            raise ValueError("The name must be of type string")
        
        file_name = name + self.ANIMATION_EXTENSION
        file_content = self.readFile(file_name)
        if file is not None:
            try:
                j =  json.loads(file_content)
                j_animation = j["animations_per_ring"][client_id]
                loops = j_animation["loops"]
                animation = Animation(loops)
                for light_animation in j_animation["light_animations"]:
                    self.addLightAnimationToAnimation(light_animation,animation)
                return animation
            except Exception, e:
                raise IOError("Failed to load animation {0}, format invalid".format(name))
        else:
           raise IOError("Failed to load animation {0}, could not read file".format(name))
        

    def addLightAnimationToAnimation(self,j_lightAnimation,animation):
        """
        Add a light animation or WAIT to the list of ligtanimations of the ANIMATION in the params
        """
        if "wait" in j_lightAnimation:
            #Must be a wait
            animation.addLightWait(j_lightAnimation["wait"])
            return
        else:
            # Standard stuff
            loop_mode = self.getLoopMode(j_lightAnimation["loop_mode"])
            loop_value = j_lightAnimation["loop_value"]
            frame_duration = j_lightAnimation["frame_duration"]

            # Drawer stuff
            drawer_string = j_lightAnimation["drawer"].lower()
            if drawer_string == "slidingpatterns":
                patterns = []
                for p in j_lightAnimation["patterns"]:
                    patterns.append(self.stringArray_to_ColorArray(p))
                drawer = SlidingPatterns(patterns)
            elif drawer_string == "repeatingpatterns":
                patterns = []
                for p in j_lightAnimation["patterns"]:
                    patterns.append(self.stringArray_to_ColorArray(p))
                drawer = RepeatingPatterns(patterns)
            
            la = LightAnimation(drawer,frame_duration,loop_mode,loop_value)
            animation.addLightAnimation(la)
            
    def getLoopMode(self,loopMode_str):
        loopMode_str = loopMode_str.lower()
        if loopMode_str == "duration":
            return LoopMode.DURATION
        elif loopMode_str == "iterations":
            return LoopMode.ITERATIONS
        elif loopMode_str == "no_loop":
            return LoopMode.NO_LOOP
        raise ValueError("can't parse loopmode, unknown loopMode ({0})".format(loopMode_str))
        

    def stringToColor(self,string):
        """
        Convert a rgb string to a color int.
        The rgb values can be separated by . or , 
        """
        split = string.split('.')
        if len(split) == 1:
            split = string.split(",")
        
        red = int(split[0])
        green = int(split[1])
        blue = int(split[2])
        return Color(red,green,blue)

    def stringArray_to_ColorArray(self,array):
        pattern =  []
        for s in array:
            pattern.append(self.stringToColor(s))
        return pattern