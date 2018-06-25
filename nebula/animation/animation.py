from ..light.light_animation import LightAnimation
from ..motion.motion_animation import MotionAnimation

class Animation(object):
    def __init__(self, lightAnimation, motionAnimation):
        if not isinstance(lightAnimation, LightAnimation):
            raise ValueError("The light animation must be an animation!")
        if not isinstance(motionAnimation, MotionAnimation):
            raise ValueError("The motion animation must be an animation!")
        self.lightAnimation = lightAnimation
        self.motionAnimation = motionAnimation

