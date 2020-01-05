# Author: Stephen Luttrell

import lib.AudioBox as AudioBox
import menu.sounds as sounds

FILE_MENU = AudioBox.FileSelectionBox(AudioBox.ALL)
FILE_MENU.set_sound('pop', sounds.MENU_POP_UP)
FILE_MENU.set_sound('tab', sounds.MENU_TAB)
FILE_MENU.set_sound('cancel', sounds.MENU_CANCEL)
FILE_MENU.set_sound('select', sounds.MENU_SELECT)
FILE_MENU.set_sound('back', sounds.MENU_BACK)
FILE_MENU.set_sound('forward', sounds.MENU_FORWARD)
FILE_MENU.set_sound('change_item', sounds.MENU_CHANGE_ITEM)
FILE_MENU.set_sound('rollback', sounds.MENU_ROLLBACK)
FILE_MENU.set_sound('alert', sounds.MENU_ALERT)