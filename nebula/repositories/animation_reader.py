import os

class AnimationReader(object):
    def __init__(self,dir_path):
        """
        string dir_path - The location the animations are stored.
        """
        if not isinstance(dir_path,str):
            raise ValueError("The dir path must be a string!")
        if not os.path.isdir(dir_path):
            raise IOError("The dir path does not point to an existing folder!")
        self.dir_path = dir_path

    