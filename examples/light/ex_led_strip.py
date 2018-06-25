def length_test(length):
    from ...nebula.light.led_strip import NeoPixelLedStrip, Color
    import time
    strip = NeoPixelLedStrip(length,18,800000,5,False)
    strip.begin()
    pattern = [Color(0,255,0), Color(200,0,0), Color(150,0,0), Color(100,0,0), Color(50,0,0)]

    for x in range(0,len(pattern)):
        strip.setPixelColor(x,pattern[x])
        strip.setPixelColor(length-1-x, pattern[len(pattern)-1-x])
    
    strip.show()

    time.sleep(5)

    for x in range(0,length):
        strip.setPixelColor(x,Color(255,0,0))
        strip.show()
        time.sleep(0.05)
    

