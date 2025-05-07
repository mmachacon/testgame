import pygame
import random
import sys
import os

pygame.init()
WIDTH, HEIGHT = 600, 600

try:
    player_img = pygame.image.load("assets/player.png")
    enemy_img = pygame.image.load("assets/enemy.png")
    background_img = pygame.image.load("assets/background.png")
except FileNotFoundError:
    player_img = pygame.image.load("testgame/assets/player.png")
    enemy_img = pygame.image.load("testgame/assets/enemy.png")
    background_img = pygame.image.load("testgame/assets/background.png")

player_img = pygame.transform.scale(player_img, (40, 40))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquiva enemigos")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# Files
SCORE_FILE = "scores.txt"
if not os.path.exists(SCORE_FILE):
    open(SCORE_FILE, "w").close()

def draw_text(text, x, y, color=WHITE):
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (x, y))

def save_score(score):
    with open(SCORE_FILE, "a") as f:
        f.write(str(score) + "\n")

def show_scores():
    screen.fill(BLACK)
    draw_text("Puntuaciones más altas:", 200, 50)
    try:
        with open(SCORE_FILE, "r") as f:
            scores = sorted([int(line.strip()) for line in f if line.strip().isdigit()], reverse=True)[:5]
            for i, score in enumerate(scores):
                draw_text(f"{i+1}. {score}", 250, 100 + i * 40)
    except:
        draw_text("No hay puntajes guardados.", 200, 100)
    pygame.display.flip()
    pygame.time.wait(3000)

def game():
    player = pygame.Rect(WIDTH//2, HEIGHT-50, 40, 40)
    enemies = [pygame.Rect(random.randint(0, WIDTH-40), -60, 40, 40) for _ in range(5)]
    base_speed = 5
    speed = base_speed
    score = 0

    running = True
    while running:
        screen.blit(background_img, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.move_ip(6, 0)

        for enemy in enemies:
            enemy.move_ip(0, speed)
            if enemy.top > HEIGHT:
                enemy.y = -40
                enemy.x = random.randint(0, WIDTH-40)
                score += 1
                speed = base_speed * (1 + 0.25 * (score // 50))

            if player.colliderect(enemy):
                if score > 0:
                    save_score(score)
                running = False

        screen.blit(player_img, player)

        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        draw_text(f"Puntuación: {score}", 10, 10)
        pygame.display.flip()
        clock.tick(60)

def menu():
    while True:
        screen.fill(BLACK)
        draw_text("1. Empezar", 200, 200)
        draw_text("2. Ver Puntuaciones", 200, 250)
        draw_text("3. Salir", 200, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game()
                elif event.key == pygame.K_2:
                    show_scores()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    menu()
