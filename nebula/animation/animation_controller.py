import threading

class AnimationController(threading.Thread):
    """
    Uses the LedController and the MotionController to animate animations.
    """
    def __init__(self,ledController, motionController):
        """
        LedController ledController - The object that handles light_animations on a ledStrip.
        MotionController motionController - the object that handles motion_animations on a motor.
        """ 
        self.ledController = ledController
        self.motionController = motionController

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()


    def stop(self):
        """Stop the animation controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the animation controller is stopping"""
        return self.stop_event.is_set()
