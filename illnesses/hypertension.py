from illnesses import base, statuses
import random
import sys
import os
import FranMongoClient
import numpy as np

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values, symptoms

class hypertension(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Hipertension"
    

    def proceed(self, name, treatment, patient, mongoclient) -> list[statuses.Status, bool, object]:
        if patient["total_ticks"]<5:
            return statuses.Status.CONTINUE, False, patient
        pat_healthatts=patient["health_attributes"]

        if statuses.treatments.LOSARTAN in treatment:
            pat_healthatts["Tension Arterial Sistólica"][0]=random.randint(90,120)
            pat_healthatts["Tension Arterial Diastólica"][0]=random.randint(60,89)
            return statuses.Status.CURED, True, patient
        
        if statuses.treatments.ENALAPRIL in treatment:
            pat_healthatts["Tension Arterial Sistólica"][0]=random.randint(90,120)
            pat_healthatts["Tension Arterial Diastólica"][0]=random.randint(60,89)
            return statuses.Status.CURED, True, patient
        
        if statuses.treatments.HIDROCLOROTIZIDA in treatment:
            pat_healthatts["Tension Arterial Sistólica"][0]=random.randint(90,120)
            pat_healthatts["Tension Arterial Diastólica"][0]=random.randint(60,89)
            return statuses.Status.CURED, True, patient

        if statuses.treatments.AMLODIPINA in treatment:
            pat_healthatts["Tension Arterial Sistólica"][0]=random.randint(90,120)
            pat_healthatts["Tension Arterial Diastólica"][0]=random.randint(60,89)
            return statuses.Status.CURED, True, patient  
      
        if pat_healthatts["Tension Arterial Sistólica"][0]>180 or pat_healthatts["Tension Arterial Diastólica"][0]>110:
            patient["color"]=0
            patient["summary"]="Recibió un ACV"
            return statuses.Status.DEAD, True, patient

        pat_healthatts["Tension Arterial Sistólica"][0]=pat_healthatts["Tension Arterial Sistólica"][0]+random.randint(10,25)
        pat_healthatts["Tension Arterial Diastólica"][0]=pat_healthatts["Tension Arterial Diastólica"][0]+random.randint(10,25)
        return super().proceed(name, treatment, patient, mongoclient)

    def update_health_attributes(self, patient):
        pat_healthatts=patient["health_attributes"]
        if patient["personaldata"]==default_values.PERSONAL_DATA.value:
            patient["personaldata"]
        pat_healthatts["Tension Arterial Sistólica"]=[random.randint(140,260), "mmHG"]
        pat_healthatts["Tension Arterial Diastólica"]=[random.randint(90,120), "mmHG"]
        if random.randint(1,2)==2:
            pat_healthatts["Urea"]=[random.randint(120,250), "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Creatinina"]=[random.randint(14,40)/10, "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Potasio"]=[random.randint(53,72)/10, "mEq/L"]
        if random.randint(1,2)==2:
            pat_healthatts["Trigliceridos"]=[random.randint(151,700)/10, "mg/dl"]

        return patient
    
    symptom_list=[symptoms.CEFALEA.value, symptoms.STOMACHACHES.value,
                  symptoms.ACCELERATED_BREATHING.value, symptoms.BREATHING_TROUBLES.value,
                  symptoms.DIZZYNESS.value, symptoms.CHESTPAINS.value]
    symptom_list_weights=[4,2,1,1,3,2]
    


    symptom_list_nums=[1,2]

    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(self.symptom_list_nums[0],self.symptom_list_nums[1])
        weights = np.array(self.symptom_list_weights)
        probabilities = weights / weights.sum()
        symptom_list_extended=np.random.choice(self.symptom_list,symtom_list_num,False,probabilities)
        symptom_list.extend(list(symptom_list_extended))
        return