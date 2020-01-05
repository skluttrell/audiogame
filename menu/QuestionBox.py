# Author: Stephen Luttrell

import lib.AudioBox as AudioBox
import menu.sounds as sounds

QUESTION_BOX = AudioBox.SimpleQuestionBox()
QUESTION_BOX.set_sound('pop', sounds.MENU_POP_UP)
QUESTION_BOX.set_sound('tab', sounds.MENU_TAB)
QUESTION_BOX.set_sound('select', sounds.MENU_SELECT)