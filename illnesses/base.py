from time import time
from strenum import StrEnum
import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values

class treatments(StrEnum):
    INSULINA="Insulina"
    LOSARTAN="Losartan"

class Illness(object):
    def __init__(self):
        self.name="Base"
        self.startTime=time()

    def proceed(self, name, treatment, patient):
        return "", False

    def update_health_attributes(self, patient):
        return

    def parse_treatment(self, treatment_str: str, patient)->list[treatments]:
        return []
    
    def generate_symptoms(self, patient):
        return