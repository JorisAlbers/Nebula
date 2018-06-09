import threading
import motion_watcher
from .. import Timing
import RPi.GPIO as GPIO
from ..config import *
import Queue


class motion_controller(threading.Thread):
    """
    Controls the motion of a motor
    """

    def __init__(self, pinPWM=motion_config.pwm_pin, pinDIR=motion_config.dir_pin, motion_watcher=None):
        """
        MotionWatcher motion_watcher - class providing speed and direction feedback\n
        int pinPWM - The GPIO pin outputing PWM to the control board to control the speed.\t
        int pinDIR - The GPIO pin outputting signal to the control board to control the direction.
        :type pinDIR: int
        :type pinPWM: int
        """
        self.motion_watcher = motion_watcher

        self.fifo = Queue.Queue()
        # GPIO
        #   PWM
        self.pinPWM = pinPWM
        self.pinDIR = pinDIR
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinPWM, GPIO.OUT)
        self.PWM = GPIO.PWM(self.pinPWM, motion_config.pwm_freq_in_hertz)
        #   DIR
        GPIO.setup(self.pinDIR, GPIO.OUT)

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the motion controller.
        """
        self.PWM.start(0)
        # motion is a 1d array, [int speed, bool forwards, int until]
        movement = None
        try:
            while not self.stop_event.is_set():
                if (movement is not None):
                    # display motion until time
                    while not self.stop_event.is_set() and movement[2] > Timing.unix_timestamp:
                        time_start = Timing.micros()
                        # do stuff
                        time_end = Timing.micros()
                        # Delay for a bit to reduce stress
                        Timing.delayMicroseconds(2000 - (time_end - time_start))
                else:
                    if (not self.fifo.empty()):
                        movement = self.fifo.get()
                    else:
                        Timing.delay(500)
        except Exception, e:
            print("Error during run of motion_controller, " + str(e))
            raise e
        finally:
            self.set_speed(0)
            self.PWM.stop()
            GPIO.cleanup()  # TODO check if this does not interfere with other GPIO using classes. If so, add wrapper

    def set_speed(self, rpm):
        pass

    def add_motion(self, speed, forwards, until):
        """
        Adds a new motion to the FIFO\n
        float speed - the RPM at which to rotate.
        bool forwards - true to rotate forwards, false to rotate backwards.
        int until - the UNIX timestamp at which the motion will stop.
        :type until: int
        :type forwards: bool
        :type speed: int
        """
        if not isinstance(speed, int):
            raise ValueError("The speed must be an integer")
        if (speed < 0 or speed > motion_config.maximum_rpm):
            raise ValueError("The speed must be between 0 and {0}".format(str(motion_config.maximum_rpm)))
        if not isinstance(forwards, bool):
            raise ValueError("The forwards parameter must be a bool")
        if not isinstance(until, float):
            raise ValueError("The until must be an integer, representing an UNIX timestamp")
        if (Timing.unix_timestamp >= until):
            raise ValueError("The until time has already passed")
        self.fifo.put([speed, forwards, until])

    def stop(self, stop_motion_watcher=True):
        """Stop the motion controller"""
        print("Stopping motion controller")
        if stop_motion_watcher:
            self.motion_watcher.stop()
        self.stop_event.set()

    def stopped(self):
        """Check if the motion controller is stopping"""
        return self.stop_event.is_set()
