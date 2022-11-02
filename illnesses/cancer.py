from illnesses import base
import random


class Cancer(base.Illness):
    def proceed(self, name, treatment, hea):
        rand = random.randint(0, 10)
        if self.env.now - self.startTime <= 5:
            if "Correcto" in treatment:
                if rand < 8:
                    return None
                else:

                    return "Heal 10"
            elif "Incorrecto" in treatment:
                if rand > 8:
                    return None
                else:
                    return "Damage 10"
            else:
                return None
                pass
        elif self.env.now - self.startTime <= 1000:
            if "Correcto" in treatment:
                return "Heal 10"
                pass
            else:
                return "Damage 10"
                pass

    def update_health_attributes(self, hea):
        hea["health-attributes"]["blood_sugar"] *= 1.2
