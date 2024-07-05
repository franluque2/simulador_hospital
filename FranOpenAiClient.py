from secret_keys import OPEN_AI_KEY
from openai import OpenAI
from illnesses import base

client=OpenAI(
    api_key=OPEN_AI_KEY
)


def generate_clinical_interview(patient, illness: base, symptoms_list: list) -> str:
    interviewreturn=client.chat.completions.create(model="gpt-3.5-turbo", messages=[
    {"role": "system", "content": f"Eres un paciente clinico simulado, {patient["sex"]}, siando admitido a un hospital, tienes {patient["age"]} años de edad,\
     estas de momento sufriendo de {illness.name}, tienes el conocimiento promedio de alguien de tu edad, pero no sabes que tienes. "},
    {"role": "user", "content": f"Da una simple entrevista que darias a un doctor sobre los síntomas que estas padeciendo, siendo estos: {symptoms_list}. Habla solo monologando como un paciente que esta por hablarle al doctor, empezando asi: Hola Doctor/a, pues el alumno a partir de ello debe diagnosticarte."}
  ])
    print(interviewreturn.choices[0].message.content)
    return interviewreturn.choices[0].message.content