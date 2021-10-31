from ScreenScanner import ScreenScanner
import json


def get_application_action(word_split):
    #   If the interpretation of word_split is successful, get_application_action
    #   will return one of the application actions: ('start listening', 'stop listening', 'quit')
    #   If word_split is not successfully interpreted, get_application_action will return False
    word_count = len(word_split)
    voice_actions = json.load(open("voice-actions-application.json"))
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
    """
    :param word_split:
    :return: list, bool
    """
    #   If the interpretation of word_split is successful, get_game_action_entity
    #   will be a list of two items [A, E]:
    #   A: is the action to take
    #   E: is the entity to perform the action upon
    #   word_split can contain >=2 and <= 6 words
    #   Successful interpretation means that both A and I will be found in their respective dictionaries:
    #   A, inside voice_actions and E, inside screen_all_entities
    #   If word_split is not successfully interpreted, get_game_action_entity will return False

    word_count = len(word_split)
    voice_actions = json.load(open("voice-actions-eve.json"))

    if word_count < 2 or word_count > 6:
        return False
    elif word_count == 2:
        try:  # find 1st word in the actions dictionary, 2nd word in the screen entities dictionary
            return [voice_actions[word_split[0]], word_split[1]]
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


# # # # # # # # # # # # # # # # # #


# screen_items = scan_screen()
# print("Screen items found:")
# for item in screen_items:
#     print(item + " (" + screen_items[item].name + ")")

# tmp_voice_text = "look station for"
# tmp_voice_split = process_and_split_voice(tmp_voice_text)
# command = get_action_item_from_split(tmp_voice_split)
#
# if not command:
#     print("\nAction: '" + tmp_voice_text + "' can not be resolved!")
# else:
#     print("\nAction: " + str(command[0]))
#     print("Entity: " + command[1].type + " (" + command[1].name + ")")
#     print("x: " + str(command[1].x_loc) + ", y: " + str(command[1].y_loc))
