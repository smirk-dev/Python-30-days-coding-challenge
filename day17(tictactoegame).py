import pygame
import sys
import random
import math
pygame.init()
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4
BG_GRADIENT_START = (40, 170, 220)
BG_GRADIENT_END = (15, 130, 180)
LINE_COLOR = (255, 255, 255)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 50)
RESULT_FONT = pygame.font.Font(None, 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
try:
    move_sound = pygame.mixer.Sound("move.wav")
    win_sound = pygame.mixer.Sound("win.wav")
    lose_sound = pygame.mixer.Sound("lose.wav")
except pygame.error:
    move_sound = win_sound = lose_sound = None
    print("Sound files not found. Continuing without sound effects.")
board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
difficulty = "Easy"
def draw_gradient():
    for i in range(HEIGHT):
        color = [
            BG_GRADIENT_START[j] + (BG_GRADIENT_END[j] - BG_GRADIENT_START[j]) * i // HEIGHT
            for j in range(3)
        ]
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    text_surface = FONT.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))
def draw_menu():
    screen.fill(BUTTON_COLOR)
    title = FONT.render("Tic-Tac-Toe", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 5))
    draw_button("Easy", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, set_easy)
    draw_button("Intermediate", WIDTH // 2 - 150, HEIGHT // 2, 300, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, set_intermediate)
    draw_button("Hard", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, set_hard)
    draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, quit_game)
    pygame.display.update()
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center = (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2))
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
def check_winner():
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            return board[row][0]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != 0:
        return board[2][0]
    if not any(0 in row for row in board):
        return -1
    return 0
def display_winner(winner):
    result = "You Win!" if winner == 1 else "You Lose!" if winner == 2 else "It's a Draw!"
    result_color = (0, 255, 0) if winner == 1 else (255, 0, 0) if winner == 2 else (255, 255, 0)
    result_text = RESULT_FONT.render(result, True, result_color)
    restart_text = FONT.render("Returning to menu...", True, TEXT_COLOR)
    draw_gradient()
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)
def restart():
    global board
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    draw_gradient()
    draw_lines()
def quit_game():
    pygame.quit()
    sys.exit()
def set_easy():
    global difficulty
    difficulty = "Easy"
    start_game()
def set_intermediate():
    global difficulty
    difficulty = "Intermediate"
    start_game()
def set_hard():
    global difficulty
    difficulty = "Hard"
    start_game()
def start_game():
    global in_menu
    in_menu = False
    restart()
def random_move():
    available = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 0]
    if available:
        move = random.choice(available)
        board[move[0]][move[1]] = 2
def smart_move():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                if check_winner() == 2:
                    return
                board[row][col] = 0
    random_move()
def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == 1:
        return -10 + depth
    if winner == 2:
        return 10 - depth
    if winner == -1:
        return 0
    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    evaluation = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    evaluation = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    min_eval = min(min_eval, evaluation)
        return min_eval
def best_move():
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = 2
def ai_move():
    if difficulty == "Easy":
        random_move()
    elif difficulty == "Intermediate":
        smart_move()
    elif difficulty == "Hard":
        best_move()
running = True
in_menu = True
player = 1
while running:
    if in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game()
    else:
        draw_gradient()
        draw_lines()
        draw_figures()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN and player == 1:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                if board[clicked_row][clicked_col] == 0:
                    board[clicked_row][clicked_col] = 1
                    if move_sound:
                        pygame.mixer.Sound.play(move_sound)
                    if check_winner():
                        display_winner(check_winner())
                        in_menu = True
                        restart()
                    player = 2
            if player == 2 and not in_menu:
                ai_move()
                if check_winner():
                    display_winner(check_winner())
                    in_menu = True
                    restart()
                player = 1
        if not any(0 in row for row in board):
            display_winner(-1)
            in_menu = True
            restart()
    pygame.display.update()
pygame.quit()