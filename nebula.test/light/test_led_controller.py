import time

def test_sliding_pattern():
    from neopixel import Color
    from ...light.led_controller import led_controller
    from ...light.light_animation import SlidingPatterns
    print("starting sliding patterns test")
    patterns = [[Color(255,0,0),Color(0,255,0),Color(0,255,0)]]
    sp = SlidingPatterns(patterns)
    lc = led_controller(18,800000,5,75,75,75,75)
    lc.start()

    lc.add_animation(sp,1.0,time.time() + 5)
    lc.join()
    lc.stop()
    print("end of sliding patterns test")