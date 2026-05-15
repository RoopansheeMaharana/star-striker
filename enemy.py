# enemy.py
import pygame
import random
from settings import WIDTH, WHITE, YELLOW
from enemy_bullet import EnemyBullet

class Enemy:
    def __init__(self):
        self.x            = random.randint(40, WIDTH - 40)
        self.y            = random.randint(-100, -40)
        self.speed        = random.uniform(1.5, 4.0)
        self.alive        = True
        self.size         = 22
        self.shoot_timer  = random.randint(0, 120)   # random start so not all shoot at once
        self.shoot_chance = 180                       # shoot every ~180 frames

    def update(self):
        self.y += self.speed
        if self.y > 650:
            self.alive = False

        # Randomly shoot
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_chance:
            self.shoot_timer = 0
            return [EnemyBullet(self.x, self.y + 10)]  # fire one bullet down
        return []

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y)
        pygame.draw.ellipse(screen, (200, 40,  40), (x-28, y-10, 56, 22))
        pygame.draw.ellipse(screen, (150, 20,  20), (x-14, y-22, 28, 20))
        pygame.draw.ellipse(screen, (255, 120,  0), (x-28, y-4,  56,  8))
        for dx in [-16, 0, 16]:
            pygame.draw.circle(screen, YELLOW, (x+dx, y+6), 4)
        pygame.draw.circle(screen, (80, 80, 255), (x,   y-14), 6)
        pygame.draw.circle(screen, WHITE,          (x-2, y-17), 2)