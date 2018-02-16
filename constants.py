import pygame
import libtcodpy as libtcod
pygame.init()
# FPS
GAME_FPS = 60
# Tamanos 
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 16
CELL_HEIGHT= 16
# Variables del mapa
MAP_WIDTH = 30
MAP_HEIGHT = 30
# Fuente
FONT = pygame.font.Font("PressStart2P.ttf", 8)
FONT_MESSAGE_TEXT = pygame.font.Font("PressStart2P.ttf", 8)
# MESSAGE DEFAULTS
NUM_MESSAGES = 4 # Numero de mensajes que queremos ver
# COLORES
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY  = (100, 100, 100)
COLOR_RED = (150, 0, 0)
# COLORES DEL JUEGO
COLOR_DEFAULT_BG = COLOR_BLACK # Color que usaremos para el fondo
# FOV
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 6
FOV_ALGO = libtcod.FOV_SHADOW
# SPRITES 
S_PLAYER = pygame.image.load("images/char16.png")
S_WALL = pygame.image.load("images/gbwall3.png")
S_WALL_EXPLORED = pygame.image.load("images/exploredwall16.png")
S_FLOOR = pygame.image.load("images/gbwall.png")
S_FLOOR_EXPLORED = pygame.image.load("images/exploredfloor16.png")
S_ENEMY = pygame.image.load("images/gbskull.png")
S_BLOOD = pygame.image.load("images/bloodgb.png")
#Pruebagit