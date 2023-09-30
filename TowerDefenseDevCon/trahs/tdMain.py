import pygame

def main ():
    
    # Game Window
    screenWidth = 1080; screenHight = 720
    
    # Loading Game Window
    windowDisplay = pygame.display.set_mode((screenWidth, screenHight))
    pygame.display.set_caption('Mage Castle Defender')
    background = (211, 211, 211)
    
    # Entities
    modelWidth = 50; modelHight = 50
    
        # Player
    playerBlock = pygame.Surface((modelWidth, modelHight))
    playerBlock.fill('blue')
    playerBlockRect = playerBlock.get_rect(center = (screenWidth // 2, screenHight // 2))
            # Player Movement
    speed = 0
    up = (0, -speed)
    down = (0, speed)
    left = (-speed, 0)
    right = (speed, 0)
        
        # Objective
        
        
        # Enemies
    
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # Game Loop
    running = True
    while running:
        
        key = pygame.key.get_pressed()
        
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Player Movement
        
            if key[pygame.K_w]:
                playerBlockRect[1] -= 1
            if key[pygame.K_s]:
                playerBlockRect[1] += 1
            if key[pygame.K_a]:
                playerBlockRect[0] -= 1
            if key[pygame.K_d]:
                playerBlockRect[0] += 1
            
                
        # Window Display(s)
        windowDisplay.fill(background)
        
        # Entities Display(s)
            # Player Display
        windowDisplay.blit(playerBlock, playerBlockRect)
            
            # Objective Display
            
            
            # Enemies Display
            
            
        # Display Update(s)
            # Update Display
        pygame.display.update()
            # Flip Display
        pygame.display.flip()
            # Display Framerate
        clock.tick(FPS)
                
    pygame.quit()
    
if __name__ == "__main__":
    pygame.init()
    main()