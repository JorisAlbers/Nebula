from neopixel import Color


class LightAnimation(object):
    def __init__(self):
        pass

    def init_ring(self, length_l1, length_l2, length_s1, length_s2):
        """
        An animation is not ring-specific. By calling init_ring, a ring can set its own dimensions
        """
        self.length_l1 = length_l1
        self.length_l2 = length_l2
        self.length_s1 = length_s1
        self.length_s2 = length_s2

    def draw_frame(self, strip):
        pass


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
        start_l1 = 0
        start_l2 = self.length_l1
        start_s1 = start_l2 + self.length_l2
        start_s2 = start_s1 + self.length_s1
        #  Sliding patterns keep going
        while True:
            for i in range(0, len(self.patterns)):
                # draw a pattern
                # TODO add spacing between patterns
                for j in range(0, len(self.patterns[i])):
                    # draw ring 1
                    pixel = (iteration % self.length_l1) + j
                    strip.setPixelColor(start_l1 + pixel, self.patterns[i][j])
                    # draw ring 2
                    pixel = (iteration % self.length_l2) + j
                    strip.setPixelColor(start_l2 + pixel, self.patterns[i][j])
                    # draw ring 3
                    pixel = (iteration % self.length_s1) + j
                    strip.setPixelColor(start_s1 + pixel, self.patterns[i][j])
                    # draw ring 4
                    pixel = (iteration % self.length_s2) + j
                    strip.setPixelColor(start_s2 + pixel, self.patterns[i][j])
            iteration += 1
            yield
