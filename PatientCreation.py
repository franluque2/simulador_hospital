import FranMongoClient
import requests
import random
import illnesses
from assets import female_names, male_names, last_names, image_assigner
import PatientSimulation
from enum import Enum

class default_values(Enum):
    PERSONAL_DATA="No Hay Datos Personales Relevantes"
    FAMILY_DATA_FATHER="No hay precedentes importantes del lado paternal"
    FAMILY_DATA_MOTHER="No hay precedentes importantes del lado maternal"
    PHYS_EVAL="Parece estar en buen estado Fisico"


def generate_rand_name(sex):
    if sex == "M":
        return random.choice(male_names.male_names) + " " + random.choice(last_names.last_names)
    if sex == "F":
        return random.choice(female_names.female_names) + " " + random.choice(last_names.last_names)
    return "ERROR IN NAME GENERATION"


def str_to_illness(illness, name):  # TODO: REEMPLAZAR POR UNA FUNCION DE VERDAD
    if illness == "cancer":
        return illnesses.cancer.Cancer(None, name)
    else:
        pass


def generate_patient(args=None):
    if args is None:
        args = {}
    patient = {}
    if "sex" in args and args["sex"] is not None:
        patient["sex"] = args["sex"]
    else:
        patient["sex"] = ["M", "F"][random.randint(0, 1)]

    if "name" in args and args["name"] is not None:
        patient["name"] = args["name"]
    else:
        patient["name"] = generate_rand_name(patient["sex"])

    if "age" in args and args["age"] is not None:
        patient["age"] = args["age"]
    else:
        patient["age"] = random.randint(25, 80)

    if "src" in args and args["src"] is not None:
        patient["src"] = args["src"]
    else:
        image_assigner.assign_image(patient)

    if "personaldata" in args and args["personaldata"] is not None:
        patient["personaldata"] = args["personaldata"]
    else:
        patient["personaldata"] = default_values.PERSONAL_DATA

    if "familydata" in args and args["familydata"] is not None:
        patient["familydata"] = args["familydata"]
    else:
        patient["familydata"] = {
            "father": default_values.FAMILY_DATA_FATHER,
            "mother": default_values.FAMILY_DATA_MOTHER
        }  # TODO: GENERAR DATOS FAMILIARES

    if "physeval" in args and args["physeval"] is not None:
        patient["physeval"] = args["physeval"]
    else:
        patient["physeval"] = default_values.PHYS_EVAL  # TODO: GENERAR PHYSEVAL

    if "labs" in args and args["labs"] is not None:
        patient["labs"] = args["labs"]
    else:
        patient["labs"] = {}  # TODO: PREGENERAR ESTUDIOS

    if "treatments" in args and args["treatments"] is not None:
        patient["treatments"] = args["treatments"]
    else:
        patient["treatments"] = ""

    if "risk_factors" in args and args["risk_factors"] is not None:
        patient["risk_factors"] = args["risk_factors"]
    else:
        patient["risk_factors"] = "No posee Factores de Riesgo"  # TODO: GENERAR FACTORES DE RIESGO

    if "motive" in args and args["motive"] is not None:
        patient["motive"] = args["motive"]
    else:
        patient["motive"] = "Chequeo Medico"  # TODO: GENERAR MOTIVO

    if "interviews" in args and args["interviews"] is not None:
        patient["interviews"] = args["interviews"]
    else:
        patient["interviews"] = {}  # TODO: GENERAR ENTREVISTAS

    if "illnesses" in args and args["illnesses"] is not None:
        patient["illnesses"] = []
        for i in range(len(args["illnesses"])):
            patient["illnesses"][i] = (str_to_illness(args["illnesses"][i], patient["name"]))
    else:
        patient["illnesses"] = ["cancer"]  # TODO: GENERAR PATOLOGIAS

    if "health_attributes" in args and args["health_attributes"] is not None:
        patient["health_attributes"] = args["health_attributes"]
    else:
        patient["health_attributes"] = {
            "Celulas Rojas": {[random.randint(4500, 5900), random.randint(3200, 5130)][patient["sex"] == "M"], ""},
            "Celulas Blancas": {random.randint(3400, 9600), ""},
            "Plaquetas": {[random.randint(137, 317), random.randint(157, 371)][patient["sex"] == "M"], ""},
            "Hemoglobina": {[random.randint(132, 166), random.randint(116, 150)][patient["sex"] == "M"], ""},
            "Glucosa": {random.randint(70, 100), ""},
            "Creatina": {random.randint(6, 13), ""},
            "Colesterol Total": {random.randint(120, 200), ""},
            "Colesterol HDL": {random.randint(42, 90), ""},
            "Colesterol LDL": {random.randint(100, 160), ""},
            "Trifliceridos": {[random.randint(30, 280), random.randint(30, 220)][patient["sex"] == "M"], ""},
            "Sodio": {random.randint(135, 145), ""},
            "Potasio": {random.randint(37, 52), ""},
            "Clorina": {random.randint(96, 106), ""},
            "Calcio": {random.randint(85, 105), ""},
            "Ácido Úrico": {random.randint(35, 72), ""},
            "Urea": {random.randint(60, 200), ""},
            "Bilirubina": {random.randint(3, 19, "")},
            "Tension Arterial Sistólica": {random.randint(90,139),"mmHg"},
            "Tension Arterial Diastólica": {random.randint(60,89),"mmHg"},
            "Leucocitos": {random.randint(4500,11000), "/mm3"},
            "Recuento de Plaquetas": {random.randint(150000,400000), "/mm3"},
            "Albúmina en Sangre": {random.randint(34,54)/10, "g/dL"},
            "Hematocrito": {[random.randint(407, 503)/10, random.randint(361, 443)/10][patient["sex"] == "M"], "%"}
        }

    if "color" in args and (args["color"] is not None) and args["color"] != "1":
        patient["color"] = args["color"]
    else:
        patient["color"] = random.random()
    if "can_transfer" in args and args["can_transfer"] is not None:
        patient["can_transfer"] = args["can_transfer"]
    else:
        patient["can_transfer"] = True

    if "should_update" in args and args["should_update"] is not None:
        patient["should_update"] = args["should_update"]
    else:
        patient["should_update"] = False

    if "illnesses" in args and args["illnesses"] is not None:
        for i in patient["illnesses"]:
            i.update_health_attributes(patient)

    if "summary" in args and args["summary"] is not None:
        patient["summary"] = args["summary"]
    else:
        patient["summary"] = "No hay Cambios Recientes"  # TODO: GENERAR RESUMEN

    patient["logs"] = {}
    patient["unparsed_treatment"]=""

    if "user_ids" in args and args["user_ids"] is not None:
        FranMongoClient.FranMongo().create_patient(patient, args["user_ids"])
    else:
        FranMongoClient.FranMongo().create_patient(patient)


if __name__ == '__main__':
    # print(insert_client_in_db("Diego", "Malaria"))
    # delete_client_in_db_by_name("Pedro")
    # print(import_clients_from_db()
    generate_patient()
    pass
