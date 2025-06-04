import pygame
import random
import sys
import time
WIDTH = 1000
HEIGHT = 600
BAR_WIDTH = 20
NUM_BARS = WIDTH // BAR_WIDTH
FPS = 60
WHITE = (240, 240, 240)
BLUE = (50, 130, 250)
RED = (255, 70, 70)
GREEN = (60, 180, 75)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (150, 150, 150)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
pygame.init()
pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
def draw_bars(screen, array, current_indices=None):
    screen.fill(WHITE)
    for i, value in enumerate(array):
        color = BLUE if not current_indices or i not in current_indices else RED
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH - 2, value))
    pygame.display.flip()
def bubble_sort(array, screen):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_bars(screen, array, [j, j + 1])
            pygame.time.delay(30)
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
def selection_sort(array, screen):
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_bars(screen, array, [j, min_idx])
            pygame.time.delay(30)
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
def insertion_sort(array, screen):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            draw_bars(screen, array, [j, j + 1])
            pygame.time.delay(30)
            j -= 1
        array[j + 1] = key
def quick_sort(array, screen, low, high):
    if low < high:
        pivot_index = partition(array, screen, low, high)
        quick_sort(array, screen, low, pivot_index - 1)
        quick_sort(array, screen, pivot_index + 1, high)
def partition(array, screen, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        draw_bars(screen, array, [j, high])
        pygame.time.delay(30)
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1
def merge_sort(array, screen, left=0, right=None):
    if right is None:
        right = len(array) - 1
    if left < right:
        mid = (left + right) // 2
        merge_sort(array, screen, left, mid)
        merge_sort(array, screen, mid + 1, right)
        temp = []
        i, j = left, mid + 1
        while i <= mid and j <= right:
            if array[i] < array[j]:
                temp.append(array[i])
                i += 1
            else:
                temp.append(array[j])
                j += 1
        while i <= mid:
            temp.append(array[i])
            i += 1
        while j <= right:
            temp.append(array[j])
            j += 1
        for k, val in enumerate(temp):
            array[left + k] = val
            draw_bars(screen, array, [left + k])
            pygame.time.delay(30)
def button(screen, text, x, y, width, height, font, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    is_hover = x < mouse[0] < x + width and y < mouse[1] < y + height
    color = HOVER_COLOR if is_hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    if is_hover and click[0] == 1 and action:
        click_sound.play()
        time.sleep(0.2)
        action()
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Visualizer")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Quick Sort": lambda arr, scr: quick_sort(arr, scr, 0, len(arr) - 1),
        "Merge Sort": lambda arr, scr: merge_sort(arr, scr),
    }
    def start_sorting(algorithm):
        array = [random.randint(50, HEIGHT - 50) for _ in range(NUM_BARS)]
        algorithm(array, screen)
    running = True
    while running:
        screen.fill(WHITE)
        title = font.render("Sorting Algorithm Visualizer", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        y_offset = 100
        for i, (name, algorithm) in enumerate(algorithms.items()):
            button(screen, name, WIDTH // 2 - 150, y_offset + i * 80, 300, 60, font, lambda alg=algorithm: start_sorting(alg))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()