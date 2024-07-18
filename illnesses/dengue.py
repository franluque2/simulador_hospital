from illnesses import base, statuses
import random
import sys
import os
import FranMongoClient

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '..'))

from default_values import default_values, symptoms

class dengue(base.Illness):
    def __init__(self):
        super().__init__()
        self.name="Dengue"
    

    def proceed(self, name, treatment, patient, mongoclient) -> list[statuses.Status, bool, object]:
            if patient["total_ticks"]<5:
                return statuses.Status.CONTINUE, False, patient
            pat_healthatts=patient["health_attributes"]

            if statuses.treatments.IBUPROFENO in treatment:
                pat_healthatts["Plaquetas"]=pat_healthatts["Plaquetas"]-random.randint(5,15)
                if pat_healthatts["Plaquetas"]<150000:
                    patient["color"]=0
                    patient["summary"]="Plaquetopenia"
                    return statuses.Status.DEAD, True, patient
            
            if statuses.treatments.ASPIRINA in treatment:
                pat_healthatts["Plaquetas"]=pat_healthatts["Plaquetas"]-random.randint(5,15)
                if pat_healthatts["Plaquetas"]<150000:
                    patient["color"]=0
                    patient["summary"]="Plaquetopenia"
                    return statuses.Status.DEAD, True, patient
                
            if (statuses.treatments.PARACETAMOL in treatment) and (statuses.treatments.HIDRATACION in treatment):
                pat_healthatts["Globulos Blancos"][0]=pat_healthatts["Globulos Blancos"][0]+((10000-pat_healthatts["Globulos Blancos"][0]/2))
                pat_healthatts["Plaquetas"][0]=pat_healthatts["Plaquetas"][0]+(450000-pat_healthatts["Plaquetas"][0]/2)
                
                if (450000-pat_healthatts["Plaquetas"][0]<50000):
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
        pat_healthatts["Tension Arterial Sistólica"]=[random.randint(110,240), "mmHG"]
        pat_healthatts["Tension Arterial Diastólica"]=[random.randint(70,110), "mmHG"]
        if random.randint(1,2)==2:
            pat_healthatts["Urea"]=[random.randint(6,120), "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Creatinina"]=[random.randint(6,40)/10, "mg/dL"]
        if random.randint(1,2)==2:
            pat_healthatts["Plaquetas"]=[random.randint(2,149000)/, "plaquetas/mm3"]
        if random.randint(1,2)==2:
            pat_healthatts["Globulos blancos"]=[random.randint(2,4500)/10, "leucocitos/mm3"]

        return patient
        
    symptom_list=[symptoms.CEFALEA.value, symptoms.STOMACHACHES.value,
                symptoms.ACCELERATED_BREATHING.value, symptoms.FEVER.value, 
                symptoms.CUTANEOUS_ERUPTIONS.value, symptoms.NASAL_HEMORRAGING.value, symptoms.EYE_PAIN.value, symptoms.MUSCLE_PAIN.value]
    symptom_list_weights=[4,2,1,4,3,2,4,4]
    


    symptom_list_nums=[1,2]

    def generate_symptoms(self, patient):
        symptom_list=patient["symptoms"]
        symtom_list_num=random.randint(self.symptom_list_nums[0],self.symptom_list_nums[1])
        weights = np.array(self.symptom_list_weights)
        probabilities = weights / weights.sum()
        symptom_list_extended=np.random.choice(self.symptom_list,symtom_list_num,False,probabilities)
        symptom_list.extend(list(symptom_list_extended))
        return