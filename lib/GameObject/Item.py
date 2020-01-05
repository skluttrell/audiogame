# Author: Stephen Luttrell

from lib.GameObject.GameObject import GameObject

class Item(GameObject):
	def __init__(self, name=''):
		self.name = name
		'''
		description: String, a description of the weapon
		rarity: String, how rare the item is such as common up to legendary
		set name: String, name of the set to which the armor pice belongs
		set total: Integer, the number of pieces in the set
		set bonus: List, the bonuses the set provides when all its pieces are united
		vitality: Integer, amount of vitality restored by a potion
		mana: Integer, amount of mana restored by a potion
		weight: String, the weight class of a weapon used in damage calculations: Light, Medium, Heavy, Epic
		ammo: String, the type of ammo it uses
		damage: Tuple, damage minimum, maximum
		defense: Integer, the amount of defense provided by an armor piece
		type: String, damage type: bludgeoning, piercing, slashing
		category: String, the category of item such as armor, weapon, potion, or other
		armor piece: String, body part that the piece is designed for such as boots, body, head, etc
		range: Integer, range of the weapon in tiles
		secondary skill effect: List, a secondary skill effect such as lightning or fire, chance percent
		secondary status effect: List, A secondary status effect such as stun or dazed, chance percent
		The following are all optional player requirements, Integers representing level: level, strength, accuracy, knowledge.
		cost: Integer, cost in game money
		'''
		self._attributes = { 'description': None, 'rarity': None, 'set name': None, 'set_total': None, 'set_bonuses': None, 'vitality': None, 'mana': None, 'weight': None, 'ammo': None, 'damage': None, 'defense': None, 'type': None, 'category': None, 'armor_piece': None, 'range': None, 'secondary_skill_effect': None, 'secondary_status_effect': None, 'level': None, 'strength': None, 'accuracy': None, 'knowledge': None, 'cost': None, }