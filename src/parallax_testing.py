# parallax_testing.py
# date: 27-nov-2023
# author: jelmore

import copy
import time
import random
import pygame as pg
from pygame.locals import *


# HEIGHT = 1080
# WIDTH = 1920
HEIGHT = 1300
WIDTH = 2880
RADIUS = 3
PAUSE_S = 0.001
NUM_PIXELS = 2000

# Initialize display
screen = pg.display.set_mode((WIDTH, HEIGHT))
square = pg.Surface((RADIUS, RADIUS))


def set_color_palette():
    """Set color palette for stars."""
    colors = []
    red = (255, 10, 10)
    blue = (10, 255, 10)
    green = (10, 10, 255)
    black = (0, 0, 0)
    colors.append(red)
    colors.append(blue)
    colors.append(green)
    colors.append(black)
    return colors


def create_star():
    """Create a randomly located and colored star."""
    x_coord = random.randint(0, WIDTH)
    y_coord = random.randint(0, HEIGHT)
    # speed = random.randrange(5, 25, 5)
    speed = random.randrange(2, 20)
    color = random.randint(0, 2)
    return [y_coord, x_coord, speed, color]


def create_starfield():
    """Randomly generate starfield array (x, y, scroll_speed, color)"""
    pixels = []
    for x in range(NUM_PIXELS):
        pixels.append(create_star())
    return pixels


def display_starfield(new_pixels, old_pixels, palette):
    """Displays the star field and updates display."""
    for star in old_pixels:
        square.fill(palette[3])  # Set *old* star color to black and blit it to screen
        draw_star = pg.Rect(star[1], star[0], 1, 1)
        screen.blit(square, draw_star)

    for star in new_pixels:
        square.fill(palette[star[3]])
        draw_star = pg.Rect(star[1], star[0], 1, 1)
        screen.blit(square, draw_star)


    # pg.display.flip()
    pg.display.update()
    # time.sleep(PAUSE_S)
    # time.sleep(3)
    # pg.display.quit()


def update_starfield(pixels):
    """Updates the starfield, drops old stars and adds new ones when needed."""
    for index, _ in enumerate(pixels):
        new_x_coord = pixels[index][1] - pixels[index][2]  # New x_coord is x_coord - speed
        if new_x_coord < 0:
            del pixels[index]
            pixels.append(create_star())
            pixels[index][1] = WIDTH
        else:
            pixels[index][1] = new_x_coord
    return pixels


if __name__ == "__main__":
    # Init the color palette
    color_palette = set_color_palette()

    # Setup the initial starfield
    pixel_map = create_starfield()
    print(f"[DEBUG] pixel_map values: {pixel_map}")

    # Initialize the old_pixel_map var (for writing over stars) and get the loop running
    old_pixel_map = pixel_map
    _running = True
    while _running:

        display_starfield(pixel_map, old_pixel_map, color_palette)
        old_pixel_map = copy.deepcopy(pixel_map)
        pixel_map = update_starfield(pixel_map)
        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_q)):  # Quit
                _running = False
