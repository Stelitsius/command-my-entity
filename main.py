from threading import Thread
from speech import listen_and_process_mic
import actions_app
import actions_eve
import json
from ScreenScanner import ScreenScanner

voice_actions = {}


def load_voice_actions(target):
    global voice_actions
    if target == "application_no_entity":
        action_voices = json.load(open("action_voices_app(no_entity).json"))
    elif target == "eve":
        action_voices = json.load(open("action_voices_eve.json"))
    elif target == "eve_no_entity":
        action_voices = json.load(open("action_voices_eve(no_entity).json"))
    else:
        return
    # derive voice_actions dictionary from action_voices_<source> json
    for action in action_voices:
        for voice in action_voices[action]:
            voice_actions[voice] = action


def get_application_action(word_split):
    #   If the interpretation of word_split is successful, get_application_action
    #   will return one of the application actions or game (eve) actions (which do not require an entity)
    #   If word_split is not successfully interpreted, get_application_action will return False
    #   word_split and hence action can be max 2 words (example: start listening)
    global voice_actions
    word_count = len(word_split)

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
    #   A: is the game (eve) action to take
    #   E: is the entity object to perform the action upon
    #   word_split can contain >=2 and <=6 words. (min 1 action + 1 entity, example: align sun
    #   max 3 action + 2 entity, example: keep at range station 1)
    #   Successful interpretation means that both A and I will be found in their respective dictionaries:
    #   A, inside voice_actions and E, inside screen_all_entities
    #   If word_split is not successfully interpreted, get_game_action_entity will return False
    global voice_actions
    word_count = len(word_split)

    if word_count < 2 or word_count > 6:
        return False
    elif word_count == 2:
        try:  # find 1st word in the actions dictionary, 2nd word in the screen entities dictionary
            return [voice_actions[word_split[0]],
                    ScreenScanner.screen_all_entities[word_split[1]]]
        except KeyError:
            return False
    elif word_count == 3:
        try:  # find 1st word in the actions dictionary, 2nd+3rd word in the screen entities dictionary
            return [voice_actions[word_split[0]],
                    ScreenScanner.screen_all_entities[word_split[1] + " " + word_split[2]]]
        except KeyError:
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
            try:  # find 1st+2nd word in the actions dictionary, 3rd+4th word in the screen entities dictionary
                return [voice_actions[word_split[0] + " " + word_split[1]],
                        ScreenScanner.screen_all_entities[word_split[2] + " " + word_split[3]]]
            except KeyError:
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
            try:  # find 1st+2nd+3rd word in the actions dictionary, 4th+5th word in the screen entities dictionary
                return [voice_actions[word_split[0] + " " + word_split[1] + " " + word_split[2]],
                        ScreenScanner.screen_all_entities[word_split[3] + " " + word_split[4]]]
            except KeyError:
                return False


# # # # # # # # # # # # # # # # # # # # #
#               main start              #
# # # # # # # # # # # # # # # # # # # # #

SS = ScreenScanner()
listening_game_commands = False
# load/transform dictionaries from json files #
screens = json.load(open("screens.json"))
load_voice_actions("application_no_entity")
load_voice_actions("eve")
load_voice_actions("eve_no_entity")

actions_app.display_application_actions()

print("Say an action to proceed")

while True:

    # listen to mic, process input and split words
    tmp_voice_split = listen_and_process_mic()
    command = get_application_action(tmp_voice_split)
    # # # # # # # # # # # # # # # # # # # # # # #
    #   1   application actions (no entity)     #
    # # # # # # # # # # # # # # # # # # # # # # #
    if command == "quit_application":
        print("Quiting application... bye!")
        break

    elif command == "display_actions":
        actions_app.display_application_actions()

    elif command == "stop_listen":
        if listening_game_commands:
            listening_game_commands = False
            print("Stopping listening to game commands...")

    elif command == "start_listen":
        if listening_game_commands:
            print("already listening to game commands...")
        else:
            found_items = SS.scan_screen()
            if found_items:
                thread_draw_entities = Thread(target=SS.draw_entities)
                thread_draw_entities.start()
                print("Listening to game commands...")
                listening_game_commands = True
    # # # # # # # # # # # # # # # # # # # # # # #
    #   2   game (eve) actions (no entity)      #
    # # # # # # # # # # # # # # # # # # # # # # #

    elif command == "escape" and listening_game_commands:
        actions_eve.escape(user_called=True)

    elif command == "display_screens" and listening_game_commands:
        actions_eve.display_screens()
    # scan_screen is in action_voices_eve as it cn take (screen) entity or no entity.
    elif command == "scan_screen" and listening_game_commands:
        found_items = SS.scan_screen()
        if found_items:
            thread_draw_entities = Thread(target=SS.draw_entities)
            thread_draw_entities.start()
    elif command == "mouse_click" and listening_game_commands:
        actions_eve.mouse_left_click()

    # # # # # # # # # # # # # # # # # # # # # # #
    #   3   game (eve) actions (with entity)    #
    # # # # # # # # # # # # # # # # # # # # # # #

    elif listening_game_commands:
        command = get_game_action_entity(tmp_voice_split)
        command_len = len(tmp_voice_split)

        if command:
            da_action = command[0]
            da_entity = command[1]
            if da_action == "scan_screen":
                found_items = SS.scan_screen(da_entity)
                if found_items:
                    thread_draw_entities = Thread(target=SS.draw_entities)
                    thread_draw_entities.start()
            elif da_action == "mouse_options":
                if SS.overlay_is_drawn:
                    actions_eve.escape(user_called=False)
                actions_eve.mouse_options(da_entity)
            elif da_action == "align":
                if SS.overlay_is_drawn:
                    actions_eve.escape(user_called=False)
                actions_eve.align(da_entity)
            elif da_action == "mouse_select":
                if SS.overlay_is_drawn:
                    actions_eve.escape(user_called=False)
                actions_eve.mouse_select(da_entity)
            elif da_action == "jump":
                if SS.overlay_is_drawn:
                    actions_eve.escape(user_called=False)
                actions_eve.jump(da_entity)
            elif da_action == "show_info":
                if SS.overlay_is_drawn:
                    actions_eve.escape(user_called=False)
                actions_eve.show_info(da_entity)
