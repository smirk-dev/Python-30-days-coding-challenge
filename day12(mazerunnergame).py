import pygame
import random
import time
import os
pygame.init()
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
BG_GRADIENT_TOP = (70, 130, 180)  # Steel Blue
BG_GRADIENT_BOTTOM = (135, 206, 250)  # Sky Blue
BUTTON_COLOR = (255, 255, 255)  # White
HOVER_COLOR = (220, 220, 220)  # Light Gray
TEXT_COLOR = (0, 102, 204)  # Dark Blue
TEXT_HOVER_COLOR = (0, 51, 102)  # Darker Blue
WALL_COLOR = (100, 149, 237)  # Cornflower Blue
END_COLOR = (50, 205, 50)  # Lime Green
pygame.mixer.init()
move_sound = pygame.mixer.Sound("move_sound.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")
pygame.mixer.music.load("background_music.mp3")
SAVE_FILE = "last_runtime.txt"
def save_runtime(runtime):
    with open(SAVE_FILE, "w") as file:
        file.write(str(runtime))
def load_runtime():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            return file.read()
    return "No previous runtime"
def draw_gradient(screen, top_color, bottom_color):
    for y in range(HEIGHT):
        color = [
            top_color[i] + (bottom_color[i] - top_color[i]) * y // HEIGHT
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
def draw_button(screen, text, font, x, y, w, h, is_hovered):
    button_color = HOVER_COLOR if is_hovered else BUTTON_COLOR
    text_color = TEXT_HOVER_COLOR if is_hovered else TEXT_COLOR
    pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=20)
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(button_text, text_rect)
def menu_screen(screen):
    font_large = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 40)
    last_runtime = load_runtime()
    title = font_large.render("Maze Runner", True, TEXT_COLOR)
    button_width, button_height = 200, 60
    play_button_rect = pygame.Rect(
        WIDTH // 2 - button_width // 2, HEIGHT // 2 - 80, button_width, button_height
    )
    quit_button_rect = pygame.Rect(
        WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height
    )
    runtime_text = font_medium.render(f"Last Runtime: {last_runtime}", True, TEXT_COLOR)
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        play_hover = play_button_rect.collidepoint(mouse_x, mouse_y)
        quit_hover = quit_button_rect.collidepoint(mouse_x, mouse_y)
        screen.fill(BG_GRADIENT_TOP)
        draw_gradient(screen, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM)
        screen.blit(
            title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - title.get_height())
        )
        draw_button(
            screen, "Play", font_medium, *play_button_rect, is_hovered=play_hover
        )
        draw_button(
            screen, "Quit", font_medium, *quit_button_rect, is_hovered=quit_hover
        )
        runtime_rect = runtime_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(runtime_text, runtime_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_hover:
                    return "play"
                if quit_hover:
                    return "quit"
def create_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    def carve_path(x, y):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx][y + dy] = 0
                carve_path(nx, ny)
    maze[1][1] = 0
    carve_path(1, 1)
    maze[rows - 2][cols - 2] = 0
    return maze
def draw_maze(screen, maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            color = WALL_COLOR if maze[row][col] == 1 else BG_GRADIENT_TOP
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
def run_game(screen):
    rows, cols = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
    maze = create_maze(rows, cols)
    player_image = pygame.image.load("player_image.png")
    player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
    player_x, player_y = TILE_SIZE, TILE_SIZE
    end_x, end_y = (cols - 2) * TILE_SIZE, (rows - 2) * TILE_SIZE
    start_time = time.time()
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(BG_GRADIENT_TOP)
        draw_maze(screen, maze)
        pygame.draw.rect(screen, END_COLOR, (end_x, end_y, TILE_SIZE, TILE_SIZE))
        screen.blit(player_image, (player_x, player_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_UP]:
            new_y -= TILE_SIZE
            move_sound.play()
        if keys[pygame.K_DOWN]:
            new_y += TILE_SIZE
            move_sound.play()
        if keys[pygame.K_LEFT]:
            new_x -= TILE_SIZE
            move_sound.play()
        if keys[pygame.K_RIGHT]:
            new_x += TILE_SIZE
            move_sound.play()
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            if maze[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0:
                player_x, player_y = new_x, new_y
        if player_x == end_x and player_y == end_y:
            screen.fill(BG_GRADIENT_BOTTOM)
            win_text = pygame.font.Font(None, 80).render("You Win!", True, TEXT_COLOR)
            screen.blit(
                win_text,
                (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2),
            )
            pygame.display.flip()
            win_sound.play()
            time.sleep(3)
            save_runtime(round(time.time() - start_time, 2))
            return
        pygame.display.flip()
        clock.tick(30)
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Runner")
    pygame.mixer.music.play(-1, 0.0)
    while True:
        choice = menu_screen(screen)
        if choice == "play":
            run_game(screen)
        elif choice == "quit":
            pygame.quit()
            exit()
if __name__ == "__main__":
    main()