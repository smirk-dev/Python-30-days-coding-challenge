import pygame
import math
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atomic Model Simulation")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NUCLEUS_COLOR = (255, 0, 0)
ELECTRON_COLOR = (66, 135, 245)
font = pygame.font.Font(None, 24)
FPS = 60
NUCLEUS_RADIUS = 20
ORBIT_COLORS = [(200, 200, 200), (170, 170, 170), (140, 140, 140)]
class Electron:
    def __init__(self, radius, speed, angle):
        self.radius = radius
        self.speed = speed
        self.angle = angle
    def update_position(self):
        self.angle += self.speed
    def draw(self, screen, nucleus_x, nucleus_y):
        x = nucleus_x + self.radius * math.cos(self.angle)
        y = nucleus_y + self.radius * math.sin(self.angle)
        pygame.draw.circle(screen, ELECTRON_COLOR, (int(x), int(y)), 5)
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
def add_electron():
    radius = random.randint(50, 200)
    speed = random.uniform(0.01, 0.05)
    angle = random.uniform(0, 2 * math.pi)
    electrons.append(Electron(radius, speed, angle))
def display_stats():
    stats_text = f"Electrons: {len(electrons)}"
    avg_radius = sum(e.radius for e in electrons) / len(electrons) if electrons else 0
    avg_radius_text = f"Average Radius: {avg_radius:.2f}"
    stats_surface = font.render(stats_text, True, WHITE)
    avg_radius_surface = font.render(avg_radius_text, True, WHITE)
    screen.blit(stats_surface, (10, 10))
    screen.blit(avg_radius_surface, (10, 40))
nucleus_x, nucleus_y = WIDTH // 2, HEIGHT // 2
electrons = [Electron(random.randint(50, 200), random.uniform(0.01, 0.05), random.uniform(0, 2 * math.pi)) for _ in range(5)]
buttons = [
    Button(10, HEIGHT - 100, 120, 30, "Add Electron", action=lambda: add_electron()),
    Button(10, HEIGHT - 60, 120, 30, "Remove Electron", action=lambda: electrons.pop() if electrons else None),
    Button(10, HEIGHT - 20, 120, 30, "Pause/Play")
]
paused = False
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    if button.action:
                        button.action()
                        if button.text == "Pause/Play":
                            paused = not paused
    pygame.draw.circle(screen, NUCLEUS_COLOR, (nucleus_x, nucleus_y), NUCLEUS_RADIUS)
    if not paused:
        for electron in electrons:
            electron.update_position()
    for electron in electrons:
        electron.draw(screen, nucleus_x, nucleus_y)
    for button in buttons:
        button.draw(screen)
    display_stats()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()