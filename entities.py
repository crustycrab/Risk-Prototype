import math
import random
import pygame
import itertools
import res
import utils


class Planet(pygame.sprite.Sprite):

    def __init__(self, image, rect, union=False, enemy=False):
        super(Planet, self).__init__()

        self.image = image
        self.surface_to_blit = self.image.copy()
        self.select_cycle = itertools.cycle(
            range(191, 63, -3) + range(64, 191, 3))

        self.rect = rect
        self.selected = False
        self.radius = self.rect.w / 2.5

        self.union_units = 0.0
        self.enemy_units = 0.0

        self.time_to_up = 0

    def draw(self, surface):
        if self.selected:
            self.surface_to_blit = res.get_alpha_surface(
                self.image, alpha=next(self.select_cycle))
        if self.is_union():
            pygame.draw.arc(surface, res.GREEN, self.rect, 0, math.pi * 2)
        elif self.is_enemy():
            pygame.draw.arc(surface, res.BLUE, self.rect, 0, math.pi * 2)
        elif self.is_warzone():
            pygame.draw.arc(surface, res.RED, self.rect, 0, math.pi * 2)
        surface.blit(self.surface_to_blit, self.rect)

    def update(self, delta):
    	self.time_to_up += delta
    	if self.time_to_up >= 2:
    		if self.is_union():
    			self.union_units += 0.1
    		if self.is_enemy():
    			self.enemy_units += 0.1
    		self.time_to_up -= 2

    def collide_with(self, obj):
        distance_to_collide = self.radius + obj.radius
        actual_distance = math.hypot(
            self.rect.centerx - obj.rect.centerx, self.rect.centery - obj.rect.centery)
        return actual_distance <= distance_to_collide

    def collide_with_point(self, pos):
        pointx, pointy = pos
        distance = math.hypot(
            self.rect.centerx - pointx, self.rect.centery - pointy)
        return distance <= self.radius

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False
        self.surface_to_blit = self.image.copy()

    def set_side(self, enemy=False, union=False):
        if union:
            self.union_units = round(self.radius / 10, 1)
            self.enemy_units = 0.0
        if enemy:
            self.enemy_units = round(self.radius / 10, 1)
            self.union_units = 0.0

    def is_union(self):
        return self.union_units > 0 and self.enemy_units == 0

    def is_enemy(self):
        return self.enemy_units > 0 and self.union_units == 0

    def is_warzone(self):
        return self.union_units > 0 and self.enemy_units > 0

    def get_pos(self):
        return self.rect.center


class Landing(pygame.sprite.Sprite):

    def __init__(self, union=True):
        self.image = res.ships['union'] if union else res.ships['enemy']
        self.rect = self.image.get_rect()
        self.radius = self.rect.w / 2

        self.union = union

        self.velocity = utils.Vector2()
        self.x, self.y = self.rect.center

    def launch(self, velocity):
        self.velocity = velocity

    def update(self, delta):
        self.x += self.velocity.x * delta
        self.y += self.velocity.y * delta
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def set_pos(self, pos):
        self.rect.center = self.x, self.y = pos
