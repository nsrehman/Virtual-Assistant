# from threading import Thread

import speech_recognition as sr
import keyboard as k
import spotipy
import os
import pyttsx3
import random
import credentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# from refresh import Refresh

# from googleText2Speech import synthesize_text

os.environ["SPOTIPY_CLIENT_ID"] = credentials.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = credentials.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = credentials.SPOTIPY_REDIRECT_URI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials.GOOGLE_APPLICATION_CREDENTIALS

deviceId = credentials.DEVICE_ID
scope = "user-modify-playback-state"

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Mic init
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)

jarvisResponses = ["I'm on it.", "Consider it done.", "Right away, Sir.", "Yes sir."]


def speak(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while 1:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                response = (r.recognize_google(audio))
                print(response)

                if any(x in response for x in ["Jarvis", "Yaris", "Garvais", "Taurus"]):
                    speak("Sir?")
                    audio = r.listen(source)
                    response = (r.recognize_google(audio))
                    # print(response)
                    # Discord Functionality
                    if any(x in response for x in ["mute", "unmute", "mutiny"]):
                        k.press_and_release('F8')
                        speak("It's done.")
                    elif any(x in response for x in ["deafen", "undeafen", "quiet"]):
                        k.press_and_release('F9')
                        speak("It's done.")

                    # Spotify Functionality
                    if any(x in response for x in ["next", "skip"]):
                        speak(jarvisResponses[random.randint(0, 3)])
                        sp.next_track(deviceId)
                    if any(x in response for x in ["previous", "last", "replay"]):
                        speak(jarvisResponses[random.randint(0, 3)])
                        sp.previous_track(deviceId)
                    if any(x in response for x in ["pause", "stop"]):
                        try:
                            speak(jarvisResponses[random.randint(0, 3)])
                            sp.pause_playback(deviceId)
                        except spotipy.exceptions.SpotifyException:
                            pass
                    elif any(x in response for x in ["resume", "continue", "play"]):
                        try:
                            speak(jarvisResponses[random.randint(0, 3)])
                            sp.start_playback(deviceId)
                        except spotipy.exceptions.SpotifyException:
                            pass
                    if any(x in response for x in ["increase", "lower", "raise", "set", "volume"]) and any(
                            char.isdigit() for char in response):
                        speak(jarvisResponses[random.randint(0, 3)])
                        volume = [int(s) for s in response.split() if s.isdigit()]
                        sp.volume(volume[0], deviceId)

                    if any(x in response for x in ["fast-forward", "fast", "forward"]) and any(
                            char.isdigit() for char in response):
                        speak(jarvisResponses[random.randint(0, 3)])
                        time = [int(s) for s in response.split() if s.isdigit()]
                        sp.seek_track(time[0] * 1000, deviceId)

                    # Application Functionality
                    if "open" in response:
                        if "valorant" in response:
                            speak(jarvisResponses[random.randint(0, 3)])
                            os.startfile(r"C:\Users\Public\Desktop\VALORANT.lnk")
                        if any(x in response for x in ["Apex", "Legends", "legend"]):
                            speak(jarvisResponses[random.randint(0, 3)])
                            os.startfile(r"C:\Users\Nasir\Desktop\Apex Legends.url")
                        if any(x in response for x in ["aim", "labs", "lab"]):
                            speak(jarvisResponses[random.randint(0, 3)])
                            os.startfile(r"C:\Users\Nasir\Desktop\Aim Lab.url")
                        if "Spotify" in response:
                            speak(jarvisResponses[random.randint(0, 3)])
                            os.startfile(r"C:\Users\Nasir\AppData\Roaming\Spotify\Spotify.exe")

                    # PC Functionality
                    if "sleep" in response:
                        speak("Goodbye for now, sir.")
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    if "quit" in response:
                        speak("Goodbye for now, sir.")
                        break

        except sr.RequestError:
            # print("API unavailable")
            pass
        except sr.UnknownValueError:
            # print("Unable to recognize speech or nothing said")
            pass

if __name__ == '__main__':
    main()