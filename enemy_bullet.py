# enemy_bullet.py
# ── Bullets fired BY enemies ────────────────────────────

import pygame
import math
from settings import WHITE

class EnemyBullet:
    def __init__(self, x, y, angle=90):
        """
        x, y  = starting position (enemy center)
        angle = direction in degrees. 90 = straight down
        """
        self.x     = x
        self.y     = y
        self.speed = 5
        self.alive = True

        # Convert angle to x/y velocity
        rad    = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = math.sin(rad) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Remove if off screen
        if self.y > 650 or self.x < 0 or self.x > 800:
            self.alive = False

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y)
        # Outer glow (red)
        pygame.draw.circle(screen, (200, 50, 50), (x, y), 6)
        # Inner bright core
        pygame.draw.circle(screen, (255, 180, 180), (x, y), 3)
        # White hot center
        pygame.draw.circle(screen, WHITE, (x, y), 1)