from enum import Enum
class default_values(Enum):
    PERSONAL_DATA="No Hay Datos Personales Relevantes"
    FAMILY_DATA_FATHER="No hay precedentes importantes del lado paternal"
    FAMILY_DATA_MOTHER="No hay precedentes importantes del lado maternal"
    PHYS_EVAL="Parece estar en buen estado Fisico"

class symptoms(Enum):
    CEFALEA="Cefalea"
    CUTANEOUS_ERUPTIONS="Erupciones Cutaneas"
    STOMACHACHES="Dolores del Estomago"