# Author: Stephen Luttrell

from lib.sound_pool import sound_pool
import pygame
import speech
import time

class SimpleQuestionBox:
	"""
	A question interface which returns a boolean answer

	Attributes
	----------
	buttons : List
		A list of available interface buttons
	running : Boolean
		The state of the interface
	sounds : Dictionary, optional
		A dictionary of interface sounds: pop, select, and tab

	Methods
	-------
	is_running()
		returns the state of the interface
	run(contents, isFile)
		Activates the interface
	set_yes_label(text)
		Sets the label for the positive response
	set_sound(sound, filename)
		Sets the interface sounds
	set_no_label(text)
		Sets the label for the negative response
	"""

	def __init__(self):
		"""
		buttons : List
			A list of available interface buttons
		running : Boolean
			The state of the interface
		sounds : Dictionary, optional
			A dictionary of interface sounds: pop, select, and tab
		"""
		self._running = False
		self._buttons = [ 'no', 'yes' ]
		self._sounds = { 'pop': None, 'tab': None, 'select': None }

	def set_sound(self, sound: str, filename: str):
		"""Sets the interface sounds

		Parameters
		----------
		sound : string
			The type of sound: cancel, change_item, rollback, and select
		filename : String
			The sound source

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._sounds[sound] = filename

	def set_no_label(self, text: str):
		"""Sets the label for the negative response

		Parameters
		----------
		text : String
			The text label

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._buttons[0] = text

	def set_yes_label(self, text: str):
		"""Sets the label for the positive response

		Parameters
		----------
		text : String
			The text label

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._buttons[1] = text

	def is_running(self) -> bool:
		"""Returns the state of the interface"""
		return self._running

	def run(self, content: str, isFile: bool=False):
		"""Activates the interface

		If `isFile` isn't passed in, the default standard is to treat the -
		content as to be spoken by the speech engine

		Parameters
		----------
		content : String
			The content of the question or sound source
		isFile : Boolean, optional
			Set this flag to True if the `content` is a sound source (default is -
			False)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')

		self._running = True
		buttonPosition = True # Return True for yes and False for no
		oldRepeat = pygame.key.get_repeat()[0]
		pygame.key.set_repeat()

		if self._sounds['pop'] != None: sound_pool.play_stationary(self._sounds['pop'])

		if isFile: source = sound_pool.play_stationary(content)
		else: speech.speak(content, True)

		while self._running:
			time.sleep(.005) # Be kind to processors

			for e in pygame.event.get():
				if pygame.key.get_pressed()[pygame.K_UP]:
					if isFile:
						if not sound_pool.sound_is_playing(source): source = sound_pool.play_stationary(content)
					else: speech.speak(content, True)
				if pygame.key.get_pressed()[pygame.K_TAB] or pygame.key.get_pressed()[pygame.K_RIGHT] or ((pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]) and pygame.key.get_pressed()[pygame.K_TAB]) or pygame.key.get_pressed()[pygame.K_LEFT]:
					if buttonPosition == False: buttonPosition = True
					else: buttonPosition = False
					if self._sounds['tab'] != None: sound_pool.play_stationary(self._sounds['tab'])
					speech.speak(self._buttons[buttonPosition], True)
				if pygame.key.get_pressed()[pygame.K_y]:
					buttonPosition = True
					self._running = False
				if pygame.key.get_pressed()[pygame.K_n]:
					buttonPosition = False
					self._running = False
				if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
					self._running = False

		pygame.key.set_repeat(oldRepeat)
		if self._sounds['select'] != None: sound_pool.play_stationary(self._sounds['select'])
		speech.speak(self._buttons[buttonPosition], True)
		return buttonPosition