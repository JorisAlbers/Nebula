from led_drawing import LedDrawer

class LightAnimation(object):
    def __init__(self,drawer,frame_duration,start_at):
        """
        LedDrawer drawer - the led animation draw logic
        int frame_duration - the number of miliseconds to wait between each frame of the animation
        float start_at - the UNIX timestamp at which the motion will start.
        """
        if not isinstance(drawer, LedDrawer):
            raise ValueError("The drawer must be an LedDrawer!")
        if not isinstance(frame_duration, int):
            raise ValueError("The frame_duration must be an int")
        if frame_duration < 1:
            raise ValueError("The frame_duration must be larger than 0")
        if not isinstance(start_at, float):
            raise ValueError("The start_at must be an integer, representing an UNIX timestamp")
        
        self.drawer = drawer
        self.frame_duration = frame_duration
        self.start_at = start_at