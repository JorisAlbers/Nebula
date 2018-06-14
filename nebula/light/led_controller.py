from neopixel import *
import threading
from .. import Timing
from light_animation import *


class led_controller(threading.Thread):
    """
    Controls ws2812b led strips
    """

    def __init__(self, pinPWM, freq, dma_channel, length_l1, length_l2, length_s1, length_s2):
        """
        int pinPWM - the PWM pin number (Must support PWM!)\t
        int freq   - LED signal frequency in hertz (usually 800khz)\t
        int dma_channel - the dma channel used to create the pwm signal\t
        int length_l1 - the number of pixel on ledstrip long 1
        int length_l2 - the number of pixel on ledstrip long 2
        int length_s1 - the number of pixel on ledstrip short 1
        int length_s2 - the number of pixel on ledstrip short 2
        """
        self.pinPWM = pinPWM
        self.freq = freq
        self.dma_channel = dma_channel
        self.led_invert = False  # True to invert the signal (when using NPN transistor level shift)
        self.length_l1 = length_l1
        self.length_l2 = length_l2
        self.length_s1 = length_s1
        self.length_s2 = length_s2
        self.total_length = length_l1 + length_l2 + length_s1 + length_s2
        self.strip = Adafruit_NeoPixel(self.total_length, self.pinPWM, self.freq, self.dma_channel, self.led_invert)
        self.next_animation = None # [light_animation, speed, start_at]
        self.current_animation = None
        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the led controller.

        An animation is an array that looks like:
        [light_animation, frame_duration, start_at]
        """
        self.strip.begin()
        standard_wait_for_ms = 200
        try:
            while not self.stop_event.is_set():
                time_start = Timing.millis()
                if (self.current_animation is not None):
                    next(self.current_animation[0])
                    self.strip.show()
                    
                if (self.next_animation is not None):
                    #There is a new animation to display.
                    if(self.current_animation is not None):
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
            print("Error during run of motion_controller, " + str(e))
            raise e
        finally:
            # todo cleanup
            pass

    def set_next_animation(self, animation, frame_duration, start_at):
        """
        Sets the next animation\n
        Animation animation - the animation to show
        int frame_duration - the number of miliseconds to wait between each frame of the animation
        float start_at - the UNIX timestamp at which the motion will start.
        """
        if not isinstance(animation, LightAnimation):
            raise ValueError("The animation must be an Light animation!")
        if not isinstance(frame_duration, int):
            raise ValueError("The frame_duration must be an int")
        if frame_duration < 1:
            raise ValueError("The frame_duration must be larger than 0")
        if not isinstance(start_at, float):
            raise ValueError("The start_at must be an integer, representing an UNIX timestamp")
        animation.init_ring(self.length_l1, self.length_l2, self.length_s1, self.length_s2)
        self.next_animation = [animation.draw_frame(self.strip), frame_duration, start_at]

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
        
        self.current_animation[1] = frame_duration

    def stop(self):
        """Stop the led controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the led controller is stopping"""
        return self.stop_event.is_set()
