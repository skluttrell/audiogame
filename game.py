# Author: Stephen Luttrell

import GameObject, openbox, pygame, shapes, speech, sys, utilities
from sound_pool import sound_pool

if __name__ == '__main__':
	WMSkill1 = GameObject.Skill('Martial Dash')
	WMSkill1.set_attribute('damage_multiplier', .5)
	WMSkill1.set_attribute('move_to_tile', True)
	WMSkill1.set_attribute('secondary_status_effect', 'stun')
	WMSkill1.set_attribute('cool_down', 60)
	stun = GameObject.StatusEffect('stun')
	stun.set_attribute('speed', 0)
	stun.set_attribute('duration', 2)
	shortsword = GameObject.Item('shortsword')
	shortsword.set_attribute('description', 'A basic shortsword.')
	shortsword.set_attribute('damage', (1, 6))
	shortsword.set_attribute('type', 'piercing')
	shortsword.set_attribute('range', 1)
	shortsword.set_attribute('weight', 'light')
	p = GameObject.Actor('Stephen')
	p.set_attribute('skills', [ WMSkill1 ])
	p.set_attribute('inventory', [ shortsword ])
	p.set_attribute('main_hand', shortsword)
	m = GameObject.Actor('Monster')
	m.set_attribute('override', True)

	print(p, m)
	for s in p.get_attribute('skills'):
		print(s)

	print('done')
	sys.exit()