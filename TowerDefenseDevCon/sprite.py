# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
# LATEST CODE
import pygame, sys, random, math

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

# Initialize Pygame
pygame.init()

#opencv setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

thumbs_up_template = [4, 3, 2]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Constants
""" SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080 """

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
GAME_FPS = 120
BACKGROUND_COLOR = (60, 60, 60)
PLAYER_COLOR = (0, 0, 255)
OBJECTIVE_COLOR = (255, 255, 255)
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 0)
PLAYER_SPEED = 5
ENEMY_SPEED = 5
ENEMY_SPAWN_INTERVAL = 55  # Number of frames between enemy spawns
ENEMY_START_SPAWN = 10
BULLET_SPEED = 8
MAX_BULLET_COUNT = 10  # Maximum number of bullets the player can carry
BULLET_RELOAD_AMOUNT = 2  # Number of additional bullets gained per enemy kill
BULLET_FIRE_DELAY = 60  # Delay in frames between consecutive shots
BULLET_AUTO_ATTACK_RADIUS = 250  # Adjust this radius as needed
OBJECTIVE_HIT_POINTS = 100
MENU_BACKGROUND_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (255, 255, 255)
MENU_FONT_SIZE = 48

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defend the Objective")

# LOAD image

    # player
player_idle = pygame.image.load("img/entity/player/idle.png").convert_alpha()
player_left = pygame.image.load("img/entity/player/left.png").convert_alpha()
player_right = pygame.image.load("img/entity/player/right.png").convert_alpha()

    # weapon
wandleft =  pygame.image.load("img/entity/player/wleft.png").convert_alpha()
wandright = pygame.image.load("img/entity/player/wright.png").convert_alpha()

    # projectile
projectile = pygame.image.load("img/entity/player/projectile.png").convert_alpha()

    # objective
stone = pygame.image.load("img/entity/player/stone.png").convert_alpha()
stone2 = pygame.image.load("img/entity/player/stone2.png").convert_alpha()
stone3 = pygame.image.load("img/entity/player/stone3.png").convert_alpha()

    # enemy
enemyspawn =  pygame.image.load("img/entity/player/spawn.png").convert_alpha()
enemyleft = pygame.image.load("img/entity/player/gleft.png").convert_alpha()
enemyright = pygame.image.load("img/entity/player/gright.png").convert_alpha()
enemydeath = pygame.image.load("img/entity/player/death.png").convert_alpha()

    # crystal visual health bar
hp100 = pygame.image.load("img/entity/player/stone.png").convert_alpha()
hp50 = pygame.image.load("img/entity/player/stone.png").convert_alpha()
hp25 = pygame.image.load("img/entity/player/stone.png").convert_alpha()

    # health bar
h10 = pygame.image.load("img/entity/player/hp11.png").convert_alpha()
h9 = pygame.image.load("img/entity/player/hp10.png").convert_alpha()
h8 = pygame.image.load("img/entity/player/hp9.png").convert_alpha()
h7 = pygame.image.load("img/entity/player/hp8.png").convert_alpha()
h6 = pygame.image.load("img/entity/player/hp7.png").convert_alpha()
h5 = pygame.image.load("img/entity/player/hp6.png").convert_alpha()
h4 = pygame.image.load("img/entity/player/hp5.png").convert_alpha()
h3 = pygame.image.load("img/entity/player/hp4.png").convert_alpha()
h2 = pygame.image.load("img/entity/player/hp3.png").convert_alpha()
h1 = pygame.image.load("img/entity/player/hp2.png").convert_alpha()

