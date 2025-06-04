import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 4
PADDLE_SPEED = 8
SCORE_HEIGHT = 50  # Height of score area
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 30
BRICK_START_Y = SCORE_HEIGHT + 20  # Start bricks below score area
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
GRAY = (40, 40, 40)
FONT = pygame.font.Font(None, 36)
SCORE_FILE = "highscores.txt"

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()


# Load high scores
def load_high_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, "r") as file:
        return [int(line.strip()) for line in file.readlines()]


# Save high scores
def save_high_score(score):
    scores = load_high_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(SCORE_FILE, "w") as file:
        for s in scores:
            file.write(f"{s}\n")


# Button class
def draw_button(text, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    is_hovered = x < mouse[0] < x + width and y < mouse[1] < y + height
    color = BLUE if is_hovered else WHITE
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=5)
    text_surf = FONT.render(text, True, BLACK)
    screen.blit(
        text_surf,
        (
            x + (width - text_surf.get_width()) // 2,
            y + (height - text_surf.get_height()) // 2,
        ),
    )
    return is_hovered and pygame.mouse.get_pressed()[0]


# Menu screen
def menu_screen():
    while True:
        screen.fill(BLACK)
        title_text = FONT.render("Breakout Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 4))

        play_clicked = draw_button("Play", WIDTH // 2 - 75, HEIGHT // 2 - 30, 150, 50)
        scores_clicked = draw_button(
            "High Scores", WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50
        )
        quit_clicked = draw_button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 110, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

        if play_clicked:
            pygame.time.delay(200)
            return "PLAY"
        if scores_clicked:
            pygame.time.delay(200)
            return "SCORES"
        if quit_clicked:
            pygame.time.delay(200)
            return "QUIT"

        pygame.display.flip()
        clock.tick(60)


# Display high scores
def display_high_scores():
    while True:
        screen.fill(BLACK)
        screen.blit(
            FONT.render("High Scores", True, WHITE), (WIDTH // 2 - 50, HEIGHT // 4)
        )
        scores = load_high_scores()
        for i, score in enumerate(scores[:5]):
            screen.blit(
                FONT.render(f"{i+1}. {score}", True, WHITE),
                (WIDTH // 2 - 50, HEIGHT // 2 + i * 30),
            )

        back_clicked = draw_button("Back", WIDTH // 2 - 50, HEIGHT - 100, 100, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

        if back_clicked:
            pygame.time.delay(200)
            return "MENU"

        pygame.display.flip()
        clock.tick(60)


# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=5)


# Ball class
class Ball:
    def __init__(self, speed):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12)
        self.dx, self.dy = random.choice([-speed, speed]), -speed
        self.speed = speed

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= SCORE_HEIGHT:  # Updated collision with top
            self.dy *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)


# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y + BRICK_START_Y, BRICK_WIDTH - 5, BRICK_HEIGHT - 5)
        self.color = random.choice([RED, GREEN, BLUE])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)


# Main game function
def play_game():
    paddle = Paddle()
    level = 1
    score = 0
    ball = Ball(BALL_SPEED)
    bricks = [
        Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT)
        for x in range(BRICK_COLUMNS)
        for y in range(BRICK_ROWS)
    ]

    while True:
        screen.fill(BLACK)

        # Draw score area background
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, SCORE_HEIGHT))
        score_text = FONT.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(score_text, (20, (SCORE_HEIGHT - FONT.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(score)
                return "QUIT"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        ball.move()

        if ball.rect.colliderect(paddle.rect):
            ball.dy *= -1

        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                bricks.remove(brick)
                ball.dy *= -1
                score += 10
                break

        if not bricks:
            level += 1
            ball = Ball(ball.speed + 1)
            bricks = [
                Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT)
                for x in range(BRICK_COLUMNS)
                for y in range(BRICK_ROWS)
            ]

        if ball.rect.bottom >= HEIGHT:
            save_high_score(score)
            return "MENU"

        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()

        pygame.display.flip()
        clock.tick(60)


# Main game loop
def main():
    current_screen = "MENU"

    while True:
        if current_screen == "MENU":
            current_screen = menu_screen()
        elif current_screen == "PLAY":
            current_screen = play_game()
        elif current_screen == "SCORES":
            current_screen = display_high_scores()
        elif current_screen == "QUIT":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
