from illnesses import base, statuses
import random
import sys
import os
import FranMongoClient
import numpy as np

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values, symptoms

class diabetes_tipo_dos(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Diabetes de Tipo Dos"
    

    def proceed(self, name, treatment, patient, mongoclient) -> list[statuses.Status, bool, object]:
        if patient["total_ticks"]<5:
            return statuses.Status.CONTINUE, False, patient
        pat_healthatts=patient["health_attributes"]

        if (statuses.treatments.METFORMINA in treatment) and (statuses.treatments.GLIMEPIRIDA in treatment):
            pat_healthatts["Glucosa"][0]=random.randint(80,100)
            return statuses.Status.CURED, True, patient
        
        if statuses.treatments.METFORMINA in treatment:
            if random.randint(1,5)==1:
                pat_healthatts["Glucosa"][0]=random.randint(80,100)
                return statuses.Status.CURED, True, patient

        
        if statuses.treatments.INSULINA in treatment:
            if random.randint(1,3)==1:
                pat_healthatts["Glucosa"][0]=random.randint(80,100)
                return statuses.Status.CURED, True, patient

        if (statuses.treatments.INSULINA in treatment) and (statuses.treatments.METFORMINA in treatment):
            pat_healthatts["Glucosa"][0]=random.randint(80,100)
            return statuses.Status.CURED, True, patient

        pat_healthatts["Glucosa"][0]=pat_healthatts["Glucosa"][0]+random.randint(80,120)
        patient["color"]=patient["color"]+0.05

        return super().proceed(name, treatment, patient, mongoclient)

    def update_health_attributes(self, patient):
        pat_healthatts=patient["health_attributes"]
        if patient["personaldata"]==default_values.PERSONAL_DATA.value:
            patient["personaldata"]
        pat_healthatts["Tension Arterial Sistólica"]=[random.randint(120,260), "mmHG"]
        pat_healthatts["Tension Arterial Diastólica"]=[random.randint(85,120), "mmHG"]
        if random.randint(1,2)==2:
            pat_healthatts["Urea"]=[random.randint(120,250), "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Creatinina"]=[random.randint(14,40)/10, "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Potasio"]=[random.randint(53,72)/10, "mEq/L"]
        if random.randint(1,2)==2:
            pat_healthatts["Sodio"]=[random.randint(125,135), "mEq/L"]

        return patient
    
    symptom_list=[symptoms.THIRST.value, symptoms.MORE_URINATION.value,
                  symptoms.BLURRY_VISION.value, symptoms.TIREDNESS.value,
                  symptoms.INVOLUNTARY_WEIGHTLOSS.value]
    symptom_list_weights=[4,3,1,2,3]
    


    symptom_list_nums=[1,3]

    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(self.symptom_list_nums[0],self.symptom_list_nums[1])
        weights = np.array(self.symptom_list_weights)
        probabilities = weights / weights.sum()
        symptom_list_extended=np.random.choice(self.symptom_list,symtom_list_num,False,probabilities)
        symptom_list.extend(list(symptom_list_extended))
        return