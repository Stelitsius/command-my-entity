import json

global entities_sum


def load_jsons():

    # dictionary with all entities sum initialized to 0
    global entities_sum
    entities_sum = json.load(open("entities.json"))



