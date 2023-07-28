import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
import gtts
import pygame
import vlc
import time
from mqtt import mqttc,send_data


# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
pygame.mixer.init()
load_dotenv()
openai.api_key ="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" 
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
engine.setProperty('rate',145)

greetings = [f"whats up master" ]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hello'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
            if "home" in text.lower():
                print("turn of led .")
                sendmessage(source)
                break
        except sr.UnknownValueError:
            pass


def sendmessage(source):
    while True:
        print("talk")
        audio= r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"said : {text}")
            if not text:
                print("errorr")
                continue
            if text=="turn on light":
                send_data("1")
                continue
            elif text=="turn off light":
                send_data("0")
                continue
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")

            break
            
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            break




# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}]) 
            response_text = response.choices[0].message.content
            print(f"OpenAI response: {response_text}")

            # Speak the response
            # engine.say(response_text)
            resp=gtts.gTTS(response_text)
            resp.save("res.mp3")
            # playsound("res.mp3")
            # sound = pygame.mixer.Sound('res.mp3')
            # playing = sound.play()
            # while playing.get_busy():
            #     pygame.time.delay(100)
            p = vlc.MediaPlayer("res.mp3")
            p.play()
            time.sleep(60)
            p.stop()
            # engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
            
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source


if __name__ == "__main__":
    #  databaseInit()
    with sr.Microphone() as source:
        listen_for_wake_word(source)
    mqttc.loop_forever()