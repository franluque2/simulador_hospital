from illnesses.statuses import treatments

from fuzzysearch import find_near_matches

def parse_treatment_string(string: str)-> list[treatments]:
    returnlist = []

    for treatment in treatments:
        if find_near_matches(treatment.value.lower(), string.lower(), max_l_dist=2)!=[]:
            returnlist.append(treatment.name)
    
    return returnlist