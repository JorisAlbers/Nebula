import os
import json

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

    def readFile(self,file_path):
        try:
            file = open(file_path,'r')
        except:
            print("AnimationReader : Failed to read file at {0}".format(file_path))
        else:
            try:
                return file.readlines()
            except:
                print("AnimationReader: Failed to read lines, filepath = {0}".format(file_path))
            finally:
                try:
                    file.close()
                except:
                    print("AnimationReader: Failed to close file after reading, filepath = {0}".format(file_path))

    def loadAnimation(self,name):
        """
        Load the animation with the name as file prefix (before .extension)
        """
        if not isinstance(name,str):
            raise ValueError("The name must be of type string")
        
        full_path = os.path.join(self.dir_path,name + self.ANIMATION_EXTENSION)
        if not os.path.isfile(full_path):
            return IOError("The animation does not exist!")

        file_content = self.readFile(full_path)
        if file is not None:
            try:
                return json.loads(file_content)
            except:
                raise IOError("Failed to load animation {0}, format invalid ,filepath = {1}".format(name,full_path))
        else:
           raise IOError("Failed to load animation {0}, could not read file, filepath = {1}".format(name,full_path))
        

