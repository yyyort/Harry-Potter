import pygame

pygame.init()

screenWidth = 1080
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Gem Defense')

clock = pygame.time.Clock()
FPS = 60

#load image(s)
background = pygame.image.load('img/bg2.png').convert_alpha()

    #Objective
gemStone100 = pygame.image.load('img/stone/stone.png').convert_alpha()
gemStone100.set_colorkey((0,0,0))

    #Player
player = pygame.image.load('img/entity/player/potter.png').convert_alpha()

black = (0,0,0)

#Objective Class
class Objective():
    def __init__(self, stone100, width, height, x, y, scale):
        self.health = 10000
        self.maxHealth = self.health
        
        width = stone100.get_width()
        height = stone100.get_height()
        
        self.stone100 = pygame.transform.scale(stone100, (int(width * scale), int(height * scale)))
        self.rect = self.stone100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.stone100
        
        screen.blit(self.image, self.rect)

#Player Class
class Player():
    def __init__(self, width, height, x, y, scale):
        self.player
        self.x = x
        self.y = y
        sel
        
#Player Initialization
gemStone = Objective(gemStone100, 24, 24, screenWidth//2-27, screenHeight//2-53, 0.1)


#main loop
run = True
while run:
    
    clock.tick(FPS)
    
    screen.blit(background,(0 - 75,0))
    
    #Draw Objective
    gem.draw()
    
    #game handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display window
    pygame.display.update()

pygame.quit()