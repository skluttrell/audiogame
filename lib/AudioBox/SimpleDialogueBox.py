# Author: Stephen Luttrell

import pygame
from lib.sound_pool import sound_pool
import speech
import time

class SimpleDialogueBox:
	"""
	A dialog interface which displays a brief message, either spoken by -
	the speech engine or played as a sound source

	if `exitAutomatically` isn't passed in, the default behavior is to -
	wait for user input to close the dialogue

	Attributes
	----------
	button : String
		The text of the confirm prompt
	content : String
		The content of the message
	exitAutomatically : Boolean
		Set this flag to True to automatically close the dialogue when a sound -
		file is finished playing (default is False)
	isFile : Boolean
		Set this flag to True if the `content` is a sound source (default is -
		False)
	running : Boolean
		The state of the interface
	sounds : Dictionary, optional
		A dictionary of interface sounds: confirm, pop

	Methods
	-------
	is_running()
		Returns the state of the interface
	run()
		Activates the interface
	set_button(value)
		Sets the text of the confirm prompt
	set_sound(sound, value)
		Sets the interface sounds
	"""

	def __init__(self, content: str, isFile: bool=False, exitAutomatically: bool=False):
		"""
		button : String
			The text of the confirm prompt
		content : String
			The content of the message
		exitAutomatically : Boolean
	Set this flag to True to automatically close the dialogue when a sound -
	file is finished playing (default is False)
		isFile : Boolean
	Set this flag to True if the `content` is a sound source (default is -
	False)
		running : Boolean
			The state of the interface
		sounds : Dictionary, optional
			A dictionary of interface sounds: confirm, pop
		"""

		self._running = False
		self._content = content
		self._sounds = { 'pop': None, 'confirm': None }
		self._button = 'continue'
		self._isFile = isFile
		self._exitAutomatically = exitAutomatically

	def set_button(value: str):
		"""Sets the confirm prompt label

		Parameters
		----------
		value : String
			The text label of the confirm prompt

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._button = value

	def set_sound(self, sound: str, filename: str):
		"""Sets the interface sounds

		Parameters
		----------
		sound : string
			The type of sound: confirm, pop
		filename : string
			The file path of the sound source

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._sounds[sound] = filename

	def is_running():
		"""Returns the state of the interface"""
		return self._running

	def run(self):
		"""Activates the interface

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')

		self._running = True
		playOK = 0 # Tells the method when it's time to play or speak the confirm prompt (0: waiting, 1: play prompt, 2: has played the prompt)

		if self._sounds['pop'] != None: sound_pool.play_stationary(self._sounds['pop'])

		# Play the message
		if self._isFile: source = sound_pool.play_stationary(self._content)
		else: speech.speak(self._content+' '+self._button, True)

		while self._running:
			time.sleep(.005) # Be kind to processors

			if self._isFile: # This is a sound file
				if not sound_pool.sound_is_playing(source): # The message has finished playing
					if playOK != 2: playOK = 1 # Setting playOK to 1 means the message is finished playing
					if playOK == 1:
						if self._exitAutomatically: # Exit the dialogue when done
							self._running = False
						else: # Play or speak the done prompt
							if self._sounds['confirm'] != None: sound_pool.play_stationary(self._sounds['confirm'])
							else: speech.speak(self._button)
						playOK = 2 # Don't play the confirm prompt again

			for e in pygame.event.get(): # Poll the key events
				if e.type == pygame.KEYDOWN:
					if e.key != pygame.K_UP: # Any key besides up exits the dialogue
						if self._isFile: sound_pool.pause_sound(source)
						else: speech.stop()
						self._running = False
					else: # Up replays the contents
						if self._isFile:
							if not sound_pool.sound_is_playing(source):
								playOK = 0
								source = sound_pool.play_stationary(self._content)
						else:
							speech.speak(self._content+' '+self._button, True)