from neopixel import *
import threading
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
        self.led_invert = False # True to invert the signal (when using NPN transistor level shift)
        self.length_l1 = length_l1
        self.length_l2 = length_l2
        self.length_s1 = length_s1
        self.length_s2 = length_s2
        self.total_length = length_l1 + length_l2 + length_s1 + length_s2
        self.strips = Adafruit_NeoPixel(self.total_length, self.pinPWM, self.freq, self.dma_channel, self.led_invert)

    def run(self):
        """
        Start the led controller.
        """
        
    def stop(self):
        """Stop the led controller"""
        self.stop_event.set()

    def stopped(self):
        """Check if the led controller is stopping"""
        return self.stop_event.is_set()
