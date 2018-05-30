import threading
import motion_watcher
from .. import Timing

class motion_controller(threading.Thread):
    """
    Controls the motion of a motor
    """
    
    #The maximum rounds per minute allowed
    MAXIMUM_RPM = 20

    def __init__(self,motion_watcher):
        """
        MotionWatcher motion_watcher - class providing speed and direction feedback
        """
        self.motion_watcher = motion_watcher

        #Threading
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        """
        Start the motion controller.
        """
        

    def stop(self, stop_motion_watcher = True):
        """Stop the motion controller"""
        print("Stopping motion controller")
        if(stop_motion_watcher):
            self.motion_watcher.stop()
        self.stop_event.set()

    def stopped(self):
        """Check if the motion controller is stopping"""
        return self.stop_event.is_set()
    