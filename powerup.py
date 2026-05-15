# powerup.py
# ── Power-up pickups ────────────────────────────────────

import pygame
import math
import random
from settings import *

class PowerUp:
    def __init__(self, x, y):
        self.x     = x
        self.y     = y
        self.speed = 2
        self.alive = True
        self.size  = 16
        self.timer = 0    # for animation

        # Randomly pick a type
        self.type  = random.choice(["triple", "shield", "speed"])

        # Each type has its own color and symbol
        self.info  = {
            "triple" : {"color": (0,   255, 120), "symbol": "3x"},
            "shield" : {"color": (80,  180, 255), "symbol": "🛡"},
            "speed"  : {"color": (255, 220,   0), "symbol": ">>"},
        }

    def update(self):
        self.y     += self.speed     # fall downward
        self.timer += 1              # animation counter
        if self.y > HEIGHT + 30:
            self.alive = False

    def draw(self, screen):
        self.timer += 1
        x     = int(self.x)
        y     = int(self.y)
        color = self.info[self.type]["color"]

        # Pulsing outer ring
        pulse  = int(3 * math.sin(self.timer * 0.1))
        radius = self.size + pulse

        # Outer glow ring
        pygame.draw.circle(screen, color, (x, y), radius, 2)

        # Inner filled circle
        inner = tuple(max(0, c - 80) for c in color)
        pygame.draw.circle(screen, inner, (x, y), self.size - 2)

        # Symbol text
        font  = pygame.font.SysFont("Consolas", 13, bold=True)
        label = font.render(self.info[self.type]["symbol"], True, color)
        screen.blit(label, (x - label.get_width()//2,
                            y - label.get_height()//2))