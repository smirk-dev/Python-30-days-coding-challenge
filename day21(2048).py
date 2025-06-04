import random
import json
import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SIZE = 4
TILE_SIZE = 150  # Increased tile size
TILE_MARGIN = 15
WINDOW_SIZE = SIZE * TILE_SIZE + (SIZE + 1) * TILE_MARGIN
FONT = pygame.font.Font(None, 72)  # Increased font size
MENU_FONT = pygame.font.Font(None, 54)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}


class Button:
    def __init__(self, text, pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = font
        self.bg = bg
        self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, True, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.change_text(self.feedback, bg="red")
            return True
        return False


class Game2048:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.moves = 0
        self.high_score = self.load_high_score()
        self.add_new_tile()
        self.add_new_tile()
        self.game_over = False
        self.game_won = False

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"score": 0, "moves": float("inf")}

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            json.dump(self.high_score, file)

    def add_new_tile(self):
        empty_cells = [
            (r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def slide_row_left(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        for i in range(SIZE - 1):
            if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                new_row[i] *= 2
                new_row[i + 1] = 0
                self.score += new_row[i]
        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def rotate_grid_clockwise(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def move_left(self):
        new_grid = [self.slide_row_left(row) for row in self.grid]
        if new_grid != self.grid:
            self.grid = new_grid
            self.add_new_tile()
            self.moves += 1

    def move_right(self):
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()
        self.move_left()
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()

    def move_up(self):
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()
        self.move_left()
        self.rotate_grid_clockwise()

    def move_down(self):
        self.rotate_grid_clockwise()
        self.move_left()
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()
        self.rotate_grid_clockwise()

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for r in range(SIZE):
            for c in range(SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        for r in range(SIZE - 1):
            for c in range(SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def check_win(self):
        return any(2048 in row for row in self.grid)

    def update_high_score(self):
        if self.score > self.high_score["score"] or (
            self.score == self.high_score["score"]
            and self.moves < self.high_score["moves"]
        ):
            self.high_score = {"score": self.score, "moves": self.moves}
            self.save_high_score()

    def draw(self, screen):
        screen.fill((187, 173, 160))
        for r in range(SIZE):
            for c in range(SIZE):
                value = self.grid[r][c]
                color = COLORS.get(value, (60, 58, 50))
                rect = pygame.Rect(
                    c * TILE_SIZE + (c + 1) * TILE_MARGIN,
                    r * TILE_SIZE + (r + 1) * TILE_MARGIN,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                pygame.draw.rect(screen, color, rect, border_radius=10)
                if value != 0:
                    text = FONT.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def display_message(self, screen, message):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Main message
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 3))
        screen.blit(text, text_rect)

        # Menu options
        restart_text = MENU_FONT.render("Press R to Restart", True, (255, 255, 255))
        quit_text = MENU_FONT.render("Press Q to Quit", True, (255, 255, 255))

        restart_rect = restart_text.get_rect(
            center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
        )
        quit_rect = quit_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50))

        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


def display_menu(screen):
    screen.fill((187, 173, 160))

    title_font = pygame.font.Font(None, 84)
    menu_font = pygame.font.Font(None, 48)

    # Title with shadow effect
    title_shadow = title_font.render("2048", True, (160, 150, 140))
    title_text = title_font.render("2048", True, (80, 80, 80))

    # Center buttons horizontally
    button_x = WINDOW_SIZE // 2 - 100

    # Create buttons with different colors
    start_button = Button("New Game", (button_x, WINDOW_SIZE // 2), menu_font)

    scores_button = Button("High Scores", (button_x, WINDOW_SIZE // 2 + 80), menu_font)

    quit_button = Button("Quit", (button_x, WINDOW_SIZE // 2 + 160), menu_font)

    # Draw title with shadow
    title_rect = title_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    shadow_rect = title_shadow.get_rect(
        center=(WINDOW_SIZE // 2 + 2, WINDOW_SIZE // 4 + 2)
    )
    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)

    # Show buttons
    start_button.show(screen)
    scores_button.show(screen)
    quit_button.show(screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.click(event):
                    return "start"
                elif scores_button.click(event):
                    return "highscores"
                elif quit_button.click(event):
                    pygame.quit()
                    sys.exit()

        # Update button hover states
        start_button.show(screen)
        scores_button.show(screen)
        quit_button.show(screen)
        pygame.display.flip()


def display_high_scores(screen):
    screen.fill((187, 173, 160))

    title_font = pygame.font.Font(None, 74)
    menu_font = pygame.font.Font(None, 48)

    title_text = title_font.render("Top 5 High Scores", True, (255, 255, 255))
    screen.blit(
        title_text, title_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    )

    try:
        with open("highscore.txt", "r") as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = []

    # Sort high scores by score and moves
    high_scores = sorted(high_scores, key=lambda x: (-x["score"], x["moves"]))

    for i, score in enumerate(high_scores[:5]):
        score_text = menu_font.render(
            f"{i + 1}. {score['score']} - {score['moves']} moves", True, (255, 255, 255)
        )
        screen.blit(
            score_text,
            score_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + i * 50)),
        )

    back_button = Button(
        "Back",
        (WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 + 300),
        menu_font,
        bg="blue",
        feedback="back",
    )
    back_button.show(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.click(event):
                    waiting = False


def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("2048 Game")

    while True:
        choice = display_menu(screen)
        if choice == "start":
            game = Game2048()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif (
                        event.type == pygame.KEYDOWN
                        and not game.game_over
                        and not game.game_won
                    ):
                        if event.key == pygame.K_UP:
                            game.move_up()
                        elif event.key == pygame.K_DOWN:
                            game.move_down()
                        elif event.key == pygame.K_LEFT:
                            game.move_left()
                        elif event.key == pygame.K_RIGHT:
                            game.move_right()

                        if game.check_win() and not game.game_won:
                            game.game_won = True
                            game.display_message(screen, "You Win!")
                        elif game.is_game_over() and not game.game_over:
                            game.game_over = True
                            game.display_message(screen, "Game Over!")

                game.draw(screen)
                pygame.display.flip()
        elif choice == "highscores":
            display_high_scores(screen)


if __name__ == "__main__":
    main()
