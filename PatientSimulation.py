import simpy
import random
from illnesses import cancer
import FranMongoClient
import BroadcastPipe
import requests

RANDOM_SEED = 42
SIM_TIME = 100
TICK_TIME = 5
SCALE_FACTOR = 1


def patient(env, name, in_pipe, out_pipe, illnesses=None, treatment=None, id=0):
    if illnesses is None:
        illnesses = []
    if treatment is None:
        treatment = []
    input_operation = in_pipe.get()
    shouldRun = True
    while shouldRun:
        treatment = FranMongoClient.gettreatment(id)
        health = FranMongoClient.get_health(id)
        # print(treatment)
        changed = False

        print("Tick")
        for i in illnesses:
            status = None
            if i is not None:
                status = i.proceed(name, treatment, health)

            if status == "Heal 10":
                print("HEAL")
                FranMongoClient.updatehealth(id, -0.1)
                changed = True

            if status == "Damage 10":
                print("DAMAGE")
                FranMongoClient.updatehealth(id, 0.1)
                changed = True

            # if status.value == "Dead":
            #     shouldRun = False
            if status == "Cured":
                illnesses.remove(i)
                changed = True
        try:
            if input_operation[0] == "treatment":
                treatment = input_operation[1]

            elif input_operation[0] == "get_illnesses":
                out_pipe.put(illnesses)
        except TypeError:
            pass
        if illnesses == []:
            print("Yo, %s, No tengo nada!" % name)
            shouldRun = False
            changed = True
        if changed:
            requests.post("http://localhost:5000/api/v1/inner/updatesims", json={'id_patient': str(id)})
        yield env.timeout(TICK_TIME)


def setup(env, patients):
    broadcast = BroadcastPipe.BroadcastPipe(env)
    pipes = []
    pipes_out = []
    for idx, p in enumerate(patients):
        print(idx)
        pipes.append(broadcast.get_output_conn())
        pipes_out.append(broadcast.get_output_conn())
        try:
            env.process(patient(env, p[0], pipes[idx], pipes_out[idx], p[1], p[2], p[3]))
        except(IndexError):
            env.process(patient(env, p[0], pipes[idx], pipes_out[idx], p[1], p[3], p[4]))


def start_sim():
    random.seed()
    env = simpy.RealtimeEnvironment(0, SCALE_FACTOR, False)
    # test_patients = [["Juan", [malaria.Malaria(env, "Juan")]], ["Ana", [malaria.Malaria(env, "Ana")], "Correcto"],
    # ["Maria", [malaria.Malaria(env, "Maria")], "Incorrecto"],["Diego", [malaria.Malaria(env, "Diego")]],["Pepe",
    # [malaria.Malaria(env, "Pepe")]]]
    patients = FranMongoClient.import_clients_from_db(env)
    print(patients)
    setup(env, patients)
    #
    env.run()
