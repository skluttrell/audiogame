# Author: Stephen Luttrell

import lib.AudioBox as AudioBox
import menu.sounds as sounds

STANDARD_MENU = AudioBox.DynamicMenu(AudioBox.ALL)
STANDARD_MENU.set_sound('change_item', sounds.MENU_CHANGE_ITEM)
STANDARD_MENU.set_sound('rollback', sounds.MENU_ROLLBACK)
STANDARD_MENU.set_sound('select', sounds.MENU_SELECT)
STANDARD_MENU.set_sound('cancel', sounds.MENU_CANCEL)

def populate_menu(items):
	STANDARD_MENU.reset(False)
	for k in items.keys():
		STANDARD_MENU.add_item(k, items[k])