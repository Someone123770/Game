import os
import sys

import pygame

from math import atan, hypot, degrees

from constants import *


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()

def load_level(filename):
    filename = "../data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def get_tile_pos(pos, shift_x, shift_y):
    x, y = pos[0], pos[1]
    grid_x, grid_y = (x - shift_x) // TILE_WIDTH, (y - shift_y) // TILE_HEIGHT
    return int(grid_x), int(grid_y)

def get_central_pos_from_tile(pos, shift_x, shift_y):
    x, y = pos[0], pos[1]
    grid_x, grid_y = x * TILE_WIDTH + shift_x + TILE_WIDTH // 2, y * TILE_HEIGHT + shift_y + TILE_HEIGHT // 2
    return grid_x, grid_y

def distance_between_points(p1, p2):
    return hypot(p2[0] - p1[0], p2[1] - p1[1])

def get_angle(point1, point2):
    try:
        return degrees(atan((point1[1] - point2[1]) / (point1[0] - point2[0])))
    except ZeroDivisionError:
        return 0

def get_game_angle(point1, point2):
    angle = get_angle(point1, point2)
    game_angle = abs(angle)
    if (0 < angle <= 90 and point2[0] < point1[0]) or (angle == 0 and point2[1] < point1[1]):
        game_angle = 90 - game_angle
        game_angle += 90
    elif -90 < angle <= 0 and point2[0] < point1[0]:
        game_angle += 180
    elif (0 < angle <= 90 and point2[0] > point1[0]) or (angle == 0 and point2[1] > point1[1]):
        game_angle = 90 - game_angle
        game_angle += 270
    return game_angle
