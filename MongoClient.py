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
    db.HospitalPatients.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"health": num}})

def gettreatment(id):
    return db.HospitalPatients.find_one({"_id": ObjectId(id)})['treatments']

def import_clients_from_db(env):
    rt = []
    patients = list(db.HospitalPatients.find({}))
    for p in patients:
        illnessesList = []
        # print(p['illnesses'])
        for i in p['illnesses']:
            # print(x)
            illnessesList.append(str_to_illness(env, p['illnesses'][i]['type'], p['name']))
            pass
        rt.append([p['name'], illnessesList, p['treatments'], p['health'], p['_id']])

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


if __name__ == '__main__':
    # print(insert_client_in_db("Diego", "Malaria"))
    # delete_client_in_db_by_name("Pedro")
    # print(import_clients_from_db()

    pass
