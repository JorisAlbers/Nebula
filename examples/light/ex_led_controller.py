import time

def set_frame_duration():
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    print("starting set_frame_duration test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    # Led strip
    length_strip = 300
    led_sections = [[0,74],[75,149],[150,224],[225,299]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)
    lc.start()

    total_iterations = 25
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns),1000,LoopMode.ITERATIONS, total_iterations))
    for x in range(1000,0,-100):
        time.sleep(1)
        lc.set_frame_duration(x)

    for x in range(100,1100,100):
        time.sleep(1)
        lc.set_frame_duration(x)
        
    lc.stop()
    print("end of set_frame_duration test")

def inversed_led_sections(run_for_seconds):
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    print("starting set_frame_duration test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    # Led strip
    length_strip = 300
    led_sections = [[0,74],[149,75],[150,224],[299,225]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)
    lc.start()

    lc.setAnimation(LightAnimation(SlidingPatterns(patterns),500,LoopMode.DURATION, run_for_seconds * 1000))
    time.sleep(run_for_seconds + 1)        
    lc.stop()
    print("end of set_frame_duration test")

def loopMode_duration_test():
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode
    import time

    print("starting loopMode_Duration_test test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    # Led strip
    length_strip = 300
    led_sections = [[0,74],[149,75],[150,224],[299,225]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)
    lc.start()
    run_for_seconds = 10

    start = time.time()
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns),500,LoopMode.DURATION, run_for_seconds * 1000))
    while lc.current_animation is not None:
        time.sleep(0.1)
    print("Took {0} miliseconds".format(int(round((time.time()-start) * 1000))))
    print("It should have taken {0} miliseconds".format(run_for_seconds * 1000))
    lc.stop()
    print("end of loopMode_Duration_test test")

def loopMode_iterations_test():
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode
    import time

    print("starting loopMode_iterations_test test")
    patterns = [[Color(0,0,0),Color(0,0,255)]]
    # Led strip
    length_strip = 300
    led_sections = [[0,74],[149,75],[150,224],[299,225]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)
    lc.start()
    iterations = 10

    start = time.time()
    la = LightAnimation(SlidingPatterns(patterns),500,LoopMode.ITERATIONS, iterations)
    print("The lightAnimation loop_value at start is {0}".format(la.loop_value))
    lc.setAnimation(la)
    while lc.current_animation is not None:
        time.sleep(0.1)
    print("Took {0} miliseconds".format(int(round((time.time()-start) * 1000))))
    print("The lightAnimation loop_value at end is {0}".format(la.loop_value))
    lc.stop()
    print("end of loopMode_iterations_test test")