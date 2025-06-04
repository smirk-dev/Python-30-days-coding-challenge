import pygame
import math
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SUN_COLOR = (255, 204, 0)
PLANET_COLORS = [(66, 135, 245), (255, 87, 51), (80, 200, 120), (255, 51, 153), (255, 153, 51), (153, 51, 255)]
font = pygame.font.Font(None, 24)
G = 0.05
FPS = 60
class Planet:
    def __init__(self, x, y, radius, color, mass, vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.orbit = []
    def draw(self, screen):
        if len(self.orbit) > 2:
            pygame.draw.lines(screen, self.color, False, self.orbit, 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    def update_position(self, celestial_body):
        dx = celestial_body.x - self.x
        dy = celestial_body.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return
        force = G * celestial_body.mass / (distance**2)
        fx = force * dx / distance
        fy = force * dy / distance
        self.vx += fx
        self.vy += fy
        self.x += self.vx
        self.y += self.vy
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 200:
            self.orbit.pop(0)
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
def add_planet():
    radius = random.randint(5, 15)
    distance = random.randint(50, 200)
    angle = random.uniform(0, 2 * math.pi)
    x = sun.x + distance * math.cos(angle)
    y = sun.y + distance * math.sin(angle)
    speed = math.sqrt(G * sun.mass / distance)
    vx = -speed * math.sin(angle)
    vy = speed * math.cos(angle)
    color = random.choice(PLANET_COLORS)
    mass = random.uniform(1, 5)
    return Planet(x, y, radius, color, mass, vx, vy)
def display_stats(planets):
    y_offset = 10
    for i, planet in enumerate(planets):
        stats_text = f"Planet {i + 1}: Mass={planet.mass:.2f}"
        stats_surface = font.render(stats_text, True, WHITE)
        screen.blit(stats_surface, (10, y_offset))
        y_offset += 20
sun = Planet(WIDTH // 2, HEIGHT // 2, 30, SUN_COLOR, mass=1000)
planets = [add_planet() for _ in range(5)]
buttons = [
    Button(10, HEIGHT - 100, 120, 30, "Add Planet", action=lambda: planets.append(add_planet())),
    Button(10, HEIGHT - 60, 120, 30, "Remove Planet", action=lambda: planets.pop() if planets else None),
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
    if not paused:
        for planet in planets:
            planet.update_position(sun)
    sun.draw(screen)
    for planet in planets:
        planet.draw(screen)
    for button in buttons:
        button.draw(screen)
    display_stats(planets)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()