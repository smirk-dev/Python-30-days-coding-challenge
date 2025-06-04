import pygame
import os
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game window setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Adventure")
clock = pygame.time.Clock()

# Load assets
def load_image(name, colorkey=None, scale=1):
    # This function would normally load images from files
    # For now, we'll create placeholder images
    image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    if name == "player":
        image.fill(BLUE)
    elif name == "platform":
        image.fill(GREEN)
    elif name == "coin":
        image.fill((255, 255, 0))  # Yellow
    elif name == "enemy":
        image.fill(RED)
    else:
        image.fill(WHITE)
        
    if scale != 1:
        image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        
    return image.convert_alpha()

# Placeholder for sounds
def load_sound(name):
    # This function would normally load sounds from files
    # For now, we'll create an empty Sound object
    return pygame.mixer.Sound(buffer=bytes([]))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("player")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.direction = "right"
        self.jump_power = -12
        self.gravity = 0.5
        self.speed = 5
        self.health = 3
        self.coins = 0
        
    def update(self, platforms, enemies, coins):
        # Apply gravity
        self.vel_y += self.gravity
        
        # Horizontal movement
        self.rect.x += self.vel_x
        
        # Check for collisions with platforms (horizontal)
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_x > 0:  # Moving right
                self.rect.right = hit.rect.left
            elif self.vel_x < 0:  # Moving left
                self.rect.left = hit.rect.right
        
        # Vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        
        # Check for collisions with platforms (vertical)
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_y > 0:  # Landing on platform
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:  # Hitting platform from below
                self.rect.top = hit.rect.bottom
                self.vel_y = 0
                
        # Check for coin collection
        coin_hits = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hits:
            self.coins += 1
            coin_sound.play()
            
        # Check for enemy collisions
        if pygame.sprite.spritecollide(self, enemies, False):
            # Check if we're stomping on the enemy
            for enemy in pygame.sprite.spritecollide(self, enemies, False):
                if self.vel_y > 0 and self.rect.bottom < enemy.rect.center[1]:
                    enemy.kill()
                    self.vel_y = self.jump_power / 2
                    hit_sound.play()
                else:
                    # We got hit
                    self.take_damage()
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.take_damage()
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            jump_sound.play()
            
    def take_damage(self):
        self.health -= 1
        damage_sound.play()
        # Flash the player to indicate damage
        original_image = self.image.copy()
        self.image.fill(RED)
        pygame.display.flip()
        pygame.time.wait(50)
        self.image = original_image
        
        # Respawn if health is still positive
        if self.health > 0:
            self.rect.x = 100
            self.rect.y = SCREEN_HEIGHT - 100
            
# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("coin", scale=0.5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, platform=None):
        super().__init__()
        self.image = load_image("enemy")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 2
        self.platform = platform
        
    def update(self, *args):  # Fixed: added *args to accept any number of arguments
        self.rect.x += self.vel_x
        
        # If enemy is on a platform, make sure it doesn't fall off
        if self.platform:
            if self.rect.right > self.platform.rect.right:
                self.rect.right = self.platform.rect.right
                self.vel_x *= -1
            elif self.rect.left < self.platform.rect.left:
                self.rect.left = self.platform.rect.left
                self.vel_x *= -1

# Background class
class Background:
    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image.fill((135, 206, 235))  # Sky blue background
        
        # Draw some clouds
        for _ in range(5):
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(0, SCREEN_HEIGHT // 2)
            pygame.draw.ellipse(self.image, WHITE, (cloud_x, cloud_y, 60, 30))
            
    def draw(self, surface):
        surface.blit(self.image, (0, 0))

# Load game sounds
jump_sound = load_sound("jump")
coin_sound = load_sound("coin")
hit_sound = load_sound("hit")
damage_sound = load_sound("damage")

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Level design function
def create_level(level_number):
    # Clear existing sprites
    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    coins.empty()
    
    # Create player
    player = Player(100, SCREEN_HEIGHT - 100)
    all_sprites.add(player)
    
    # Create ground platform
    ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(ground)
    platforms.add(ground)
    
    # Basic level design
    if level_number == 1:
        # Level 1: Simple platforms
        platform_data = [
            (200, 400, 150, 20),
            (400, 300, 150, 20),
            (200, 200, 150, 20),
            (500, 150, 150, 20)
        ]
        
        enemy_data = [
            (250, 380, None),
            (450, 280, None)
        ]
        
        coin_data = [
            (250, 350),
            (450, 250),
            (250, 150),
            (550, 100)
        ]
    else:
        # Level 2: More complex
        platform_data = [
            (100, 450, 100, 20),
            (300, 400, 100, 20),
            (500, 350, 100, 20),
            (300, 250, 100, 20),
            (100, 200, 100, 20),
            (600, 200, 100, 20)
        ]
        
        enemy_data = [
            (350, 380, None),
            (150, 180, None),
            (650, 180, None)
        ]
        
        coin_data = [
            (150, 420),
            (350, 370),
            (550, 320),
            (350, 220),
            (150, 170),
            (650, 170)
        ]
    
    # Create platforms
    for x, y, width, height in platform_data:
        p = Platform(x, y, width, height)
        all_sprites.add(p)
        platforms.add(p)
    
    # Create enemies
    for x, y, plat in enemy_data:
        e = Enemy(x, y, plat)
        all_sprites.add(e)
        enemies.add(e)
    
    # Create coins
    for x, y in coin_data:
        c = Coin(x, y)
        all_sprites.add(c)
        coins.add(c)
    
    return player

# Game state variables
current_level = 1
player = create_level(current_level)
background = Background()
game_over = False
game_won = False
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    # Keep the game running at the right speed
    clock.tick(FPS)
    
    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_r and (game_over or game_won):
                # Restart game
                current_level = 1
                player = create_level(current_level)
                game_over = False
                game_won = False
    
    # Get key states for continuous movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.vel_x = -player.speed
        player.direction = "left"
    elif keys[pygame.K_RIGHT]:
        player.vel_x = player.speed
        player.direction = "right"
    else:
        player.vel_x = 0
    
    # Update all sprites if game is active
    if not game_over and not game_won:
        all_sprites.update(platforms, enemies, coins)
        # We don't need to update enemies separately - they're already in all_sprites
        # Removed: enemies.update()
        
        # Check health
        if player.health <= 0:
            game_over = True
            
        # Check if player collected all coins
        if len(coins) == 0:
            if current_level < 2:
                current_level += 1
                player = create_level(current_level)
            else:
                game_won = True
    
    # Draw / render
    background.draw(screen)
    all_sprites.draw(screen)
    
    # Draw UI
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    coins_text = font.render(f"Coins: {player.coins}", True, WHITE)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(coins_text, (10, 50))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
    
    # Game over or victory message
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    
    if game_won:
        game_won_text = font.render("You Win! Press R to play again", True, GREEN)
        screen.blit(game_won_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    
    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()