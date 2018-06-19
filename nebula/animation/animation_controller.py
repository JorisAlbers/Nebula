import threading
from .. import Timing

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

        self.ledController = ledController
        self.motionController = motionController

        self.current_animation = None
        self.next_animation = None

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        if self.ledController is not None:
            self.ledController.run()
        if self.motionController is not None:
            self.motionController.run()
        standard_wait_for_ms = 200
        try:
            while not self.stop_event.is_set():
                time_start = Timing.millis()
                if(self.current_animation is not None):
                    # Animate current animation
                    pass
                
                if(self.next_animation is not None):
                    # There already was an aniamtion playing
                    next_cyle_start = Timing.unix_timestamp() + float(self.current_animation[1]) / 1000.0
                    time_left = next_cyle_start - self.next_animation[2]
                    if(time_left < self.current_animation[1]):
                        self.current_animation = self.next_animation
                        self.next_animation = None
                        Timing.delay(time_left * 1000)
                        continue
                    else:
                        # There was no animation playing.
                        wait_ms = (self.next_animation[1] - Timing.unix_timestamp()) / 1000.0
                        self.current_animation = self.next_animation
                        self.next_animation = None
                        Timing.delay(wait_ms)
                        continue

                if(self.current_animation is not None):
                    Timing.delay(self.current_animation[1] - (Timing.millis() - time_start))
                else:
                    Timing.delay(standard_wait_for_ms)

        except Exception, e:
            print("Error during run of animationController, " + str(e))
            raise e
        finally:
            # todo cleanup
            pass

    def stop(self):
        """Stop the animation controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the animation controller is stopping"""
        return self.stop_event.is_set()
