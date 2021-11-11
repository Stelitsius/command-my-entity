import json

voice_actions = {}


def load_voice_actions_application():
    global voice_actions
    action_voices = json.load(open("action_voices_application.json"))
    # derive voice_actions dictionary from action_voices_application json
    for action in action_voices:
        for voice in action_voices[action]:
            voice_actions[voice] = action


load_voice_actions_application()
