import random
import illnesses
import FranMongoClient
import requests
from illnesses.statuses import Status
import threading
import time


RANDOM_SEED = 42
TICK_TIME = 5
SCALE_FACTOR = 1


class patient_executor:

    def __init__(self, pname: str, illnesses=None, treatment=None, id=0, mongoclient=FranMongoClient):
        self.pname = pname
        self.illnesses=illnesses
        self.treatment=treatment
        self.id=id
        self.mongoclient=mongoclient

    def run(self):
        if illnesses is None:
            illnesses = []
        if treatment is None:
            treatment = []
        shouldRun = True
        while shouldRun:
            treatment = self.mongoclient.gettreatment(id)
            health = self.mongoclient.get_health(id)
            # print(treatment)
            changed = False

            for i in illnesses:
                status = None
                if i is not None:
                    status, changed = i.proceed(self.pname, treatment, health, self.mongoclient)
                if status.value == Status.DEAD:
                    shouldRun = False
                if status == Status.CURED:
                    illnesses.remove(i)
                    changed = True
            if illnesses == []:
                shouldRun = False
                changed = True
            if changed:
                requests.post("http://localhost:5000/api/v1/inner/updatesims", json={'id_patient': str(id)})
            time.sleep(TICK_TIME)


def setup(patients: list, mongoclient: FranMongoClient) -> list:
    plist=[]
    for idx, p in enumerate(patients):
        plist.append(patient_executor(p[0], p[1], p[2], p[3], mongoclient))

def add_patient_sim(patient: patient_executor, mongoclient: FranMongoClient):
    thread=threading.Thread(target=patient.run())
    thread.start()

def start_sim():
    random.seed()
    mongoclient=FranMongoClient.FranMongo()
    patients = mongoclient.import_clients_from_db()
    plist=setup(patients, FranMongoClient.MongoClient())
    threadlist=[]
    for p in plist:
        thread=threading.Thread(target=p.run())
        threadlist.append(thread)
    for thread in threadlist:
        thread.start()
