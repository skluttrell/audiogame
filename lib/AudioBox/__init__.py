# Author: Stephen Luttrell
"""Provides an audio only interface for menus and basic popups

Fixed Constants
---------------
ESCAPE : integer, 1
	Sets the escape keyboard key to exit the current focus
HOME_AND_END : integer, 3
	Sets the home and end keyboard keys to jump the cursor to the top or bottom of a menu respectively
WRAP : integer, 5
	Sets the cursor to return to the top or bottom of a menu when the selection limits have been reached
ALL : integer, 9
	Sets all the above parameters to be in effect

Classes
-------
DynamicMenu
	a basic audio menu with vertical selections
FileSelectionBox
	A file selector that queries the file structure and allows files or -
	directories to be selected
SimpleInputBox
	A popup for entering text or integers
SimpleDialogueBox
	A popup window which provides information to the user and a button to -
	close the popup
SimpleQuestionBox
	A popup window containing a yes or no question

Module Functions
----------------
Window
	displays a basic pygame window which advises the user that this is an -
	audio only program

Required External Packages
--------------------------
accessible_output2
pygame
sound_lib
time
types
"""

# Used in the menu classes to set cursor behavior
ESCAPE = 1
HOME_AND_END = 3
WRAP = 5
ALL = 9

from .DynamicMenu import DynamicMenu
from .FileSelectionBox import FileSelectionBox
from .SimpleInputBox import SimpleInputBox
from .SimpleDialogueBox import SimpleDialogueBox
from .SimpleQuestionBox import SimpleQuestionBox
from .Window import window