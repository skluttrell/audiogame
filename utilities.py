# Author: Stephen Luttrell

import os, pickle, random, speech

oldRandom = 0
newRandom = 0

def get_random(path):
	global oldRandom, newRandom
	count = 0
	if os.path.isdir(os.path.join(path)):
		list = os.listdir(path)
		if not list == None:
			while newRandom == oldRandom and count < 10:
				newRandom = random.randint(1, len(list))
				count += 1
			oldRandom = newRandom

	return newRandom

def save_data(data, file='untitled'):
	with open(file, 'ab') as o:
		pickle.dump(data, o)

def retrieve_data(file):
	with open(file, 'rb') as i:
		return pickle.load(i)

SPEECH_VOLUME=100
SPEECH_RATE=1

# text-to-speech manipulation Callback functions
def tts_change_volume(value):
	global SPEECH_VOLUME
	if (value == -1 and SPEECH_VOLUME > 0) or (value == 1 and SPEECH_VOLUME < 100):
		SPEECH_VOLUME += value * 10
		speech.set_volume(SPEECH_VOLUME)
	speech.speak(str(SPEECH_VOLUME), True)

def tts_change_rate(value):
	global SPEECH_RATE
	if (value == -1 and SPEECH_RATE > -10) or (value == 1 and SPEECH_RATE < 10):
		SPEECH_RATE += value
		speech.set_rate(SPEECH_RATE)
	speech.speak(str(SPEECH_RATE), True)