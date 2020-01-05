import pygame

def window(text = '', width = 640, height = 480):
	if (text == ''):
		title = 'Game Title'
	else:
		title = text

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption(title)
	backgroundColor = (0, 0, 0)
	screen.fill(backgroundColor)
	pygame.display.flip()