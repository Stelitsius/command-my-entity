import json


def display_application_actions():
    print("Available application actions: = = = = =")
    actions = json.load(open("action_voices_app(no_entity).json"))
    for action in actions:
        print(action)
    print(" = = = = = = = = = = = = = = = = = = = =")
