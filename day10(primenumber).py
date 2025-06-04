import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 600, 400
LIGHT_BG = (230, 230, 250)  # Lavender
DARK_BG = (32, 58, 67)  # Teal
BUTTON_COLOR = (244, 164, 96)  # Light Coral
BUTTON_HOVER = (255, 99, 71)  # Bright Coral
TEXT_COLOR_LIGHT = (25, 25, 112)  # Midnight Blue
TEXT_COLOR_DARK = (245, 245, 245)  # Warm White
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prime Number Checker")
input_number = ""
result_message = ""
dark_mode = False
def toggle_dark_mode():
    """Switch between light and dark mode."""
    global dark_mode
    dark_mode = not dark_mode
def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
def draw_text(text, font, color, x, y):
    """Draw text on the screen."""
    render = font.render(text, True, color)
    screen.blit(render, (x, y))
def draw_button(x, y, width, height, text, action=None):
    """Draw a button with hover effects."""
    global dark_mode
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_color = BUTTON_COLOR
    text_color = TEXT_COLOR_LIGHT if not dark_mode else TEXT_COLOR_DARK
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER, (x, y, width, height), border_radius=10)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    draw_text(text, font_small, text_color, x + width // 4, y + height // 4)
def check_prime():
    """Check the input number and update the result."""
    global input_number, result_message
    try:
        num = int(input_number)
        if is_prime(num):
            result_message = f"{num} is a prime number!"
        else:
            result_message = f"{num} is not a prime number."
    except ValueError:
        result_message = "Invalid input. Enter a valid number!"
def reset_input():
    """Reset the input field and result."""
    global input_number, result_message
    input_number = ""
    result_message = ""
running = True
while running:
    screen.fill(DARK_BG if dark_mode else LIGHT_BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_number = input_number[:-1]
            elif event.key == pygame.K_RETURN:
                check_prime()
            elif event.unicode.isdigit():
                input_number += event.unicode
    draw_text("Prime Checker", font_large, TEXT_COLOR_DARK if dark_mode else TEXT_COLOR_LIGHT, WIDTH // 5, HEIGHT // 10)
    draw_text("Enter a number:", font_medium, TEXT_COLOR_DARK if dark_mode else TEXT_COLOR_LIGHT, 50, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 160, 500, 50), border_radius=10)
    draw_text(input_number, font_medium, TEXT_COLOR_LIGHT if not dark_mode else TEXT_COLOR_DARK, 60, 165)
    draw_text(result_message, font_small, TEXT_COLOR_LIGHT if dark_mode else TEXT_COLOR_DARK, 50, 230)
    draw_button(50, 300, 150, 50, "Check", check_prime)
    draw_button(225, 300, 150, 50, "Reset", reset_input)
    draw_button(400, 300, 175, 50, "Dark Mode", toggle_dark_mode)
    pygame.display.flip()