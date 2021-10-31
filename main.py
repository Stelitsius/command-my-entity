import pyautogui
from cv2 import cv2
from functions import *
from speech import listen_and_process_mic
import actions


listening_game_commands = False
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
            listening_game_commands = True
            ScreenScanner().scan_screen("dynamic_entities")
            print("Listening to game commands...")
    elif command == "escape":
        actions.escape()
    elif command == "mouse_left_click":
        actions.mouse_left_click()
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

            try:
                da_item = ScreenScanner.screen_all_entities[speech_item]
            except KeyError:
                da_item = ""

            if da_item != "":
                if da_action == "mouse_options":
                    actions.mouse_options(da_item)
                elif da_action == "align":

                    actions.align(da_item)
                elif da_action == "mouse_select":
                    actions.mouse_select(da_item)
                else:
                    print("No action interpreted!")
            else:
                print("No screen item interpreted!")