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


    
