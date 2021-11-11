from functions import *
from speech import listen_and_process_mic
import actions_eve
import json

voice_actions = {}


def load_voice_actions(target):
    global voice_actions
    if target == "application":
        action_voices = json.load(open("action_voices_application.json"))
    elif target == "eve":
        action_voices = json.load(open("action_voices_eve.json"))
    else:
        return

    # derive voice_actions dictionary from action_voices_<source> json
    for action in action_voices:
        for voice in action_voices[action]:
            voice_actions[voice] = action


def get_application_action(word_split):
    #   If the interpretation of word_split is successful, get_application_action
    #   will return one of the application actions: ('start listening', 'stop listening', 'quit')
    #   If word_split is not successfully interpreted, get_application_action will return False
    global voice_actions
    word_count = len(word_split)
    # voice_actions = json.load(open("voice-actions-application_OLD.json"))
    if word_count > 2:
        return False
    elif word_count == 1:
        try:
            return voice_actions[word_split[0]]
        except KeyError:
            return False
    elif word_count == 2:
        try:
            return voice_actions[word_split[0] + " " + word_split[1]]
        except KeyError:
            return False


def get_game_action_entity(word_split):
    #   If the interpretation of word_split is successful, get_game_action_entity
    #   will be a list of two items [A, E]:
    #   A: is the action to take
    #   E: is the entity to perform the action upon
    #   word_split can contain >=2 and <= 6 words
    #   Successful interpretation means that both A and I will be found in their respective dictionaries:
    #   A, inside voice_actions and E, inside screen_all_entities
    #   If word_split is not successfully interpreted, get_game_action_entity will return False
    global voice_actions
    word_count = len(word_split)
    # voice_actions = json.load(open("voice-actions-eve_OLD.json"))

    if word_count < 2 or word_count > 6:
        return False
    elif word_count == 2:
        try:  # find 1st word in the actions dictionary, 2nd word in the screen entities dictionary
            return [voice_actions[word_split[0]],
                    ScreenScanner.screen_all_entities[word_split[1]]]
        except KeyError:
            pass
        try:
            return [voice_actions[word_split[0] + " " + word_split[1]], None]
        except KeyError:
            return False
    elif word_count == 3:
        try:  # find 1st word in the actions dictionary, 2nd+3rd word in the screen entities dictionary

            return [voice_actions[word_split[0]],
                    ScreenScanner.screen_all_entities[word_split[1] + " " + word_split[2]]]
        except KeyError:
            pass
        try:  # find 1st+2nd word in the actions dictionary, 3rd word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1]],
                    ScreenScanner.screen_all_entities[word_split[2]]]
        except KeyError:
            return False
    elif word_count == 4:
        try:  # find 1st word in the actions dictionary, 2nd+3rd + 4th word in the screen entities dictionary
            return [voice_actions[word_split[0]],
                    ScreenScanner.screen_all_entities[word_split[1] + " " + word_split[2] + " " + word_split[3]]]
        except KeyError:
            pass
        try:  # find 1st+2nd word in the actions dictionary, 3rd+4th word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1]],
                    ScreenScanner.screen_all_entities[word_split[2] + " " + word_split[3]]]
        except KeyError:
            pass
        try:  # find 1st+2nd+3rd word in the actions dictionary, 4th word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1] + " " + word_split[2]],
                    ScreenScanner.screen_all_entities[word_split[3]]]
        except KeyError:
            return False
    elif word_count == 5:
        try:  # find 1st+2nd word in the actions dictionary, 3rd+4th+5th word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1]],
                    ScreenScanner.screen_all_entities[word_split[2] + " " + word_split[3] + " " + word_split[4]]]
        except KeyError:
            pass
        try:  # find 1st+2nd+3rd word in the actions dictionary, 4th+5th word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1] + " " + word_split[2]],
                    ScreenScanner.screen_all_entities[word_split[3] + " " + word_split[4]]]
        except KeyError:
            return False
    elif word_count == 6:
        try:  # find 1st+2nd+3rd word in the actions dictionary, 4th+5th+6th word in the screen entities dictionary
            return [voice_actions[word_split[0] + " " + word_split[1] + " " + word_split[2]],
                    ScreenScanner.screen_all_entities[word_split[3] + " " + word_split[4] + " " + word_split[5]]]
        except KeyError:
            return False


listening_game_commands = False
# load/transform dictionaries from json files #
screens = json.load(open("screens.json"))
load_voice_actions("application")
load_voice_actions("eve")

print("Speak 'start listening' when ready")
print("Speak 'stop listening' when you want to pause")
print("Speak 'quit application' when you want to quit")

while True:

    # listen to mic, process input and split words
    tmp_voice_split = listen_and_process_mic()
    command = get_application_action(tmp_voice_split)

    if command == "quit_application":
        print("Quiting application... bye!")
        break

    elif command == "stop_listen":
        if listening_game_commands:
            listening_game_commands = False
            print("Stopping listening to game commands...")

    elif command == "start_listen":
        if not listening_game_commands:
            found_items = ScreenScanner().scan_screen()
            if found_items:
                print("Listening to game commands...")
                listening_game_commands = True
        else:
            print("already listening to game commands...")
    elif command == "escape":
        actions_eve.escape()
    elif command == "mouse_left_click":
        actions_eve.mouse_left_click()
    elif command == "display_screens":
        display_screens()
    elif not command and listening_game_commands is True:
        # make a dictionary with all screen items

        command = get_game_action_entity(tmp_voice_split)
        command_len = len(tmp_voice_split)

        if not command and (command_len < 2 or command_len > 6):
            print(f"Commands must be between 2 and 6 words: {tmp_voice_split} is not within range!")
        elif not command and 1 < command_len < 7:
            print(f"Command {tmp_voice_split} can not be resolved!")
        else:
            pass
            # print(f"Action: {command[0]}")
            # print(f"Entity: {command[1].entity_name} ({command[1].item_name})\n")

            da_action = command[0]
            speech_item = command[1]

            if da_action == "":
                print("No action interpreted!")
            elif da_action == "scan_screen" and speech_item is None:
                ScreenScanner().scan_screen(None)
            else:
                try:
                    # try to find the item inside screen entities
                    da_item = ScreenScanner.screen_all_entities[speech_item.entity_display_name]
                    if da_action == "mouse_options":
                        actions_eve.mouse_options(da_item)
                    elif da_action == "align":
                        actions_eve.align(da_item)
                    elif da_action == "mouse_select":
                        actions_eve.mouse_select(da_item)
                except KeyError:
                    try:
                        # try to find the item inside screens
                        da_item = screens[speech_item]
                    except KeyError:
                        da_item = None

                    if da_action == "scan_screen":
                        ScreenScanner().scan_screen(da_item)

                    elif da_action != "scan_screen":
                        print("No screen item interpreted!")



