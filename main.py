import simpy
import random
from illnesses import malaria
import BroadcastPipe

RANDOM_SEED = 42
SIM_TIME = 10
TICK_TIME = 1
SCALE_FACTOR=0.001


def patient(env, name, in_pipe, out_pipe, illnesses=None, treatment=None):
    if illnesses is None:
        illnesses = []
    input = in_pipe.get()
    shouldRun = True
    ill_pipe = simpy.Store(env)
    while shouldRun:
        for i in illnesses:
            i.proceed(name, treatment, ill_pipe)
            status = ill_pipe.get()
            if status.value == "Dead":
                shouldRun = False
            elif status.value == "Cured":
                illnesses.remove(i)
        try:
            if input[0] == "treatment":
                treatment = input[1]

            elif input[0] == "get_illnesses":
                out_pipe.put(illnesses)
        except TypeError:
            pass
        if (illnesses == []):
            print("Yo, %s, No tengo nada!" % name)
            shouldRun = False
        yield env.timeout(TICK_TIME)


def setup(env, patients):
    pipe = simpy.Store(env)
    pipe_out = simpy.Store(env)
    for p in patients:
        try:
            env.process(patient(env, p[0], pipe, pipe_out, p[1], p[2]))
        except(IndexError):
            env.process(patient(env, p[0], pipe, pipe_out, p[1]))


if __name__ == '__main__':
    random.seed()
    env = simpy.RealtimeEnvironment(0, SCALE_FACTOR, False)
    test_patients = [["Juan", [malaria.Malaria(env, "Juan")]], ["Ana", [malaria.Malaria(env, "Ana")], "Correcto"]]
    setup(env, test_patients)
    env.run(until=SIM_TIME)
