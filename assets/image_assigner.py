import os, random

IMAGES_PATH = "/home/fran/WebstormProjects/Hospital-web/my-app/hospital-prueba/public/patient_images"
WEBSITE_PATH="patient_images"

def assign_image(patient):
    if patient["sex"] == "M":
        if patient["age"] > 50:
            patient["src"] = WEBSITE_PATH + "/male/old/"+random.choice(os.listdir(IMAGES_PATH + "/male/old"))
        else:
            patient["src"] = WEBSITE_PATH + "/male/young_adult/"+random.choice(os.listdir(IMAGES_PATH + "/male/young_adult"))
    else:
        if patient["age"] > 50:
            patient["src"] = WEBSITE_PATH + "/female/old/"+random.choice(os.listdir(IMAGES_PATH + "/female/old"))
        else:
            patient["src"] = WEBSITE_PATH + "/female/young_adult/"+random.choice(os.listdir(IMAGES_PATH + "/female/young_adult"))
