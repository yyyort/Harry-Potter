from pygame import mixer

import pygame, sys, random, math, time

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

pygame.init()
#   Pygame Initializing Pygame

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

thumbs_up_template = [4, 3, 2]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
#   Open Computer Vision Setup

#   Game Constants

    #   Window Dimension
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
    #   Pygame Framerate
GAME_FPS = 240
    #   Pygame Background Color
BACKGROUND_COLOR = (60, 60, 60)
    #   Player Movement and Enemy Movement Speed
PLAYER_SPEED = 10   #   Default 10
ENEMY_SPEED = 10    #   Default 10
    #   Interval Constant(s)
ENEMY_SPAWN_INTERVAL = 30   #   Frames between enemy spawn (Default 30)
ENEMY_SPAWN_DECREASE = 2    #   Increasing enemy spawn rate (Default 2)
ENEMY_SPAWN_DECREASE_INTERVAL = 5000    #   5 seconds (milliseconds)

ENEMY_START_SPAWN = 2  # The delay of the spawning phase of the enemy

ENEMY_SPEED_INCREASE = 3  # Speed increase after 10 seconds
ENEMY_SPEED_INCREASE_INTERVAL = 10000  # 10 seconds in milliseconds

BULLET_SPEED = 16 * 2
BULLET_SPEED_INCREASE = 8
BULLET_SPEED_INCREASE_INTERVAL = 5000

BULLET_FIRE_DELAY = 30 # Delay in frames between consecutive shots
BULLET_FIRE_DELAY_INCREASE = 2
BULLET_FIRE_DELAY_INCREASE_INTERVAL = 5000

MAX_BULLET_COUNT = 9999 # Maximum number of bullets the player can carry
BULLET_RELOAD_AMOUNT = 2  # Number of additional bullets gained per enemy kill
BULLET_AUTO_ATTACK_RADIUS = 250  # Adjust this radius as needed

OBJECTIVE_HIT_POINTS = 100

MENU_BACKGROUND_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (255, 255, 255)
MENU_FONT_SIZE = 48

ABLE_TO_ATTACK_DELAY = 10

#   Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defend the Objective")

# Image Variables

    #   Player Sprites
player_idle = pygame.image.load("HarryPotterSprite/PlayerSprite/player_idle.png").convert_alpha()
player_left = pygame.image.load("HarryPotterSprite/PlayerSprite/player_move_left.png").convert_alpha()
player_right = pygame.image.load("HarryPotterSprite/PlayerSprite/player_move_right.png").convert_alpha()

    #   Weapon Sprite
player_weapon = pygame.image.load("HarryPotterSprite/PlayerWeaponSprite/player_weapon.png").convert_alpha()

    #   Projectile
player_projectile = pygame.image.load("HarryPotterSprite/PlayerProjectileSprite/projectile_magic.png").convert_alpha()

    #   Enemy Sprites
enemy_death = pygame.image.load("HarryPotterSprite/GhostSprite/ghost_death.png").convert_alpha()
enemy_spawn = pygame.image.load("HarryPotterSprite/GhostSprite/ghost_spawn.png").convert_alpha()
enemy_move_left = pygame.image.load("HarryPotterSprite/GhostSprite/ghost_move_left.png").convert_alpha()
enemy_move_right = pygame.image.load("HarryPotterSprite/GhostSprite/ghost_move_right.png").convert_alpha()

    # Objective Sprites
objective_full = pygame.image.load("HarryPotterSprite/ObjectiveSprite/objective_full.png").convert_alpha()
objective_half = pygame.image.load("HarryPotterSprite/ObjectiveSprite/objective_half.png").convert_alpha()
objective_quarter = pygame.image.load("HarryPotterSprite/ObjectiveSprite/objective_quarter.png").convert_alpha()

    # Objective Health Bar Sprites
health_bar_10 = pygame.image.load("HarryPotterSprite/HPSprite/hp10.png").convert_alpha()
health_bar_9 = pygame.image.load("HarryPotterSprite/HPSprite/hp9.png").convert_alpha()
health_bar_8 = pygame.image.load("HarryPotterSprite/HPSprite/hp8.png").convert_alpha()
health_bar_7 = pygame.image.load("HarryPotterSprite/HPSprite/hp7.png").convert_alpha()
health_bar_6 = pygame.image.load("HarryPotterSprite/HPSprite/hp6.png").convert_alpha()
health_bar_5 = pygame.image.load("HarryPotterSprite/HPSprite/hp5.png").convert_alpha()
health_bar_4 = pygame.image.load("HarryPotterSprite/HPSprite/hp4.png").convert_alpha()
health_bar_3 = pygame.image.load("HarryPotterSprite/HPSprite/hp3.png").convert_alpha()
health_bar_2 = pygame.image.load("HarryPotterSprite/HPSprite/hp2.png").convert_alpha()
health_bar_1 = pygame.image.load("HarryPotterSprite/HPSprite/hp1.png").convert_alpha()

