# Author: Stephen Luttrell

from lib.sound_pool import sound_pool
import pygame
import speech
import time

class SimpleInputBox:
	"""
	An input box interface which returns user input

	Attributes
	----------
	buttons : List
		A list of available interface buttons
	running : boolean
		The state of the interface
	sounds : dictionary : optional
		A dictionary of interface sounds: cancel, change_item, rollback, and -
		select

	Methods
	-------
	is_running()
		returns the state of the interface
	run(intro, numbersOnly, text)
		Activates the interface
	set_sound(sound, filename)
		Sets the interface sounds
	"""

	def __init__(self):
		"""
		buttons : List
			A list of available interface buttons
		running : boolean
			The state of the interface
		sounds : dictionary : optional
			A dictionary of interface sounds: cancel, change_item, rollback, and -
			select
		"""
		self._buttons = ['ok', 'clear', 'cancel'] # The buttons for the input box
		self._sounds = { 'pop': '', 'typing': '', 'select': '', 'cancel': '', 'tab': '' }
		self._running = False

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

	def is_running(self) -> bool:
		"""Returns the state of the interface"""
		return self._running

	def run(self, intro: str, numbersOnly: bool=False, text: str='') -> int or str:
		"""Activates the interface

		If `numbersOnly` isn't passed in, the default behavior is to allow any -
		alphanumeric input

		If `text` isn't passed in, the default behavior is to start with a -
		blank input string

		Parameters
		----------
		intro: String
			A short introduction
		numbersOnly : Boolean, optional
			An optional flag to only allow integers to be entered (default is False)
		text : String, optional
			An optional default text string

		raises
		------
		InterfaceIsRunningError
			If the interface is currently running
		"""

		if self._running: raise InterfaceIsRunningError('The interface is currently running!')

		self._running = True
		text = ''
		position = len(text) # The cursor position
		buttonPosition = 0 # The currently selected button
		char = 0
		pitch = speech.get_pitch()
		oldRepeat = pygame.key.get_repeat()[0]
		pygame.key.set_repeat()

		if self._sounds['pop'] != None: sound_pool.play_stationary(self._sounds['pop'])
		speech.speak(intro)

		while self._running:
			time.sleep(.005) # Be kind to processors

			for e in pygame.event.get(): # Check the event pool
				# Text entry keys
				if e.type == pygame.KEYDOWN:
					if pygame.K_SPACE <= e.key <= pygame.K_z:
						if e.key == pygame.K_c and (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
							pyperclip.copy(text)
							speech.speak('text copied')
						elif e.key == pygame.K_v and (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
							text += pyperclip.paste()
							speech.speak(text)
						else: # Standard entry
							if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]) and not numbersOnly:
								if e.key == pygame.K_1: char = 33 # Exclaim
								if e.key == pygame.K_QUOTE: char = 34 # Double quote
								elif e.key == pygame.K_3: char = 35 # Pound sign
								elif e.key == pygame.K_4: char = 36 # Dollar sign
								elif e.key == pygame.K_5: char= 37 # Percent sign
								elif e.key == pygame.K_7: char= 38 # Ampersand sign
								elif e.key == pygame.K_9: char= 40 # Left parenthesis
								elif e.key == pygame.K_0: char= 41 # Right parenthesis
								elif e.key == pygame.K_8: char= 42 # Asterik sign
								elif e.key == pygame.K_EQUALS: char = 43 # Plus sign
								elif e.key == pygame.K_SEMICOLON: char = 58 # Colon
								elif e.key == pygame.K_COMMA: char = 60 # Less-than
								elif e.key == pygame.K_PERIOD: char = 62 # Greater-than
								elif e.key == pygame.K_SLASH: char = 63 # Question mark
								elif e.key == pygame.K_2: char = 64 # At sign
								elif e.key == pygame.K_6: char= 94 # Caret sign
								elif e.key == pygame.K_MINUS: char = 95 # Underscore
								elif e.key == pygame.K_LEFTBRACKET: char = 123 # Left brace
								elif e.key == pygame.K_BACKSLASH: char = 124 # Vertical bar
								elif e.key == pygame.K_RIGHTBRACKET: char = 125 # Right Brace
								elif e.key == pygame.K_BACKQUOTE: char = 126 # Tilda
								else: char = e.key - 32 # Capitalize the character
							else: # Without shift pressed
								if not numbersOnly: char = e.key
								elif pygame.K_0 <= e.key <= pygame.K_9: char = e.key

					# Add the new character to the text string
					if char > 0:
						if self._sounds['typing'] != None: sound_pool.play_stationary(self._sounds['typing'])
						if position == 0: text = chr(char) + text[:len(text)] # The cursor is at the beginning of the string
						elif position == len(text) - 1: text = text + chr(char) # The cursor is at the end of the string
						else: text = text[0:position] + chr(char) + text[position:len(text)] # The cursor is somewhere between the first and last character
						position += 1

				# User interface keys
				if pygame.key.get_pressed()[pygame.K_UP]:
					if text != '': speech.speak(text)
					else: speech.speak('blank')
				if pygame.key.get_pressed()[pygame.K_RIGHT]:
					if len(text) > 0:
						if position < len(text): position += 1
						if position == len(text): speech.speak('end of text')
						else: char = ord(text[position])
					else:
						speech.speak('please enter some text')
				if pygame.key.get_pressed()[pygame.K_LEFT]:
					if len(text) > 0:
						if position > 0: position -= 1
						char = ord(text[position])
					else:
						speech.speak('please enter some text')
				if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
					if position > 0:
						if self._sounds['typing'] != None: sound_pool.play_stationary(self._sounds['typing'])
						speech.set_pitch(speech.get_pitch() - 10)
						speech.speak(text[position - 1])
						if position == 1: text = text[1:] # The cursor is on the second character
						elif position == len(text): text = text[:-1] # The cursor is at the end
						else: text = text[:position - 1] + text[position:] # The cursor is anywhere else
						position -= 1
				if pygame.key.get_pressed()[pygame.K_HOME]:
					if len(text) > 0:
						position = 0
						speech.speak('beginning of text')
					else:
						speech.speak('please enter some text')
				if pygame.key.get_pressed()[pygame.K_END]:
					if len(text) > 0:
						position = len(text)
						speech.speak('end of text')
					else:
						speech.speak('please enter some text')
				if pygame.key.get_pressed()[pygame.K_TAB]:
					if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
						if buttonPosition > 0: buttonPosition -= 1 # Reverse through the tab order
						else: buttonPosition = len(self._buttons) - 1 # Go to the end of the tab order
					else: # Shift is not pressed
						if buttonPosition < len(self._buttons) - 1: buttonPosition += 1 # Advance through the tab order
						else: buttonPosition = 0 # return to the beginning of the tab order
					if self._sounds['tab'] != None: sound_pool.play_stationary(self._sounds['tab'])
					speech.speak(self._buttons[buttonPosition]) # Announce the current button selection
				if pygame.key.get_pressed()[pygame.K_RETURN]:
					if self._buttons[buttonPosition] == 'ok':
						if self._sounds['select'] != None: sound_pool.play_stationary(self._sounds['select'])
						self._running = False
					elif self._buttons[buttonPosition] == 'clear':
						text = ''
					elif self._buttons[buttonPosition] == 'cancel':
						if self._sounds['cancel'] != None: sound_pool.play_stationary(self._sounds['cancel'])
						text = ''
						self._running = False
				if pygame.key.get_pressed()[pygame.K_ESCAPE]:
					if self._sounds['cancel'] != None: sound_pool.play_stationary(self._sounds['cancel'])
					text = ''
					self._running = False

				# Speak the character
				if pygame.K_a - 32 <= char <= pygame.K_z - 32: speech.set_pitch(speech.get_pitch() + 10) # Raise pitch for capitals
				speech.speak(chr(char))

			# FINALLY: return pitch and char to baseline
			if speech.get_pitch() != pitch: speech.set_pitch(pitch)
			char = 0

		pygame.key.set_repeat(oldRepeat)
		if numbersOnly:
			if text == '': return 0
			return int(text)
		return text