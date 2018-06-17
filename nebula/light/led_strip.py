def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue


class LedStrip(object):
    """
    Base class for all ledstrips
    """
    def __init__(self,length, pinPWM, freq, dma_channel,invert):
        pass

	def setPixelColor(self, n, color):
		pass

	def setPixelColorRGB(self, n, red, green, blue, white = 0):
		pass

	def setBrightness(self, brightness):
		pass

	def getBrightness(self):
		pass

	def getPixels(self):
		pass

	def numPixels(self):
		pass

	def getPixelColor(self, n):
		pass

    
class NeoPixelLedStrip(LedStrip):
    """
    This class is a wrapper around the Adafruit_NeoPixel ledstrip class.
    Here, events around strip functions can be triggered.
    """
    from neopixel import *

    def __init__(self,length, pinPWM, freq, dma_channel,invert):
        """
        int pinPWM - the PWM pin number (Must support PWM!)\t
        int freq   - LED signal frequency in hertz (usually 800khz)\t
        int dma_channel - the dma channel used to create the pwm signal\t
        bool invert - True to invert the signal (when using NPN transistor level shift)
        """
        self.strip = Adafruit_NeoPixel(length, pinPWM, freq, dma_channel, invert)
    
    def _cleanup(self):
		self.strip._cleanup()

    def begin(self):
        self.strip.begin()
    
    def show(self):
        self.strip.show()

	def setPixelColor(self, n, color):
		"""Set LED at position n to the provided 24-bit color value (in RGB order).
		"""
		self.strip.setPixelColor(n,Color)

	def setPixelColorRGB(self, n, red, green, blue, white = 0):
		"""Set LED at position n to the provided red, green, and blue color.
		Each color component should be a value from 0 to 255 (where 0 is the
		lowest intensity and 255 is the highest intensity).
		"""
		self.setPixelColor(n, Color(red, green, blue, white))

	def setBrightness(self, brightness):
		"""Scale each LED in the buffer by the provided brightness.  A brightness
		of 0 is the darkest and 255 is the brightest.
		"""
		self.strip.setBrightness(brightness)

	def getBrightness(self):
		"""Get the brightness value for each LED in the buffer. A brightness
		of 0 is the darkest and 255 is the brightest.
		"""
		return self.strip.getBrightness()

	def getPixels(self):
		"""Return an object which allows access to the LED display data as if
		it were a sequence of 24-bit RGB values.
		"""
		return self.strip.getPixels()

	def numPixels(self):
		"""Return the number of pixels in the display."""
		return self.strip.numPixels()

	def getPixelColor(self, n):
		"""Get the 24-bit RGB color value for the LED at position n."""
        return self.strip.getPixelColor(n)