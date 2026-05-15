# player.py
# ── Player drawing and movement ─────────────────────────

import pygame
from settings import (WIDTH, HEIGHT, WHITE, ORANGE,
                      LIGHT_GREY, BLUE_FLAME, CYAN_FLAME, DARK_RED)

class Player:
    def __init__(self):
        self.x      = WIDTH  // 2
        self.y      = HEIGHT - 100
        self.speed  = 5
        self.health = 3

    def update(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:  self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  self.x += self.speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]:  self.y -= self.speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]:  self.y += self.speed

        # Keep inside window
        self.x = max(25, min(WIDTH  - 25, self.x))
        self.y = max(25, min(HEIGHT - 25, self.y))

    def draw(self, screen):
        x, y = self.x, self.y
        pygame.draw.polygon(screen, BLUE_FLAME, [
            (x-14, y+28), (x+14, y+28), (x, y+58)])
        pygame.draw.polygon(screen, CYAN_FLAME, [
            (x-7,  y+28), (x+7,  y+28), (x, y+46)])
        pygame.draw.polygon(screen, WHITE, [
            (x-3,  y+28), (x+3,  y+28), (x, y+36)])
        pygame.draw.polygon(screen, ORANGE, [
            (x, y-30), (x+18, y+10),
            (x+14, y+28), (x-14, y+28), (x-18, y+10)])
        pygame.draw.polygon(screen, WHITE, [
            (x, y-30), (x+10, y-10), (x-10, y-10)])
        pygame.draw.polygon(screen, DARK_RED, [
            (x-14, y+10), (x-24, y+28), (x-14, y+28)])
        pygame.draw.polygon(screen, DARK_RED, [
            (x+14, y+10), (x+24, y+28), (x+14, y+28)])
        pygame.draw.circle(screen, LIGHT_GREY, (x,   y-2), 9)
        pygame.draw.circle(screen, BLUE_FLAME, (x,   y-2), 6)
        pygame.draw.circle(screen, WHITE,      (x-2, y-5), 2)