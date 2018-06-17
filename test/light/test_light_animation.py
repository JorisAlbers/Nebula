

def test_section_index_to_strip_index__forwards_section():
    from ...nebula.light.light_animation import LightAnimation
    sections = [[0,4],[9,5]]
    la = LightAnimation()
    la.led_sections = sections
    expectedIndexes_section1 = [0,1,2,3,4]
    for i in range(0,len(expectedIndexes_section1)):
        assert la.section_index_to_strip_index(i,0) == expectedIndexes_section1[i]

def test_section_index_to_strip_index__reversed_section():
    from ...nebula.light.light_animation import LightAnimation
    sections = [[9,5]]
    la = LightAnimation()
    la.led_sections = sections
    expectedIndexes_section1 = [9,8,7,6,5]
    for i in range(0,len(expectedIndexes_section1)):
        assert la.section_index_to_strip_index(i,0) == expectedIndexes_section1[i]
