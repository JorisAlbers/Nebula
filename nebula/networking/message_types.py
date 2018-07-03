from enum import IntEnum

class MessageType(IntEnum):
    NONE = 0,
    CONNECT = 1,
    DISCONNECT = 2,
    RECEIVED = 3,
    START_ANIMATION = 4
