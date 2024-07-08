from enum import Enum

class Status(Enum):
    CONTINUE= 0,
    HEAL = 1,
    DAMAGE = 2,
    CURED = 3,
    DEAD = 4