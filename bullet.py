# bullet.py
import pygame
import math
from settings import WHITE

class Bullet:
    def __init__(self, x, y, angle=-90):
        """
        angle = -90 means straight up (default)
        Triple shot fires at -75, -90, -105
        """
        self.x     = float(x)
        self.y     = float(y)
        self.speed = 11
        self.alive = True

        rad        = math.radians(angle)
        self.vx    = math.cos(rad) * self.speed
        self.vy    = math.sin(rad) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y < 0 or self.x < 0 or self.x > 800:
            self.alive = False

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y)
        pygame.draw.rect(screen, (0, 100, 255),
                         (x - 4, y, 8, 20), border_radius=4)
        pygame.draw.rect(screen, (150, 220, 255),
                         (x - 2, y, 4, 20), border_radius=2)
        pygame.draw.circle(screen, WHITE, (x, y), 3)