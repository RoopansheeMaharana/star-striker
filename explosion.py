# explosion.py
# ── Particle explosion effect ───────────────────────────

import pygame
import random
import math
from settings import WHITE, YELLOW, ORANGE

class Particle:
    def __init__(self, x, y):
        self.x     = x
        self.y     = y

        # Random direction using angle
        angle      = random.uniform(0, math.tau)   # tau = 2*pi = full circle
        speed      = random.uniform(1, 6)
        self.vx    = math.cos(angle) * speed       # horizontal velocity
        self.vy    = math.sin(angle) * speed       # vertical velocity

        self.life  = random.randint(20, 45)        # how many frames it lives
        self.max_life = self.life                  # remember starting life for fade

        # Random warm color
        self.color = random.choice([ORANGE, YELLOW, WHITE, (255, 80, 0)])
        self.size  = random.randint(2, 5)

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.1      # gravity pulls particles down
        self.life -= 1

    def draw(self, screen):
        # Fade out as life decreases
        alpha = int(255 * self.life / self.max_life)
        size  = max(1, int(self.size * self.life / self.max_life))
        color = tuple(min(255, max(0, c)) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)


class Explosion:
    def __init__(self, x, y, count=25):
        self.particles = [Particle(x, y) for _ in range(count)]
        self.alive     = True

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
        if len(self.particles) == 0:
            self.alive = False       # all particles dead = explosion done

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)