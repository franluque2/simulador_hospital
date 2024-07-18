from time import time
from strenum import StrEnum
from . import statuses
import sys
import os
import FranMongoClient
import random


here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values

class Illness(object):
    def __init__(self):
        self.name="Base"
        self.startTime=time()

    def proceed(self, name, treatment, patient, mongoclient):
        pat_healthatts=patient["health_attributes"]
        if statuses.treatments.INSULINA in treatment:
            pat_healthatts["Glucosa"]=pat_healthatts["Glucosa"]-random.randint(5,15)
            if pat_healthatts["Glucosa"]<40:
                patient["color"]=0
                patient["summary"]="Hipoglucemia Severa"
                return statuses.Status.DEAD, True, patient
            

        return statuses.Status.CONTINUE, False, patient

    def update_health_attributes(self, patient):
        return

    def parse_treatment(self, treatment_str: str, patient)->list[statuses.treatments]:
        return []
    
    def generate_symptoms(self, patient):
        return
    
    def __str__(self) -> str:
        return self.name