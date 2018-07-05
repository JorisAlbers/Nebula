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

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,299]])
    controller = AnimationController(led_controller,None)
    print("Starting controller")
    controller.start()
    controller.setNextAnimations(animation,time.time() + 1)
    print("Next animation has been set")
    
    time.sleep(15)
    controller.stop()
    print("End of lightAnimation_callback example")

def wait_in_animation(wait_seconds):
    print("Start of wait_in_animation example")
    from ...nebula.animation.animation_controller import AnimationController
    from ...nebula.animation.animation import Animation
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.led_drawing import RepeatingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    lightAnimation1 = LightAnimation(SlidingPatterns([[Color(0,0,255),Color(0,0,0)]]),100,LoopMode.ITERATIONS,20)
    lightAnimation2 = LightAnimation(SlidingPatterns([[Color(0,255,255),Color(0,0,0)]]),100,LoopMode.ITERATIONS,20)
    
    animation = Animation(False)
    animation.addLightAnimation(lightAnimation1)
    animation.addLightWait(wait_seconds * 1000,False)
    animation.addLightAnimation(lightAnimation2)

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,299]])
    controller = AnimationController(led_controller,None)
    print("Starting controller")
    controller.start()
    controller.setNextAnimations(animation,time.time() + 1)
    print("Next animation has been set")
    
    time.sleep(15 + wait_seconds)
    controller.stop()
    print("End of wait_in_animation example")

def loop_example(seconds_per_light_animation):
    print("Start of loop_example example")
    from ...nebula.animation.animation_controller import AnimationController
    from ...nebula.animation.animation import Animation
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import SlidingPatterns
    from ...nebula.light.led_drawing import RepeatingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    lightAnimation1 = LightAnimation(SlidingPatterns([[Color(0,0,255),Color(0,0,0)]]),100,LoopMode.DURATION,seconds_per_light_animation * 1000)
    lightAnimation2 = LightAnimation(SlidingPatterns([[Color(0,255,255),Color(0,0,0)]]),100,LoopMode.DURATION,seconds_per_light_animation* 1000)
    
    animation = Animation(True)
    animation.addLightAnimation(lightAnimation1)
    animation.addLightAnimation(lightAnimation2)

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,299]])
    controller = AnimationController(led_controller,None)
    controller.start()
    controller.setNextAnimations(animation,time.time() + 1)
    
    time.sleep(seconds_per_light_animation * 3 +  5)
    controller.stop()
    print("End of loop_example example")

def loop_repeating_patterns(iterations):
    print("Start of loop_repeating_patterns example")
    from ...nebula.animation.animation_controller import AnimationController
    from ...nebula.animation.animation import Animation
    from ...nebula.light.led_controller import LedController
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    from ...nebula.light.led_drawing import RepeatingPatterns
    from ...nebula.light.light_animation import LightAnimation
    from ...nebula.animation.animation_loop_mode import LoopMode

    lightAnimation1 = LightAnimation(RepeatingPatterns([[Color(0,255,0),Color(0,0,0),Color(0,0,0),Color(0,0,0)]]),100,LoopMode.ITERATIONS,iterations)
    lightAnimation2 = LightAnimation(RepeatingPatterns([[Color(0,255,255),Color(0,0,0)]]),100,LoopMode.DURATION,iterations)
    
    animation = Animation(True)
    animation.addLightAnimation(lightAnimation1)
    animation.addLightAnimation(lightAnimation2)

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,299]])
    controller = AnimationController(led_controller,None)
    controller.start()
    controller.setNextAnimations(animation,time.time() + 1)
    
    time.sleep(20)
    controller.stop()
    print("End of loop_repeating_patterns example")

def clear_animation_test():
    print("Home of clear_animation_test example")
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

    led_controller = LedController(NeoPixelLedStrip(300,18,800000,5,False),[[0,299]])
    controller = AnimationController(led_controller,None)
    print("Starting controller")
    controller.start()
    controller.setNextAnimations(animation,time.time())
    time.sleep(2)
    controller.clear()
    print("clear has been set")
    
    time.sleep(15)
    controller.stop()
    print("End of clear_animation_test example")
    



