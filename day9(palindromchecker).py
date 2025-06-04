import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Palindrome Checker")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
DARK_MODE_BG = (30, 30, 30)
DARK_MODE_TEXT = (200, 200, 200)
LIGHT_MODE_BG = WHITE
LIGHT_MODE_TEXT = BLACK
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)
input_text = ""
feedback_message = ""
history = []
dark_mode = False
def draw_text(text, font, color, x, y, center=False):
    """Draw text on the screen."""
    render = font.render(text, True, color)
    if center:
        text_rect = render.get_rect(center=(x, y))
        screen.blit(render, text_rect)
    else:
        screen.blit(render, (x, y))
def draw_button(x, y, width, height, text, color, text_color, action=None):
    """Draw a clickable button."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, GRAY, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font_small, text_color, x + width // 2, y + height // 2, center=True)
def toggle_dark_mode():
    """Toggle between dark and light modes."""
    global dark_mode
    dark_mode = not dark_mode
def check_palindrome():
    """Check if the input text is a palindrome."""
    global feedback_message, history
    cleaned_text = ''.join(char.lower() for char in input_text if char.isalnum())
    is_palindrome = cleaned_text == cleaned_text[::-1]
    feedback_message = "Palindrome!" if is_palindrome else "Not a Palindrome."
    history.append((input_text, feedback_message))
def reset_input():
    """Reset the input text and feedback message."""
    global input_text, feedback_message
    input_text = ""
    feedback_message = ""
def render_history():
    """Render the history of past checks."""
    y_offset = 350
    for i, (text, result) in enumerate(history[-5:]):
        draw_text(f"{i+1}. {text} - {result}", font_small, DARK_MODE_TEXT if dark_mode else BLACK, 50, y_offset)
        y_offset += 30
running = True
while running:
    screen.fill(DARK_MODE_BG if dark_mode else LIGHT_MODE_BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                check_palindrome()
            elif event.unicode.isprintable():
                input_text += event.unicode
    draw_text("Palindrome Checker", font_large, DARK_MODE_TEXT if dark_mode else BLACK, WIDTH // 2, 50, center=True)
    draw_text("Enter Text:", font_medium, DARK_MODE_TEXT if dark_mode else BLACK, 50, 150)
    pygame.draw.rect(screen, GRAY, (50, 200, 700, 50))
    draw_text(input_text, font_medium, DARK_MODE_TEXT if dark_mode else BLACK, 60, 205)
    draw_text(feedback_message, font_medium, GREEN if "Palindrome" in feedback_message else RED, WIDTH // 2, 300, center=True)
    draw_button(50, 500, 200, 50, "Check", BLUE, WHITE, check_palindrome)
    draw_button(300, 500, 200, 50, "Reset", RED, WHITE, reset_input)
    draw_button(550, 500, 200, 50, "Toggle Mode", DARK_GRAY, WHITE, toggle_dark_mode)
    draw_text("History (Last 5):", font_medium, DARK_MODE_TEXT if dark_mode else BLACK, 50, 320)
    render_history()
    pygame.display.flip()