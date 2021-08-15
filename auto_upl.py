#!/usr/bin/env python3
import sys
import os


if __name__ == "__main__":
    py_ver = sys.version.split('.',2)[:2]
    
    if int(py_ver[0]) >= 3 and int(py_ver[1]) >= 7:
        cmd = input("What is your python command?(python|py|etc) > ")
        os.system(f"{cmd} -m pip install cryptocode")
        os.system(f"{cmd} -m pip install pyautogui")
        os.system(f"{cmd} -m pip install playsound")
        os.system(f"{cmd} -m pip install pydub")
        os.system(f"{cmd} -m pip install pyttsx3")
        os.system(f"{cmd} -m pip install ffmpeg")      
    else:
        raise Exception("You are too out dated for this library.")
    
else:
    raise ImportError("This script cannot be imported")
