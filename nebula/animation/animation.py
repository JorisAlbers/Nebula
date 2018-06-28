from ..light.light_animation import LightAnimation
from ..motion.motion_animation import MotionAnimation

class Animation(object):
    """
    A Animation has a list of LightAnimation and a list of MotionAnimations.
    Each of these lists can also contain a WAIT block.

    A WAIT block is an integer, showing miliseconds

    ~ = WAIT
    Time                0|------------------------------|100
    Light  animations:  -[1111111][~][2222][~~~~][3][~~]-
    Motion animations:  -[1111111111][2222][~~~~][3][44]-
    """
    def __init__(self, loops):
        if not isinstance(loops,bool):
            raise ValueError("loops must be of type bool")
        self.lightAnimations  = []
        self.motionAnimations = []
        self.index = 0
        self.loops = False

    def addLightAnimation(self, lightAnimation):
        """
        Add a new lightAnimation to the lightAnimations list
        lightAnimation = the lightAnimation to add.
        """
        if not isinstance(lightAnimation,LightAnimation):
            raise ValueError("The lightAnimation must be of type LightAnimation")
        self.lightAnimations.append(lightAnimation)

    def addLightWait(self, waitForSeconds):
        """
        Add a WAIT to the lightAnimations
        """
        if not isinstance(waitForSeconds,int):
            raise ValueError("The waitForSeconds must be of type int!")
        self.lightAnimations.append(waitForSeconds)

    def addMotionAnimation(self,motionAnimation):
        """
        Add a new motionAnimation to the motionAnimations list
        """
        if not isinstance(motionAnimation,MotionAnimation):
            raise ValueError("The motionAnimation must be of type MotionAnimation")
        self.motionAnimations.append(motionAnimation)

    def addMotionWait(self, waitForSeconds):
        """
        Add a WAIT to the motionAnimations
        """
        if not isinstance(waitForSeconds,int):
            raise ValueError("The waitForSeconds must be of type int!")
        self.motionAnimations.append(waitForSeconds)
