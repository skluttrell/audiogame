# Author: Stephen Luttrell

import lib.AudioBox as AudioBox
from lib.sound_pool import sound_pool
import speech
import pygame
import os
import time

class FileSelectionBox:
	"""
	A file selection interface which returns a string containing the file -
	path

	attributes
	----------
	allows : Integer, optional
		Set this flag for the following behavior: ESCAPE, exits/cancels the -
		menu, WRAP, cursor wraps around, HOME_AND_END, `home` and `end` keys -
		move to the first or last selection, ALL, activates all options
	buttons : List
		A list of available interface buttons
	running : Boolean
		The state of the interface
	sounds : Dictionary, optional
		A dictionary of interface sounds: alert, back, cancel, change_item, -
		forward, rollback, select, tab

	Methods
	-------
	allow(value)
		sets cursor behavior properties
	is_running()
		returns the state of the interface
	run(intro, isFile)
		Activates the interface
	set_sound(sound, filename)
		Sets the interface sounds
	"""

	def __init__(self, allows=0):
		"""
		allows : Integer, optional
			Flags the following behaviors: ESCAPE, escape key exits the menu, -
			WRAP, cursor wraps back around, HOME_AND_END, the `home` and `end` -
			keys jump to the top or bottom of the menu, ALL activates all options
		buttons : Dictionary
			A list of available interface buttons
		running : Boolean
			The state of the interface
		sounds : Dictionary, optional
			A dictionary of interface sounds: alert, back, cancel, change_item, -
			forward, rollback, select, tab
		"""

		self._allows = allows
		self._sounds = { 'back': None, 'forward': None, 'tab': None, 'change_item': None, 'rollback': None, 'alert': None, 'pop': None, 'cancel': None }
		self._buttons = [ 'select', 'cancel', 'back', 'forward' ]
		self._running = False

	def __get_files(self, dir: str, dirOnly: bool, types: list) -> list:
		# PRIVATE: returns a list of files/directories

		directories = [] # List of only directories
		files = [] # List of only files

		try:
			for entry in os.listdir(dir): # directory list
				fullPath = os.path.join(dir, entry)
				if os.path.exists(fullPath): # Check full path
					if os.path.isdir(fullPath): directories.append(entry) # Fill out directory list
					elif os.path.isfile(fullPath) and not dirOnly: # The entry is a file
						if types == None:
							files.append(entry) # Add all files to the files list
						else:
							for t in types: # Iterate through all the type extensions
								if entry.lower().endswith(t.lower()): files.append(entry)

			sorted(directories)
			sorted(files)
		except:
			return None
		else:
			if len(directories) == 0 and len(files) == 0: return [ 'no files' ]

		return directories + files

	def allow(self, value: int):
		"""sets cursor behavior properties

		Parameters
		----------
		value : Integer
			A constant representing cursor behavior: ALL, ESCAPE, HOME_AND_END, and -
			WRAP

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._allows = value

	def set_sound(self, sound: str, filename: str):
		"""Sets the interface sounds

		Parameters
		----------
		sound : String
			The type of sound: alert, back, cancel, change_item, forward, -
			rollback, select, and tab
		filename : string
			The file path of the sound source

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._sounds[sound] = filename

	def is_running(self) -> bool:
		"""Returns the state of the interface"""
		return self._running

	def run(self, dir: str, dirOnly: bool=False, types: list=None) -> str:
		"""Activates the interface

		if `dirOnly` isn't passed in, the default standard is to list all -
		files and directories as limited only by type

		if `types` isn't passed in, the default standard is to list all files

		parameters
		----------
		dir : String
			The active directory
		dirOnly : Boolean, optional
			Set this flag to show only directories (default is False)
		types : List, optional
			A list of file type extensions (default is None)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')

		self._running = True
		buttonPosition = 0
		listOfFiles = self.__get_files(dir, dirOnly, types) # Get the list of files under this directory
		position = 0 # set the index at the top of the file tree
		filename = os.path.join(dir, listOfFiles[position])
		oldRepeat = pygame.key.get_repeat()[0]
		pygame.key.set_repeat()

		if self._sounds['pop'] != None: sound_pool.play_stationary(self._sounds['pop']) # Play the pop up sound
		speech.speak('Please select a file or directory: ' + listOfFiles[position]) # Speak the first file

		while self._running:
			time.sleep(.005) # Be kind to processors

			for e in pygame.event.get():
				if pygame.key.get_pressed()[pygame.K_UP]:
					if position > 0:
						position -= 1
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
					elif self._allows - AudioBox.WRAP >= 0:
						position = len(listOfFiles) - 1
						if self._sounds['rollback'] != None: sound_pool.play_stationary(self._sounds['rollback'])
					filename = os.path.join(dir, listOfFiles[position])
					speech.speak(listOfFiles[position], True)
				if pygame.key.get_pressed()[pygame.K_DOWN]:
					if position < len(listOfFiles) - 1:
						position += 1
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
					elif self._allows - AudioBox.WRAP >= 0:
						position = 0
						if self._sounds['rollback'] != None: sound_pool.play_stationary(self._sounds['rollback'])
					filename = os.path.join(dir, listOfFiles[position])
					speech.speak(listOfFiles[position], True)
				if pygame.key.get_pressed()[pygame.K_TAB]:
					if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
						if buttonPosition > 0: buttonPosition -= 1 # Reverse through the tab order
						else: buttonPosition = len(self._buttons) - 1 # Go to the end of the tab order
					else: # Shift is not pressed
						if buttonPosition < len(self._buttons) - 1: buttonPosition += 1 # Advance through the tab order
						else: buttonPosition = 0 # return to the beginning of the tab order
					if self._sounds['tab'] != None: sound_pool.play_stationary(self._sounds['tab']) # Play the tab sound
					speech.speak(self._buttons[buttonPosition]) # Announce the current button selection
				if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_b] or ((pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]) and self._buttons[buttonPosition] == 'back'): # Go backward through the directory tree
					if not os.path.dirname(dir) == dir:
						dir = os.path.dirname(dir)
						position = 0 # Reset position
						listOfFiles = self.__get_files(dir, dirOnly, types) # Get the new list of files and directories from the new absolute directory path
						filename = os.path.join(dir, listOfFiles[position])
						if self._sounds['back'] != None: sound_pool.play_stationary(self._sounds['back']) # Play the back sound
						speech.speak(listOfFiles[position], True) # Announce the first file
				if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_f] or ((pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]) and self._buttons[buttonPosition] == 'forward'): # Go forward through the directory tree
					if os.path.isdir(filename): # Is a directory
						dir = os.path.join(dir, listOfFiles[position])
						temp = self.__get_files(dir, dirOnly, types) # Get the new list of files
						if not temp == None: # This is a valid directory
							position = 0 # Return the position to the top
							listOfFiles = temp
							filename = os.path.join(dir, listOfFiles[position])
							if self._sounds['forward'] != None: sound_pool.play_stationary(self._sounds['forward']) # Play the forward sound
							speech.speak(listOfFiles[position], True) # speak the first file
						else: # The directory is invalid
							dir = os.path.dirname(dir)
							if self._sounds['alert'] != None: sound_pool.play_stationary(self._sounds['alert']) # Play the alert sound
				if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
					if self._buttons[buttonPosition] == 'select':
						if not listOfFiles[position] == 'no files':
							self._running = False
							if self._sounds['select'] != None: sound_pool.play_stationary(self._sounds['select'])
						else: # There are no valid files selected
							if self._sounds['alert'] != None: sound_pool.play_stationary(self._sounds['alert']) # Play the alert sound
					elif self._buttons[buttonPosition] == 'cancel':
						filename = None
						self._running = False # Exit the file selection menu
						if self._sounds['cancel'] != None: sound_pool.play_stationary(self._sounds['cancel'])
				if pygame.key.get_pressed()[pygame.K_ESCAPE]:
					filename = None
					self._running = False
					if self._sounds['cancel'] != None: sound_pool.play_stationary(self._sounds['cancel'])

		pygame.key.set_repeat(oldRepeat)
		return filename