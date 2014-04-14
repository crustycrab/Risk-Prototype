import pygame
import os
import random
import res

class Camera:

	def __init__(self):
		self.x = self.y = 0
		self.speed = 500

	def update(self, dt, key_state):
		speed = self.speed * dt
		if key_state[0]:
			self.x = min(self.x + speed, 0)
		if key_state[1]:
			self.x = max(self.x - speed, res.WIN_WIDTH - res.MAP_WIDTH)
		if key_state[2]:
			self.y = min(self.y + speed, 0)
		if key_state[3]:
			self.y = max(self.y - speed, res.WIN_HEIGHT - res.MAP_HEIGHT)

	def convert_pos(self, pos):
		return (pos[0] - self.x, pos[1] - self.y)

	def get_pos(self):
		return (self.x, self.y)

	def set_pos(self, pos):
		self.x, self.y = pos


class Hud:

	def __init__(self):
		pass



class Stars:

    def __init__(self, num_stars=256):
        self.num_stars = num_stars
        self.stars = []
        self.gen_stars()

    def draw(self, surface):
        for star in self.stars:
            pygame.draw.rect(surface, star['color'], star['rect'], 1)

    def update(self, dt):
        for i, star in enumerate(self.stars):
            speed = star['speed'] * dt
            x, y = star['rect'].topleft
            x -= speed
            if x < 0:
                x, y = (res.MAP_WIDTH + x, random.randint(0, res.MAP_HEIGHT))
            self.stars[i]['rect'].topleft = (int(x), y)

    def gen_stars(self):
        for _ in range(self.num_stars):
            x, y = self.get_random_cords()
            star = {'speed': random.randint(1, 100),
                    'rect': pygame.Rect((x, y), (random.randint(2, 4),) * 2),
                    'color': (random.randint(153, 204), random.randint(153, 204), random.randint(178, 229))}
            self.stars.append(star)

    def get_random_cords(self):
        return (random.randint(0, res.MAP_WIDTH - 1), random.randint(0, res.MAP_HEIGHT - 1))
