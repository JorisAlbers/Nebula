from neopixel import *
import threading
import Queue
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
        self.strips = Adafruit_NeoPixel(self.total_length, self.pinPWM, self.freq, self.dma_channel, self.led_invert)
        self.fifo = Queue.Queue()

    def run(self):
        """
        Start the led controller.
        """
        self.strips.start()
        animation = None  # [light_animation, speed, until]
        try:
            while not self.stop_event.is_set():
                if (animation is not None):
                    # display animation until time
                    while not self.stop_event.is_set() and animation[2] > Timing.unix_timestamp:
                        time_start = Timing.micros()
                        # Do stuff
                        animation[0].draw_frame(self.strips)
                        strip.show()
                        time_end = Timing.micros()
                        # Delay for a bit to reduce stress
                        Timing.delayMicroseconds(2000 - (time_end - time_start))
                else:
                    if (not self.fifo.empty()):
                        animation = self.fifo.get()
                    else:
                        Timing.delay(500)
        except Exception, e:
            print("Error during run of motion_controller, " + str(e))
            raise e
        finally:
            # todo cleanup
            pass

    def add_animation(self, animation, speed, until):
        """
        Adds a new animation to the FIFO\n
        Animation animation - the animation to show
        float speed - the percentage speed a at which to animate.
        int until - the UNIX timestamp at which the motion will stop.
        """
        if not isinstance(animation, LightAnimation):
            raise ValueError("The animation must be an Light animation!")
        if not isinstance(speed, float):
            raise ValueError("The speed must be an float")
        if speed < 1:
            raise ValueError("The percentage speed must be larger than 0")
        if not isinstance(until, int):
            raise ValueError("The until must be an integer, representing an UNIX timestamp")
        if Timing.unix_timestamp >= until:
            raise ValueError("The until time has already passed")
        animation.init_ring(self.length_l1, self.length_l2, self.length_s1, self.length_s2)
        self.fifo.put([animation, speed, until])

    def stop(self):
        """Stop the led controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the led controller is stopping"""
        return self.stop_event.is_set()
