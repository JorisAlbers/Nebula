class led_controller(threading.Thread):
    """
    Controls ws2812b led strips
    """

    def __init__(self, pinPWM):
        """
        int pinPWM - the PWM pin number
        """
        self.pinPWM = pinPWM

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
