def sliding_pattern(run_for_seconds, frame_duration=100):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

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
    run_for_seconds = 10
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns,0),frame_duration, LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)

    patterns = [[Color(0,0,0),Color(0,0,255)]]
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns,0),frame_duration,LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)

    lc.stop()
    print("end of sliding patterns test")

def sliding_patterns_margin(run_for_seconds, frame_duration=100):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    print("starting sliding_patterns_margin test")
    # Light Animation
    patterns = [[Color(0,0,0),Color(255,0,0)],[Color(0,0,0),Color(0,255,0)]]
    margin = 50
    # Led strip
    length_strip = 300
    led_sections = [[0,200]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    # Led controller
    lc = LedController(strip,led_sections)

    #Start
    lc.start()
    run_for_seconds = 10
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns,margin),frame_duration, LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)

    patterns = [[Color(0,0,0),Color(0,0,255)],[Color(0,0,0),Color(0,0,255)]]
    lc.setAnimation(LightAnimation(SlidingPatterns(patterns,margin),frame_duration,LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)

    lc.stop()
    print("end of sliding_patterns_margin test")

def repeatingPatterns(run_for_seconds, frame_duration=100):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import RepeatingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    print("starting repeating patterns test")
    patterns = [[Color(255,0,0),Color(0,0,0)],[Color(0,0,0),Color(255,0,0)]]
    length_strip = 300
    led_sections = [[0,300,300]]
    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    lc = LedController(strip,led_sections)
    
    #Start
    lc.start()
    run_for_seconds = 10
    lc.setAnimation(LightAnimation(RepeatingPatterns(patterns),frame_duration,LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)
    lc.stop()
    print("end of repeating patterns test")

def patternfade(run_for_seconds, max_n,fade_steps,frame_duration=100):
    import time
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import RandomFade
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    print("starting patternfade patterns test")
    patterns = [[80,80,80],[160,160,160],[80,80,80]],[[80,0,0],[160,0,0],[80,0,0]]
    length_strip = 300
    led_sections = [[0,300,300]]

    strip = NeoPixelLedStrip(length_strip, 18,800000,5,False)
    lc = LedController(strip,led_sections)
    la = RandomFade(patterns,max_n,fade_steps)
    #Start
    lc.start()
    run_for_seconds = 10
    lc.setAnimation(LightAnimation(la,frame_duration,LoopMode.DURATION, run_for_seconds * 1000))

    time.sleep(run_for_seconds + 1)
    lc.stop()
    print("end of patternfade test")