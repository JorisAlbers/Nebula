import time

def set_frame_duration():
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation import LoopMode

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
    from ...nebula.animation.animation import LoopMode

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
