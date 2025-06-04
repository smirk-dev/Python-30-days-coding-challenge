import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
BG_COLOR = (30, 30, 30)  # Dark gray
HOVER_COLOR = (100, 100, 100)  # Lighter gray for hover
WHITE = (255, 255, 255)
rock_img = pygame.image.load("rock.png")
paper_img = pygame.image.load("paper.png")
scissors_img = pygame.image.load("scissors.png")
click_sound = pygame.mixer.Sound("click.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
draw_sound = pygame.mixer.Sound("draw.wav")
choice_size = (150, 150)
hover_size = (170, 170)  # Slightly larger for hover effect
rock_img = pygame.transform.scale(rock_img, choice_size)
paper_img = pygame.transform.scale(paper_img, choice_size)
scissors_img = pygame.transform.scale(scissors_img, choice_size)
font = pygame.font.Font(pygame.font.get_default_font(), 36)
result_font = pygame.font.Font(pygame.font.get_default_font(), 50)
rock_pos = (150, 300)
paper_pos = (325, 300)
scissors_pos = (500, 300)
choices = ["Rock", "Paper", "Scissors"]
user_choice = None
computer_choice = None
result = None
def draw_text(text, font, color, x, y):
    """Draws text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)
def check_hover(pos, rect):
    """Checks if the mouse is hovering over a button."""
    return rect.collidepoint(pos)
def play_game(user_choice):
    """Handles the game logic."""
    global computer_choice, result
    computer_choice = random.choice(choices)
    if user_choice == computer_choice:
        result = "Draw"
        pygame.mixer.Sound.play(draw_sound)
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "You Win!"
        pygame.mixer.Sound.play(win_sound)
    else:
        result = "You Lose"
        pygame.mixer.Sound.play(lose_sound)
def draw_buttons():
    """Draws buttons with hover effect."""
    mouse_pos = pygame.mouse.get_pos()
    rock_img_scaled = pygame.transform.scale(rock_img, hover_size if check_hover(mouse_pos, pygame.Rect(*rock_pos, *choice_size)) else choice_size)
    rock_rect = screen.blit(rock_img_scaled, rock_pos)
    paper_img_scaled = pygame.transform.scale(paper_img, hover_size if check_hover(mouse_pos, pygame.Rect(*paper_pos, *choice_size)) else choice_size)
    paper_rect = screen.blit(paper_img_scaled, paper_pos)
    scissors_img_scaled = pygame.transform.scale(scissors_img, hover_size if check_hover(mouse_pos, pygame.Rect(*scissors_pos, *choice_size)) else choice_size)
    scissors_rect = screen.blit(scissors_img_scaled, scissors_pos)
    return rock_rect, paper_rect, scissors_rect
running = True
while running:
    screen.fill(BG_COLOR)
    draw_text("Rock, Paper, Scissors", font, WHITE, WIDTH // 2, 50)
    rock_rect, paper_rect, scissors_rect = draw_buttons()
    if result:
        draw_text(result, result_font, WHITE, WIDTH // 2, 150)
        draw_text(f"Computer chose: {computer_choice}", font, WHITE, WIDTH // 2, 200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if check_hover(pygame.mouse.get_pos(), rock_rect):
                    pygame.mixer.Sound.play(click_sound)
                    play_game("Rock")
                elif check_hover(pygame.mouse.get_pos(), paper_rect):
                    pygame.mixer.Sound.play(click_sound)
                    play_game("Paper")
                elif check_hover(pygame.mouse.get_pos(), scissors_rect):
                    pygame.mixer.Sound.play(click_sound)
                    play_game("Scissors")
    pygame.display.flip()