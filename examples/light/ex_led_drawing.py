def sliding_pattern(run_for_seconds):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    print("starting sliding patterns test")
    # Light Animation
    patterns = [[Color(255,0,0),Color(0,0,255),Color(0,255,0),Color(0,0,0)]]
    # Led strip
    length_strip = 300
    led_sections = [[0,74],[75,149],[150,224],[225,299]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)

    #Start
    lc.start()
    start_at = time.time()
    wait_ms = 100
    lc.set_next_animation(LightAnimation(SlidingPatterns(patterns),wait_ms,start_at))
    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)

    patterns = [[Color(0,0,0),Color(0,0,255)]]
    lc.set_next_animation(LightAnimation(SlidingPatterns(patterns),wait_ms,time.time()))
    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)


    lc.stop()
    print("end of sliding patterns test")


def repeatingPatterns(run_for_seconds):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import RepeatingPatterns
    from ...nebula.light.light_animation import LightAnimation
    print("starting repeating patterns test")
    patterns = [[Color(255,0,0),Color(0,0,0)],[Color(0,0,0),Color(255,0,0)]]
    length_strip = 300
    led_sections = [[0,300,300]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    lc = LedController(strip,led_sections)
    
    #Start
    lc.start()
    start_at = time.time()
    wait_ms = 100
    lc.set_next_animation(LightAnimation(RepeatingPatterns(patterns),wait_ms,start_at))
    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)
    lc.stop()
    print("end of repeating patterns test")