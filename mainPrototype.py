# ADDED BORDER FOR ALL RECTs, ADDED NEW CONDITION FOR GAME OVER SCREENs

import pygame, sys, random, math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (60, 60, 60)
PLAYER_COLOR = (0, 0, 255)
OBJECTIVE_COLOR = (255, 255, 255)
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 0)
PLAYER_SPEED = 5
ENEMY_SPEED = 2
ENEMY_SPAWN_INTERVAL = 60  # Number of frames between enemy spawns
ENEMY_START_SPAWN = 60
BULLET_SPEED = 8
MAX_BULLET_COUNT = 10  # Maximum number of bullets the player can carry
BULLET_RELOAD_AMOUNT = 2  # Number of additional bullets gained per enemy kill
BULLET_FIRE_DELAY = 5  # Delay in frames between consecutive shots
OBJECTIVE_HIT_POINTS = 100

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defend the Objective")

# Player Class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50)
        self.score = 0
        self.bullet_count = MAX_BULLET_COUNT  # Initialize the bullet count
        self.bullet_fire_delay = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

    def update(self):
        if self.bullet_fire_delay > 0:
            self.bullet_fire_delay -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
        #Rect Border
        border_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 4)

# Objective Class
class Objective:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50)
        self.health = OBJECTIVE_HIT_POINTS

    def draw(self, screen):
        pygame.draw.rect(screen, OBJECTIVE_COLOR, self.rect)
        #Rect Border
        border_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 4)

# Enemy Class
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH -100), random.randint(0, SCREEN_HEIGHT - 100), 75, 75)

    def move_towards_objective(self, objective):
        dx = objective.rect.x - self.rect.x
        dy = objective.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            self.rect.x += ENEMY_SPEED * dx / distance
            self.rect.y += ENEMY_SPEED * dy / distance

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, self.rect)
        #Rect Border
        border_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 4)

# Bullet Class
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)

    def move(self):
        self.rect.x += BULLET_SPEED * math.cos(self.angle)
        self.rect.y += BULLET_SPEED * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.rect(screen, BULLET_COLOR, self.rect)

# Create instances of player, objective, enemies, and bullets
player = Player()
objective = Objective()
enemies = []
bullets = []

# Game loop
clock = pygame.time.Clock()
frame_count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Spawn enemies at regular intervals
    if frame_count % ENEMY_SPAWN_INTERVAL == 0:
        enemies.append(Enemy())

    # Update enemy positions and check for collisions with the objective
    for enemy in enemies:
        enemy.move_towards_objective(objective)
        if enemy.rect.colliderect(objective.rect):
            objective.health -= 10
            enemies.remove(enemy)  # Remove enemy when it reaches the objective

    # Check for player shooting
    if pygame.mouse.get_pressed()[0] and player.bullet_count > 0:
        if player.bullet_fire_delay == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = Bullet(player.rect.centerx - 5, player.rect.centery - 5, mouse_x, mouse_y)
            bullets.append(bullet)
            player.bullet_fire_delay = BULLET_FIRE_DELAY  # Set the firing delay
            player.bullet_count -= 1  # Decrement the bullet count

    # Update bullet fire delay
    if player.bullet_fire_delay > 0:
        player.bullet_fire_delay -= 1


    # Update bullet positions and check for collisions with enemies
    for bullet in bullets:
        bullet.move()
        if bullet.rect.y < 0 or bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or bullet.rect.y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                player.score += 1
                player.bullet_count += BULLET_RELOAD_AMOUNT  # Gain additional bullets

    # Cap the bullet count to the maximum value
    if player.bullet_count > MAX_BULLET_COUNT:
        player.bullet_count = MAX_BULLET_COUNT

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw player, objective, enemies, and bullets
    objective.draw(screen)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Check for game over condition (objective health <= 0) or (player(s) bullet count is == 0)
    if objective.health <= 0:
        running = False
    if player.bullet_count == 0:
        running = False

    # Display player score, objective health, and remaining bullets
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    health_text = font.render(f"Objective Health: {objective.health}", True, (255, 255, 255))
    bullet_text = font.render(f"Bullets: {player.bullet_count}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(bullet_text, (10, 90))

    # Update the display
    pygame.display.flip()

    # Increment frame count
    frame_count += 1

    # Cap the frame rate
    clock.tick(60)

# Game over screen
game_over_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 36)
game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
game_over_no_bullet_text = game_over_font.render("Game Over! You ran out of bullets", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
game_over_no_bullet_rect = game_over_no_bullet_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

screen.fill(BACKGROUND_COLOR)

#Game over screen(s)
if objective.health <= 0:
    screen.blit(game_over_text, game_over_rect)
elif player.bullet_count == 0:
    screen.blit(game_over_no_bullet_text, game_over_no_bullet_rect)
else:
    screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.delay(3000)

# Quit Pygame
pygame.quit()
sys.exit()
