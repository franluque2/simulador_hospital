from time import time
from strenum import StrEnum
from PatientCreation import default_values

class treatments(StrEnum):
    INSULINA="Insulina"
    LOSARTAN="Losartan"


class Illness(object):
    def __init__(self):
        self.name=""
        self.startTime=time()

    def proceed(self, name, treatment, patient):
        return ""

    def update_health_attributes(self, patient):
        return

    def parse_treatment(self, treatment_str: str, patient)->list[treatments]:
        return []