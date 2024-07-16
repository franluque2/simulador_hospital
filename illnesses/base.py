from time import time
from strenum import StrEnum
from . import statuses
import sys
import os
import FranMongoClient


here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values

class Illness(object):
    def __init__(self):
        self.name="Base"
        self.startTime=time()

    def proceed(self, name, treatment, patient, mongoclient):
        return "", False

    def update_health_attributes(self, patient):
        return

    def parse_treatment(self, treatment_str: str, patient)->list[statuses.treatments]:
        return []
    
    def generate_symptoms(self, patient):
        return