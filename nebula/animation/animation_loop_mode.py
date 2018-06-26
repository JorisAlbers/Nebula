from enum import Enum

class LoopMode(Enum):
    NO_LOOP = 0    # Default value, runs one iteration. Same as a DURATION loopMode with 1 as value
    DURATION = 1   # Run until x miliseconds
    ITERATIONS = 2 # Run until the iterations have passed