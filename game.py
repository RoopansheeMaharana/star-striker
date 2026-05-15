# game.py
import pygame
import sys
import random
from settings    import *
from stars       import draw_stars
from bullet      import Bullet
from enemy       import Enemy
from enemy_bullet import EnemyBullet
from player      import Player
from explosion   import Explosion
from sounds      import load_sounds
from highscore   import load_high_score, save_high_score
from screens     import start_screen, game_over_screen
from boss        import Boss
from powerup     import PowerUp

pygame.mixer.pre_init(44100, -16, 2)
pygame.init()

screen   = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR STRIKER")
clock    = pygame.time.Clock()
font     = pygame.font.SysFont("Consolas", 26, bold=True)

sounds     = load_sounds()
high_score = load_high_score()

start_screen(screen, high_score)

# ── GAME OBJECTS ────────────────────────────────────────
player           = Player()
bullets          = []
enemies          = []
enemy_bullets    = []
explosions       = []
powerups         = []
boss             = None
shoot_cooldown   = 0
enemy_timer      = 0
enemy_spawn_rate = 90
score            = 0
shake_timer      = 0
last_level       = 1
boss_spawned_at  = set()

# ── GAME LOOP ───────────────────────────────────────────
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # ── UPDATE ──────────────────────────────────────────
    player.update(keys)

    # Shooting — triple shot if active
    if shoot_cooldown > 0:
        shoot_cooldown -= 1
    if keys[pygame.K_SPACE] and shoot_cooldown == 0:
        if player.triple_timer > 0:
            bullets.append(Bullet(player.x, player.y - 30, angle=-90))
            bullets.append(Bullet(player.x, player.y - 30, angle=-75))
            bullets.append(Bullet(player.x, player.y - 30, angle=-105))
        else:
            bullets.append(Bullet(player.x, player.y - 30))
        shoot_cooldown = 10
        sounds["shoot"].play()

    # Difficulty scaling
    enemy_spawn_rate = max(SPAWN_RATE_MIN, 90 - (score // 5) * 3)

    # Level up sound
    current_level = score // 50 + 1
    if current_level > last_level:
        sounds["levelup"].play()
        last_level = current_level

    # Boss spawn
    boss_milestone = (score // 100) * 100
    if boss_milestone > 0 and boss_milestone not in boss_spawned_at:
        if boss is None or not boss.alive:
            boss = Boss()
            boss_spawned_at.add(boss_milestone)
            enemies.clear()

    # Update boss
    if boss and boss.alive:
        new_boss_bullets = boss.update()
        enemy_bullets.extend(new_boss_bullets)
    elif boss and not boss.alive:
        boss = None

    # Spawn regular enemies
    if boss is None:
        enemy_timer += 1
        if enemy_timer >= enemy_spawn_rate:
            enemies.append(Enemy())
            enemy_timer = 0

    # Update enemies + collect their bullets
    for enemy in enemies[:]:
        new_bullets = enemy.update()
        enemy_bullets.extend(new_bullets)
        if not enemy.alive:
            enemies.remove(enemy)

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()
        if not bullet.alive:
            bullets.remove(bullet)

    # Update enemy bullets
    for eb in enemy_bullets[:]:
        eb.update()
        if not eb.alive:
            enemy_bullets.remove(eb)

    # Update power-ups
    for pu in powerups[:]:
        pu.update()
        if not pu.alive:
            powerups.remove(pu)

    # ── COLLISIONS ──────────────────────────────────────

    # Player bullet vs enemy
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dx   = bullet.x - enemy.x
            dy   = bullet.y - enemy.y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < enemy.size + 5:
                bullet.alive = False
                enemy.alive  = False
                score       += 10
                explosions.append(Explosion(enemy.x, enemy.y))
                sounds["explosion"].play()
                if random.random() < 0.25:
                    powerups.append(PowerUp(enemy.x, enemy.y))

    # Player bullet vs boss
    if boss and boss.alive:
        for bullet in bullets[:]:
            dx   = bullet.x - boss.x
            dy   = bullet.y - boss.y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < boss.size:
                bullet.alive = False
                died = boss.hit()
                if died:
                    score += 100
                    for _ in range(5):
                        explosions.append(
                            Explosion(
                                boss.x + random.randint(-40, 40),
                                boss.y + random.randint(-20, 20),
                                count=30))
                    sounds["explosion"].play()
                    powerups.append(PowerUp(boss.x, boss.y))
                else:
                    sounds["hit"].play()

    # Enemy bullet vs player
    for eb in enemy_bullets[:]:
        dx   = eb.x - player.x
        dy   = eb.y - player.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < 20:
            eb.alive = False
            took_damage = player.take_hit()
            if took_damage:
                shake_timer = 20
                sounds["hit"].play()
                explosions.append(
                    Explosion(player.x, player.y, count=10))
            else:
                explosions.append(
                    Explosion(eb.x, eb.y, count=6))

    # Enemy ramming player
    for enemy in enemies[:]:
        dx   = player.x - enemy.x
        dy   = player.y - enemy.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < enemy.size + 20:
            enemy.alive = False
            took_damage = player.take_hit()
            if took_damage:
                shake_timer = 20
                sounds["hit"].play()
                explosions.append(
                    Explosion(enemy.x, enemy.y, count=15))

    # Player collecting power-ups
    for pu in powerups[:]:
        dx   = pu.x - player.x
        dy   = pu.y - player.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < pu.size + 20:
            player.apply_powerup(pu.type)
            pu.alive = False
            sounds["levelup"].play()

    # Update explosions
    for explosion in explosions[:]:
        explosion.update()
        if not explosion.alive:
            explosions.remove(explosion)

    # Game Over
    if player.health <= 0:
        is_new_best = save_high_score(score)
        game_over_screen(screen, score, high_score, is_new_best)
        pygame.quit()
        sys.exit()

    # ── DRAW ────────────────────────────────────────────
    shake_x, shake_y = 0, 0
    if shake_timer > 0:
        shake_timer -= 1
        shake_x = random.randint(-6, 6)
        shake_y = random.randint(-6, 6)

    game_surf = pygame.Surface((WIDTH, HEIGHT))
    game_surf.fill(DARK_BLUE)

    draw_stars(game_surf)

    for bullet    in bullets:       bullet.draw(game_surf)
    for eb        in enemy_bullets: eb.draw(game_surf)
    for enemy     in enemies:       enemy.draw(game_surf)
    for pu        in powerups:      pu.draw(game_surf)
    for explosion in explosions:    explosion.draw(game_surf)

    if boss and boss.alive:
        boss.draw(game_surf)

    player.draw(game_surf)

    screen.fill(DARK_BLUE)
    screen.blit(game_surf, (shake_x, shake_y))

    # HUD
    screen.blit(font.render("SCORE: " + str(score),
                True, CYAN_FLAME),    (10, 10))
    screen.blit(font.render("LIVES: " + "♥ " * player.health,
                True, (255, 80, 80)), (10, 40))
    screen.blit(font.render("LEVEL: " + str(score // 50 + 1),
                True, YELLOW),        (WIDTH - 150, 10))
    screen.blit(font.render("BEST: "  + str(high_score),
                True, LIGHT_GREY),    (WIDTH - 180, 40))

    # Active power-up indicators
    hud_y = HEIGHT - 40
    if player.triple_timer > 0:
        screen.blit(font.render("3x SHOT  " + str(player.triple_timer // 60 + 1) + "s",
                    True, (0, 255, 120)), (10, hud_y))
    if player.speed_timer > 0:
        screen.blit(font.render("SPEED  "  + str(player.speed_timer  // 60 + 1) + "s",
                    True, (255, 220, 0)),  (10, hud_y - 30))
    if player.shield:
        screen.blit(font.render("SHIELD  " + str(player.shield_timer // 60 + 1) + "s",
                    True, (80, 180, 255)), (10, hud_y - 60))

    # Boss warning
    if boss and boss.alive and not boss.entered:
        warn_font = pygame.font.SysFont("Consolas", 36, bold=True)
        warn      = warn_font.render("⚠ BOSS INCOMING ⚠", True, RED)
        screen.blit(warn, (WIDTH//2 - warn.get_width()//2, HEIGHT//2 - 18))

    pygame.display.flip()
    clock.tick(FPS)
