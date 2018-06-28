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
        self.lightAnimationIndex = 0
        self.motionAnimationIndex = 0
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

    def hasNextLightAnimation(self):
        """
        Returns true if there is a next light animation
        """
        if self.loops:
            return True
        else:
            return self.lightAnimationIndex +1 < len(self.lightAnimations)

    def getNextLightAnimation(self):
        """
        Gets the next light animation. Might raise error if there is no next animation
        """
        animation = self.lightAnimations[self.lightAnimationIndex]
        if self.loops:
            self.lightAnimationIndex += 1 % len(self.lightAnimations)
        else:
            self.lightAnimationIndex += 1

        return animation

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

    def hasNextMotionAnimation(self):
        """
        Returns true if there is a next motion animation
        """
        if self.loops:
            return True
        else:
            return self.motionAnimationIndex +1 < len(self.motionAnimations)

    def getNextMotionAnimation(self):
        """
        Gets the next motion animation. Might raise error if there is no next animation
        """
        animation = self.motionAnimations[self.motionAnimationIndex]
        if self.loops:
            self.motionAnimationIndex += 1 % len(self.motionAnimations)
        else:
            self.motionAnimationIndex += 1
        
        return animation

    