import pygame
import random
import sys
import os
import math
import json
from datetime import datetime

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
MINE_COUNT = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HOVER_BLUE = (30, 144, 255)  # Dodger blue for hover effect
BUTTON_NORMAL = (70, 130, 180)  # Steel blue for normal state
BUTTON_HOVER = (100, 149, 237)  # Cornflower blue for hover state

# Initialize fonts
pygame.font.init()
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 48)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Game states
PLAYING = 0
WON = 1
LOST = 2
MENU = 3
HIGH_SCORES = 4

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# High scores file
SCORES_FILE = "high_scores.json"

class Button:
    def __init__(self, x, y, width, height, text, font=FONT):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.normal_color = BUTTON_NORMAL
        self.hover_color = BUTTON_HOVER
        self.text_color = WHITE
        self.animation_progress = 0
        self.animation_speed = 0.2

    def draw(self, screen):
        # Update animation
        if self.is_hovered:
            self.animation_progress = min(1, self.animation_progress + self.animation_speed)
        else:
            self.animation_progress = max(0, self.animation_progress - self.animation_speed)

        # Interpolate color based on animation progress
        current_color = [
            self.normal_color[i] + (self.hover_color[i] - self.normal_color[i]) * self.animation_progress
            for i in range(3)
        ]

        # Draw button with rounded corners
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Add subtle border
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False
def load_mine_image():
    try:
        mine_image = pygame.image.load("mine.png")
        mine_image = pygame.transform.scale(mine_image, (CELL_SIZE - 4, CELL_SIZE - 4))
        return mine_image
    except pygame.error:
        return None

def load_high_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_high_score(time_taken):
    scores = load_high_scores()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    scores.append({"time": time_taken, "date": date_str})
    scores.sort(key=lambda x: x["time"])
    scores = scores[:10]  # Keep only top 10 scores
    
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def create_menu_buttons():
    buttons = {}
    start_y = HEIGHT // 2 - BUTTON_HEIGHT
    
    buttons['start'] = Button(
        WIDTH//2 - BUTTON_WIDTH//2,
        start_y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Start Game"
    )
    
    buttons['scores'] = Button(
        WIDTH//2 - BUTTON_WIDTH//2,
        start_y + BUTTON_HEIGHT + BUTTON_MARGIN,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "High Scores"
    )
    
    buttons['quit'] = Button(
        WIDTH//2 - BUTTON_WIDTH//2,
        start_y + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN),
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Quit"
    )
    
    return buttons

def create_back_button():
    return Button(
        WIDTH//2 - BUTTON_WIDTH//2,
        HEIGHT - BUTTON_HEIGHT - 20,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Back to Menu"
    )

