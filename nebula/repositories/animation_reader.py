import os


class AnimationReader(object):
    ANIMATION_EXTENSION = ".nebula_animation"
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