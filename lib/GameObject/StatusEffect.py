# Author: Stephen Luttrell

from lib.GameObject.GameObject import GameObject

class StatusEffect(GameObject):
	def __init__(self, name=''):
		self.name = name
		'''
		strength: Integer, effect plus or minus
		constitution: Integer, effect plus or minus
		agility: Integer, effect plus or minus
		accuracy: Integer, effect plus or minus
		speed: Integer, effect plus or minus
		knowledge: Integer, effect plus or minus
		luck: Integer, effect plus or minus
		duration: Integer, how long the effect lasts
		'''
		self._attributes = { 'strength': None, 'constitution': None, 'agility': None, 'accuracy': None, 'speed': None, 'knowledge': None, 'luck': None, 'duration': None }