import threading
from .. import Timing
from animation import Animation

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

        self.current_animation = None
        self.next_animation = None
        self.next_animation_start_at = 0.0

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        if self.ledController is not None:
            self.ledController.start()
        if self.motionController is not None:
            self.motionController.start()
        
        # Loop to check if a next animation has been set
        while not self.stop_event.is_set():
            if self.next_animation is not None:
                self.current_animation = self.next_animation
                self.next_animation = None
                while self.next_animation_start_at > Timing.unix_timestamp() and self.next_animation is not None:
                    # Wait until start has passed
                    Timing.delayMicroseconds(1000)
                # it has passed, notify controllers
                if self.ledController is not None and self.current_animation.hasNextLightAnimation():
                    self.ledController.setAnimation(self.current_animation.getNextLightAnimation())
                if self.motionController is not None and self.current_animation.hasNextMotionAnimation():
                    self.motionController.setAnimation(self.current_animation.getNextMotionAnimation())

            else:
                Timing.delay(200) # TODO check if 200 is not too much

    
    def lightAnimationFinished_callback(self):
        """
        Called by the ledController to notify this AnimationController that a LightAnimation has finished
        """
        # TODO create new thread?
        if self.current_animation is not None:
            if self.current_animation.hasNextLightAnimation():
                self.ledController.setAnimation(self.current_animation.getNextLightAnimation())
            else:
                if not self.current_animation.hasNextMotionAnimation():
                    self.current_animation = None
                # TODO clear?

    def motionAnimationFinished_callback(self):
        """
        Called by the motionController to notify this AnimationController that a motionAnimation has finished
        """
        #TODO add logic
        pass

    def setNextAnimations(self, animation, start_at):
        if not isinstance(animation,Animation):
            raise ValueError("The animations must be of type Animations! (The list object)")
        if not isinstance(start_at, float):
            raise ValueError("The start_at must be an integer, representing an UNIX timestamp")
        if Timing.unix_timestamp() > start_at:
            raise ValueError("The start_at has already passed!")
        self.next_animation = animation
        self.next_animation_start_at = start_at
        
    def stop(self):
        """Stop the animation controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the animation controller is stopping"""
        return self.stop_event.is_set()
