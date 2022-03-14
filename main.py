# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import simpy
import random

RANDOM_SEED = 42
SIM_TIME = 60
TICK_TIME_MALARIA = 5


class BroadcastPipe(object):
    """A Broadcast pipe that allows one process to send messages to many.

    This construct is useful when message consumers are running at
    different rates than message generators and provides an event
    buffering to the consuming processes.

    The parameters are used to create a new
    :class:`~simpy.resources.store.Store` instance each time
    :meth:`get_output_conn()` is called.

    """

    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def put(self, value):
        """Broadcast a *value* to all receivers."""
        if not self.pipes:
            raise RuntimeError('There are no output pipes.')
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)  # Condition event for all "events"

    def get_output_conn(self):
        """Get a new output connection for this broadcast pipe.

        The return value is a :class:`~simpy.resources.store.Store`.

        """
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe


def patient(env, name, in_pipe, out_pipe, illnesses=[], treatment=None):
    input = in_pipe.get()
    shouldRun = True
    ill_pipe=simpy.Store(env)
    while shouldRun:
        for i in illnesses:
            i.proceed(name, treatment, ill_pipe)
            status=ill_pipe.get()
            if status.value == "Dead":
                shouldRun = False
                print("Yo, %s , mori!" % name)
            elif status.value == "Cured":
                illnesses.remove(i)
        try:
            if input[0] == "treatment":
                treatment = input[1]

            elif input[0] == "get_illnesses":
                out_pipe.put(illnesses)
        except TypeError:
            pass
        if(illnesses==[]):
            print("Yo, %s, No tengo nada!" % name)
            shouldRun=False
        yield env.timeout(TICK_TIME_MALARIA)

class Illness(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name

    def proceed(self, name, treatment, ill_pipe):
        return None


class Malaria(Illness):
    def __init__(self, env, name):
        super().__init__(env, name)

    def proceed(self, name, treatment, ill_pipe):
        if treatment == "Correcto":
            rand = random.randint(0, 10)
            if (rand < 3):
                print("Yo, %s, me mantuve igual a las %d." % (name,self.env.now))
                ill_pipe.put(None)
                return
            else:
                print("Yo, %s, me cure de malaria a las %d!" % (name,self.env.now))
                ill_pipe.put("Cured")
                return
        else:
            rand = random.randint(0, 10)
            if (rand < 2):
                print("Yo, %s, mori a las %d!" % (name,self.env.now))
                ill_pipe.put("Dead")
                return
            elif (rand < 8):
                print("Yo, %s, me mantuve igual a las %d." % (name,self.env.now))
                ill_pipe.put(None)
                return
            else:
                print("Yo, %s, me cure de malaria a las %d!" % (name,self.env.now))
                ill_pipe.put("Cured")
                return


def setup(env, patients):
    pipe = simpy.Store(env)
    pipe_out = simpy.Store(env)
    for p in patients:
        try:
            env.process(patient(env, p[0], pipe, pipe_out, p[1], p[2]))
        except(IndexError):
            env.process(patient(env, p[0], pipe, pipe_out, p[1]))


if __name__ == '__main__':
    #random.seed(RANDOM_SEED)
    env = simpy.Environment()
    test_patients = [["Juan", [Malaria(env, "Juan")]], ["Ana", [Malaria(env, "Ana")], "Correcto"]]
    setup(env, test_patients)
    env.run(until=SIM_TIME)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
