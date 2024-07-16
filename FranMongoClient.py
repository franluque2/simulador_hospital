from pymongo import MongoClient

import illnesses
from bson.objectid import ObjectId
import PatientSimulation
import PatientCreation

client = MongoClient("localhost", 27017)

db = client.hospital


class FranMongo:
    def updatehealth(self, id, num):
        val = float(db.HospitalPatients.find_one({"_id": ObjectId(id)})["color"])
        if (val + num) > 1:
            val = 1
        elif (val + num) < 0:
            val = 0
        else:
            val = val + num
        db.HospitalPatients.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"color": val}})


    def gettreatment(self, id):
        return db.HospitalPatients.find_one({"_id": ObjectId(id)})['treatments']


    def get_health(self,id):
        return db.HospitalPatients.find_one({"_id": ObjectId(id)})['color']


    def import_clients_from_db(self):
        rt = []
        patients = list(db.HospitalPatients.find({}))
        for p in patients:
            illnessesList = []
            # print(p['illnesses'])
            for i in p['illnesses']:
                # print(x)
                illnessesList.append(PatientCreation.str_to_illness(p['name']))
                pass
            rt.append([p['name'], illnessesList, p['treatments'], p['_id']])

        return rt


    def insert_client_in_db(self, name, illnesses=None, treatments=None):
        if illnesses is None:
            illnesses = []
        if treatments is None:
            treatments = []
        return db.HospitalPatients.insert_one({
            'name': name,
            'illnesses': illnesses,
            'treatments': treatments
        })


    def delete_client_in_db(self, id):
        db.HospitalPatients.delete_many({'_id': id})


    def delete_client_in_db_by_name(self, name):
        db.HospitalPatients.delete_many({'name': name})


    def getUsers(self):
        return db.Accounts.find({})


    def get_patient_by_id(self, id):
        return db.HospitalPatients.find_one({"_id": ObjectId(id)})


    def determine(self, x, id):
        return ObjectId(id) not in x["patients"]


    def get_users_by_assigned_patient(self, patientid):
        users = list(db.Accounts.find({}))
        users[:] = [x for x in users if not self.determine(x, patientid)]
        return users


    def create_patient(self, patient, user_ids=None):
        patientid = db.HospitalPatients.insert_one(patient)
        if user_ids is not None:
            for u in user_ids:
                db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$push": {"patients": patientid.inserted_id}})
                PatientSimulation.add_patient_sim(PatientSimulation.patient_executor(patient["name"], patient["illnesses"], patient["treatments"], patientid.inserted_id, self))



    def assign_patient(self, patientid, userids):
        for patient in patientid:
            for u in userids:
                db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$push": {"patients": ObjectId(patient)}})


    def unassign_patient(self, patientids, userids):
        for patient in patientids:
            for u in userids:
                db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$pull": {"patients": ObjectId(patient)}})


    def delete_patients(self, patientids):
        userids = db.Accounts.find({})
        if patientids is not None:
            for p in patientids:
                patient_to_delete = db.HospitalPatients.find_one({"_id": ObjectId(p)})
                if patient_to_delete is not None:
                    for u in userids:
                        db.Accounts.find_one_and_update({"_id": u["_id"]},
                                                        {"$pull": {"patients": patient_to_delete["_id"]}})
                    db.HospitalPatients.delete_one({"_id": patient_to_delete["_id"]})


    def send_request(self, userid_sender, userid_receiver, patientids):
        receiver = db.Accounts.find_one({"_id": ObjectId(userid_receiver[0])})
        sender = db.Accounts.find_one({"_id": ObjectId(userid_sender)})

        if patientids is not None:
            if sender is not None:
                if receiver is not None:
                    print(patientids)
                    p = ObjectId(patientids)
                    db.Accounts.find_one_and_update({"_id": receiver["_id"]},
                                                    {"$push": {"pending_transfers": {"patient_id": p,
                                                            "sender_id": sender["_id"]}}})
                    db.HospitalPatients.find_one_and_update({"_id": p},
                                                            {"$set": {"can_transfer": False}})
                    patient = db.HospitalPatients.find_one({"_id": p})
                    notification_string = sender["name"] + " esta queriendo transferirte a un paciente: " + patient[
                        "name"] + " , ve a Transferir Pacientes para Aceptar o Denegar la derivación."
                    self.send_notification(str(receiver["_id"]), notification_string)


    def process_request(self, userid_receiver, userid_sender, patientids, accepting):
        receiver = db.Accounts.find_one({"_id": ObjectId(userid_receiver)})
        patients = []
        temp = db.HospitalPatients.find_one({"_id": (ObjectId(patientids["$oid"]))})
        if temp:
            patients.append((temp))
        if patients:
            if receiver:
                for p in patients:
                    senderid = None
                    senders = receiver["pending_transfers"]
                    db.Accounts.find_one_and_update({"_id": receiver["_id"]},
                                                    {"$pull": {"pending_transfers": {"patient_id": p["_id"]}}})
                    db.HospitalPatients.find_one_and_update({"_id": p["_id"]},
                                                            {"$set": {"can_transfer": True}})
                    if accepting:
                        db.Accounts.find_one_and_update({"_id": ObjectId(userid_sender["$oid"])}, {"$pull": {"patients": p["_id"]}})
                        db.Accounts.find_one_and_update({"_id": receiver["_id"]}, {"$push": {"patients": p["_id"]}})

                    else:
                        pass


    def send_notification(self, userid, notification):
        db.Accounts.find_one_and_update({"_id": ObjectId(userid)}, {"$push": {"notifications": notification}})


    def delete_notification(self, userid, notification):
        db.Accounts.find_one_and_update({"_id": ObjectId(userid)}, {"$pull": {"notifications": notification}})


if __name__ == '__main__':
    # print(insert_client_in_db("Diego", "Malaria"))
    # delete_client_in_db_by_name("Pedro")
    # print(import_clients_from_db()
    pass
