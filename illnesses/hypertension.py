from illnesses import base, statuses
import random
from PatientCreation import default_values
from FranOpenAiClient import generate_clinical_interview

class hypertension(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Hipertension"
    

    def proceed(self, name, treatment, patient):
        return ""

    def update_health_attributes(self, patient):
        pat_healthatts=patient["health_attributes"]
        if patient["personaldata"]==default_values.PERSONAL_DATA.value:
            patient["personaldata"]
        return