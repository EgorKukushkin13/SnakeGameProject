from constants import *
import pygame

game_map = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
level = 1

clock = pygame.time.Clock()
main_menu_timer = pygame.time.Clock()
color_menu_timer = pygame.time.Clock()
edit_level_timer = pygame.time.Clock()
lvl_edit_menu_timer = pygame.time.Clock()
select_lvl_menu_timer = pygame.time.Clock()
records_menu_timer = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

