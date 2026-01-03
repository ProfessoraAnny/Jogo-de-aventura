import pygame
import random
import math

# Constants
WIDTH = 800
HEIGHT = 450
GRAVITY = 0.6
SPEED = 4
JUMP_VELOCITY = -12
ENEMY_SPEED = 2
FPS = 60

# Game State
game_state = "game"
sound_on = True

# Initialize Pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meu Jogo")  # Titulo da janela

# Colors
SKY_COLOR = (135, 206, 235)

# Load Sounds (Verifique os caminhos dos arquivos!)
try:
    pygame.mixer.music.load("sons/music.wav")  # Música de fundo (looping)
    pygame.mixer.music.set_volume(0.5)  # Ajusta o volume (0.0 a 1.0)
    pygame.mixer.music.play(-1)  # -1 significa loop infinito

    run_sound = pygame.mixer.Sound("sons/run.wav")
    hit_sound = pygame.mixer.Sound("sons/hit.wav")
except pygame.error as e:
    print(f"Erro ao carregar sons: {e}")
    run_sound = None
    hit_sound = None

# Load Images (Verifique os caminhos dos arquivos!)
try:
    captain_idle_img = pygame.image.load("images/captain_idle_0.png").convert_alpha()
    captain_run_img = pygame.image.load("images/captain_run_0.png").convert_alpha()
    enemy_image = pygame.image.load("images/enemy_idle_0.png").convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    # Criar uma superfície vazia como fallback
    captain_idle_img = pygame.Surface((50, 50))  # Tamanho arbitrário
    captain_run_img = pygame.Surface((50, 50))
    enemy_image = pygame.Surface((50, 50))
    captain_idle_img.fill((255, 0, 255))  # Cor magenta para indicar erro
    captain_run_img.fill((255, 0, 255))
    enemy_image.fill((255, 0, 255))

# Captain (Player)
captain_x = 200
captain_y = HEIGHT - 100
captain_vx = 0
captain_vy = 0

# Enemies
enemies = []
enemies.append({"x": 500, "y": HEIGHT - 100, "vx": ENEMY_SPEED}) # Usamos dicionários para guardar as propriedades
enemies.append({"x": 650, "y": HEIGHT - 100, "vx": ENEMY_SPEED})

# Game Loop
running = True
clock = pygame.time.Clock()

# Definir as superficies
class CaptainClass(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = int(x)  # Garante que x seja inteiro
        self.y = int(y)  # Garante que y seja inteiro


class EnemiesClass(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y


# Definir as instancias
captain = CaptainClass(captain_idle_img, captain_x, captain_y)
inimigo1 = EnemiesClass(enemy_image, enemies[0]["x"], enemies[0]["y"])
inimigo2 = EnemiesClass(enemy_image, enemies[1]["x"], enemies[1]["y"])

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and captain_vy == 0:
                captain_vy = JUMP_VELOCITY
                if sound_on and run_sound:
                    run_sound.play()

    # Input (Keyboard)
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_RIGHT]:
        captain_vx = SPEED
        moving = True
    elif keys[pygame.K_LEFT]:
        captain_vx = SPEED
        moving = True
    else:
        captain_vx = 0

    # --- Captain Logic ---
    # Gravity
    captain_vy += GRAVITY

    # Update Position
    captain_x += captain_vx
    captain_y += captain_vy

    # Keep on screen
    if captain_y > HEIGHT - 50:
        captain_y = HEIGHT - 50
        captain_vy = 0

    # --- Enemies Logic ---
    for enemy in enemies:
        enemy["x"] += enemy["vx"]
        if enemy["x"] < 0 or enemy["x"] > WIDTH:
            enemy["vx"] *= -1

    #Converter para inteiro e atualizando com as novas coordenas
    captain.x = int(captain_x)
    captain.y = int(captain_y)

    # --- Draw ---
    screen.fill(SKY_COLOR)  # Sky

    # Draw the Captain
    if moving:
        screen.blit(captain_run_img, (captain.x, captain.y)) #jogador  - Jogador escrito de forma errada
    else:
        screen.blit(captain_idle_img, (captain.x, captain.y)) #jogador   - Jogador escrito de forma errada

    # Draw the Enemies
    for enemy in enemies:
        screen.blit(enemy_image, (enemy["x"], enemy["y"]))

    # Update the display
    pygame.display.flip()  # Mostra tudo na tela

    # Control the speed
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
