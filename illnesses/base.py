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
                patient["color"]=1
                patient["summary"]="Hipoglucemia Severa"
                return statuses.Status.DEAD, True, patient
        
        if pat_healthatts["Colesterol Total"][0]>400:
            patient["color"]=1
            patient["summary"]="Desarolló una Hipertensión Severa"
            return statuses.Status.DEAD, True, patient
        
     
        if pat_healthatts["Plaquetas"][0]<6000:
            patient["color"]=1
            patient["summary"]="Sufrio de Plaquetopenia Grave"
            return statuses.Status.DEAD, True, patient
            
        if pat_healthatts["Globulos Blancos"][0]<1000:
            patient["color"]=1
            patient["summary"]="Leucopenia Grave"
            return statuses.Status.DEAD, True, patient
        
        if pat_healthatts["Glucosa"][0]>300:
            patient["color"]=1
            patient["summary"]="Hiperglucemia Severa"
            return statuses.Status.DEAD, True, patient
            
        if pat_healthatts["Tension Arterial Sistólica"][0]>300 or pat_healthatts["Tension Arterial Diastólica"][0]>200:
            patient["color"]=1
            patient["summary"]="Recibió un ACV"
            return statuses.Status.DEAD, True, patient

        if pat_healthatts["Tension Arterial Sistólica"][0]==0 or pat_healthatts["Tension Arterial Diastólica"][0]==0:
            patient["color"]=1
            patient["summary"]="Hipotensión Severa"
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