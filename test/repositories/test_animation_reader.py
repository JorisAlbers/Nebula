import os
from ...nebula.repositories.animation_reader import AnimationReader
from ...nebula.animation.animation import Animation
from ...nebula.animation.animation_loop_mode import LoopMode
from ...nebula.light.led_drawing import LedDrawer, SlidingPatterns, RepeatingPatterns
from ...nebula.light.light_animation import LightAnimation

def test_readFile_file_returnsLines():
    dirname = os.path.dirname(__file__)
    dir_path = os.path.join(dirname,"../../resources")
    file_name = "blue_dot.nebula.json"
    
    reader = AnimationReader(dir_path)
    lines = reader.readFile(file_name)
    assert(lines is not None)
    assert(len(lines) > 0)

def test_loadAnimation_file_returnsCorrectAnimation():
    # EXPECTED VALUES, from file blue_dot.nebula.json
    ex_initial_start_delay = 1000
    ex_loops = False
    #First light animation
    ex1_drawer = SlidingPatterns([[]])
    ex1_patterns = [["255,0,0","0,0,0"]]
    ex1_loop_mode = LoopMode.DURATION
    ex1_loop_value = 100000
    ex1_frame_duration = 200
    #Second light animation
    ex2_wait = 1000
    # type = int
    #Third light animation
    ex2_drawer = RepeatingPatterns([[]])
    ex2_patterns = [["0,255,0","0,0,0","0.0.0","0.0.0"]]
    ex2_loop_mode = LoopMode.ITERATIONS
    ex2_loop_value = 15
    ex2_frame_duration = 100

    dirname = os.path.dirname(__file__)
    dir_path = os.path.join(dirname,"../../resources")
    file_name = "blue_dot"
    client_id = "ring_1"
    reader = AnimationReader(dir_path)
    animation = reader.loadAnimation(file_name,client_id)

    #ASSERTS
    #animation properties
    assert(ex_loops == animation.loops)
    #first light animation
    la = animation.lightAnimations[0]
    assert(type(ex1_drawer) == type(la.drawer))
    assert all([a == b for a, b in zip(ex1_patterns[0], la.drawer.patterns[0])])
    assert(type(ex1_loop_mode) == type(la.loop_mode))
    assert(ex1_loop_value == la.ex1_loop_value)
    assert(ex1_frame_duration == la.ex1_frame_duration)
    #Second light animation

    #Third light animation

