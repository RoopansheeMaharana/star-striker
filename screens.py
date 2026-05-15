# screens.py
# ── Start screen and Game Over screen ───────────────────

import pygame
import sys
from settings import *

def draw_centered(screen, text, font, color, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))

def start_screen(screen, high_score):
    """Show title screen and wait for player to press SPACE."""
    clock    = pygame.time.Clock()
    font_big = pygame.font.SysFont("Consolas", 64, bold=True)
    font_med = pygame.font.SysFont("Consolas", 28, bold=True)
    font_sml = pygame.font.SysFont("Consolas", 20)

    # Animated star scroll for background
    import random
    stars = [(random.randint(0, WIDTH),
              random.randint(0, HEIGHT),
              random.uniform(0.5, 2.5)) for _ in range(150)]
    scroll = 0

    # Pulsing animation counter
    pulse = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return    # start the game!

        # Draw background
        screen.fill(DARK_BLUE)
        scroll += 1
        for x, y, speed in stars:
            yy         = (y + scroll * speed) % HEIGHT
            brightness = int(100 + speed * 60)
            pygame.draw.circle(screen,
                               (brightness, brightness, brightness),
                               (x, int(yy)), 1)

        # Draw rocket ship in center top
        cx, cy = WIDTH // 2, 160
        pygame.draw.polygon(screen, BLUE_FLAME, [
            (cx-14, cy+28), (cx+14, cy+28), (cx, cy+58)])
        pygame.draw.polygon(screen, CYAN_FLAME, [
            (cx-7, cy+28), (cx+7, cy+28), (cx, cy+46)])
        pygame.draw.polygon(screen, ORANGE, [
            (cx, cy-30), (cx+18, cy+10),
            (cx+14, cy+28), (cx-14, cy+28), (cx-18, cy+10)])
        pygame.draw.polygon(screen, WHITE, [
            (cx, cy-30), (cx+10, cy-10), (cx-10, cy-10)])
        pygame.draw.polygon(screen, DARK_RED, [
            (cx-14, cy+10), (cx-24, cy+28), (cx-14, cy+28)])
        pygame.draw.polygon(screen, DARK_RED, [
            (cx+14, cy+10), (cx+24, cy+28), (cx+14, cy+28)])
        pygame.draw.circle(screen, LIGHT_GREY, (cx,   cy-2), 9)
        pygame.draw.circle(screen, BLUE_FLAME, (cx,   cy-2), 6)
        pygame.draw.circle(screen, WHITE,      (cx-2, cy-5), 2)

        # Title
        draw_centered(screen, "STAR STRIKER", font_big, CYAN_FLAME, 230)

        # Pulsing SPACE prompt
        pulse += 0.05
        alpha = int(180 + 75 * __import__("math").sin(pulse))
        color = (alpha, alpha, alpha)
        draw_centered(screen, "PRESS SPACE TO PLAY", font_med, color, 320)

        # Controls
        draw_centered(screen, "WASD / Arrow Keys — Move", font_sml, LIGHT_GREY, 380)
        draw_centered(screen, "SPACE — Shoot",             font_sml, LIGHT_GREY, 405)

        # High score
        if high_score > 0:
            draw_centered(screen,
                          "Best Score: " + str(high_score),
                          font_med, YELLOW, 460)

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(screen, score, high_score, is_new_best):
    """Show game over screen for 4 seconds."""
    font_big = pygame.font.SysFont("Consolas", 56, bold=True)
    font_med = pygame.font.SysFont("Consolas", 28, bold=True)

    screen.fill(DARK_BLUE)

    draw_centered(screen, "GAME OVER",           font_big, RED,        160)
    draw_centered(screen, "Score: " + str(score), font_med, WHITE,      260)

    if is_new_best:
        draw_centered(screen, "★ NEW HIGH SCORE! ★", font_med, YELLOW,  310)
    else:
        draw_centered(screen, "Best: " + str(high_score), font_med,
                      LIGHT_GREY, 310)

    draw_centered(screen, "Thanks for playing!", font_med, CYAN_FLAME,  370)

    pygame.display.flip()
    pygame.time.wait(4000)