# Menu Class
class Menu:
    def __init__(self):
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        
    def draw(self, screen):
        screen.fill(MENU_BACKGROUND_COLOR)
        play_text = self.font.render("PLAY", True, MENU_TEXT_COLOR)
        exit_text = self.font.render("EXIT", True, MENU_TEXT_COLOR)
        screen.blit(play_text, (self.play_button.centerx - play_text.get_width() // 2, self.play_button.centery - play_text.get_height() // 2))
        screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    return "PLAY"
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        return None

# Game Over Menu Class
class GameOverMenu:
    def __init__(self):
        self.replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        
    def draw(self, screen):
        screen.fill(MENU_BACKGROUND_COLOR)
        game_over_text = self.font.render("GAME OVER!", True, MENU_TEXT_COLOR)
        replay_text = self.font.render("REPLAY", True, MENU_TEXT_COLOR)
        exit_text = self.font.render("EXIT", True, MENU_TEXT_COLOR)
        screen.blit(replay_text, (self.replay_button.centerx - replay_text.get_width() // 2, self.replay_button.centery - replay_text.get_height() // 2))
        screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.replay_button.collidepoint(event.pos):
                    return "REPLAY"
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        return None
                
# Player Class
class Player:
    def __init__(self, wandleft, wandright):
        # Load and scale down the idle image for the player
        self.image_idle = pygame.transform.scale(player_idle, (50, 75))
        # Load and scale down the left and right images for the player
        self.image_left = pygame.transform.scale(player_left, (50, 75))
        self.image_right = pygame.transform.scale(player_right, (50, 75))
        self.image = pygame.transform.scale(player_idle, (50, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.score = 0
        self.bullet_count = MAX_BULLET_COUNT
        self.bullet_fire_delay = 0
        self.gun = Gun(self.rect, wandleft, wandright)

    def comvis(self, x, y):
        self.rect.x = x
        self.rect.y = y
        pass

    def move(self, keys):
        
         # Calculate the boundaries for player movement
        min_x = SCREEN_WIDTH // 2 - 250
        max_x = SCREEN_WIDTH // 2 + 250
        min_y = SCREEN_HEIGHT // 2 - 250
        max_y = SCREEN_HEIGHT // 2 + 250

        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.x > min_x:
            self.rect.x -= PLAYER_SPEED
            self.image = self.image_left  # Set the left image when moving left
            self.gun.update_last_direction("left")  # Update the last_direction attribute
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.x < max_x:
            self.rect.x += PLAYER_SPEED
            self.image = self.image_right  # Set the right image when moving right
            self.gun.update_last_direction("right")  # Update the last_direction attribute
        else:
            self.image = self.image_idle  # Set the idle image when not moving

        if keys[pygame.K_UP] or keys[pygame.K_w] and self.rect.y > min_y:
            self.rect.y -= PLAYER_SPEED
            self.gun.update_last_direction("up")  # Update the last_direction attribute
        elif keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.y < max_y:
            self.rect.y += PLAYER_SPEED
            self.gun.update_last_direction("down")  # Update the last_direction attribute
        else:
            self.gun.update_last_direction(None)  # No specific direction when not moving vertically
        
    def auto_attack(self, enemies):
        for enemy in enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Check if the enemy is within the auto-attack radius
            if distance <= BULLET_AUTO_ATTACK_RADIUS:
                if self.bullet_fire_delay == 0 and self.bullet_count > 0:
                    bullet = Bullet(self.rect.centerx - 5, self.rect.centery - 5, enemy.rect.centerx, enemy.rect.centery)
                    bullets.append(bullet)
                    self.bullet_fire_delay = BULLET_FIRE_DELAY  # Set the firing delay
                    self.bullet_count -= 1  # Decrement the bullet count
    
    def update(self):
        self.move(keys)
        self.gun.update(keys)
        
        if self.bullet_fire_delay > 0:
            self.bullet_fire_delay -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.gun.draw(screen)

# Gun Class
class Gun:
    def __init__(self, player_rect, wandleft, wandright):
        wandrightflipV = pygame.transform.flip(wandright, False, True)
        wandrightflipH = pygame.transform.flip(wandright, True, False)
        wandleftscale = pygame.transform.scale(wandleft, (50, 50))
        wandrightscale = pygame.transform.scale(wandright, (50, 50))
        wandflipscaleV = pygame.transform.scale(wandrightflipV, (50, 50))
        wandflipscaleH = pygame.transform.scale(wandrightflipH, (50, 50))
        self.original_left_image = wandleftscale
        self.original_right_image = wandrightscale
        self.original_flipV_image = wandflipscaleV
        self.original_flipH_image = wandflipscaleH
        self.image = self.original_left_image
        self.rect = self.image.get_rect()
        self.player_rect = player_rect  # Store a reference to the player's rect
        self.last_direction = None  # Initialize the last_direction attribute


    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.image = self.original_left_image
            self.rect.center = (self.player_rect.left, self.player_rect.centery)  # Stick to player's left
            self.last_direction = "left"  # Update the last_direction attribute
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.image = self.original_right_image
            self.rect.center = (self.player_rect.right, self.player_rect.centery)  # Stick to player's right
            self.last_direction = "right"  # Update the last_direction attribute
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = self.original_flipV_image
            self.rect.center = (self.player_rect.right - 14, self.player_rect.bottom + 4)  # Stick to player's right
            self.last_direction = "down"  # Update the last_direction attribute
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = self.original_flipH_image
            self.rect.center = (self.player_rect.right - 14, self.player_rect.bottom + 4)  # Stick to player's right
            self.last_direction = "up"  # Update the last_direction attribute

    def update_last_direction(self, direction):
        self.last_direction = direction


    def draw(self, screen):
        if self.last_direction == "left":
            self.rect.center = (self.player_rect.left, self.player_rect.centery)  # Stick to player's left
        elif self.last_direction == "right":
            self.rect.center = (self.player_rect.right, self.player_rect.centery)  # Stick to player's right
        elif self.last_direction == "up":
            self.rect.center = (self.player_rect.centerx, self.player_rect.top + 30)  # Stick above the player
        elif self.last_direction == "down":
            self.rect.center = (self.player_rect.centerx, self.player_rect.bottom)  # Stick below the player

        screen.blit(self.image, self.rect)
        
# Objective Class
class Objective:
    def __init__(self):
        self.ruby = pygame.transform.scale(stone, (50, 50))
        self.ruby2 = pygame.transform.scale(stone2, (50, 50))
        self.ruby3 = pygame.transform.scale(stone3, (50, 50))
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50)
        self.bRect = pygame.Rect(SCREEN_WIDTH // 2 - 960 / 2, 40, SCREEN_WIDTH // 2, 50)
        self.bar10 = pygame.transform.scale(h10, (SCREEN_WIDTH // 2, 50))
        self.bar9 = pygame.transform.scale(h9, (SCREEN_WIDTH // 2, 50))
        self.bar8 = pygame.transform.scale(h8, (SCREEN_WIDTH // 2, 50))
        self.bar7 = pygame.transform.scale(h7, (SCREEN_WIDTH // 2, 50))
        self.bar6 = pygame.transform.scale(h6, (SCREEN_WIDTH // 2, 50))
        self.bar5 = pygame.transform.scale(h5, (SCREEN_WIDTH // 2, 50))
        self.bar4 = pygame.transform.scale(h4, (SCREEN_WIDTH // 2, 50))
        self.bar3 = pygame.transform.scale(h3, (SCREEN_WIDTH // 2, 50))
        self.bar2 = pygame.transform.scale(h2, (SCREEN_WIDTH // 2, 50))
        self.bar1 = pygame.transform.scale(h1, (SCREEN_WIDTH // 2, 50))
        self.bar_image = self.bar10
        self.health = OBJECTIVE_HIT_POINTS
        
    def update(self):
        if self.health == 100 and self.health >= 70:
            self.bar_image = self.bar10
            self.image = self.ruby
        elif self.health == 90:
            self.bar_image = self.bar9
        elif self.health == 80:
            self.bar_image = self.bar8
        elif self.health == 70:
            self.bar_image = self.bar7
        elif self.health == 60:
            self.bar_image = self.bar6
        elif self.health == 50 and self.health >= 50:
            self.bar_image = self.bar5
            self.image = self.ruby2
        elif self.health >= 40:
            self.bar_image = self.bar4
        elif self.health >= 30:
            self.bar_image = self.bar3
        elif self.health >= 20:
            self.bar_image = self.bar2
        else:
            self.image = self.bar1
            self.image = self.ruby3
        
        

    def draw(self, screen):
        screen.blit(self.bar_image, self.bRect)
        screen.blit(self.image, self.rect)

# Enemy Class
class Enemy:
    def __init__(self):
        self.spawn_image = pygame.transform.scale(enemyspawn, (75, 75))
        self.walk_left_image = pygame.transform.scale(enemyleft, (75, 75))
        self.walk_right_image = pygame.transform.scale(enemyright, (75, 75))
        self.death_image = pygame.transform.scale(enemydeath, (75, 75))
        self.image = self.spawn_image  # Initialize with the spawn image
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 75, 75)
        self.is_alive = True  # Flag to track if the enemy is alive
        self.disappear_timer = 0  # Timer for controlling enemy's visibility after being hit
        self.start_spawn_timer = ENEMY_START_SPAWN  # Timer to control when the enemy starts moving
        self.can_move = False  # Flag to control enemy movement

    def move_towards_objective(self, objective):
        if self.can_move:
            dx = objective.rect.x - self.rect.x
            dy = objective.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 0:
                self.rect.x += ENEMY_SPEED * dx / distance
                self.rect.y += ENEMY_SPEED * dy / distance

    def take_damage(self):
        self.is_alive = False
        self.image = self.death_image  # Change the image to death when the enemy dies
        self.disappear_timer = 100  # Set the disappear timer to 1000 ms (1 second)

    def update(self):
        if self.is_alive:
            if self.start_spawn_timer > 0:
                self.start_spawn_timer -= 1
                if self.start_spawn_timer <= 0:
                    self.can_move = True  # Start moving and change the image

            if self.can_move:
                self.image = self.spawn_image
                # Update the image based on the enemy's movement direction
                if self.rect.x < SCREEN_WIDTH // 2:
                    self.image = self.walk_right_image  # Facing left when moving right
                else:
                    self.image = self.walk_left_image  # Facing right when moving left
        elif self.disappear_timer > 0:
            self.disappear_timer -= 1
        else:
            # When the timer reaches 0, remove the enemy from the game
            enemies.remove(self)

    def draw(self, screen):
        if self.is_alive or self.disappear_timer % 2 == 0:
            screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.image = pygame.transform.scale(projectile, (25, 25))
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)

    def move(self):
        self.rect.x += BULLET_SPEED * math.cos(self.angle)
        self.rect.y += BULLET_SPEED * math.sin(self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
# Create instances for game menu
menu = Menu()


# Game loop
clock = pygame.time.Clock()
frame_count = 0

running = False
game_over = False # Game over flag
game_over_menu = None
while True:
    if not running and not game_over:
        menu_choice = None
        while menu_choice is None:
            menu.draw(screen)
            pygame.display.flip()
            menu_choice = menu.handle_events()
        # Game start
        if menu_choice == "PLAY":
            running = True
        # Create instances of player, objective, enemies, and bullets
            player = Player(wandleft, wandright)
            objective = Objective()
            enemies = []
            bullets = []


    #opencv
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to RGB format (MediaPipe requires RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using the Hands model
    results = hands.process(frame_rgb)
    
    gesture = None

    # Draw hand landmarks on the frame if hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, landmarks, mp_hands.HAND_CONNECTIONS)
            #if results:  # Add your hand gesture detection logic here
            thumb_landmarks = [landmarks.landmark[i] for i in thumbs_up_template]

            # Calculate the Euclidean distances between the thumb landmarks
            distances = [((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 for a, b in zip(thumb_landmarks, thumb_landmarks[1:])]

            # Define a threshold for the distances
            if all(lm.y < landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y for lm in landmarks.landmark):
                print(landmarks)
                gesture = "Fist"
            else:
                print(landmarks)
                gesture = "Open Hand"
            
            comvis_x = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
            comvis_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
             #comvis
            player.comvis(comvis_x * SCREEN_WIDTH, comvis_y * SCREEN_HEIGHT)

        cv2.putText(frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    # Display the frame in a window
    cv2.imshow("Camera Preview", frame)

    # Exit the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #opencv end
    
    if running:
       

        # Game Loop
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.auto_attack(enemies)
        
         # Spawn enemies at regular intervals
        if frame_count % ENEMY_SPAWN_INTERVAL == 0:
            enemies.append(Enemy())
        
        player.update()
        objective.update()

        # Update enemy positions and check for collisions with the objective
        for enemy in enemies:
            if enemy.is_alive:
                enemy.move_towards_objective(objective)
                enemy.update()  # Update the enemy's image
                if enemy.rect.colliderect(objective.rect):
                    objective.health -= 10
                    enemy.take_damage()  # Mark the enemy as dead when it collides with the objective

                    
            # Remove dead enemies
            if not enemy.is_alive:
                enemies.remove(enemy)

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
        bullets_to_remove = []
        for bullet in bullets:
            bullet.move()
            if bullet.rect.y < 0 or bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or bullet.rect.y > SCREEN_HEIGHT:
                bullets_to_remove.append(bullet)
            else:
                for enemy in enemies:
                    if enemy.is_alive and bullet.rect.colliderect(enemy.rect):
                        bullets_to_remove.append(bullet)
                        enemy.take_damage()
                        player.score += 1
                        player.bullet_count += BULLET_RELOAD_AMOUNT

        # Remove bullets that hit enemies or went out of bounds
        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        # Cap the bullet count to the maximum value
        if player.bullet_count > MAX_BULLET_COUNT:
            player.bullet_count = MAX_BULLET_COUNT

        # Game over condition
        if objective.health <= 0 or player.bullet_count == 0:
            running = False
            game_over = True
        
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw player, objective, enemies, and bullets
        #
        #
        #
            
        for enemy in enemies:
            enemy.draw(screen)
            
        objective.draw(screen)
        player.draw(screen)
        
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
        clock.tick(GAME_FPS)

    if game_over:
        
        if game_over_menu is None:
            game_over_menu = GameOverMenu()
            
        game_over_choice = None
        while game_over_choice is None:
            game_over_menu.draw(screen)
            pygame.display.flip()
            game_over_choice = game_over_menu.handle_events()
            
        if game_over_choice == "REPLAY":
            game_over = False
            game_over_menu = None # Will reset game

            # Reset player's score, bullet count, and other game variables
            player.score = 0
            player.bullet_count = MAX_BULLET_COUNT
            player.bullet_fire_delay = 0
            objective.health = OBJECTIVE_HIT_POINTS
            enemies.clear()
            bullets.clear()
            
        """ # Game over screen
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
        sys.exit()"""

    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()