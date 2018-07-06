from led_strip import Color, LedStrip
from collections import Iterator
import random

class LedDrawer(Iterator):
    def __init__(self):
        self.iteration = 0

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

        strip_length = 0
        for x in range(0,len(led_sections)):
            if (len(led_sections[x]) != 3 ):
                raise ValueError("The led section at index {0} must have 3 items!".format(x))
            for y in range(0,len(led_sections[x])):
                if not isinstance(led_sections[x][y],int):
                    raise ValueError("The element at index {0} in led_section {1} must be an int, was {2}!".format(y,x, type(led_sections[x][y])))
            strip_length += led_sections[x][2]
        self.strip = strip        
        self.led_sections = led_sections
        self.strip_lenght = strip_length

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

    def reset(self):
        """
        Set the drawer iteration index back to 0
        """
        if self.iteration != 0:
            self.iteration = 0

    
class SlidingPatterns(LedDrawer):
    """
    One pattern sliding over the ledstrip
    """
    def __init__(self, patterns,margin):
        """
        array patterns - the patterns to slide. A pattern is an array of rgb vaues
        [pattern1, patter2]
        pattern = [[Color],[Color],[Color]]
        """
        LedDrawer.__init__(self)
        self.patterns = patterns
        self.margin = margin
        
    def next(self):
        """
        Draw the next frame in the animation
        """
        # Each iteration draws the patterns a position further on the strip
        pattern_start = self.iteration
        for i in range(0, len(self.patterns)):
            # draw a pattern
            # TODO add spacing between patterns
            for j in range(0, len(self.patterns[i])):
                for k in range(0,len(self.led_sections)):
                     # Get the pixel index in the section k
                    p_section = (pattern_start + j) % self.led_sections[k][2]
                    # Get the actual pixel index on the strip
                    p_strip = super(SlidingPatterns,self).section_index_to_strip_index(p_section,k)
                    # Draw the pixel
                    self.strip.setPixelColor(p_strip, self.patterns[i][j])
            pattern_start += len(self.patterns[i]) + self.margin
        self.iteration += 1

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

class RandomFade(LedDrawer):
    """
    Fades a patterns in and out, randomly over the led strip
    A fade takes 11 iterations to complete
    """
    def __init__(self,patterns, max_n, fade_steps):
        """
        list patterns - the patterns to randomly fade, NOT WITH COLORS, BUT WITH LISTS OF RGB!
        max_n - the manimum number of patterns
        """
        LedDrawer.__init__(self)
        self.fade_steps = fade_steps
        self.patterns = patterns
        self.max_n = max_n
        self.displayed_items = [] #start_index, patternINdex , fadeStep index
        self.faded_patterns = []
        for pattern_index in range(0,len(patterns)):
            pattern_fades = []
            # Creates a list with all fades of a pattern
            for x in range(0,self.fade_steps+1):
                pattern_fades.append([])
            print("new pattern")
            for p in range(0,len(patterns[pattern_index])): 
                step_R = (patterns[pattern_index][p][0]) / self.fade_steps
                step_G = (patterns[pattern_index][p][1]) / self.fade_steps
                step_B = (patterns[pattern_index][p][2]) / self.fade_steps
                for x in range(0,self.fade_steps +1):
                    pattern_fades[x].append(Color(step_R * x, step_G* x,step_B * x))
            self.faded_patterns.append(pattern_fades)



    def reset(self):
        self.displayed_items = []
        LedDrawer.reset(self)

    def next(self):
        """
        Draw the next frame in the animation
        """
        #Create new patterns on the strip
        
        for x in range(0,random.randint(0,self.max_n - len(self.displayed_items))):
            start_index = random.randint(0,self.strip_lenght)-1
            pattern_index = random.randint(0,len(self.patterns)-1)
            self.displayed_items.append([start_index,pattern_index,0])

        for item in self.displayed_items:
            fade_step = item[2]
            pattern_index = item[1]
            start_index = item[0]
            if fade_step > self.fade_steps * 2 -1:  #TODO check if this is correct, maybe 1 off
                self.displayed_items.remove(item)
                # clear the pattern from the strip
                for p in range(0,len(self.patterns[pattern_index])):
                    self.strip.setPixelColor((start_index + p) % self.strip_lenght , Color(0,0,0))
                    continue
    
            fade_index = fade_step
            if fade_step > self.fade_steps:
                # Fade out, override fade_index
                 fade_index = self.fade_steps - (fade_step-self.fade_steps)
            
            for p in range(0,len(self.patterns[pattern_index])):
                    try:
                        print("-----")
                        print("start index = " +str(start_index))
                        print("p = " +str(p))
                        print("p + start_index % modulo strip length = " +str((start_index + p )% self.strip_lenght))
                        print("pattern index = " +str(pattern_index))
                        print("fade index = " +str(fade_index))
                        print("p = " +str(p))
                        print("start index = " +str(start_index))
                        self.strip.setPixelColor((start_index + p) % self.strip_lenght , self.faded_patterns[pattern_index][fade_index][p])
                    except Exception,e:

                        raise e



            
            item[2] += 1 # Increment the fade index

            
            
            



        



        
