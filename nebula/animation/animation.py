from ..light.light_animation import LightAnimation
from ..motion.motion_animation import MotionAnimation

class Animation(object):
    def __init__(self, light_or_motion_animation, duration):
        """
        The animation is a container class for a led or motion animation.
        The duration of the led or motion animation is also set in the animation
        """

        if not isinstance(light_or_motion_animation, LightAnimation) and not isinstance(light_or_motion_animation, MotionAnimation):
            raise ValueError("The animation must be an LightAnimation or MotionAnimation!")
        if not isinstance(int,duration):
            raise ValueError("The duration must be an int!")

        self.animation = light_or_motion_animation
        self.duration = duration

class Animations(list):
    def __getitem__(self,key):
        if not isinstance(key,int):
            raise IndexError("Only integer indexing allowed")
        return super(Animations,self).__getitem__(key)

    def append(self,item):
        if not isinstance(item,Animation):
            raise ValueError("Can only add Animations!")
        super(Animations,self).append(item)
    
    def addAnimation(self,light_or_motion_animation, duration):
        animation = Animation(light_or_motion_animation,duration)
        super(Animations,self).append(animation)
