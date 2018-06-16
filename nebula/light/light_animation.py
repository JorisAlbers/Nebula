from neopixel import Color


class LightAnimation(object):
    def __init__(self):
        pass

    def init_ring(self, led_sections):
        """
        An animation is not ring-specific. By calling init_ring, a ring can set its own dimensions
        array led_sections [ring1, ring2,...] ring = [int start, int stop, int length]
        """
        if len(led_sections < 1):
            raise ValueError("There must be at least 1 defined led section")

        for x in range(0,len(led_sections)):
            if (len(x) != 3 ):
                raise ValueError("The led section at index {0} must have 3 items!".format(x))
            for y in range(0,len(led_sections[x])):
                if not isinstance(led_sections[x][y],int):
                    raise ValueError("The element at index {0} in led_section {1} must be an int!".format(y,x))
        
        self.led_sections = led_sections


    def draw_frame(self, strip):
        pass

    def section_index_to_strip_index(self, section_pixel_index, section):
        start = self.led_sections[section][0]
        stop  = self.led_sections[section][1]

        if(stop > start):
            # Forwards
            return start + section_pixel_index
        else:
            # Reverse
            return stop - section_pixel_index

    
class SlidingPatterns(LightAnimation):
    def __init__(self, patterns):
        """
        array patterns - the patterns to slide. A pattern is an array of rgb vaues
        [pattern1, patter2]
        pattern = [[Color],[Color],[Color]]
        """
        LightAnimation.__init__(self)
        self.patterns = patterns

    def draw_frame(self, strip):
        """
        Draw the next frame in the animation
        strip - the Adafruit strip containing the 4 led strips
        """
        iteration = 0
        #  Sliding patterns keep going
        while True:
            for i in range(0, len(self.patterns)):
                # draw a pattern
                # TODO add spacing between patterns
                for j in range(0, len(self.patterns[i])):
                    for k in range(0,len(self.led_sections)):
                        # Get the pixel index in the section k
                        p_section = (iteration % self.led_sections[k][2]) + j
                        # Get the actual pixel index on the strip
                        p_strip = super(SlidingPatterns,self).section_index_to_strip_index(p_section,k)
                        # Draw the pixel
                        strip.setPixelColor(p_strip, self.patterns[i][j])
            iteration += 1
            yield
