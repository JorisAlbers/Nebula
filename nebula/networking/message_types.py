from enum import IntEnum

class MessageType(IntEnum):
    NONE = 0,
    CONNECT = 1,
    DISCONNECT = 2,
    START_ANIMATION = 3