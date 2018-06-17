import time

def sliding_pattern(run_for_seconds):
    from neopixel import Color
    from ...nebula.light.led_controller import led_controller
    from ...nebula.light.light_animation import SlidingPatterns
    print("starting sliding patterns test")
    patterns = [[Color(255,0,0),Color(0,0,255),Color(0,255,0),Color(0,0,0)]]
    sp = SlidingPatterns(patterns)
    lc = led_controller(18,800000,5,[[0,74],[75,149],[150,224],[225,299]])
    lc.start()

    start_at = time.time()
    wait_ms = 100
    lc.set_next_animation(sp,wait_ms,start_at)

    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)

    patterns = [[Color(0,0,0),Color(0,0,255)]]
    sp = SlidingPatterns(patterns)
    lc.set_next_animation(sp,1,time.time())
    end_time = time.time() + run_for_seconds

    while time.time() < end_time:
        time.sleep(1)


    lc.stop()
    print("end of sliding patterns test")

def set_frame_duration():
    from neopixel import Color
    from ...nebula.light.led_controller import led_controller
    from ...nebula.light.light_animation import SlidingPatterns
    print("starting set_frame_duration test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    sp = SlidingPatterns(patterns)
    lc = led_controller(18,800000,5,[[0,74],[75,149],[150,224],[225,299]])
    lc.start()

    lc.set_next_animation(sp,1000,time.time())
    for x in range(1000,0,-100):
        time.sleep(1)
        lc.set_frame_duration(x)

    for x in range(100,1100,100):
        time.sleep(1)
        lc.set_frame_duration(x)
        
    lc.stop()
    print("end of set_frame_duration test")

def inversed_led_sections(run_for_seconds):
    from neopixel import Color
    from ...nebula.light.led_controller import led_controller
    from ...nebula.light.light_animation import SlidingPatterns
    print("starting set_frame_duration test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    sp = SlidingPatterns(patterns)
    lc = led_controller(18,800000,5,[[0,74],[149,75],[150,224],[299,225]])
    lc.start()

    lc.set_next_animation(sp,500,time.time())
    time.sleep(run_for_seconds)        
    lc.stop()
    print("end of set_frame_duration test")