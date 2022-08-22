from illnesses import base
import random


class Cancer(base.Illness):
    def proceed(self, name, treatment, ill_pipe):
        rand = random.randint(0, 10)
        if self.env.now - self.startTime <= 5:
            if "Correcto" in treatment:
                if rand<8:
                    ill_pipe.put(None)
                    return
                else:
                    ill_pipe.put("Heal 10")
                    return
            elif "Incorrecto" in treatment:
                if rand>8:
                    ill_pipe.put(None)
                    return
                else:
                    ill_pipe.put("Damage 10")
                    return
            else:
                ill_pipe.put(None)
                return
                pass
        elif self.env.now - self.startTime <= 10:
            if "Correcto" in treatment:
                ill_pipe.put(None)
                return
                pass
            else:
                ill_pipe.put(None)
                return
                pass
