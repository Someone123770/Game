import pygame

from animations import AnimatedSprite
from base_functions import *
from constants import *
from end_menu import end_menu
from movement import next_move

class Player(AnimatedSprite):
    def __init__(self, pos, group):
        player_image = load_image('character/Mage-M-01.png', -1)
        super().__init__(player_image, 3, 4, group)
        pos_x = pos[0]
        pos_y = pos[1]
        centering_x = (TILE_WIDTH - self.image.get_width()) // 2
        centering_y = (TILE_HEIGHT - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(
            (TILE_WIDTH * pos_x) + centering_x,
            (TILE_HEIGHT * pos_y) + centering_y)
        self.end_location = [self.rect.x, self.rect.y]
        self.v = 5
        self.dy = 0
        self.dx = 0
        self.health = self.max_health = 100
        self.energy = self.max_energy = 100
        self.repair_hp = 0.1
        self.repair_en = 0.1

    def update_location(self):
        if self.rect.x == self.end_location[0] and self.rect.y == self.end_location[1]:
            self.stand_or_go = False
            return

        dist = distance_between_points((self.rect.x, self.rect.y), self.end_location)
        self.dx, self.dy = next_move((self.rect.x, self.rect.y), self.end_location, dist,  self.v)

        if self.dx > 0 and self.rect.x > self.end_location[0]:
            self.stand_or_go = False
            return
        elif self.dx < 0 and self.rect.x < self.end_location[0]:
            self.stand_or_go = False
            return
        if self.dy > 0 and self.rect.y > self.end_location[1]:
            self.stand_or_go = False
            return
        elif self.dy < 0 and self.rect.y < self.end_location[1]:
            self.stand_or_go = False
            return
        if (not self.dy > 0 and not self.dy < 0) and (not self.dx > 0 and not self.dx < 0):
            self.stand_or_go = False
            return
        self.stand_or_go = True
        game_angle = get_game_angle((self.rect.x, self.rect.y), self.end_location)
        if 135 >= game_angle >= 45:
            self.update_animathion_line(2, 4, 1, 1)
        elif 225 <= game_angle <= 315:
            self.update_animathion_line(4, 4, 1, 3)
        elif 135 < game_angle < 225:
            self.update_animathion_line(5, 4, 1, 4)
        else:
            self.update_animathion_line(3, 4, 1, 2)
        past_pos = self.rect.copy()
        self.rect.x += self.dx
        self.rect.y += self.dy

        if pygame.sprite.spritecollideany(self, impassable_cells) or \
            pygame.sprite.spritecollideany(self, enemies_group):
            self.rect = past_pos.copy()
            self.end_location = [self.rect.x, self.rect.y]

    def characteristics(self):
        if self.health <= 0:
            end_menu(False)
        self.health += self.repair_hp if self.health < self.max_health else 0
        self.energy += self.repair_en if self.energy < self.max_energy else 0
        if self.health > self.max_health:
            self.health = self.max_health
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def new_duration(self, pos):
        if pygame.sprite.spritecollideany(self, impassable_cells):
            return
        self.end_location = [pos[0] - self.rect.width // 2, pos[1] - self.rect.height // 2]
