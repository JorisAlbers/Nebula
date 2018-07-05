import os
from ...nebula.repositories.animation_reader import AnimationReader
from ...nebula.animation.animation import Animation
from ...nebula.animation.animation_loop_mode import LoopMode
from ...nebula.light.led_drawing import *
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
    ex1_patterns = [[Color(255,0,0),Color(0,0,0)]]
    ex1_loop_mode = LoopMode.DURATION
    ex1_loop_value = 100000
    ex1_frame_duration = 200
    #Second light animation
    ex2_wait = 1000
    # type = int
    #Third light animation
    ex2_drawer = RepeatingPatterns([[]])
    ex2_patterns = [[Color(0,255,0),Color(0,0,0),Color(0,0,0),Color(0,0,0)]]
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
    assert(len(ex1_patterns) == len(la.drawer.patterns))
    assert all([a == b for a, b in zip(ex1_patterns[0], la.drawer.patterns[0])])
    assert(type(ex1_loop_mode) == type(la.loop_mode))
    assert(ex1_loop_value == la.loop_value)
    assert(ex1_frame_duration == la.frame_duration)
    #Second light animation
     # This is a wait
    la = animation.lightAnimations[1]
    assert(isinstance(la,int))
    assert(ex2_wait == la)

    #Third light animation
    la = animation.lightAnimations[2]
    assert(type(ex2_drawer) == type(la.drawer))
    assert(len(ex2_patterns) == len(la.drawer.patterns))
    assert all([a == b for a, b in zip(ex2_patterns[0], la.drawer.patterns[0])])
    assert(type(ex2_loop_mode) == type(la.loop_mode))
    assert(ex2_loop_value == la.loop_value)
    assert(ex2_frame_duration == la.frame_duration)
