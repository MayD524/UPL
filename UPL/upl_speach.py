import pyttsx3

def speach(words):
	engine = pyttsx3.init()
	engine.say(words)
	engine.runAndWait()