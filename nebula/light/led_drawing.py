from led_strip import Color, LedStrip
from collections import Iterator

class LedDrawer(Iterator):
    def __init__(self):
        pass

    def init_ring(self, strip, led_sections):
        """
        An LedDrawer is not ring-specific. By calling init_ring, a ring can set its own dimensions
        LedStrip strip - The Led strip to draw on
        array led_sections [ring1, ring2,...] ring = [int start, int stop, int length]
        """
        if not isinstance(strip,LedStrip):
            raise ValueError("The strip must be a LedStrip!")

        if len(led_sections) < 1:
            raise ValueError("There must be at least 1 defined led section")

        for x in range(0,len(led_sections)):
            if (len(led_sections[x]) != 3 ):
                raise ValueError("The led section at index {0} must have 3 items!".format(x))
            for y in range(0,len(led_sections[x])):
                if not isinstance(led_sections[x][y],int):
                    raise ValueError("The element at index {0} in led_section {1} must be an int, was {2}!".format(y,x, type(led_sections[x][y])))
        self.strip = strip        
        self.led_sections = led_sections

    def iter(self):
        return self

    def next(self):
        pass

    def section_index_to_strip_index(self, section_pixel_index, section):
        start = self.led_sections[section][0]
        stop  = self.led_sections[section][1]

        if(stop > start):
            # Forwards
            return start + section_pixel_index
        else:
            # Reverse
            return start - section_pixel_index

    
class SlidingPatterns(LedDrawer):
    """
    One pattern sliding over the ledstrip
    """
    def __init__(self, patterns):
        """
        array patterns - the patterns to slide. A pattern is an array of rgb vaues
        [pattern1, patter2]
        pattern = [[Color],[Color],[Color]]
        """
        LedDrawer.__init__(self)
        self.patterns = patterns
        self.iteration = 0

    def next(self):
        """
        Draw the next frame in the animation
        """
        # Each iteration draws the patterns a position further on the strip
        for i in range(0, len(self.patterns)):
            # draw a pattern
            # TODO add spacing between patterns
            for j in range(0, len(self.patterns[i])):
                for k in range(0,len(self.led_sections)):
                     # Get the pixel index in the section k
                    p_section = (self.iteration + j) % self.led_sections[k][2]
                    # Get the actual pixel index on the strip
                    p_strip = super(SlidingPatterns,self).section_index_to_strip_index(p_section,k)
                    # Draw the pixel
                    self.strip.setPixelColor(p_strip, self.patterns[i][j])
        self.iteration += 1
        yield

class RepeatingPatterns(LedDrawer):
    """
    A pattern repeating itself over the ledstrip.
    Multiple patterns can be set. Each frame will display the next pattern
    """
    def __init__(self, patterns):
        """
        array patterns - the patterns to repeat. A pattern is an array of rgb vaues
        [pattern1, patter2]
        pattern = [[Color],[Color],[Color]]
        """
        LedDrawer.__init__(self)
        self.patterns = patterns
        self.iteration = 0

    def next(self):
        """
        Draw the next frame in the animation
        """
        #Each iteration draws a different pattern
        pattern = self.patterns[self.iteration]
        for y in range(0, len(self.led_sections)):
            patterns_in_section = self.led_sections[y][2] / len(pattern)
            for z in range(0,patterns_in_section):
                p_left = len(pattern) * z 
                for pixel_on_pattern in range(0,len(pattern)):
                    p_section = p_left + pixel_on_pattern
                    p_strip = super(RepeatingPatterns,self).section_index_to_strip_index(p_section,y)
                    self.strip.setPixelColor(p_strip,pattern[pixel_on_pattern])
        self.iteration += 1
        self.iteration = self.iteration % len(self.patterns)