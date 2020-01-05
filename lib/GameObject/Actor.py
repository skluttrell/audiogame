# Author: Stephen Luttrell

from lib.GameObject.GameObject import GameObject
from math import pow, ceil, floor

class Actor(GameObject):
	def __init__(self, name=''):
		self.name = name
		self.x = 0
		self.y = 0
		'''
		override: Boolean, allows game calculations to be overwritten with special, monster specific, ones
		Vitality: Integer, a creature's health: usually done with a calculation based on strength unless overwritten
		mana: Integer, a creature's ability to use magic: usually done with a calculation based on knowledge unless overwritten
		strength: Integer, applies to whether a mundain melee attack hits and how much damage it does
		constitution: Integer, determines vitality
		agility: Integer, applies to defense of mundain attacks
		accuracy: Integer, applies to whether a mundain ranged attack hits and how much damage it does
		speed: Integer, applies to how often you can carry out mundain melee and ranged attacks and their potential to hit opponents
		knowledge: Integer, applies to how much damage spells do, how much Eldritch power you have and how fast it recovers
		,luck: Integer, a minor potential boost to various actions
		class: String, the player's class: Weapons Master, Eldritch Infuser, and Spellmonger
	The following are all Items representing the name of an armor the creature is wearing or weapon they are holding: main hand, off hand, head, shoulders, body, hands, belt, legs, feet, fingers
		skills: Skill, the skills available to the player
		status effects: StatusEffect, any buffs or debuffs effecting the creature
		inventory: Items, items the creature is carying
		gold: Integer, the amount of gold the creature is carying
		path: List of Tuples, if the creature is computer controlled, these are coordinates representing the points of its path (ending the path with the same coordinates that started the path will make it a circuit, otherwise it will move back and forth along the path).
		walk_speed: Float, The speed with which a character moves on the map
		'''
		self._attributes = { 'override': False, 'current_vitality': None, 'max_vitality': None, 'mana': None, 'strength': None, 'constitution': None, 'agility': None, 'accuracy': None, 'speed': None, 'knowledge': None,'luck': None, 'class': None, 'main_hand': None, 'off_hand': None, 'head': None, 'shoulders': None, 'body': None, 'hands': None, 'belt': None, 'legs': None, 'feet': None, 'fingers': None, 'skills': None, 'status_effects': None, 'inventory': None, 'gold': None, 'path': None, 'walk_speed': None }
		self._formulas = { 'defense': None, 'to_hit': None, 'damage': None, 'vitality': None, 'eldritch_power': None, 'eldritch_power_regen': None }
		self._target = None

	def __formula(fma):
		fma = fma.replace(' ', '') # remove any spaces

		# replace the variables with their respective stat numbers
		p = []
		r = []
		for i in range(0, len(fma)):
			if fma[i] == '%': p.append(i)
		for i in range(0, len(p), 2):
			if not fma[p[i] + 1:p[i + 1]] in r: r.append(fma[p[i] + 1:p[i + 1]])
		for i in r:
			if not i[0] == 't': fma = fma.replace('%' + i + '%', str(self._attributes[i]))
			else: fma = fma.replace('%' + i + '%', str(self._target[i]))

		# replace exponents with pow
		e = []
		exp = []
		for i in range(0, len(fma)):
			if fma[i] == '^': e.append(i)
		for i in e:
			temp = ""
			for ii in range(len(fma[:i - 1]), -1, -1):
				if fma[ii].isdigit(): temp += fma[ii]
				else: break
			exp.append(temp[len(temp)::-1])
			temp = ''
			for ii in range(i + 1, len(fma)):
				if fma[ii].isdigit(): temp += fma[ii]
				else: break
			exp.append(temp)
		for i in range(0, len(exp), 2): fma = fma.replace(exp[i] + '^' + exp[i + 1], 'pow(' + exp[i] + ',' + exp[i + 1] + ')')

		return eval(fma, { '__builtins__': None }, { 'pow': pow, 'round': round, 'ceil': ceil, 'floor': floor })

	def set_formula(self, type, value): self._formulas[type] = value # Set or add (if it does not already exist) a formula  to the formulas dictionary: type is the formula reference name (unique identifier), value is the new value to update the formula with
	def get_formula(self, type): return self._formulas[type] # Returns the value of a formula
	def set_target(monster): self._target = { 'name': monster.name, 'current_vitality': monster.get_attribute('current_vitality'), 'max_vitality': monster.get_attribute('max_vitality'), 'strength': monster.get_attribute('strength'), 'constitution': monster.get_attribute('constitution'), 'agility': monster.get_attribute('agility'), 'accuracy': monster.get_attribute('accuracy'), 'speed': monster.get_attribute('speed'), 'knowledge': monster.get_attribute('knowledge'), 'luck': monster.get_attribute('luck') }
	def get_target_stats(type):
		if type == 'current_vitality':
			if self._target['max_vitality']: max = self._target['max_vitality']
			else: max = self._formulas['tvitality']
			if 1 < self._target['current_vitality'] / max < 20: return 'critically hurt'
			elif 21 < self._target['current_vitality'] / max < 40: return 'very hurt'
			elif 41 < self._target['current_vitality'] / max < 60: return 'wounded'
			elif 61 < self._target['current_vitality'] / max < 80: return 'injured'
			elif 81 < self._target['current_vitality'] / max < 99: return 'minor injuries'
			else: return 'uninjured'
		return self._target[type]
	def remove_target(): self._target = None

	def collision(self, x, y, m):
		collision = True

		if x >= 0 and y >= 0 and x < m.get_width() and y < m.get_height(): collision = False
		if not collision:
			collision = m.get_tile(x, y).get_attribute('solidity') == 10

		return collision