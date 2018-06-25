import threading
from .. import Timing
from led_drawing import *
from light_animation import *


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
        self.next_animation = None
        self.current_animation = None
        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the led controller.
        """
        self.strip.begin()
        standard_wait_for_ms = 200
        try:
            while not self.stop_event.is_set():
                time_start = Timing.millis()
                if (self.current_animation is not None):
                    next(self.current_animation.drawer)
                    self.strip.show()
                    
                if (self.next_animation is not None):
                    #There is a new animation to display.
                    if(self.current_animation is not None):
                        # There already was an aniamtion playing
                        next_cyle_start = Timing.unix_timestamp() + float(self.current_animation.frame_duration) / 1000.0
                        time_left = next_cyle_start - self.next_animation.start_at
                        if(time_left < self.current_animation.frame_duration):
                            self.current_animation = self.next_animation
                            self.next_animation = None
                            Timing.delay(time_left * 1000)
                            continue
                    else:
                        # There was no animation playing.
                        wait_ms = (self.next_animation.start_at - Timing.unix_timestamp()) / 1000.0
                        self.current_animation = self.next_animation
                        self.next_animation = None
                        Timing.delay(wait_ms)
                        continue
                    
                if(self.current_animation is not None):
                    Timing.delay(self.current_animation.frame_duration - (Timing.millis() - time_start))
                else:
                    Timing.delay(standard_wait_for_ms)

        except Exception, e:
            print("Error during run of LedController, " + str(e))
            raise e
        finally:
            # todo cleanup
            pass

    def set_next_animation(self, lightAnimation):
        """
        Sets the next animation\n
        Animation lightAnimation - the lightAnimation to show
        """
        if not isinstance(lightAnimation, LightAnimation):
            raise ValueError("The lightAnimation must be an Light animation!")

        lightAnimation.drawer.init_ring(self.strip,self.led_sections)
        self.next_animation = lightAnimation

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
