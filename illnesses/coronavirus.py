from illnesses import base
import random


class CoronavirusDelta(base.Illness):
    def proceed(self, name, treatment, ill_pipe):
        rand = random.randint(0, 10)
        if self.env.now - self.startTime <= 5:
            if "Respirador" in treatment:
                if rand<8:
                    print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                    ill_pipe.put(None)
                    return
                else:
                    print("Yo, %s, me cure de Coronavirus (Delta) a las %d!" % (name, self.env.now))
                    ill_pipe.put("Cured")
                    return
            else:
                print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                ill_pipe.put(None)
                return
                pass
        elif self.env.now - self.startTime <= 10:
            if "Respirador" in treatment:
                print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                ill_pipe.put(None)
                return
                pass
            else:
                print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                ill_pipe.put(None)
                return
                pass
