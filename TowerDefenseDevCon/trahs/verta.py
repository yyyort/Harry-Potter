import pygame, sys

pygame.init()

#Variable Constants
    #Display
screenWidth = 1080
screenHeight = 720
title = "MAGE GEM DEFENSE"
clock = pygame.time.Clock()
FPS = 10

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(title)

#Setting Game Variable
objectiveHitPoint = 100

#Player Class
class PLAYER:
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
        
    def playerDraw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
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

#Objective Class
class OBJECTIVE:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = objectiveHitPoint
        
    def objectiveDraw(self, screen):
        pygame.draw.rect(screen, (255, 32, 28), (self.x, self.y, 50, 50))
        
    def update(self):
        if self.health < 75:
            pygame.draw.rect(screen, (100, 32, 28), (self.x, self.y, 50, 50))

#Object Initialization
player = PLAYER(screenWidth//2, screenHeight//2)
objective = OBJECTIVE(screenWidth//2, screenHeight//2)

#Main Loop
RUNNING = True
while RUNNING:
    
    #Drawing BACKGROUND
    screen.fill((12,24,36))
    #Drawing PLAYER
    player.playerDraw(screen)
    #Drawing OBJECTIVE
    objective.objectiveDraw(screen)
    
    #Event Handler
    for event in pygame.event.get():
        
        #PLAYER MOVEMENT
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
        
        #Pygame QUIT
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            
    #Pygame Display Update(s)
    player.update()
    objective.update()
    pygame.display.flip()
    
    clock.tick(FPS)