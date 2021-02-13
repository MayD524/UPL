from playsound import playsound
from pydub import AudioSegment
import pyttsx3
import os

class player:
    def start(file):
        if os.path.exists(file):
            playsound(file)
            return True
        else:
            print('File does not exist')
            return False

    ## renamed and reworked to for all file formats default wav
    def fileConvert(fileIn, fileOut, form="wav", bitrate="320k"):
        if os.path.exists(fileIn):
            audioData = AudioSegment.from_file(fileIn, "webm")
            print(f"Got song data from {audioData}")
            audioData.export(fileOut, format=form, bitrate=bitrate)
        else:
            print(f"{fileIn} does not exist or is spelled wrong.")


def speech(words):
	engine = pyttsx3.init()
	engine.say(words)
	engine.runAndWait()