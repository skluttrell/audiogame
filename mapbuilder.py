# Author: Stephen Luttrell

import copy, os, pygame, shapes, speech, sys, time, utilities
import lib.AudioBox as AudioBox
from lib.AudioBox import window
import lib.GameObject as GameObject
from menu.StandardMenu import populate_menu
from menu import STANDARD_MENU, INPUT_BOX

from lib.sound_pool import sound_pool

def start_menu():
	STANDARD_MENU.reset(False)
	STANDARD_MENU.allow(AudioBox.ALL - AudioBox.ESCAPE)
	populate_menu({ 'new project': False, 'load project': False, 'settings': False, 'exit': False })
	choice = STANDARD_MENU.run('map builder main menu', False)
	if choice == 1: # new project
		msg = 'Please enter a project name.'
		while True:
			projectName = INPUT_BOX.run(msg)
			if projectName == '': break
			if not os.path.exists(os.path.join('projects\\', projectName)): break
			msg = 'That project name already exists. Please enter a different project name.'
		if projectName != '':
			newMap = new_map_menu()
			if newMap:
				GAME_DATA['maps'].clear()
				GAME_DATA['maps'].append(newMap)
				#os.mkdir(os.path.join('projects\\', projectName))
				map_editor(GAME_DATA['maps'][0])
		start_menu()
	elif choice == 2: # load project
		print('load project')
		#retrieve_data(FILE_MENU.run())
		#map_editor(GAME_DATA['maps'][0])
		start_menu()
	elif choice == 3: # settings
		settings_menu('start')

def new_map_menu() -> GameObject.Map:
	newMap = GameObject.Map('new map')
	width = 0
	height = 0
	defaultTile = 0
	STANDARD_MENU.reset(False)
	STANDARD_MENU.allow(AudioBox.ALL)
	populate_menu({ 'name: ' + newMap.name: False, 'height: ' + str(height): False, 'width: ' + str(width): False, 'starting tile set: ' + GameObject.TILE_TYPES[defaultTile]: False, 'create the map': False, 'cancel': False })
	choice = STANDARD_MENU.run('create a new map', False)
	while choice != STANDARD_MENU.get_item_count() - 1 or height == 0 or width == 0:
		if choice == 0 or choice == STANDARD_MENU.get_item_count():
			return None
		elif choice == 1: # name
			newMap.name = INPUT_BOX.run('Please enter the name of the map.')
			STANDARD_MENU.set_item(1, 'name: ' + newMap.name)
		elif choice == 2: # height
			height = INPUT_BOX.run('Enter the maps height.', True)
			STANDARD_MENU.set_item(2, 'height: ' + str(height))
		elif choice == 3: # width
			width = INPUT_BOX.run('Enter the maps width.', True)
			STANDARD_MENU.set_item(3, 'width: ' + str(width))
		elif choice == 4: # default tile set
			tileMenu = copy.copy(STANDARD_MENU)
			tileMenu.reset(False)
			for t in GameObject.TILE_TYPES:
				tileMenu.add_item(t, False)
			newTileSet = tileMenu.run('Please choose which tile set to start the new map with.')
			if newTileSet > 0:
				defaultTile = newTileSet - 1
				STANDARD_MENU.set_item(4, 'default tile set: ' + GameObject.TILE_TYPES[defaultTile], False)
			tileMenu = None
		choice = STANDARD_MENU.run_extended('new map', False, choice)
	newMap.initialize(GameObject.Tile(type=defaultTile, description=None, sequence=None, solidity=1, durability=None, items=None, rarity=None, keys=None, quests=None, ambient=None, gotoCoords=None, location=None), width, height)
	return newMap

def settings_menu(prevMenu):
	STANDARD_MENU.reset(False)
	STANDARD_MENU.allow(AudioBox.ALL)
	STANDARD_MENU.add_callback_function(utilities.tts_change_volume, 'volume', False)
	STANDARD_MENU.add_callback_function(utilities.tts_change_rate, 'rate', False)
	STANDARD_MENU.add_item('save and return to previous menu', False)
	choice = STANDARD_MENU.run('settings', False)
	if choice == 3:
		utilities.save_data([ utilities.SPEECH_VOLUME, utilities.SPEECH_RATE ], 'settings.dat')
		if prevMenu == 'start':
			start_menu()

def mapbuilder_menu():
	STANDARD_MENU.reset(False)
	STANDARD_MENU.allow(AudioBox.ALL)
	populate_menu({ 'edit map name': False, 'add tiles': False, 'set start position': False, 'settings': False, 'save map': False, 'load map from project': False, 'add new map': False, 'load project': False, 'back to editor': False, 'back to start menu': False, 'quit editor': False })
	choice = STANDARD_MENU.run('mapbuilder menu', False)

def map_editor(map):
	quit = False
	player.x = map.get_attribute('start')[0]
	player.y = map.get_attribute('start')[1]
	yAxis = 0
	xAxis = 0
	oldTime = time.time()
	pygame.key.set_repeat(50)

	while not quit:
		time.sleep(.005) # Be kind to processors

		for e in pygame.event.get():
			if pygame.key.get_pressed()[pygame.K_UP]: yAxis = 1
			if pygame.key.get_pressed()[pygame.K_DOWN]: yAxis = -1
			if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]: yAxis = 0
			if pygame.key.get_pressed()[pygame.K_RIGHT]: xAxis = 1
			if pygame.key.get_pressed()[pygame.K_LEFT]: xAxis = -1
			if not pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]: xAxis = 0

			if not xAxis == 0 or not yAxis == 0:
				if time.time() - oldTime >= player.get_attribute('walk_speed'):
					oldTime = time.time()
					if not player.collision(player.x + xAxis, player.y + yAxis, map):
						player.x += xAxis
						player.y += yAxis
						dir = 'sounds\\footsteps\\' + GameObject.TILE_TYPES[map.get_tile(player.x, player.y).get_attribute('type')]
						footstep = dir + '\\' + str(utilities.get_random(dir)) + '.wav'
						sound_pool.play_stationary(footstep)
					else:
						speech.speak('bump')

			if pygame.key.get_pressed()[pygame.K_z]: speech.speak(str(player.x) + ': ' + str(player.y))
			if pygame.key.get_pressed()[pygame.K_ESCAPE]: quit = True #mapbuilder_menu()

if __name__ == '__main__':
	GAME_DATA = { 'maps': [] }
	player = GameObject.Actor()
	player.set_attribute('walk_speed', .35)
	if os.path.exists('settings.dat'):
		s = utilities.retrieve_data('settings.dat')
		utilities.SPEECH_VOLUME = s[0]
		speech.set_volume(utilities.SPEECH_VOLUME)
		utilities.SPEECH_RATE = s[1]
		speech.set_rate(utilities.SPEECH_RATE)
	window('Map Builder')
	start_menu()

	print('done')
	sys.exit(0)