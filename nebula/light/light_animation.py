from led_drawing import LedDrawer
from ..animation.animation import LoopMode

class LightAnimation(object):
    def __init__(self,drawer,frame_duration, loop_mode, loop_value):
        """
        LedDrawer drawer - the led animation draw logic
        int frame_duration - the number of miliseconds to wait between each frame of the animation
        LoopMode loopMode - The way to loop the animation
        LoopValue loopValue - The number of loops, depending on the loopMode
        """
        if not isinstance(drawer, LedDrawer):
            raise ValueError("The drawer must be an LedDrawer!")
        if not isinstance(frame_duration, int):
            raise ValueError("The frame_duration must be an int")
        if frame_duration < 1:
            raise ValueError("The frame_duration must be larger than 0")
        if not isinstance(loop_mode, LoopMode):
            raise ValueError("LoopMode must be a LoopMode")
        if not isinstance(loop_value, int):
            raise ValueError("The loop_value must be an int")

        self.drawer = drawer
        self.frame_duration = frame_duration
        self.loop_mode = loop_mode
        self.loop_value = loop_value