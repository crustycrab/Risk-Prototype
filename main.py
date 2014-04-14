import pygame
from pygame.locals import *
import random
import sys
import graphics
import entities
import res
import utils


class Game:

    def __init__(self, map_surface, camera, count=10):
        self.map_surface = map_surface
        self.planets = self.init_planets(count)

        self.camera = camera

        self.started = False
        self.paused = False

        self.selected_planet = None

        self.union = []
        self.enemy = []
        self.init_players()

        self.landings = []

    def init_planets(self, count):
        raw_planets = res.planets
        random.shuffle(raw_planets)
        count = min(count, len(raw_planets))

        planets = []

        for i in range(count):
            image = raw_planets[i]
            size = (random.randint(64, 192),) * 2
            image = pygame.transform.scale(image, size)
            rect = image.get_rect()

            while True:
                rect.x = random.randint(0, res.MAP_WIDTH - rect.width)
                rect.y = random.randint(0, res.MAP_HEIGHT - rect.height)
                new_planet = entities.Planet(image, rect)
                for planet in planets:
                    if planet.collide_with(new_planet):
                        break
                else:
                    break

            planets.append(new_planet)

        return planets

    def init_players(self):
        players = random.sample(self.planets, 2)

        player = players.pop()
        player.set_side(union=True)
        self.union.append(player)

        player = players.pop()
        player.set_side(enemy=True)
        self.enemy.append(player)

    def draw(self):
        for planet in self.planets:
            planet.draw(self.map_surface)

        for landing in self.landings:
            landing.draw(self.map_surface)

    def update(self, delta):
        to_remove = []

        for planet in self.planets:
            for landing in self.landings:
                if planet.collide_with_point(landing.get_pos()):
                    if landing.union:
                        planet.union_units += 1
                    else:
                        planet.enemy_units += 1
                    to_remove.append(landing)
                else:
                    landing_x, landing_y = landing.get_pos()
                    planet_x, planet_y = planet.get_pos()
                    direction = utils.Vector2(x=landing_x - planet_x, y=landing_y - planet_y)
                    force = direction * ((3000 * planet.radius) / pow(direction.modul(), 3))
                    landing.velocity = landing.velocity - (force * delta)

        for planet in self.planets:
            planet.update(delta)

        for landing in self.landings:
            if landing in to_remove:
                self.landings.remove(landing)
                continue
            landing.update(delta)


    def select_planet(self, pos):
        for planet in self.planets:
            if planet.collide_with_point(self.camera.convert_pos(pos)):
                if self.selected_planet:
                    self.selected_planet.unselect()
                self.selected_planet = planet
                planet.select()
                break
        else:
            if self.selected_planet:
                self.selected_planet.unselect()
                self.selected_planet = None

    def launch_landing(self, pos, union=True):
        if not self.selected_planet:
            return

        x, y = self.selected_planet.get_pos()
        result_x, result_y = self.camera.convert_pos(pos)
        radius = self.selected_planet.radius
        direction = utils.Vector2(x=result_x - x, y=result_y - y)
        start_position = (direction * ((radius + 5) / direction.modul())) + utils.Vector2(x=x, y=y)

        new_landing = entities.Landing(union)
        new_landing.set_pos(start_position.as_tuple())
        velocity = direction * (80 / direction.modul()) 

        if velocity * direction > 0:
            if self.selected_planet.is_union() and self.selected_planet.union_units > 1.0 and union \
            or self.selected_planet.is_enemy() and self.selected_planet.enemy_units > 1.0 and not union:
                new_landing.launch(velocity)
                self.landings.append(new_landing)
                if union: self.selected_planet.union_units -= 1
                else: self.selected_planet.enemy_units -= 1


def main():
    pygame.init()
    window = pygame.display.set_mode(res.WIN_SIZE)
    pygame.display.set_caption('Risk')
    clock = pygame.time.Clock()
    res.init()
    camera = graphics.Camera()

    map_surface = pygame.Surface(res.MAP_SIZE)
    game = Game(map_surface, camera)

    stars = graphics.Stars()
    key_states = [False, False, False, False]

    while True:
        delta = clock.tick(res.FPS) / 1000.0
        map_surface.fill((32, 32, 48))

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.select_planet(pygame.mouse.get_pos())
                if event.button == 3:
                    game.launch_landing(pygame.mouse.get_pos(), union=True)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                if event.key == K_LEFT:
                    key_states[0] = True
                if event.key == K_RIGHT:
                    key_states[1] = True
                if event.key == K_UP:
                    key_states[2] = True
                if event.key == K_DOWN:
                    key_states[3] = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    key_states[0] = False
                if event.key == K_RIGHT:
                    key_states[1] = False
                if event.key == K_UP:
                    key_states[2] = False
                if event.key == K_DOWN:
                    key_states[3] = False

        stars.draw(map_surface)

        game.draw()
        camera.update(delta, key_states)

        window.blit(map_surface, camera.get_pos())
        pygame.display.flip()

        stars.update(delta)
        game.update(delta)

if __name__ == '__main__':
    main()
