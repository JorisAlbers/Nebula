import threading
import motion_watcher
from .. import Timing
import RPi.GPIO as GPIO


class motion_controller(threading.Thread):
    """
    Controls the motion of a motor
    """

    # The maximum rounds per minute allowed
    MAXIMUM_RPM = 20
    PWM_FREQ_IN_HERTZ = 2000
    PWM_MAX_DUTYCYCLE = 100

    def __init__(self, pinPWM, pinDIR, motion_watcher):
        """
        MotionWatcher motion_watcher - class providing speed and direction feedback\n
        int pinPWM - The GPIO pin outputing PWM to the control board to control the speed.\t
        int pinDIR - The GPIO pin outputting signal to the control board to control the direction.
        """
        self.motion_watcher = motion_watcher

        self.fifo = Queue()
        # GPIO
        #   PWM
        self.pinPWM = pinPWM
        self.pinDIR = pinDIR
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinPWM, GPIO.OUT)
        self.PWM = GPIO.PWM(pinPWM, self.PWM_FREQ_IN_HERTZ)
        #   DIR
        GPIO.setup(pinDIR, GPIO.OUT)

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the motion controller.
        """
        self.PWM.start(0)

    def add_motion(speed, forwards, until):
        """
        Adds a new motion to the FIFO\n
        int speed - the RPM at which to rotate.
        bool forwards - true to rotate forwards, false to rotate backwards.
        int until - the UNIX timestamp at which the motion will stop.
        """
        if (not isinstance(speed, int)):
            raise ValueError("The speed must be an integer")
        if (speed < 0 or speed > self.MAXIMUM_RPM):
            raise ValueError("The speed must be between 0 and {0}".format(str(self.MAXIMUM_RPM)))
        if (not isinstance(forwards, bool)):
            raise ValueError("The forwards parameter must be a bool")
        if (not isinstance(until, int)):
            raise ValueError("The until must be an integer, representing an UNIX timestamp")
        # TODO check if until is a valid timestamp
        # TODO check if the until timestamp has not already passed
        self.fifo.put([speed, forwards, until])

    def stop(self, stop_motion_watcher=True):
        """Stop the motion controller"""
        print("Stopping motion controller")
        if (stop_motion_watcher):
            self.motion_watcher.stop()
        self.stop_event.set()

    def stopped(self):
        """Check if the motion controller is stopping"""
        return self.stop_event.is_set()
