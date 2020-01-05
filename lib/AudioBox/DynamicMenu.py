# Author: Stephen Luttrell

import lib.AudioBox, pygame, speech, time
from lib.sound_pool import sound_pool
from types import FunctionType as func

class DynamicMenu:
	"""
	A menu interface which returns an integer representing the item at index

	attributes
	----------
	allows : Integer, optional
		Set this flag for the following behavior: ESCAPE, exits/cancels the -
		menu, WRAP, cursor wraps around, HOME_AND_END, `home` and `end` keys -
		move to the first or last selection, ALL, activates all options
	sounds : Dictionary, optional
		A dictionary of interface sounds: cancel, change_item, rollback, select
	running : Boolean
		The state of the interface
	items : Dictionary
		A dictionary of menu items

	Methods
	-------
	add_item(text, isFile)
		adds a new item to the menu
	add_callback_function(callbackFunction, text, isFile)
		adds a user defined function to the menu (e.g. a slider for a setting)
	allow(value)
		sets cursor behavior properties
		get_item(index)
			returns the item content
		get_item_count()
			returns the number of items
		is_running()
			returns the state of the interface
	reset(completely)
		resets the menu to default values
	run(intro, isFile)
		Activates the interface
	run_extended(intro, isFile, startPosition, speakInitialItem)
		Activates the interface with additional properties
	set_item(index, text, isFile)
		Sets the contents of an item
	set_sound(sound, filename)
		Sets the interface sounds
	"""

	def __init__(self, allows=0):
		"""
		allows : Integer, optional
			Set this flag for the following behavior: ESCAPE, exits/cancels the -
			menu, WRAP, cursor wraps around, HOME_AND_END, `home` and `end` keys -
			move to the first or last selection, ALL, activates all options
		sounds : Dictionary, optional
			A dictionary of interface sounds: cancel, change_item, rollback, select
		running : Boolean
			The state of the interface
		items : Dictionary
			A dictionary of menu items
		"""

		self._allows = allows
		self._sounds = { 'change_item': None, 'rollback': None, 'select': None, 'cancel': None } # Where change_item is the sound of changing from one item to another, rollback is the sound made when the cursor moves back to the top or bottem when the boundry of the list is reached, select is the sound made when a selection is made, and cancel is the sound of quitting the menu
		self._running = False # Set to True when the menu is started
		self._items = [ None ] # Dictionary of items

	def __present_item(self, text: str, isFilename: bool) -> int:
		# PRIVATE: plays or speaks the item

		if isFilename: return sound_pool.play_stationary(text) # The index of the sound in the sound_pool
		else: speech.speak(text, False)
		return 0

	def reset(self, completely: bool=False):
		"""resets the menu to default values

		If completely isn't passed in, the default standard is to only reset -
		the items

		Parameters
		----------
		completely : Boolean, optional
			Set this flag to True to completely reset the menu, including all -
			sounds, flags, and items (default is False)

		Raises
		------
		MenuIsRunningError
			If the menu is currently running
		"""

		if self._running: raise MenuIsRunningError('The menu is currently running!')

		if completely: # reset all the menu variables to default values if `completely` is set to true, otherwise only reset the items list
			self._allows = 0
			self._sounds = { 'change_item': None, 'rollback': None, 'select': None, 'exit': None }
		# Clear the `items` dictionary and reset `position`
		self._position = 1
		self._items = [ None ]

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
			The type of sound: cancel, change_item, rollback, and select
		filename : string
			The file path of the sound source

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._sounds[sound] = filename

	def add_item(self, text: str, isFilename: bool=False):
		"""Adds a new item to the menu

		If `isFile` isn't passed in, the default standard is to treat the -
		contents as to be spoken by the speech engine

		Parameters
		----------
		text : String
			The contents of the item
		isFile : Boolean, optional
			Set this flag to True if the contents is a sound source (default is -
			False)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._items.append({ 'callback_function': None, 'text': text, 'is_filename': isFilename })

	def add_callback_function(self, callbackFunction: func, text: str, isFilename: bool=False):
		"""adds a user defined function to the menu -
			(e.g. a slider for a setting)

		If `isFile` isn't passed in, the default standard is to treat the -
		content label as to be spoken by the speech engine

		Parameters
		----------
		callbackFunction : User-Defined Function
			An external function
		text : String
			The content label
		isFile : Boolean, optional
			Set this flag to True if the content label is a sound source (default -
			is False)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._items[len(self._items) + 1] = {'callback_function': callbackFunction, 'text': text, 'is_filename': isFilename}

	def set_item(self, index: int, text: str, isFile: bool=False):
		"""Sets the contents of an item

		If `isFile` isn't passed in, the default standard is to treat the -
		contents as to be spoken by the speech engine

		Parameters
		----------
		index : Integer
			The index (location in the list) of the menu item
		text : String
			The contents of the item
		isFile : boolean : optional
			Set this flag to True if the contents is a sound source (default is -
			False)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')
		self._items[index]['text'] = text
		self._items[index]['is_file'] = isFile

	def get_item(self, index: int) -> str:
		"""Returns the item content

		Parameters
		----------
		index : Integer
			The index (location in the list) of the menu item
		"""

		return self._items[index]['text']

	def get_item_count(self) -> int:
		"""Returns the number of items in the menu"""

		return len(self._items) - 1

	def is_running(self) -> bool:
		"""Returns the state of the interface"""
		return self._running

	def run(self, intro: str, isFilename=False) -> int:
		"""Activates the interface

		If `isFile` isn't passed in, the default standard is to treat the -
		`intro` as to be spoken by the speech engine

		Parameters
		----------
		intro : String
			A short introduction
		isFile : boolean : optional
			Set this flag to True if the `intro` is a sound source (default is -
			False)
		"""

		return self.run_extended(intro, isFilename, 1, True)

	def run_extended(self, intro: str, isFilename: bool, startPosition: int, speakInitialItem=True) -> int:
		"""Activates the interface with additional properties

		If `isFile` isn't passed in, the default standard is to treat the -
		`intro` as to be spoken by the speech engine

		If `speakInitialItem` isn't passed in, the default standard is to -
		speak the initial item under the cursor after the menu loads

		Parameters
		----------
		intro : String
			A short introduction
		isFile : Boolean, optional
			Set this flag to True if the `intro` is a sound source (default is -
			False)
		startPosition : Integer
			The starting position of the cursor
		speakInitialItem : Boolean
			Set this flag to True if the initial item is to be spoken (default is -
			True)

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')

		position = startPosition # Set the cursor on the default item.
		self._running = True; # Set the menu as active.
		oldRepeat = pygame.key.get_repeat()[0] # Store the pygame key repeat state
		pygame.key.set_repeat() # Disable key repeat

		# Play the intro
		self.__present_item(intro, isFilename)

		# Play the default item selection
		if speakInitialItem:
			self.__present_item(self._items[position]['text'], self._items[position]['is_filename'])

		while self._running:
			time.sleep(.005) # Be kind to other processes

			for e in pygame.event.get(): # Query the event pool
				if pygame.key.get_pressed()[pygame.K_UP]:
					if position > 1:
						position -= 1
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
					elif self._allows - AudioBox.WRAP >= 0:
						position = len(self._items) - 1
						if self._sounds['rollback'] != None: sound_pool.play_stationary(self._sounds['rollback'])
					self.__present_item(self._items[position]['text'], self._items[position]['is_filename'])
				if pygame.key.get_pressed()[pygame.K_DOWN]:
					if position < len(self._items) - 1:
						position += 1
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
					elif self._allows - AudioBox.WRAP >= 0:
						position = 1
						if self._sounds['rollback'] != None: sound_pool.play_stationary(self._sounds['rollback'])
					self.__present_item(self._items[position]['text'], self._items[position]['is_filename'])
				if pygame.key.get_pressed()[pygame.K_LEFT]:
					if not self._items[position]['callback_function'] == None: self._items[position]['callback_function'](-1)
				if pygame.key.get_pressed()[pygame.K_RIGHT]:
					if not self._items[position]['callback_function'] == None: self._items[position]['callback_function'](1)
				if pygame.key.get_pressed()[pygame.K_HOME]:
					if self._allows == AudioBox.HOME_AND_END or self._allows == AudioBox.WRAP + AudioBox.HOME_AND_END or self._allows == AudioBox.ESCAPE + AudioBox.HOME_AND_END or self._allows == AudioBox.ALL:
						position = 1
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
						self.__present_item(self._items[position]['text'], self._items[position]['is_filename'])
				if pygame.key.get_pressed()[pygame.K_END]:
					if self._allows == AudioBox.HOME_AND_END or self._allows == AudioBox.WRAP + AudioBox.HOME_AND_END or self._allows == AudioBox.ESCAPE + AudioBox.HOME_AND_END or self._allows == AudioBox.ALL:
						position = self.get_item_count()
						if self._sounds['change_item'] != None: sound_pool.play_stationary(self._sounds['change_item'])
						self.__present_item(self._items[position]['text'], self._items[position]['is_filename'])
				if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
					self._running = False
				if pygame.key.get_pressed()[pygame.K_ESCAPE] and (self._allows == 1 or self._allows == 4 or self._allows == 6 or self._allows == 9):
					position = 0
					self._running = False

		if position == 0:
			if self._sounds['cancel'] != None: sound_pool.play_stationary(self._sounds['cancel'])
		else:
			if self._sounds['select'] != None: sound_pool.play_stationary(self._sounds['select'])
		pygame.key.set_repeat(oldRepeat)
		return position