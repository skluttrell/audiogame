# Author: Stephen Luttrell

from lib.GameObject.GameObject import GameObject

class Skill(GameObject):
	def __init__(self, name=''):
		self.name = name
		'''
		description: String, description of skill
		type: String, type of effect such as elemental, weapon, or vitality
		level restriction: Integer, restricted to a certain level or above
		skill restriction: List, requires certain skills
		move to target tile: Boolean, True moves the player to that tile (e.g. teleport and dash)
		bonus multiplier: Integer, used in place of effect bonus if the skill multiplies something instead
		effect bonus: Tuple, one time bonus min and max
		ebot: effect bonus Over Time: tuple, amount of damage, lasting time
		range: Integer, range in tiles
		aoe: Area of Effect, integer, radius from center tile
		secondary effect: List, A secondary skill effect such as stun or dazed, chance percent
		casting time: Integer, build up time for the skill in seconds
		cool down: Integer, Time until next available cast in seconds
		duration: Integer, how long the effect lasts
		'''
		self._attributes = { 'description': None, 'type': None, 'move_to_tile': None, 'bonus_multiplier': None, 'bonus_effect': None, 'ebot': None, 'range': None, 'aoe': None, 'secondary_status_effect': None, 'casting_time': None, 'cool_down': None, 'duration': None }