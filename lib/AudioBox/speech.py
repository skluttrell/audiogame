from sys import platform

if platform == 'win32':
	from accessible_output2.outputs.sapi5 import SAPI5
	TTS = SAPI5()
elif platform == 'darwin':
	from accessability_output2.outputs.voiceover import VoiceOver
	TTS = VoiceOver()

# Speak the text
def speak(text, interrupt=False):
	if len(text) == 1: # This is a single character
		if text == '.':
			text = 'period'
		elif text == ',':
			text = 'comma'
		elif text == ' ':
			text = 'space'
		elif text == ':':
			text = 'colon'
		elif text == ';':
			text = 'semicolon'
		elif text == '-':
			text = 'dash'
		elif text == '?':
			text = 'question'
		elif text == '*':
			text = 'asterisk'
		elif text == '!':
			text = 'exclaim'
		elif text == '_':
			text = 'Underscore'
		elif text == '+':
			text = 'plus'
		elif text == '|':
			text = 'bar'
		elif text == '>':
			text = 'greater'
		elif text == '<':
			text = 'less'
		elif text == '\\':
			text = 'backslash'
		elif text == '/':
			text = 'slash'
		elif text == '[':
			text = 'left bracket'
		elif text == ']':
			text = 'right bracket'
		elif text == '{':
			text = 'left brace'
		elif text == '}':
			text = 'right brace'
		elif text == '\'':
			text = 'tick'
		elif text == '"':
			text = 'quote'
		elif text == '`':
			text = 'back quote'
		elif text == '~':
			text = 'tilda'
		elif text == '@':
			text = 'at'
		elif text == '^':
			text = 'caret'
		elif text == '%':
			text = 'percent'
		elif text == '$':
			text = 'dollar'
		elif text == '#':
			text = 'number'
		elif text == '&':
			text = 'ampersand'
		elif text == '*':
			text = 'asterik'
		elif text == '(':
			text = 'left paren'
		elif text == ')':
			text = 'right paren'

	TTS.speak(text, interrupt) # Send the text to speech output to be spoken

# Stop the text-to-speech engine from speaking
def stop():
	TTS.silence()

# Get the pitch from the text-to-speech engine
def get_pitch():
	return TTS.get_pitch()

# Get the rate of speech from the text-to-speech engine
def get_rate():
	return TTS.get_rate()

# Get the volume level from the text-to-speech engine
def get_volume():
	return TTS.get_volume()

# Set the pitch from the text-to-speech engine
def set_pitch(pitch):
	TTS.set_pitch(pitch)

# Set the speech rate
def set_rate(rate):
	TTS.set_rate(rate)

# Set the volume level for speech
def set_volume(volume):
	TTS.set_volume(volume)