class Illness(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.startTime=env.now

    def proceed(self, name, treatment, hea):
        return ""

    def update_health_attributes(self, hea):
        return hea
