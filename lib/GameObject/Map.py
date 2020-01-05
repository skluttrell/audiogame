# Author: Stephen Luttrell

from lib.GameObject import GameObject
import os

# Tile types
TILE_TYPES = []
if os.path.isdir('sounds\\footsteps'):
	for entry in os.listdir('sounds\\footsteps'):
		TILE_TYPES.append(entry)

class Map(GameObject):
	def __init__(self, name):
		self.name = name
		self._width = 0 # Width (x-axis) of the map area
		self._height = 0 # Height (y-axis) of the map area
		self._tiles = []
		self._field = {} # Dictionary of x and y
		'''
		music: String, file path of the map's music
		sequence: List, a sequence to play upon  loading (text (String), is_file (Boolean), play_once (Boolean), played (Boolean))
		start: Tuple, The starting coordinates of the map
		'''
		self._attributes = { 'music': None, 'sequence': None, 'start': (0, 0) }

	def initialize(self, newTile, width, height):
		if width == 0: width = 1
		if height == 0: height = 1

		if len(self._tiles) > 0: self.tiles.clear()
		if len(self._field) > 0: self.field.clear()

		# Set all the tiles in the field to newTile
		self._field = list(range(width))
		for w in range(0, width):
			self._field[w] = list(range(height))
			for h in range(0, height):
				self.set_tile(w, h, newTile)

		self._width = width
		self._height = height

	# Expands the map
	# def grow(self, newTile, XAxis, YAxis):

	# Trims the map down
		# def trim(self, XAxis, YAxis):

	def set_width(self, value): self._width = value
	def get_width(self): return self._width
	def set_height(self, value): self._height = value
	def get_height(self): return self._height
	def get_tile(self, x, y): return self._tiles[self._field[x][y]] # Returns a tile at the x and y location

	# Places a a tile index in the field
	def set_tile(self, x, y, newTile):
		index = self._tile_exists(newTile) # Check the new tile against the tiles list
		if index == -1: # Create a new tile in the tiles list
			self._tiles.append(newTile)
			self._field[x][y] = len(self._tiles) - 1
		else: # Use the index of the existing tile in the tiles list
			self._field[x][y] = index

	# Check to see if the tile exists in the tiles list
	# Returns -1 if the tile does not exist or the index if it does (0 to the length of the tiles list)
	def _tile_exists(self, newTile):
		count = 0 # Counts the number of matches found
		index = 0 # The index of the tile in tiles being examined

		if not len(self._tiles) == 0: # The tiles list is not empty
			for t in self._tiles: # Each tile in the tiles list
				for k in t.get_attributes(): # Examine each tile attribute against the new one
					if t.get_attribute(k) == newTile.get_attribute(k): # the attribute of the new tile is equal to the current one from the tiles list
						count += 1 # Increase the counter because of the match
				if count == len(t.get_attributes()): # If the number of matches equals the number of attributes in the tile than these two tiles are the same
					return index
				else:
					count = 0 # Reset the match counter for the next tile in the tiles list
					index += 1

		return -1 # If the new tile did not match any of the tiles in the tiles list

# A class to set up a tile as an object to hold any information the game needs to store about it
class Tile(GameObject):
	def __init__(self, type: int=None, description: str=None, sequence: list=None, solidity: int=None, durability: int=None, items: list=None, rarity: int=None, keys: list=None, quests: list=None, ambient: str=None, gotoCoords: tuple=None, location: str=None):
		'''
		type: Integer, the type of tile (i.e. water, dirt, stone, etc.)
		description: String, a description of the tile
		sequence: List, a sequence to play upon triggering a tile (text (String), is_file (Boolean), play_once (Boolean), played (Boolean))
		solidity: Integer, describes how passable the tile is (i.e. 1 does not block a player or monster... 10 completely closes off passage like a wall)
		durability: Integer, The tiles hit points to break it (set to negative 1 for unbreakable, anything above 0 is how much damage needs to be done to the tile to break it, 0 means the tile is rubble and allows unfettered passage)
		items: List, a list of items contained by the tile
		rarity: Integer, the rarity of the items in this container (for random loot)
		keys: List, any keys or items needed to unlock the tile
		quests: List, a list of quests required to unlock the tile
		ambient: String, the location of an ambient sound file if the tile makes a continuous noise like birds or crickets
		goto: List, a pair of coordinates if this tile is a transporter
		location: string, the file path of the file which is to be loaded upon triggering a transport
		'''
		self._attributes = { 'type': type, 'description': description, 'sequence': sequence, 'solidity': solidity, 'durability': durability, 'items': items, 'rarity': rarity, 'keys': keys, 'quests': quests, 'ambient': ambient, 'goto': gotoCoords, 'location': location }