from illnesses import base
import random


class Cancer(base.Illness):
    def proceed(self, name, treatment):
        rand = random.randint(0, 10)
        if self.env.now - self.startTime <= 5:
            if "Correcto" in treatment:
                if rand<8:
                    return None
                else:

                    return "Heal 10"
            elif "Incorrecto" in treatment:
                if rand>8:

                    return None
                else:
                    return "Damage 10"
            else:
                return None
                pass
        elif self.env.now - self.startTime <= 10:
            if "Correcto" in treatment:
                return None
                pass
            else:
                return None
                pass
