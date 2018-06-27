import threading
from .. import Timing
from animation import Animations

class AnimationController(threading.Thread):
    """
    Uses the LedController and the MotionController to animate animations.
    """
    def __init__(self,ledController, motionController):
        """
        LedController ledController - The object that handles light_animations on a ledStrip.
        MotionController motionController - the object that handles motion_animations on a motor.
        """ 
        if ledController is None and motionController is None:
            raise ValueError("At least one of the controller must be set!")

        if ledController is not None:
            ledController.setLightAnimationFinished_callback(self.lightAnimationFinished_callback)
        self.ledController = ledController
        self.motionController = motionController

        self.current_animations = None
        self.next_animations = None
        self.next_animations_start_at = 0.0

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        if self.ledController is not None:
            self.ledController.run()
        if self.motionController is not None:
            self.motionController.run()
        
        if(self.ledController is not None):
            self.ledController.join()
        if(self.motionController is not None):
            self.motionController.join()

        # Both controllers have stopped working. 
        # TODO restart controllers?
        self.stop()
    
    def lightAnimationFinished_callback(self):
        """
        Called by the ledController to notify this AnimationController that a LightAnimation has finished
        """
        # TODO add logic
        pass

    def setNextAnimations(self, animations, start_at):
        if not isinstance(animations,Animations):
            raise ValueError("The animations must be of type Animations! (The list object)")
        if not isinstance(start_at, float):
            raise ValueError("The start_at must be an integer, representing an UNIX timestamp")
        if Timing.unix_timestamp() > start_at:
            raise ValueError("The start_at has already passed!")
        self.next_animations = animations
        self.next_animations_start_at = start_at
        
    def stop(self):
        """Stop the animation controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the animation controller is stopping"""
        return self.stop_event.is_set()
