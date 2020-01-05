# Author: Stephen Luttrell

import lib.AudioBox as AudioBox
import menu.sounds as sounds

INPUT_BOX = AudioBox.SimpleInputBox()
INPUT_BOX.set_sound('pop', sounds.MENU_POP_UP)
INPUT_BOX.set_sound('tab', sounds.MENU_TAB)
INPUT_BOX.set_sound('typing', sounds.MENU_TYPING)
INPUT_BOX.set_sound('cancel', sounds.MENU_CANCEL)
INPUT_BOX.set_sound('select', sounds.MENU_SELECT)