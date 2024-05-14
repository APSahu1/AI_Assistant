import datetime
import getpass as gp
import sys
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia

mic_name = "Microphone (Realtek(R) Audio)"
sample_rate = 48000
chunk_size = 2048

listener = sr.Recognizer()
engine = pyttsx3.init()
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list):
    print(microphone_name)
    if microphone_name == mic_name:
        device_id = i
        break


# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender):
    voices = engine.getProperty('voices')
    for voice in voices:
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as source:
            listener.pause_threshold = 1
            listener.adjust_for_ambient_noise(source, duration=1)
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='en_IN' or 'hi_IN')
            command = command.lower()
            if 'wake up' in command:
                talk("What happend master, How can I help you?")
                voice2 = listener.listen(source)
                command = listener.recognize_google(voice2, language='en_IN')
            if 'echo' or 'eco' or 'eko' in command:
                talk("kya bhaiya? boliye!")
                voice2 = listener.listen(source)
                command = listener.recognize_google(voice2, language='en_IN')
    except sr.UnknownValueError as e:
        command = "no command"
    except Exception as ex:
        print("Oops!", ex.__class__, "occurred that says", ex.__cause__)
    return command


def run_AI():
    command = take_command()
    print(command)
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk('Current time is ' + time)
        elif 'who is' in command:
            person = command.replace('who is ', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'joke' in command:
            print(pyjokes.get_joke())
            talk(pyjokes.get_joke())
        elif 'what happened' in command:
            print('nothing happened saahu ji')
            talk('nothing happened')
        elif 'are you single' in command:
            print('no, i am in relationship with google')
            talk('no, i am in relationship with google')
        elif 'message' in command:
            print('who do you wanna message')
            talk('who do you wanna message')
            name = take_command()
            pnum = gp.getpass(prompt=name, stream=None)
            print(pnum)
            print('tell me the massage...')
            talk('tell me the massage...')
            msg = take_command()
            print('sending massage')
            talk('sending massage')
            pywhatkit.sendwhatmsg(pnum, msg)
        elif 'no command' in command:
            print('did not hear anything, please try again...')
            talk('did not hear anything, please try again...')
        elif 'shut up' in command:
            talk('Shutting down. Have a nice time.')
            sys.exit(0)
        else:
            talk("i don't understand, please say again.")


while True:
    change_voice(engine, "hi", "VoiceGenderMale")
    run_AI()
