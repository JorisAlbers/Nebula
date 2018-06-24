

def test_section_index_to_strip_index__forwards_section():
    from ...nebula.light.led_drawing import LedDrawer
    sections = [[0,4,5],[9,5,5]]
    la = LedDrawer()
    la.led_sections = sections
    expectedIndexes_section1 = [0,1,2,3,4]
    for i in range(0,len(expectedIndexes_section1)):
        assert la.section_index_to_strip_index(i,0) == expectedIndexes_section1[i]

def test_section_index_to_strip_index__reversed_section():
    from ...nebula.light.led_drawing import LedDrawer
    sections = [[9,5,5]]
    la = LedDrawer()
    la.led_sections = sections
    expectedIndexes_section1 = [9,8,7,6,5]
    for i in range(0,len(expectedIndexes_section1)):
        assert la.section_index_to_strip_index(i,0) == expectedIndexes_section1[i]

def test_repeating_pattern_time():
    from ...nebula.light.led_strip import Color
    from ...nebula.light.led_drawing import RepeatingPatterns
    patterns = [[Color(255,255,255), Color(0,0,0)]]
    sections = [[0,10,10]]
    rp = RepeatingPatterns(patterns)
    rp.init_ring(sections)
    #TODO check if correct items are set




