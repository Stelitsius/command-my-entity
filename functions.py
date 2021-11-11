from ScreenScanner import ScreenScanner
import json


def display_screens():
    print("Available screens: = = = = = =")
    screens = json.load(open("screens.json"))
    for screen in screens:
        print(screen)
    print("= = = = = = = = = = = = = = = =")





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
