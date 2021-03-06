import threading
from .. import Timing
from animation import Animation
from ..light.light_animation import LightAnimation

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
                    animation = self.current_animation.getNextLightAnimation()
                    if isinstance(animation,LightAnimation):
                        self.ledController.setAnimation(animation)
                    else: #Must be WAIT
                        self.ledController.setWait(Timing.unix_timestamp() + (float(animation[0]) / 1000.0),animation[1])
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
                animation = self.current_animation.getNextLightAnimation()
                if isinstance(animation,LightAnimation):
                    self.ledController.setAnimation(animation)
                else:
                    #Animation must be a WAIT. wait is a list, [wait_for_ms,clearStrip]
                    self.ledController.setWait(Timing.unix_timestamp() + (float(animation[0]) / 1000.0),animation[1])
            

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
        self.next_animation = animation
        self.next_animation_start_at = start_at

    def clear(self):
        """
        Removes the current animation.
        Call the clear functions of led and motion controllers.
        """
        # Animation to clear the controllers
        clear_animation = Animation(False)
        clear_animation.addLightWait(1,True)
        # TODO add motion wait motionAnimation
        self.setNextAnimations(clear_animation,Timing.unix_timestamp())
        
    def stop(self):
        """Stop the animation controller"""
        self.stop_event.set()
        if self.ledController is not None:
            self.ledController.stop()
        if self.motionController is not None:
            self.motionController.stop()

    def stopped(self):
        """Check if the animation controller is stopping"""
        return self.stop_event.is_set()
