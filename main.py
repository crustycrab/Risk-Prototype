import pygame
from pygame.locals import *
import res
import sys


def main():
    pygame.init()
    window = pygame.display.set_mode(res.WIN_SIZE)
    pygame.display.set_caption('Risk')
    clock = pygame.time.Clock()

    while True:
    	delta = clock.tick(res.FPS) / 1000.0

        for event in pygame.event.get():
            if (event.type == QUIT):
                sys.exit(0)

        pygame.display.flip()

if __name__ == '__main__':
    main()
