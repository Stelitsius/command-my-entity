import speech_recognition as sr


def listen_and_process_mic():
    tmp_voice_text = listen_to_mic()
    tmp_voice_split = process_and_split_voice(tmp_voice_text)
    return tmp_voice_split


def listen_to_mic():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=1)
                audio = r.listen(mic)
                text = r.recognize_google(audio)
                # print(text)
                return text
        except sr.UnknownValueError:
            r = sr.Recognizer()
            print("Can not understand audio")
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue


def process_and_split_voice(voice_text):
    voice_text = voice_text.strip()
    voice_text = voice_text.lower()
    voice_split = voice_text.split()

    if voice_split[-1] == "one":
        voice_split[-1] = "1"
    elif voice_split[-1] in ("to", "tube"):
        voice_split[-1] = "2"
    elif voice_split[-1] == "three":
        voice_split[-1] = "3"
    elif voice_split[-1] == "for":
        voice_split[-1] = "4"

    if "weed" in voice_split:
        voice_split[voice_split.index("weed")] = "quit"
    if "quick" in voice_split:
        voice_split[voice_split.index("quick")] = "quit"
    return voice_split
