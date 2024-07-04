from illnesses import base, statuses
import random
import sys
import os

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values, symptoms

class hypertension(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Hipertension"
    

    def proceed(self, name, treatment, patient):
        return "", True

    def update_health_attributes(self, patient):
        pat_healthatts=patient["health_attributes"]
        if patient["personaldata"]==default_values.PERSONAL_DATA.value:
            patient["personaldata"]
        return
    
    symptom_list=[symptoms.CEFALEA.value, symptoms.CUTANEOUS_ERUPTIONS.value, symptoms.STOMACHACHES.value]
    symptom_list_nums=[1,6]
    symptom_list_weights=[1,1,3]
    
    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(self.symptom_list_nums[0],self.symptom_list_nums[1])
        symptom_list_extended=random.choices(population=self.symptom_list, cum_weights=self.symptom_list_weights, k=symtom_list_num)
        symptom_list.extend(symptom_list_extended)
        return