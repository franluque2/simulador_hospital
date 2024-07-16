from enum import Enum, StrEnum

class Status(Enum):
    CONTINUE= 0,
    HEAL = 1,
    DAMAGE = 2,
    CURED = 3,
    DEAD = 4

class treatments(StrEnum):
    INSULINA="Insulina"
    LOSARTAN="Losartan"