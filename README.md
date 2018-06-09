# Nebula
A nebula (Latin for "cloud" or "fog";[2] pl. nebulae, nebulæ, or nebulas) is an interstellar cloud of dust, hydrogen, helium and other ionized gases. Originally, nebula was a name for any diffuse astronomical object, including galaxies beyond the Milky Way. The Andromeda Galaxy, for instance, was once referred to as the Andromeda Nebula (and spiral galaxies in general as "spiral nebulae") before the true nature of galaxies was confirmed in the early 20th century by Vesto Slipher, Edwin Hubble and others.

## Motor

The cables of the motor are attached to the following components:
```
* red    = motor+
* black  = motor-
* green  = hall sensor GND
* blue   = hall sensor Vcc (5v)
* yellow = hall sensor A Vout
* white  = hall sensor B Vout
```

## Dependencies

#neopixel:

"""
sudo apt-get update
sudo apt-get install build-essential python-dev git scons swig

git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons

cd python
sudo python setup.py install
"""