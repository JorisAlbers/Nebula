import time

def lightAnimation_callback():
    print("Home of lightAnimation_callback example")
    from ...nebula.animation.animation_controller import AnimationController
    from ...nebula.animation.animation import Animation
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    lightAnimation1 = LightAnimation(SlidingPatterns([[Color(0,0,255),Color(0,0,0)]]),100,LoopMode.ITERATIONS,10)
    lightAnimation2 = LightAnimation(SlidingPatterns([[Color(0,255,255),Color(0,0,0)]]),100,LoopMode.ITERATIONS,10)
    
    animation = Animation(False)
    animation.addLightAnimation(lightAnimation1)
    animation.addLightAnimation(lightAnimation2)

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,300]])
    controller = AnimationController(led_controller,None)

    controller.run()
    controller.setNextAnimations(animation,time.time() + 1)

    while controller.current_animation is not None:
        time.sleep(1)

    print("End of lightAnimation_callback example")