def draw_menu():
    screen.fill(WHITE)
    
    # Draw title
    title = LARGE_FONT.render("MINESWEEPER", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    
    # Draw buttons
    buttons = create_menu_buttons()
    for button in buttons.values():
        button.draw(screen)
    
    pygame.display.flip()
    return buttons

def draw_high_scores():
    screen.fill(WHITE)
    
    # Draw title
    title = LARGE_FONT.render("HIGH SCORES", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Draw scores
    scores = load_high_scores()
    if not scores:
        no_scores = FONT.render("No scores yet!", True, BLACK)
        screen.blit(no_scores, (WIDTH//2 - no_scores.get_width()//2, HEIGHT//2))
    else:
        for i, score in enumerate(scores):
            score_text = FONT.render(
                f"{i+1}. {score['time']:.1f}s - {score['date']}", 
                True, 
                BLACK
            )
            screen.blit(score_text, (WIDTH//4, 120 + i*40))
    
    # Draw back button
    back_button = create_back_button()
    back_button.draw(screen)
    
    pygame.display.flip()
    return back_button

def generate_board():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < MINE_COUNT:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[y][x] = -1
    for x, y in mines:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] != -1:
                    board[ny][nx] += 1
    return board, mines

NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

def draw_board(board, revealed, flagged, game_state, mine_image, time_elapsed=None):
    screen.fill(WHITE)
    if time_elapsed is not None and game_state == PLAYING:
        timer_text = FONT.render(f"Time: {time_elapsed:.1f}s", True, BLACK)
        screen.blit(timer_text, (10, 10))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) in revealed:
                if board[y][x] == -1:
                    pygame.draw.rect(screen, RED, rect)
                    if mine_image:
                        screen.blit(mine_image, (x * CELL_SIZE + 2, y * CELL_SIZE + 2))
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if board[y][x] > 0:
                        text = FONT.render(str(board[y][x]), True, NUMBER_COLORS.get(board[y][x], BLACK))
                        text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
            elif (x, y) in flagged:
                pygame.draw.rect(screen, GRAY, rect)
                text = FONT.render("🚩", True, RED)
                text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
    if game_state in [WON, LOST]:
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((255, 255, 255, 128))
        screen.blit(surface, (0, 0))
        message = "You Won!" if game_state == WON else "Game Over!"
        text = FONT.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        if time_elapsed is not None:
            time_text = FONT.render(f"Time: {time_elapsed:.1f}s", True, BLACK)
            time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            screen.blit(time_text, time_rect)
        continue_text = FONT.render("Press ENTER to continue", True, BLACK)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(continue_text, continue_rect)
    pygame.display.flip()
    
def reveal_empty(board, x, y, revealed, flagged):
    if (x, y) in revealed or (x, y) in flagged:
        return
    revealed.add((x, y))
    if board[y][x] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    reveal_empty(board, nx, ny, revealed, flagged)
                    
def check_win(board, revealed, mines):
    return len(revealed) == GRID_SIZE * GRID_SIZE - len(mines)

def play_game():
    board, mines = generate_board()
    revealed = set()
    flagged = set()
    game_state = PLAYING
    mine_image = load_mine_image()
    start_time = pygame.time.get_ticks() / 1000
    time_elapsed = 0
    back_button = create_back_button()

    while True:
        if game_state == PLAYING:
            time_elapsed = pygame.time.get_ticks() / 1000 - start_time
        
        draw_board(board, revealed, flagged, game_state, mine_image, time_elapsed)
        
        if game_state in [WON, LOST]:
            back_button.draw(screen)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state in [WON, LOST]:
                if back_button.handle_event(event):
                    if game_state == WON:
                        save_high_score(time_elapsed)
                    return MENU

            if game_state == PLAYING and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    if event.button == 1:  # Left click
                        if (x, y) not in flagged:
                            if (x, y) in mines:
                                revealed.update(mines)
                                game_state = LOST
                            else:
                                reveal_empty(board, x, y, revealed, flagged)
                                if check_win(board, revealed, mines):
                                    game_state = WON
                    elif event.button == 3:  # Right click
                        if (x, y) not in revealed:
                            if (x, y) not in flagged:
                                flagged.add((x, y))
                            else:
                                flagged.remove((x, y))

def main():
    game_state = MENU
    clock = pygame.time.Clock()
    
    while True:
        if game_state == MENU:
            buttons = draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Update hover states
                if event.type == pygame.MOUSEMOTION:
                    for button in buttons.values():
                        button.handle_event(event)
                
                # Handle clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if buttons['start'].handle_event(event):
                        game_state = play_game()
                    elif buttons['scores'].handle_event(event):
                        game_state = HIGH_SCORES
                    elif buttons['quit'].handle_event(event):
                        pygame.quit()
                        sys.exit()
            
            # Ensure smooth hover animations
            pygame.display.flip()
            clock.tick(60)
        
        elif game_state == HIGH_SCORES:
            back_button = draw_high_scores()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Update hover state
                if event.type == pygame.MOUSEMOTION:
                    back_button.handle_event(event)
                
                # Handle click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.handle_event(event):
                        game_state = MENU
            
            # Ensure smooth hover animations
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()