#   Sound Effects Variables

    #   Background SFX
pygame_background_music = pygame.mixer.Sound("HarryPotterSFX/pygame_background_music.mp3")

    #   Game Over Background SFX
pygame_gameover_background_music = pygame.mixer.Sound("HarryPotterSFX/pygame_background_gameover.mp3")

    #   Player Movement SFX
player_movement_sfx = pygame.mixer.Sound("HarryPotterSFX/player_movement.mp3")

    #   Player Attack SFX
player_attack_sfx = pygame.mixer.Sound("HarryPotterSFX/player_attack_sfx.mp3")

    #   Enemy Spawn SFX
enemy_spawn_sfx = pygame.mixer.Sound("HarryPotterSFX/enemy_spawn_sfx.mp3")

    #   Enemy Death SFX
enemy_death_sfx = pygame.mixer.Sound("HarryPotterSFX/enemy_death_sfx.mp3")

#   Menu Class
class Menu:
    def __init__(self):
        self.welcome_text_title = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 150, 200, 50)
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        
    def draw(self, screen):
        screen.fill(MENU_BACKGROUND_COLOR)
        welcome_text = self.font.render("HARRY POTTER TOWER DEFENSE", True, MENU_TEXT_COLOR)
        play_text = self.font.render("PLAY", True, MENU_TEXT_COLOR)
        exit_text = self.font.render("EXIT", True, MENU_TEXT_COLOR)
        screen.blit(welcome_text, (self.welcome_text_title.centerx - welcome_text.get_width() // 2, self.welcome_text_title.centery - welcome_text.get_height() // 2))
        screen.blit(play_text, (self.play_button.centerx - play_text.get_width() // 2, self.play_button.centery - play_text.get_height() // 2))
        screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #q: how to get mouse 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    return "PLAY"
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        #return None

#   Gameover Menu
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
        player_score_text = self.font.render (f"Your Score: {player.score}", True, MENU_TEXT_COLOR)
        screen.blit(replay_text, (self.replay_button.centerx - replay_text.get_width() // 2, self.replay_button.centery - replay_text.get_height() // 2))
        screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
        screen.blit(player_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150))
        
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

#   Player Class
class Player:
    def __init__(self, player_weapon):
        self.image_idle = pygame.transform.scale(player_idle, (50, 75))
        self.image_left = pygame.transform.scale(player_left, (50, 75))
        self.image_right = pygame.transform.scale(player_right, (50, 75))
        self.image = pygame.transform.scale(player_idle, (50, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.score = 0
        self.bullet_count = MAX_BULLET_COUNT
        self.bullet_fire_delay = 0
        self.gun = Weapon(player_weapon)

    def comvis(self, x, y):
        self.rect.x = x
        self.rect.y = y
        pass

    def move(self, cv_x, cv_y):
        # Calculate the boundaries for player movement
        min_x = 0
        max_x = SCREEN_WIDTH - 50
        min_y = 100
        max_y = SCREEN_HEIGHT - 75

        # Calculate the new position based on computer vision input
        new_x = self.rect.x + cv_x
        new_y = self.rect.y + cv_y

        # Ensure the new position is within the bounds
        new_x = max(min_x, min(max_x, new_x))
        new_y = max(min_y, min(max_y, new_y))

        self.rect.x = new_x
        self.rect.y = new_y

        # Determine the player's area on the screen
        screen_width_mid = SCREEN_WIDTH // 2
        screen_height_mid = SCREEN_HEIGHT // 2

        if self.rect.centerx < screen_width_mid:
            # Player is in the left half of the screen
            self.image = self.image_left
        elif self.rect.centerx > screen_width_mid:
            # Player is in the right half of the screen
            self.image = self.image_right
        else:
            # Player is in the center of the screen
            self.image = self.image_idle
        
        # Update the gun's position based on the new player position
        self.gun.rect.center = (self.rect.centerx, self.rect.centery)
        
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
                    
                    # Play the player attack SFX
                    player_attack_sfx.play()
    
    
    
    def update(self):
        self.move(cv_x, cv_y)
        
        if self.bullet_fire_delay > 0:
            self.bullet_fire_delay -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.gun.draw(screen)

#   Weapon Class  
class Weapon:
    def __init__(self, player_weapon):
        player_weapon_scale = pygame.transform.scale(player_weapon, (50, 50))
        player_weapon_flip_scale = pygame.transform.scale(player_weapon, (50, 50))
        self.player_weapon_flip = pygame.transform.flip(player_weapon_flip_scale, True, False)
        self.original_player_weapon_flip = player_weapon_flip_scale
        self.original_player_weapon = player_weapon_scale
        self.image = self.original_player_weapon_flip
        self.rect = self.image.get_rect()

    def move(self, cv_x, cv_y):
        # Calculate the boundaries for player movement
        min_x = 0
        max_x = SCREEN_WIDTH - 50
        min_y = 100
        max_y = SCREEN_HEIGHT - 75

        # Calculate the new position based on computer vision input
        new_x = self.rect.x + cv_x
        new_y = self.rect.y + cv_y

        # Ensure the new position is within the bounds
        new_x = max(min_x, min(max_x, new_x))
        new_y = max(min_y, min(max_y, new_y))

        self.rect.x = new_x
        self.rect.y = new_y

        screen_width_mid = SCREEN_WIDTH // 2

        if self.rect.centerx < screen_width_mid:
            # Player is in the left half of the screen
            self.image = self.original_player_weapon_flip
        elif self.rect.centerx > screen_width_mid:
            # Player is in the right half of the screen
            self.image = self.original_player_weapon
        else:
            # Player is in the center of the screen
            self.image = self.original_player_weapon_flip

    def update(self, cv_x, cv_y):
        self.move(cv_x, cv_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
#   Objective Class
class Objective:
    def __init__(self):
        self.ruby = pygame.transform.scale(objective_full, (50, 50))
        self.ruby2 = pygame.transform.scale(objective_half, (50, 50))
        self.ruby3 = pygame.transform.scale(objective_quarter, (50, 50))
        
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50)
        self.bRect = pygame.Rect(SCREEN_WIDTH // 2 - 960 / 2, 40, SCREEN_WIDTH // 2, 50)
        
        # Initialize all health bars, including bar10
        health_bars = [pygame.transform.scale(h, (SCREEN_WIDTH // 2, 50)) for h in [health_bar_1,
                                                                                    health_bar_2,
                                                                                    health_bar_3,
                                                                                    health_bar_4,
                                                                                    health_bar_5,
                                                                                    health_bar_6,
                                                                                    health_bar_7,
                                                                                    health_bar_8,
                                                                                    health_bar_9,
                                                                                    health_bar_10]]
        self.bar_1, self.bar_2, self.bar_3, self.bar_4, self.bar_5, self.bar_6, self.bar_7, self.bar_8, self.bar_9, self.bar_10 = health_bars

        # Set the initial bar image
        self.bar_image = self.bar_10
        self.health = OBJECTIVE_HIT_POINTS
        
    def update(self):
        health_mapping = {
            100: (self.bar_10, self.ruby),
            90: (self.bar_9, None),
            80: (self.bar_8, None),
            70: (self.bar_7, None),
            60: (self.bar_6, None),
            50: (self.bar_5, self.ruby2),
            40: (self.bar_4, None),
            30: (self.bar_3, None),
            20: (self.bar_2, self.ruby3),
            10: (self.bar_1, None),
        }

        for health_value, (bar, image) in health_mapping.items():
            if self.health >= health_value:
                self.bar_image = bar
                if image:
                    self.image = image
                return

        self.bar_image = self.bar_1
        self.image = self.ruby3
        
        

    def draw(self, screen):
        screen.blit(self.bar_image, self.bRect)
        screen.blit(self.image, self.rect)

#   Enemy Class
      
class Enemy:
    def __init__(self):
        self.spawn_image = pygame.transform.scale(enemy_spawn, (75, 75))
        self.death_image = pygame.transform.scale(enemy_death, (75, 75))
        self.walk_left_image = pygame.transform.scale(enemy_move_left, (75, 75))
        self.walk_right_image = pygame.transform.scale(enemy_move_right, (75, 75))
        self.image = self.spawn_image  # Initialize with the spawn image
        
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 75, 75)
        
        self.is_alive = True  # Flag to track if the enemy is alive
        
        self.disappear_timer = 0  # Timer for controlling enemy's visibility after being hit
        
        self.start_spawn_timer = ENEMY_START_SPAWN  # Timer to control when the enemy starts moving
        
        self.can_move = False  # Flag to control enemy movement
        
        self.spawn_sound_played = False  # Flag to track if the spawn sound has been played

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
                    if not self.spawn_sound_played:
                        # Play the Enemy Spawn SFX
                        enemy_spawn_sfx.play()
                        self.spawn_sound_played = True

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
            
#   Projectile Class
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.image = pygame.transform.scale(player_projectile, (10, 10))
        self.rect = pygame.Rect(x, y, 10, 10)
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)

    def move(self):
        self.rect.x += BULLET_SPEED * math.cos(self.angle)
        self.rect.y += BULLET_SPEED * math.sin(self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
#   Game Timer Class
class Timer:
    def __init__(self):
        self.start_time = 0
        self.font = pygame.font.Font(None, 36)
        self.elapsed_time = 0
        self.running = False  # Variable to track whether the timer is running or not

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        self.elapsed_time += time.time() - self.start_time
        self.running = False

    def reset(self):
        self.elapsed_time = 0
        self.running = False

    def update(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time

    def draw(self, screen):
        if self.running:
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            time_text = f"Time: {minutes:02d}:{seconds:02d}"
            text_surface = self.font.render(time_text, True, (255, 255, 255))
            screen.blit(text_surface, (10, SCREEN_HEIGHT - 40))
            
# Game Menu Instance
menu = Menu()

clock = pygame.time.Clock()
frame_count = 0
game_timer = Timer()

start_time = pygame.time.get_ticks()    #   Record the start time when the game starts
is_attack = False
running = False
game_over = False   #   Gameover Flag
game_over_menu = None

desired_fps = 60
cap.set(cv2.CAP_PROP_FPS, desired_fps)

if not cap.set(cv2.CAP_PROP_FPS, desired_fps):
    print("Error: Could not set the desired frame rate.")
    
set_fps = cap.get(cv2.CAP_PROP_FPS)
print("Set frame rate:", set_fps)

#music
#pygame_background_music.play()

while True:

    if not running and not game_over:
        menu_choice = None
        while menu_choice is None:
            menu.draw(screen)
            pygame.display.flip()
            menu_choice = menu.handle_events()

            #opencv 1st instance
            ret, frame = cap.read()

            frame = cv2.flip(frame, 1)

            if not ret:
                print("Error: Could not read frame.")
                break

            # Convert the frame to RGB format (MediaPipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame using the Hands model
            results = hands.process(frame_rgb)

            #gesture = None

            # Draw hand landmarks on the frame if hands are detected
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, landmarks, mp_hands.HAND_CONNECTIONS)
                    #if results:  # Add your hand gesture detection logic here
                    thumb_landmarks = [landmarks.landmark[i] for i in thumbs_up_template]

                    # Calculate the Euclidean distances between the thumb landmarks
                    distances = [((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5 for a, b in zip(thumb_landmarks, thumb_landmarks[1:])]

                    comvis_x = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
                    comvis_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                        #comvis
                    #player.comvis(comvis_x * SCREEN_WIDTH, comvis_y * SCREEN_HEIGHT)


                    pygame.mouse.set_pos(comvis_x * SCREEN_WIDTH, comvis_y * SCREEN_HEIGHT)
                
                
            # Display the frame in a window
            cv2.imshow("Camera Preview", frame)
            cv2.waitKey(1)
            #opencv end
        # Game start
        if menu_choice == "PLAY":
            running = True
            is_attack = True
            game_running = True
            time_start = True
            game_timer.start()  # Start the game timer when the player clicks "PLAY"

        # Create instances of player, objective, enemies, and bullets
            player = Player(player_weapon)
            weapon = Weapon(player_weapon)
            objective = Objective()
            enemies = []
            bullets = []

            
    
    #opencv 1st instance
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

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
            
            comvis_x = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
            comvis_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                #comvis
            player.comvis(comvis_x * SCREEN_WIDTH, comvis_y * SCREEN_HEIGHT)
        
    # Display the frame in a window
    cv2.imshow("Camera Preview", frame)
    cv2.waitKey(1)
    #opencv end
    
    if running:
        # Game Loop
         # Update the game timer when the game is actively running
        if game_running is True:
            game_timer.update()
                
        # Process the frame using the Hands model
        results = hands.process(frame_rgb)

        gesture = None
        cv_x = 0
        cv_y = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
                
        player.move(cv_x, cv_y)
        player.auto_attack(enemies)
        weapon.move(cv_x, cv_y)
        
        player.update()
        weapon.update(cv_x, cv_y)
        objective.update()

         # Spawn enemies at regular intervals
        if frame_count % ENEMY_SPAWN_INTERVAL == 0:
            enemies.append(Enemy())
            
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
                enemy_death_sfx.play()
                enemies.remove(enemy)

        # Check for player shooting
        
        if is_attack is True:
            ABLE_TO_ATTACK_DELAY -= 1
            if ABLE_TO_ATTACK_DELAY <= 0:
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
            if bullet in bullets:
                bullets.remove(bullet)

        # Cap the bullet count to the maximum value
        if player.bullet_count > MAX_BULLET_COUNT:
            player.bullet_count = MAX_BULLET_COUNT

        if game_running:
            # Check if 10 seconds have passed and increase enemy speed
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= ENEMY_SPEED_INCREASE_INTERVAL:
                ENEMY_SPEED += ENEMY_SPEED_INCREASE
                # Reset the start time to the current time
                start_time = pygame.time.get_ticks()
                
        if game_running:
            # Check if 10 seconds have passed and increase bullet speed
            if elapsed_time >= BULLET_SPEED_INCREASE_INTERVAL:
                BULLET_SPEED += BULLET_SPEED_INCREASE
                if BULLET_SPEED >= 72:
                    BULLET_SPEED_INCREASE = 0
                # Reset the start time to the current time
                start_time = pygame.time.get_ticks()
                
        if game_running:
            # Check if 10 seconds have passed and increase fire rate
            if elapsed_time >= BULLET_FIRE_DELAY_INCREASE_INTERVAL:
                BULLET_FIRE_DELAY -= BULLET_FIRE_DELAY_INCREASE
                if BULLET_FIRE_DELAY <= 15:
                    BULLET_FIRE_DELAY_INCREASE = 0
                    BULLET_FIRE_DELAY = 5
                # Reset the start time to the current time
                start_time = pygame.time.get_ticks()
                
            # Check if 10 seconds have passed and increase enemy spawn rate
            if elapsed_time >= ENEMY_SPAWN_DECREASE_INTERVAL:
                ENEMY_SPAWN_INTERVAL -= ENEMY_SPAWN_DECREASE
                if ENEMY_SPAWN_INTERVAL <= 5:
                    ENEMY_SPAWN_DECREASE = 0
                # Reset the start time to the current time
                start_time = pygame.time.get_ticks()

        # Game over condition
        if objective.health <= 0 or player.bullet_count == 0:
            running = False
            game_over = True
        
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw player, objective, enemies, and bullets
            
        for enemy in enemies:
            enemy.draw(screen)
            
        objective.draw(screen)
        player.draw(screen)
        
        
        # Draw the game timer
        game_timer.draw(screen)
        
        for bullet in bullets:
            bullet.draw(screen)

        # Check for game over condition (objective health <= 0) or (player(s) bullet count is == 0)
        if objective.health <= 0:
            running = False
        if player.bullet_count == 0:
            running = False

        font = pygame.font.Font(None, 36)
        score_text_menu = font.render(f"Your Score: {player.score}", True, (255, 255, 255))
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100))
        
        # Update the display
        pygame.display.flip()

        # Increment frame count
        frame_count += 1

    if game_over:
        
        #pygame_background_music.stop()
        #pygame_gameover_background_music.play()
        # Stop the game timer when the game is over
        game_timer.stop()

        if game_over_menu is None:
            game_over_menu = GameOverMenu()

            #opencv 1st instance
            ret, frame = cap.read()

            frame = cv2.flip(frame, 1)

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
                    
                    comvis_x = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
                    comvis_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                        #comvis
                    #player.comvis(comvis_x * SCREEN_WIDTH, comvis_y * SCREEN_HEIGHT)
                
            # Display the frame in a window
            cv2.imshow("Camera Preview", frame)
            cv2.waitKey(1)
            #opencv end
            
        #game_over_choice = None
        #while game_over_choice is None:
        #q: how isnt the game over menu working?
        if game_over_menu is not None:
            game_over_menu.draw(screen)
            
            pygame.display.flip()
            game_over_choice = game_over_menu.handle_events()

            
        if game_over_choice == "REPLAY":
            game_over = False
            game_over_menu = None # Will reset game

            pygame_gameover_background_music.stop()
            pygame_background_music.play()
            # Reset player's score, bullet count, and other game variables
            
            player.score = 0
            player.bullet_count = MAX_BULLET_COUNT
            player.bullet_fire_delay = 0
            objective.health = OBJECTIVE_HIT_POINTS
            ENEMY_SPEED = 10
            ENEMY_SPAWN_INTERVAL = 30
            enemies.clear()
            bullets.clear()
            game_timer.reset()

            
    pygame.display.flip()
    clock.tick(GAME_FPS)
    
cap.release()
cv2.destroyAllWindows()
