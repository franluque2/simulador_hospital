from illnesses import base
import random


class Malaria(base.Illness):
    def proceed(self, name, treatment, ill_pipe):
        if treatment == "Correcto":
            rand = random.randint(0, 10)
            if rand < 3:
                print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                ill_pipe.put(None)
                return
            else:
                print("Yo, %s, me cure de malaria a las %d!" % (name, self.env.now))
                ill_pipe.put("Cured")
                return
        else:
            rand = random.randint(0, 10)
            if rand < 2:
                print("Yo, %s, mori a las %d de Malaria!" % (name, self.env.now))
                ill_pipe.put("Dead")
                return
            elif rand < 8:
                print("Yo, %s, me mantuve igual a las %d." % (name, self.env.now))
                ill_pipe.put(None)
                return
            else:
                print("Yo, %s, me cure de malaria a las %d!" % (name, self.env.now))
                ill_pipe.put("Cured")
                return
