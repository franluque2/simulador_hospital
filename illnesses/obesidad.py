from illnesses import base, statuses
import random
import sys
import os
import FranMongoClient
import numpy as np

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values, symptoms

class obesidad(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Obesidad"
    

    def proceed(self, name, treatment, patient, mongoclient) -> list[statuses.Status, bool, object]:
        if patient["total_ticks"]<5:
            return statuses.Status.CONTINUE, False, patient
        pat_healthatts=patient["health_attributes"]

        if statuses.treatments.ORLISTAT in treatment:

            pat_healthatts["Trigliceridos"][0]=pat_healthatts["Trigliceridos"][0]-((pat_healthatts["Trigliceridos"][0]-90)/4)
            pat_healthatts["Colesterol Total"][0]=pat_healthatts["Colesterol Total"][0]-(random.randint(20, 70))
            patient["color"]=patient["color"]-0.05

            if (pat_healthatts["Trigliceridos"][0]-90<50):
                patient["color"]=0

                return statuses.Status.CURED, True, patient
                    
        if statuses.treatments.LIRAPLOTIDA in treatment:
            pat_healthatts["Trigliceridos"][0]=pat_healthatts["Trigliceridos"][0]-((pat_healthatts["Trigliceridos"][0]-90)/4)
            pat_healthatts["Colesterol Total"][0]=pat_healthatts["Colesterol Total"][0]-(random.randint(20, 70))
            patient["color"]=patient["color"]-0.05

            if (pat_healthatts["Trigliceridos"][0]-90<50):
                patient["color"]=0

                return statuses.Status.CURED, True, patient

        pat_healthatts["Trigliceridos"][0]=pat_healthatts["Trigliceridos"][0]+random.randint(10,50)
        pat_healthatts["Colesterol Total"][0]=pat_healthatts["Colesterol Total"][0]+random.randint(30,70)
        patient["color"]=patient["color"]+0.05

        return super().proceed(name, treatment, patient, mongoclient)

    def update_health_attributes(self, patient):
        pat_healthatts=patient["health_attributes"]
        if patient["personaldata"]==default_values.PERSONAL_DATA.value:
            patient["personaldata"]
        pat_healthatts["Tension Arterial Sistólica"]=[random.randint(140,260), "mmHG"]
        pat_healthatts["Tension Arterial Diastólica"]=[random.randint(90,120), "mmHG"]
        if random.randint(1,2)==2:
            pat_healthatts["Trigliceridos"]=[random.randint(150,900), "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Glucosa"]=[random.randint(100,600), "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Colesterol Total"]=[random.randint(200,500), "mg/dl"]
        if random.randint(1,2)==2:
            pat_healthatts["Acido Urico"]=[random.randint(72,400)/10, "mg/dl"]

        return patient
    
    symptom_list=[symptoms.BREATHING_TROUBLES.value, symptoms.SLEEP_APNEA.value,
                  symptoms.BACK_PAIN.value, symptoms.INCREASED_SWEATING.value,
                  symptoms.HEAT_INTOLERANCE.value, symptoms.SKIN_FOLD_INFECTIONS.value,
                  symptoms.TIREDNESS.value, symptoms.DEPRESSION.value, symptoms.DYSPNOEA.value]
    symptom_list_weights=[3,3,4,4,3,2,3,2,3]
    


    symptom_list_nums=[1,2]

    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(self.symptom_list_nums[0],self.symptom_list_nums[1])
        weights = np.array(self.symptom_list_weights)
        probabilities = weights / weights.sum()
        symptom_list_extended=np.random.choice(self.symptom_list,symtom_list_num,False,probabilities)
        symptom_list.extend(list(symptom_list_extended))
        return