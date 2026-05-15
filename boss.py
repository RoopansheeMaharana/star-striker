# boss.py
# ── Boss enemy ──────────────────────────────────────────

import pygame
import random
import math
from settings  import *
from enemy_bullet import EnemyBullet

class Boss:
    def __init__(self):
        self.x          = WIDTH // 2
        self.y          = -120           # start above screen
        self.speed      = 1.5
        self.alive      = True
        self.max_health = 30             # takes 30 hits to kill
        self.health     = self.max_health
        self.size       = 55            # collision radius
        self.entered    = False          # has boss reached its position?

        # Movement pattern
        self.move_timer = 0
        self.move_dir   = 1             # 1 = right, -1 = left

        # Shooting pattern
        self.shoot_timer    = 0
        self.shoot_interval = 60        # shoot every 60 frames
        self.phase          = 1         # phase 1 = normal, phase 2 = aggressive

    def update(self):
        # ── ENTRY: fly down to position ─────────────────
        if not self.entered:
            self.y += 2
            if self.y >= 120:
                self.entered = True
            return []            # no shooting while entering

        # ── PHASE 2: more aggressive below half health ──
        if self.health <= self.max_health // 2:
            self.phase          = 2
            self.shoot_interval = 35
            self.speed          = 2.5

        # ── MOVEMENT: drift left and right ──────────────
        self.move_timer += 1
        if self.move_timer > 90:        # change direction every 90 frames
            self.move_dir  *= -1
            self.move_timer = 0

        self.x += self.speed * self.move_dir
        # Bounce off walls
        if self.x > WIDTH - 80:
            self.x        = WIDTH - 80
            self.move_dir = -1
        if self.x < 80:
            self.x        = 80
            self.move_dir = 1

        # ── SHOOTING ────────────────────────────────────
        new_bullets = []
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            if self.phase == 1:
                new_bullets = self._shoot_spread()
            else:
                new_bullets = self._shoot_aimed()
        return new_bullets

    def _shoot_spread(self):
        """Phase 1: Fire 5 bullets in a spread pattern"""
        bullets = []
        for angle in [70, 80, 90, 100, 110]:   # spread around 90 (straight down)
            bullets.append(EnemyBullet(self.x, self.y + 60, angle))
        return bullets

    def _shoot_aimed(self):
        """Phase 2: Fire 3 aimed at player + spread"""
        bullets = self._shoot_spread()
        # Extra fast aimed shots
        for offset in [-15, 0, 15]:
            bullets.append(EnemyBullet(self.x + offset, self.y + 60, 90))
        return bullets

    def hit(self):
        """Called when a player bullet hits the boss."""
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            return True   # boss died
        return False      # boss still alive

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y)

        # ── BODY ────────────────────────────────────────
        # Main hull (large dark ellipse)
        pygame.draw.ellipse(screen, (80,  0,  80),  (x-60, y-20, 120, 44))
        # Top dome
        pygame.draw.ellipse(screen, (120,  0, 120),  (x-30, y-44,  60, 44))
        # Glowing rim
        col = ORANGE if self.phase == 1 else RED
        pygame.draw.ellipse(screen, col,             (x-60, y-8,  120, 16))

        # ── LIGHTS ──────────────────────────────────────
        # Belly lights (5 dots)
        for i, dx in enumerate([-40, -20, 0, 20, 40]):
            pulse = int(180 + 75 * math.sin(
                pygame.time.get_ticks() * 0.005 + i))
            pygame.draw.circle(screen, (pulse, pulse, 0),
                               (x+dx, y+12), 5)

        # ── CANNONS ─────────────────────────────────────
        for dx in [-30, 0, 30]:
            pygame.draw.rect(screen, DARK_RED,
                             (x+dx-4, y+18, 8, 18), border_radius=3)

        # ── WINDOW ──────────────────────────────────────
        pygame.draw.circle(screen, (60,  60, 200), (x, y-24), 14)
        pygame.draw.circle(screen, (100, 100, 255), (x, y-24), 10)
        pygame.draw.circle(screen, WHITE,            (x-4, y-28),  4)

        # ── HEALTH BAR ──────────────────────────────────
        self._draw_health_bar(screen)

    def _draw_health_bar(self, screen):
        """Draw health bar at top of screen."""
        bar_w    = 400
        bar_h    = 22
        bar_x    = WIDTH//2 - bar_w//2
        bar_y    = 10
        fill     = int(bar_w * self.health / self.max_health)

        # Background
        pygame.draw.rect(screen, (60, 0, 0),
                         (bar_x, bar_y, bar_w, bar_h), border_radius=5)

        # Health fill — green → orange → red based on health
        ratio = self.health / self.max_health
        if ratio > 0.6:
            color = (50, 220, 50)      # green
        elif ratio > 0.3:
            color = ORANGE             # orange
        else:
            color = RED                # red (danger!)

        if fill > 0:
            pygame.draw.rect(screen, color,
                             (bar_x, bar_y, fill, bar_h), border_radius=5)

        # Border
        pygame.draw.rect(screen, WHITE,
                         (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)

        # Label
        font = pygame.font.SysFont("Consolas", 16, bold=True)
        label = font.render("BOSS", True, WHITE)
        screen.blit(label, (bar_x - 44, bar_y + 3))