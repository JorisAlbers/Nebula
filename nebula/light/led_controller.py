import threading
from .. import Timing
from led_drawing import *
from light_animation import *
from ..animation.animation_loop_mode import LoopMode


class LedController(threading.Thread):
    """
    Controls ws2812b led strips
    """

    def __init__(self, ledstrip, led_sections):
        """
        LedStrip ledstrip - the ledstrip to draw on
        array led_sections = [section1 = [int start, int stop], section2, ..] 
        """
        
        #Calulate length of each section and the total length of the led strip
        self.total_length = 0
        self.led_sections = [] # [[int start, int stop, int length],[], ...]
        for x in range(0,len(led_sections)):
            length = abs(led_sections[x][0] - led_sections[x][1]) + 1 # +1 as the led_sections are index ranges which are 0 based
            self.led_sections.append([led_sections[x][0],led_sections[x][1],length])
            self.total_length += length

        self.strip = ledstrip
        self.current_animation = None
        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def setLightAnimationFinished_callback(self,callback):
        """
        Sets the callback to call if a lightAnimation has finished
        """
        self.callback = callback

    def run(self):
        """
        Start the led controller.
        """
        self.strip.begin()
        standard_wait_for_ms = 200
        standard_wait_for_seconds = float(standard_wait_for_ms) / 1000.0
        try:
            while not self.stop_event.is_set():
                time_start = Timing.millis()
                if self.current_animation is not None:
                    if isinstance(self.current_animation,LightAnimation):
                        #Draw the lightAnimation
                        #TODO add lock 
                        next(self.current_animation.drawer)
                        self.strip.show()
                        # Tell the lightAnimation that a iteration passed. 
                        if self.current_animation.loop_mode == LoopMode.ITERATIONS:
                            self.current_animation.loop_value -= 1
                        if self.current_animation.loop_mode == LoopMode.DURATION or self.current_animation.loop_mode == LoopMode.NO_LOOP:
                            self.current_animation.loop_value -= self.current_animation.frame_duration

                        wait_for = self.current_animation.frame_duration
                        
                        if self.current_animation.loop_value < 1:
                            self.current_animation = None
                            #Notify the AnimationController that an lightAnimation has fininshed
                            #TODO release lock
                            if self.callback is not None:
                                self.callback()
                        #TODO release lock
                        Timing.delay(wait_for - (Timing.millis() - time_start))
                        continue

                    else:
                        #Must be WAIT, check if time reached this block
                        next_cycle_start = Timing.unix_timestamp() + standard_wait_for_seconds
                        time_left = self.current_animation - next_cycle_start
                        if time_left < standard_wait_for_ms:
                            Timing.delay(time_left)
                            if self.callback is not None:
                                self.callback()
                            
                Timing.delay(standard_wait_for_ms)

        except Exception, e:
            print("Error during run of LedController, " + str(e))
            raise e
        finally:
            # todo cleanup
            pass

    def setAnimation(self, lightAnimation):
        """
        Sets the animation\n
        Animation lightAnimation - the lightAnimation to show
        """
        if not isinstance(lightAnimation, LightAnimation):
            raise ValueError("The lightAnimation must be an Light animation!")

        lightAnimation.drawer.init_ring(self.strip,self.led_sections)
        self.current_animation = lightAnimation

    def setWait(self,until):
        """
        Sets a WAIT until unix timestamp.
        """
        if not isinstance(until,float):
            raise ValueError("The until must be a float, representing an Unix timestamp")
        self.current_animation = until


    def set_frame_duration(self, frame_duration):
        """
        Set the frame duration of the current animation
        """
        if not isinstance(frame_duration, int):
            raise ValueError("The frame_duration must be an int")
        if frame_duration < 1:
            raise ValueError("The frame_duration must be larger than 0")
        if self.current_animation is None:
            raise Exception("There is no animation active at the moment!")
        
        self.current_animation.frame_duration = frame_duration

    def stop(self):
        """Stop the led controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the led controller is stopping"""
        return self.stop_event.is_set()
