from enum import IntEnum


class TypeGameMode(IntEnum):
    INVALID = 0
    SINGLEPLAYER = 1
    MULTIPLAYERCREATE = 2
    MULTIPLAYERJOIN = 3
