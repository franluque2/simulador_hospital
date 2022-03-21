from pymongo import MongoClient

import illnesses.malaria
from illnesses import base, coronavirus, malaria

client = MongoClient("localhost", 27017)

db = client.Hospital


def str_to_illness(env, illness, name):
    if illness == "Malaria":
        return illnesses.malaria.Malaria(env, name)
    if illness == "Coronavirus (Delta)":
        return illnesses.coronavirus.CoronavirusDelta(env, name)
    else:
        pass


def import_clients_from_db(env):
    rt = []
    patients = list(db.HospitalPatients.find({}))
    for p in patients:
        illnessesList = []
        for i in p['illnesses']:
            illnessesList.append(str_to_illness(env, i, p['name']))
            pass
        rt.append([p['name'], illnessesList, p['treatments']])

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


if __name__ == '__main__':
    # print(insert_client_in_db("Diego", "Malaria"))
    # delete_client_in_db_by_name("Pedro")
    # print(import_clients_from_db()

    pass
