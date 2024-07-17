from enum import Enum, StrEnum

class Status(Enum):
    CONTINUE= 0,
    HEAL = 1,
    DAMAGE = 2,
    CURED = 3,
    DEAD = 4,
    IMPORTANT_CHANGE= 5

class treatments(StrEnum):
    INSULINA="Insulina"
    LOSARTAN="Losartan"
    ENALAPRIL="Enalapril"
    DIETA="Dieta"
    EJERCICIO="Ejercicio"
    METFORMINA="Metformina"
    GLIMEPIRIDA="Glimepirida"
    ANTINFLAMATORIOS="Antinflamatorios"
    ESTEROIDES="Esteroides"
    IBUPROFENO="Ibuprofeno"
    ASPIRINA="Aspirina"
    PARACETAMOL="Paracetamol"
    HIDRATACION="Hidratación"
    REPOSO="Reposo"
    CIRUGIA="Cirugia"
    ORLISTAT="Orlistat"
    LIRAPLOTIDA="Liraplotida"
    AMLODIPINA="Amlodipina"
    HIDROCLOROTIZIDA="Hidroclorotizida"
    AMOXICILINA="Amoxicilina"
    METIFORMINA="Metiformina"