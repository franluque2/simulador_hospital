import random
import illnesses
import FranMongoClient
import requests
from illnesses.statuses import Status
import threading
import time
import PatientCreation

RANDOM_SEED = 42
TICK_TIME = 3
SCALE_FACTOR = 1


class patient_executor:

    def __init__(self, pname: str, illnesses=None, treatment=None, id=0, mongoclient=FranMongoClient):
        self.pname = pname
        self.illnesses=illnesses
        self.treatment=treatment
        self.id=id
        self.mongoclient=mongoclient

    def run(self):
        if self.illnesses is None:
            self.illnesses = []
        if self.treatment is None:
            self.treatment = []
        patient=self.mongoclient.get_patient_by_id(self.id)
        shouldRun = patient["should_update"]
        tick_modifier=self.mongoclient.get_tick_time(self.id)
        print(f"Started Thread {self.pname}!")
        while shouldRun:
            patient=self.mongoclient.get_patient_by_id(self.id)
            self.treatment = self.mongoclient.gettreatment(self.id)
            health = self.mongoclient.get_health(self.id)
            # print(treatment)
            changed = False

            for i in self.illnesses:
                status = None
                if i is not None:
                    status, changed, patient = PatientCreation.str_to_illness(i).proceed(self.pname, self.treatment, patient, self.mongoclient)
                if status == Status.DEAD:
                    shouldRun = False
                    requests.post("http://localhost:5000/api/v1/inner/senddangernotification", json={'id_patient': str(self.id)})
                if status == Status.CURED:
                    self.illnesses.remove(i)
                    changed = True
                    requests.post("http://localhost:5000/api/v1/inner/senddangernotification", json={'id_patient': str(self.id)})

                if status ==Status.IMPORTANT_CHANGE:
                    requests.post("http://localhost:5000/api/v1/inner/senddangernotification", json={'id_patient': str(self.id)})

            if self.illnesses == []:
                shouldRun = False
                changed = True
            if changed:
                requests.post("http://localhost:5000/api/v1/inner/updatesims", json={'id_patient': str(self.id)})
            patient["should_update"]=shouldRun
            self.mongoclient.update_patient(self.id,patient)
            self.mongoclient.increasetotalticks(self.id)
            shouldRun = patient["should_update"]
            time.sleep(TICK_TIME*tick_modifier)


def setup(patients: list, mongoclient: FranMongoClient) -> list:
    plist=[]
    for idx, p in enumerate(patients):
        plist.append(patient_executor(p[0], p[1], p[2], p[3], mongoclient))
    return plist

def add_patient_sim(patient: patient_executor, mongoclient: FranMongoClient):
    thread=threading.Thread(target=patient.run)
    thread.start()

def start_sim():
    random.seed()
    mongoclient=FranMongoClient.FranMongo()
    patients = mongoclient.import_clients_from_db()
    plist=setup(patients, FranMongoClient.FranMongo())
    for p in plist:
        thread=threading.Thread(target=p.run)
        thread.start()