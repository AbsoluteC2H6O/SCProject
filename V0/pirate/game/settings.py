from pathlib import Path

import pygame

from .src.frames import generate_frames

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 18

BASE_DIR = Path(__file__).parent

ENVIRONMENT = BASE_DIR / "env.txt"

# Graphics
GAME_TEXTURES = {
    "ice": pygame.image.load(BASE_DIR / "graphics" / "ice.png"),
    "snow": pygame.image.load(BASE_DIR / "graphics" / "snow.png"),
    "box": pygame.image.load(BASE_DIR / "graphics" / "box.png"),
    "bomb": pygame.image.load(BASE_DIR / "graphics" / "bomba.png"),
    "explosion": pygame.image.load(BASE_DIR / "graphics" / "explosion.png"),
    "character": pygame.image.load(BASE_DIR / "graphics" / "character.png"),
    "switch": pygame.image.load(BASE_DIR / "graphics" / "switch.png"),
    "floor": pygame.image.load(BASE_DIR / "graphics" / "floor.png"),
    "life0": pygame.image.load(BASE_DIR / "graphics" / "life0.png"),
    "life50": pygame.image.load(BASE_DIR / "graphics" / "life1.png"),
    "life100": pygame.image.load(BASE_DIR / "graphics" / "life2.png"),
}

# Frames
GAME_FRAMES = {
    "ice": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "snow": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "box": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "bomb": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "explosion": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "switch": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "floor": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "life0": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "life50": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "life100": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "character": generate_frames(
        GAME_TEXTURES["character"], PLAYER_WIDTH, PLAYER_HEIGHT
    ),
}

# Fonts
pygame.font.init()

FONTS = {
    'large': pygame.font.Font(BASE_DIR / "fonts" / "Bangers-Regular.ttf", 22),
    'short': pygame.font.Font(BASE_DIR / "fonts" / "Bangers-Regular.ttf", 16),
    'short-1': pygame.font.Font(BASE_DIR  / "fonts" / "Bangers-Regular.ttf", 10)
}

COPY = "The Pirate Treasure - By: Abe & Alfredo"
LIFE_POINTS = "Life points"
LOST = "¡LOST GAME!"

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "sound" / "pirates.ogg")

# Sound effects
SOUNDS = {
    'explosion': pygame.mixer.Sound(BASE_DIR / "sound" / "explosion.ogg"),
    'lose': pygame.mixer.Sound(BASE_DIR / "sound" / "lose.ogg"),
    'win': pygame.mixer.Sound(BASE_DIR / "sound" / "win.ogg"),
}