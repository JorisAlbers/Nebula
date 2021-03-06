import RPi.GPIO as GPIO
from .. import Timing
import threading
from ..config import *


class MotionWatcher(threading.Thread):
    """
    Watches the movement speed and direction of a motor.
    """

    def __init__(self, pinA=motion_config.hall_sensor_a, pinB=motion_config.hall_sensor_b,
                 pinC=motion_config.hall_sensor_c):
        """
        int pinA - the GPIO BCM pin number of pin A.
        int pinB - the GPIO BCM pin number of pin B.
        int pinC - the GPIO BCM pin number of pin C.
        """
        self.pinA = pinA
        self.pinB = pinB
        self.pinC = pinC

        self.signals = 0
        self.direction = 0  # 0 = forward, 1 = backwards
        self.rpm = 0.0
        # GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pinC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pinA, GPIO.BOTH, callback=self.sensor_callback, bouncetime=10)
        GPIO.add_event_detect(pinB, GPIO.BOTH, callback=self.sensor_callback, bouncetime=10)
        GPIO.add_event_detect(pinC, GPIO.BOTH, callback=self.sensor_callback, bouncetime=10)

        # Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def sensor_callback(self, channel):
        """Called when a channel's output changes"""
        signal = GPIO.input(channel)
        # Direction is measured utilising both pins

        # RPM is measured utilizing one pin, pinA
        if channel == self.pinA:
            if signal:
                self.signals += 1

    def run(self, wait_ms=200):
        """
        Start the motion watcher.
        int wait_ms - The period in miliseconds to count pulses."""
        minute_in_miliseconds = 60000
        periods_in_minute = minute_in_miliseconds / wait_ms
        try:
            while not self.stop_event.is_set():
                # TODO LOCK
                self.signals = 0
                Timing.delay(wait_ms)
                signals_passed_in_period = float(self.signals)
                rotations_in_period = signals_passed_in_period / motion_config.pulses_per_rotation
                self.rpm = rotations_in_period * periods_in_minute
        except KeyboardInterrupt:
            print("Quitting motion_watcher due to keyboard interrupt")
        except Exception, e:
            print("Error during run of MotionWatcher")
            raise e
        finally:
            GPIO.cleanup()  # TODO check if this does not interfere with other GPIO using classes. If so, add wrapper

    def get_motor_rpm(self):
        """Get the rpm of the motor."""
        return self.rpm

    def get_axial_rpm(self):
        """Get the rpm of the axis"""
        motor_rpm = self.get_motor_rpm()
        return motor_rpm / motion_config.reduction

    def stop(self):
        """Stop the motion watcher"""
        self.stop_event.set()

    def stopped(self):
        """Check if the motion watcher is or has stopped"""
        return self.stop_event.is_set()
