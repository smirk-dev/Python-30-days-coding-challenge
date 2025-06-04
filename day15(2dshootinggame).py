import pygame
import random
import sys
import os
import time
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Space Shooting Game")
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (64, 64))
target_img = pygame.image.load("target.png")
target_img = pygame.transform.scale(target_img, (64, 64))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (16, 32))
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100
player_speed = 5
bullets = []
targets = []
bullet_speed = -10
target_speed = 1
score = 0
lives = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True
SCORE_FILE = "scores.txt"
def draw_player(x, y):
    screen.blit(player_img, (x, y))
def draw_bullet(bullet):
    screen.blit(bullet_img, (bullet[0], bullet[1]))
def draw_target(target):
    screen.blit(target_img, (target[0], target[1]))
def display_score_and_lives(score, lives):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
def show_menu():
    button_font = pygame.font.Font(None, 48)
    while True:
        screen.fill((0, 0, 0))
        color1 = (20, 20, 20)
        color2 = (60, 60, 60)
        pygame.draw.rect(screen, color1, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, color2, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        title_font = pygame.font.Font(None, 64)
        title = title_font.render("Space Shooting Game", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        menu_font = pygame.font.Font(None, 36)
        play_text = menu_font.render("Play Game", True, (255, 255, 255))
        high_scores_text = menu_font.render("High Scores", True, (255, 255, 255))
        quit_text = menu_font.render("Quit", True, (255, 255, 255))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        play_rect = pygame.Rect(SCREEN_WIDTH // 2 - play_text.get_width() // 2, 200, play_text.get_width(), play_text.get_height())
        high_scores_rect = pygame.Rect(SCREEN_WIDTH // 2 - high_scores_text.get_width() // 2, 250, high_scores_text.get_width(), high_scores_text.get_height())
        quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300, quit_text.get_width(), quit_text.get_height())
        if play_rect.collidepoint(mouse_x, mouse_y):
            play_text = menu_font.render("Play Game", True, (0, 255, 0))
        if high_scores_rect.collidepoint(mouse_x, mouse_y):
            high_scores_text = menu_font.render("High Scores", True, (0, 255, 0))
        if quit_rect.collidepoint(mouse_x, mouse_y):
            quit_text = menu_font.render("Quit", True, (0, 255, 0))
        screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, 200))
        screen.blit(high_scores_text, (SCREEN_WIDTH // 2 - high_scores_text.get_width() // 2, 250))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))
        instruction_font = pygame.font.Font(None, 24)
        instruction = instruction_font.render("-By Suryansh Mishra", True, (255, 255, 255))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "high_scores"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(mouse_x, mouse_y):
                    return "play"
                if high_scores_rect.collidepoint(mouse_x, mouse_y):
                    return "high_scores"
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
def save_score(score):
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as file:
            file.write(f"{score}\n")
    else:
        with open(SCORE_FILE, "a") as file:
            file.write(f"{score}\n")
def get_high_scores():
    if not os.path.exists(SCORE_FILE):
        return [], None
    with open(SCORE_FILE, "r") as file:
        scores = [int(line.strip()) for line in file.readlines()]
    scores.sort(reverse=True)
    last_score = scores[-1] if scores else None
    return scores[:5], last_score
def display_high_scores():
    scores, last_score = get_high_scores()
    while True:
        screen.fill((0, 0, 0))
        title_font = pygame.font.Font(None, 64)
        menu_font = pygame.font.Font(None, 36)
        title = title_font.render("High Scores", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        if scores:
            for i, score in enumerate(scores):
                score_text = menu_font.render(f"{i + 1}. {score}", True, (255, 255, 255))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150 + i * 40))
            last_score_text = menu_font.render(f"Last Score: {last_score}", True, (255, 255, 255))
            screen.blit(last_score_text, (SCREEN_WIDTH // 2 - last_score_text.get_width() // 2, 400))
        else:
            no_scores_text = menu_font.render("No scores yet.", True, (255, 255, 255))
            screen.blit(no_scores_text, (SCREEN_WIDTH // 2 - no_scores_text.get_width() // 2, 200))
        back_text = menu_font.render("Press B to return to menu", True, (255, 255, 255))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 500))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return
def game_over_screen(score, start_time):
    scores, last_score = get_high_scores()
    is_new_highscore = False
    if score > (last_score or 0):
        is_new_highscore = True
        save_score(score)
    time_taken = int(time.time() - start_time)
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
        if is_new_highscore:
            highscore_text = font.render("New High Score! Congratulations!", True, (0, 255, 0))
            screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, SCREEN_HEIGHT // 2))
        else:
            time_text = font.render(f"Time Taken: {time_taken} sec", True, (255, 255, 255))
            screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
        back_text = font.render("Press B to return to menu", True, (255, 255, 255))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return
def main_game():
    global score, lives
    player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100
    bullets = []
    targets = []
    running = True
    start_time = time.time()
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_img.get_width():
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append([player_x + player_img.get_width() // 2, player_y])
                shoot_sound.play()
        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        if random.randint(1, 50) == 1:
            targets.append([random.randint(0, SCREEN_WIDTH - target_img.get_width()), 0])
        for target in targets[:]:
            target[1] += target_speed
            if target[1] > SCREEN_HEIGHT:
                targets.remove(target)
                lives -= 1
                if lives == 0:
                    game_over_screen(score, start_time)
                    running = False
            for bullet in bullets[:]:
                if (
                    bullet[0] in range(target[0], target[0] + target_img.get_width())
                    and bullet[1] in range(target[1], target[1] + target_img.get_height())
                ):
                    bullets.remove(bullet)
                    targets.remove(target)
                    score += 1
                    hit_sound.play()
                    break
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet)
        for target in targets:
            draw_target(target)
        display_score_and_lives(score, lives)
        pygame.display.flip()
        clock.tick(60)
def run_game():
    while True:
        action = show_menu()
        if action == "play":
            main_game()
        elif action == "high_scores":
            display_high_scores()
        elif action == "quit":
            pygame.quit()
            sys.exit()
run_game()