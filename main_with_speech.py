import speech_recognition as sr
from functions import *
import actions_eve

voice_text = ""
rec = ""


def process_and_split_voice():
    global voice_text
    voice_text = voice_text.strip()
    voice_text = voice_text.lower()
    voice_split = voice_text.split()
    # word 'for' is must not be included in our dict. whenever found, it will be interpreted as '4' instead
    if "for" in voice_split:
        voice_split[voice_split.index("for")] = "4"
    if "one" in voice_split:
        voice_split[voice_split.index("one")] = "1"
    if "tube" or "to" in voice_split:
        voice_split[voice_split.index("to")] = "2"
    return voice_split


def callback(recognizer, audio):
    try:
        global voice_text
        voice_text = recognizer.recognize_google(audio)
        return voice_text
    except sr.UnknownValueError:
        global rec
        rec = sr.Recognizer()
        print("Can not understand audio")
        return None
    except sr.RequestError as e:
        return None
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))


rec = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    rec.adjust_for_ambient_noise(source, duration=1)

background_listening = rec.listen_in_background(mic, callback)

listening_game_commands = False

print("Speak 'start listening' when ready")
print("Speak 'stop listening' when you want to pause")
print("Speak 'quit application' when you want to quit")

while True:

    # listen to mic, process input and split words
    # tmp_voice_split = listen_and_process_mic()
    tmp_voice_split = ""
    tmp_voice_split = process_and_split_voice()
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

    elif not command and listening_game_commands is True:
        # make a dictionary with all screen items

        command = get_game_action_entity(tmp_voice_split)
        command_len = len(tmp_voice_split)

        if not command and (command_len < 3 or command_len > 6):
            print(f"Commands must be between 3 and 6 words: {tmp_voice_split} is not within range!")
        elif not command and 2 < command_len < 7:
            print(f"Command {tmp_voice_split} can not be resolved!")
        else:
            print(f"Action: {command[0]}")
            print(f"Entity: {command[1].entity_name} ({command[1].item_name})\n")

            da_action = str(command[0])
            speech_item = command[1].entity_name

            try:
                da_item = ScreenScanner.screen_all_entities[speech_item]
            except KeyError:
                da_item = ""

            if da_item != "":
                if da_action == "mouse_options":
                    actions_eve.mouse_options(da_item)
                elif da_action == "align":
                    actions_eve.align(da_item)
                elif da_action == "mouse_select":
                    actions_eve.mouse_select(da_item)
                else:
                    print("No action interpreted!")
            else:
                print("No screen item interpreted!")
