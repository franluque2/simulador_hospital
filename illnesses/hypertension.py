from illnesses import base, statuses
import random
from PatientCreation import default_values

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
    
    symptom_list=["Sintoma A", "Sintoma B", "Sintoma C"]
    symptom_list_weights=[]
    
    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(1,6)
        symptom_list_extended=random.choices(population=self.symptom_list, cum_weights=self.symptom_list_weights, k=symtom_list_num)
        symptom_list.extend(symptom_list_extended)
        return