import threading
import motion_watcher
from .. import Timing
import RPi.GPIO as GPIO

class motion_controller(threading.Thread):
    """
    Controls the motion of a motor
    """
    
    #The maximum rounds per minute allowed
    MAXIMUM_RPM = 20
    PWM_FREQ_IN_HERTZ = 2000
    PWM_MAX_DUTYCYCLE = 100

    def __init__(self,pinPWM, pinDIR, motion_watcher):
        """
        MotionWatcher motion_watcher - class providing speed and direction feedback\n
        int pinPWM - The GPIO pin outputing PWM to the control board to control the speed.\t
        int pinDIR - The GPIO pin outputting signal to the control board to control the direction.
        """
        self.motion_watcher = motion_watcher

        #GPIO
        #   PWM
        self.pinPWM = pinPWM
        self.pinDIR = pinDIR
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinPWM , GPIO.OUT)
        self.PWM = GPIO.PWM(pinPWM, self.PWM_FREQ_IN_HERTZ)
        #   DIR
        GPIO.setup(pinDIR , GPIO.OUT)

        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the motion controller.
        """
        self.PWM.start(0)
            
    def stop(self, stop_motion_watcher = True):
        """Stop the motion controller"""
        print("Stopping motion controller")
        if(stop_motion_watcher):
            self.motion_watcher.stop()
        self.stop_event.set()

    def stopped(self):
        """Check if the motion controller is stopping"""
        return self.stop_event.is_set()
    