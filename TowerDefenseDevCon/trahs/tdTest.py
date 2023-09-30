#Imports
import pygame, sys, random

#Constants
WIDTH, HEIGHT = 1080, 720
TITLE = "Mage Gem Defense"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#Player Class
class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (0, 0, 255)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        
        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

#Enemy Class
class Enemy:
    def __init__(self, objective):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(0, HEIGHT - 50)
        self.health = 100
        self.speed = 1
        self.objective = objective

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 32, 32))

    def update(self):
        # Move the enemy directly towards the objective in a randomized pattern.
        dx = self.objective.x - self.x
        dy = self.objective.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        self.x += (dx + random.uniform(-1, 1)) / distance * self.speed
        self.y += (dy + random.uniform(-1, 1)) / distance * self.speed
        
        #if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
        #    # Reset the enemy's position
        #    self.x = random.randint(0, WIDTH - 32)
        #    self.y = random.randint(0, HEIGHT - 32)

        # Attack the objective if it is within range.
        if distance <= 32:
            self.objective.health -= 1

            # Reset the enemy's position
            self.x = random.randint(0, WIDTH - 32)
            self.y = random.randint(0, HEIGHT - 32)
            

        # Attack the objective if it is within range.
        if distance <= 32:
            self.objective.health -= 1

    def is_destroyed(self):
        return self.health <= 0
    
#Objective Class
class Objective:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100

    def draw(self, win):
        pygame.draw.rect(win, (100, 32.5, 28.6), (self.x, self.y, 32, 32))

    def is_destroyed(self):
        return self.health <= 0

#Player Initialization
player = Player(WIDTH/2, HEIGHT/2)
objective = Objective(WIDTH // 2, HEIGHT // 2)
enemy = Enemy(objective)
enemy2 = Enemy(objective)


#Main Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up_pressed = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down_pressed = False
    #Draw
    win.fill((12, 24, 36))  
    objective.draw(win)
    enemy.draw(win)
    enemy2.draw(win)
    player.draw(win)

    #update
    player.update()
    enemy.update()
    enemy2.update()
    pygame.display.flip()

    clock.tick(120)