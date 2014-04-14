import os
import random
import entities
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert_alpha()
    return image


def get_alpha_surface(surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
    tmp = pygame.Surface(surf.get_size(), pygame.SRCALPHA, 32)
    tmp.fill((red, green, blue, alpha))
    tmp.blit(surf, (0, 0), surf.get_rect(), mode)
    return tmp

def size_mul(size, mul):
	return tuple((int(i * mul) for i in size))

WIN_WIDTH = 800
WIN_HEIGHT = 600
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

MAP_WIDTH = MAP_HEIGHT = 1024
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)

FPS = 60

GREEN = pygame.Color(69, 176, 108)
RED = pygame.Color(176, 69, 94)
BLUE = pygame.Color(69, 70, 176)

planets = []
ships = dict()


def init():
    global planets, ships
    for image_name in os.listdir(os.path.join('data', 'planets')):
        image = load_image(os.path.join('planets', image_name))
        planets.append(image)

    for image_name in os.listdir(os.path.join('data', 'ships')):
    	image = load_image(os.path.join('ships', image_name))
    	ship_name = image_name.split('.')[0]
    	print(ship_name)
    	ships[ship_name] = image

  
