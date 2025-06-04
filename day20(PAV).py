import pygame
import random
import heapq
from typing import List, Tuple, Optional
import math
import time

# initialize pygame
pygame.init()

# set window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# set grid size and animation speed
GRID_SIZE = 25
ANIMATION_SPEED = 8
FPS = 60

# define colors
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (20, 20, 20),
    'BLUE': (65, 105, 225),
    'RED': (220, 50, 50),
    'GREEN': (34, 139, 34),
    'YELLOW': (255, 215, 0),
    'GREY': (128, 128, 128),
    'LIGHT_BLUE': (176, 224, 230),
    'LIGHT_GREEN': (144, 238, 144),
    'VISITED_A': (147, 112, 219, 150),
    'VISITED_D': (144, 238, 144, 150),
    'BUTTON_NORMAL': (70, 70, 70),
    'BUTTON_HOVER': (90, 90, 90),
    'BUTTON_TEXT': (240, 240, 240)
}

# button class to create interactive buttons
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False
        self.font = pygame.font.Font(None, 28)

    # handle mouse events for the button
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    # draw the button on the screen
    def draw(self, surface: pygame.Surface):
        color = COLORS['BUTTON_HOVER'] if self.is_hovered else COLORS['BUTTON_NORMAL']
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        border_color = COLORS['WHITE'] if self.is_hovered else (*COLORS['WHITE'][:3], 150)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)
        text_surface = self.font.render(self.text, True, COLORS['BUTTON_TEXT'])
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)

# node class to represent each cell in the grid
class Node:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.visited = False
        self.parent = None
        self.g = float('inf')
        self.h = float('inf')
        self.animation_progress = 0.0
        self.visit_time = 0

    # comparison method for priority queue
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    # draw the node on the screen
    def draw(self, surface: pygame.Surface, offset_x: int = 0, current_time: float = 0):
        rect = pygame.Rect(
            self.x + offset_x, 
            self.y, 
            GRID_SIZE - 1, 
            GRID_SIZE - 1
        )
        if self.is_wall:
            pygame.draw.rect(surface, COLORS['BLACK'], rect, border_radius=3)
        else:
            pygame.draw.rect(surface, COLORS['WHITE'], rect, border_radius=3)
        if self.visited:
            progress = min(1.0, (current_time - self.visit_time) / 0.5)
            if progress < 1.0:
                size_factor = 1.0 - math.sin(progress * math.pi) * 0.2
                animation_rect = pygame.Rect(
                    rect.centerx - (rect.width * size_factor) / 2,
                    rect.centery - (rect.height * size_factor) / 2,
                    rect.width * size_factor,
                    rect.height * size_factor
                )
                color = COLORS['VISITED_A'] if offset_x == 0 else COLORS['VISITED_D']
                color_with_alpha = (*color[:3], int(255 * progress))
                pygame.draw.rect(surface, color_with_alpha, animation_rect, border_radius=3)
            else:
                color = COLORS['VISITED_A'] if offset_x == 0 else COLORS['VISITED_D']
                pygame.draw.rect(surface, color, rect, border_radius=3)
        if self.is_start:
            self._draw_triangle(surface, rect, COLORS['BLUE'])
        elif self.is_end:
            self._draw_target(surface, rect)

    # draw a triangle to represent the start node
    def _draw_triangle(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int]):
        points = [
            (rect.centerx - 8, rect.centery + 8),
            (rect.centerx + 8, rect.centery),
            (rect.centerx - 8, rect.centery - 8)
        ]
        pygame.draw.polygon(surface, color, points)

    # draw a target to represent the end node
    def _draw_target(self, surface: pygame.Surface, rect: pygame.Rect):
        pygame.draw.circle(surface, COLORS['RED'], rect.center, 8)
        pygame.draw.circle(surface, COLORS['WHITE'], rect.center, 6)
        pygame.draw.circle(surface, COLORS['RED'], rect.center, 4)

