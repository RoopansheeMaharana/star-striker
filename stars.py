# stars.py
# ── Starfield background ────────────────────────────────

import pygame
import random
from settings import WIDTH, HEIGHT

# Generate stars once when this file is imported
stars = [
    (random.randint(0, WIDTH),
     random.randint(0, HEIGHT),
     random.uniform(0.5, 2.5))
    for _ in range(150)
]

scroll = 0

def draw_stars(screen):
    global scroll
    scroll += 1
    for x, y, speed in stars:
        yy         = (y + scroll * speed) % HEIGHT
        brightness = int(100 + speed * 60)
        pygame.draw.circle(screen,
                           (brightness, brightness, brightness),
                           (x, int(yy)), 1)