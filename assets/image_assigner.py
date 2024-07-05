import os, random

IMAGES_PATH = "D:/Tesis/hospital-web/public/patient_images"
WEBSITE_PATH="patient_images"

def assign_image(patient):
    if patient["sex"] == "M":
        if int(patient["age"]) > 50:
            patient["src"] = WEBSITE_PATH + "/male/old/"+random.choice(os.listdir(IMAGES_PATH + "/male/old"))
        else:
            patient["src"] = WEBSITE_PATH + "/male/young_adult/"+random.choice(os.listdir(IMAGES_PATH + "/male/young_adult"))
    else:
        if int(patient["age"]) > 50:
            patient["src"] = WEBSITE_PATH + "/female/old/"+random.choice(os.listdir(IMAGES_PATH + "/female/old"))
        else:
            patient["src"] = WEBSITE_PATH + "/female/young_adult/"+random.choice(os.listdir(IMAGES_PATH + "/female/young_adult"))
