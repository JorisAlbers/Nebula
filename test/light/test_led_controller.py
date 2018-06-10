import time

def test_sliding_pattern(run_for_seconds):
    from neopixel import Color
    from ...nebula.light.led_controller import led_controller
    from ...nebula.light.light_animation import SlidingPatterns
    print("starting sliding patterns test")
    patterns = [[Color(255,0,0),Color(0,255,0),Color(0,255,0)]]
    sp = SlidingPatterns(patterns)
    lc = led_controller(18,800000,5,75,75,75,75)
    lc.start()

    lc.add_animation(sp,1.0,time.time() + 5)
    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)

    lc.stop()
    print("end of sliding patterns test")