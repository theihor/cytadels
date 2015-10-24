# -*- coding:utf-8 -*-

import pygame, sys

SIZE = (640, 480)

# create window
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Citadels')
# work display
screen = pygame.Surface(SIZE)
done = True
pygame.key.set_repeat(1, 1)

class Menu:
	"""docstring for Menu"""
	def __init__(self, items = [120, 140, u'Item', (250, 250, 30), (250, 30, 250)]):
		self.items = items
	
	def render(self, surface, font, num_item):
		for i in self.items:
			if num_item == i[5]:
				surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
			else:
				surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
	
	def menu(self):
		done = True
		pygame.font.init()
		font_menu = pygame.font.Font('fonts/OldEnglishFive.ttf', 50)
		pygame.key.set_repeat(0, 0)
		item = 0
		while done:
			screen.fill((50, 50, 50))

			mp = pygame.mouse.get_pos()
			for i in self.items:
				if mp[0]>i[0] and mp[0]<i[0]+165 and mp[1]>i[1] and mp[1]<i[1]+50:
					item = i[5]
			self.render(screen, font_menu, item)

			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					sys.exit()
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						sys.exit()
					if e.key == pygame.K_UP:
						if item > 0:
							item -= 1
					if e.key == pygame.K_DOWN:
						if item < len(self.items) - 1:
							item += 1
				if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
					if item == 0:
						done = False
					elif item == 1:
						sys.exit()

			window.blit(screen, (0, 0))
			pygame.display.flip()

items = [(SIZE[0]/2-105, 140, u'Play', (10, 50, 73), (42, 40, 66), 0),
		 (SIZE[0]/2-105, 210, u'Quit', (10, 50, 73), (42, 40, 66), 1)]
game = Menu(items)
game. menu()