# pathfinding visualizer class to manage the visualization
class PathfindingVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pathfinding Visualizer - A* vs Dijkstra")
        self.clock = pygame.time.Clock()
        self.rows = WINDOW_HEIGHT // GRID_SIZE
        self.cols = (WINDOW_WIDTH // 2) // GRID_SIZE
        self.grid_a = self._create_grid()
        self.grid_d = self._create_grid()
        button_width = 160
        button_height = 40
        total_buttons_width = button_width * 3 + 40
        start_x = (WINDOW_WIDTH - total_buttons_width) // 2
        self.buttons = [
            Button(start_x, WINDOW_HEIGHT - 60, button_width, button_height, "Generate Maze", self._generate_new_maze),
            Button(start_x + button_width + 20, WINDOW_HEIGHT - 60, button_width, button_height, "Start Search", self._start_search),
            Button(start_x + (button_width + 20) * 2, WINDOW_HEIGHT - 60, button_width, button_height, "Clear Path", self._clear_path)
        ]
        self.running = True
        self.searching = False
        self.path_a = []
        self.path_d = []
        self.start_time = time.time()

    # a* algorithm implementation
    def _a_star(self, grid: List[List[Node]]) -> List[Node]:
        start = grid[0][0]
        end = grid[self.rows-1][self.cols-1]
        start.g = 0
        start.h = self._manhattan_distance(start, end)
        open_set = [(start.g + start.h, start)]
        closed_set = set()
        while open_set and self.searching:
            current = heapq.heappop(open_set)[1]
            if current == end:
                return self._reconstruct_path(current)
            if current not in closed_set:
                closed_set.add(current)
                current.visited = True
                current.visit_time = time.time()
                self._draw()
                pygame.time.wait(ANIMATION_SPEED)
                for neighbor in self._get_neighbors(current, grid):
                    if neighbor in closed_set or neighbor.is_wall:
                        continue
                    tentative_g = current.g + 1
                    if tentative_g < neighbor.g:
                        neighbor.parent = current
                        neighbor.g = tentative_g
                        neighbor.h = self._manhattan_distance(neighbor, end)
                        heapq.heappush(open_set, (neighbor.g + neighbor.h, neighbor))
        return []

    # dijkstra's algorithm implementation
    def _dijkstra(self, grid: List[List[Node]]) -> List[Node]:
        start = grid[0][0]
        end = grid[self.rows-1][self.cols-1]
        start.g = 0
        pq = [(0, start)]
        visited = set()
        while pq and self.searching:
            current = heapq.heappop(pq)[1]
            if current == end:
                return self._reconstruct_path(current)
            if current not in visited:
                visited.add(current)
                current.visited = True
                current.visit_time = time.time()
                self._draw()
                pygame.time.wait(ANIMATION_SPEED)
                for neighbor in self._get_neighbors(current, grid):
                    if neighbor in visited or neighbor.is_wall:
                        continue
                    tentative_g = current.g + 1
                    if tentative_g < neighbor.g:
                        neighbor.parent = current
                        neighbor.g = tentative_g
                        heapq.heappush(pq, (neighbor.g, neighbor))
        return []

    # draw the grid and paths on the screen
    def _draw(self):
        self.screen.fill(COLORS['GREY'])
        current_time = time.time()
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_a[r][c].draw(self.screen, 0, current_time)
                self.grid_d[r][c].draw(self.screen, WINDOW_WIDTH//2, current_time)
        self._draw_path(self.path_a, COLORS['BLUE'], 0)
        self._draw_path(self.path_d, COLORS['GREEN'], WINDOW_WIDTH//2)
        pygame.draw.line(self.screen, COLORS['WHITE'],
            (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT), 2)
        font = pygame.font.Font(None, 36)
        a_star_text = font.render("A* Algorithm", True, COLORS['BLUE'])
        dijkstra_text = font.render("Dijkstra's Algorithm", True, COLORS['GREEN'])
        padding = 40
        self.screen.blit(a_star_text, (WINDOW_WIDTH//4 - a_star_text.get_width()//2, padding))
        self.screen.blit(dijkstra_text, (3*WINDOW_WIDTH//4 - dijkstra_text.get_width()//2, padding))
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    # draw the path on the screen
    def _draw_path(self, path: List[Node], color: Tuple[int, int, int], offset_x: int):
        if not path:
            return
        for i in range(len(path) - 1):
            start_pos = (path[i].x + GRID_SIZE//2 + offset_x, path[i].y + GRID_SIZE//2)
            end_pos = (path[i+1].x + GRID_SIZE//2 + offset_x, path[i+1].y + GRID_SIZE//2)
            pygame.draw.line(self.screen, color, start_pos, end_pos, 4)
            pygame.draw.circle(self.screen, color, start_pos, 4)
        if path:
            final_pos = (path[-1].x + GRID_SIZE//2 + offset_x, path[-1].y + GRID_SIZE//2)
            pygame.draw.circle(self.screen, color, final_pos, 4)

    # main loop to run the visualizer
    def run(self):
        self._generate_new_maze()
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()

    # create a grid of nodes
    def _create_grid(self) -> List[List[Node]]:
        return [[Node(r, c) for c in range(self.cols)] for r in range(self.rows)]

    # generate a new maze
    def _generate_new_maze(self):
        self.grid_a = self._create_grid()
        self.grid_d = self._create_grid()

        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < 0.3:
                    self.grid_a[r][c].is_wall = True
                    self.grid_d[r][c].is_wall = True
        self.grid_a[0][0].is_start = True
        self.grid_d[0][0].is_start = True
        self.grid_a[self.rows-1][self.cols-1].is_end = True
        self.grid_d[self.rows-1][self.cols-1].is_end = True
        for grid in [self.grid_a, self.grid_d]:
            grid[0][0].is_wall = False
            grid[self.rows-1][self.cols-1].is_wall = False
        self._clear_path()

    # clear the current path
    def _clear_path(self):
        self.path_a = []
        self.path_d = []
        self.searching = False
        for r in range(self.rows):
            for c in range(self.cols):
                for node in [self.grid_a[r][c], self.grid_d[r][c]]:
                    node.visited = False
                    node.parent = None
                    node.g = float('inf')
                    node.h = float('inf')
                    node.animation_progress = 0
                    node.visit_time = 0

    # start the search algorithms
    def _start_search(self):
        if not self.searching:
            self._clear_path()
            self.searching = True
            self.path_a = self._a_star(self.grid_a)
            self.path_d = self._dijkstra(self.grid_d)

    # calculate manhattan distance between two nodes
    def _manhattan_distance(self, node1: Node, node2: Node) -> int:
        return abs(node1.row - node2.row) + abs(node1.col - node2.col)

    # get the neighbors of a node
    def _get_neighbors(self, node: Node, grid: List[List[Node]]) -> List[Node]:
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r, c = node.row + dr, node.col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbors.append(grid[r][c])
        return neighbors

    # reconstruct the path from end node to start node
    def _reconstruct_path(self, end_node: Node) -> List[Node]:
        path = []
        current = end_node
        while current:
            path.append(current)
            current = current.parent
            self._draw()
            pygame.time.wait(ANIMATION_SPEED // 2)
        return path[::-1]

    # handle events like key presses and mouse clicks
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self._start_search()
                elif event.key == pygame.K_r:
                    self._generate_new_maze()
                elif event.key == pygame.K_c:
                    self._clear_path()
            for button in self.buttons:
                button.handle_event(event)

    # update the state of the visualizer
    def _update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.is_hovered = button.rect.collidepoint(mouse_pos)

# main entry point to run the visualizer
if __name__ == "__main__":
    visualizer = PathfindingVisualizer()
    visualizer.run()