from pymongo import MongoClient

import illnesses.malaria
from illnesses import base, coronavirus, malaria, cancer
from bson.objectid import ObjectId

client = MongoClient("localhost", 27017)

db = client.Hospital


def str_to_illness(env, illness, name):
    if illness == "Malaria":
        return illnesses.malaria.Malaria(env, name)
    if illness == "Coronavirus (Delta)":
        return illnesses.coronavirus.CoronavirusDelta(env, name)
    if illness == "cancer":
        return illnesses.cancer.Cancer(env, name)
    else:
        pass


def updatehealth(id, num):
    val = float(db.HospitalPatients.find_one({"_id": ObjectId(id)})["color"])
    print(val)
    print(num)
    if (val + num )> 1:
        val = 1
    elif (val + num )< 0:
        val = 0
    else:
        val = val + num
        print(val)
    db.HospitalPatients.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"color": val}})


def gettreatment(id):
    return db.HospitalPatients.find_one({"_id": ObjectId(id)})['treatments']


def get_health(id):
    return db.HospitalPatients.find_one({"_id": ObjectId(id)})['color']


def import_clients_from_db(env):
    rt = []
    patients = list(db.HospitalPatients.find({}))
    for p in patients:
        illnessesList = []
        # print(p['illnesses'])
        for i in p['illnesses']:
            # print(x)
            illnessesList.append(str_to_illness(env, i, p['name']))
            pass
        rt.append([p['name'], illnessesList, p['treatments'], p['_id']])

    return rt


def insert_client_in_db(name, illnesses=None, treatments=None):
    if illnesses is None:
        illnesses = []
    if treatments is None:
        treatments = []
    return db.HospitalPatients.insert_one({
        'name': name,
        'illnesses': illnesses,
        'treatments': treatments
    })


def delete_client_in_db(id):
    db.HospitalPatients.delete_many({'_id': id})


def delete_client_in_db_by_name(name):
    db.HospitalPatients.delete_many({'name': name})


def getUsers():
    return db.Accounts.find({})


def get_patient_by_id(id):
    return db.HospitalPatients.find_one({"_id": ObjectId(id)})

def determine(x,id):
    return ObjectId(id) not in x["patients"]

def get_users_by_assigned_patient(patientid):
    users = list(db.Accounts.find({}))
    users[:] = [x for x in users if not determine(x,patientid)]
    return users

def create_patient(patient, user_ids=None):
    patientid = db.HospitalPatients.insert_one(patient)
    if user_ids is not None:
        for u in user_ids:
            db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$push": {"patients": patientid.inserted_id}})


def assign_patient(patientid, userids):
    for patient in patientid:
        for u in userids:
            db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$push": {"patients": ObjectId(patient)}})


def unassign_patient(patientids, userids):
    for patient in patientids:
        for u in userids:
            db.Accounts.find_one_and_update({"_id": ObjectId(u)}, {"$pull": {"patients": ObjectId(patient)}})


def delete_patients(patientids):
    userids = db.Accounts.find({})
    if patientids is not None:
        for p in patientids:
            patient_to_delete = db.HospitalPatients.find_one({"_id": ObjectId(p)})
            if patient_to_delete is not None:
                for u in userids:
                    db.Accounts.find_one_and_update({"_id": u["_id"]},
                                                    {"$pull": {"patients": patient_to_delete["_id"]}})
                db.HospitalPatients.delete_one({"_id": patient_to_delete["_id"]})


def send_request(userid_sender, userid_receiver, patientids):
    receiver = db.Accounts.find_one({"_id": ObjectId(userid_receiver)})
    sender = db.Accounts.find_one({"_id": ObjectId(userid_sender)})

    if patientids is not None:
        if sender is not None:
            if receiver is not None:
                for p in patientids:
                    if p in receiver["patients"]:
                        if p["can_transfer"]:
                            db.Accounts.find_one_and_update({"_id": receiver["_id"]},
                                                            {"$push": {"pending_transfers": {"patient_id": p["_id"]},
                                                                       "sender_id": sender["_id"]}})

# def accept_requests(userid_receiver, patientids, accepting):
#     receiver = db.Accounts.find_one({"_id": ObjectId(userid_receiver)})
#     patients = []
#     for p in patientids:
#         temp=db.HospitalPatients.find_one({"_id": ObjectId(p)})
#         if temp:
#             patients.append(ObjectId(p))
#
#     if patients:
#         if receiver:
#             for p in patients:
#                 senderid=None
#                 senders=receiver["pending_transfer"]
#                 db.Accounts.find_one_and_update({"_id": receiver["_id"]},
#                                                 {"pull": {"pending_transfers": {"patient_id": p["_id"]}}})
#
#                 if accepting:
#                     db.Accounts.find_one_and_update
#                 else:


# def process_request(userid_sender, userid_receiver, patientids, status):



if __name__ == '__main__':
    # print(insert_client_in_db("Diego", "Malaria"))
    # delete_client_in_db_by_name("Pedro")
    # print(import_clients_from_db()
    print(get_users_by_assigned_patient("63507d66b84a3d48122fb8b1"))

    pass
