import pygame as pg
import sys
import random

pg.init()
pg.mixer.init()

# ======================
# TELA
# ======================
WIDTH, HEIGHT = 900, 500
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Captain Adventure")

clock = pg.time.Clock()
FPS = 60

# ======================
# CORES / FONTES
# ======================
WHITE = (255, 255, 255)
font = pg.font.SysFont(None, 36)

# ======================
# IMAGENS
# ======================
def load(img):
    return pg.image.load(f"images/{img}").convert_alpha()

background = pg.transform.scale(load("background.png"), (1800, HEIGHT))
clouds = pg.transform.scale(load("big_clouds.png"), (1800, 200))
platform_img = pg.transform.scale(load("platform.png"), (400, 40))

idle_imgs = [pg.transform.scale(load(f"captain_idle_{i}.png"), (96, 96)) for i in range(5)]
run_imgs = [pg.transform.scale(load(f"captain_run_{i}.png"), (96, 96)) for i in range(5)]

enemy_idle = [pg.transform.scale(load(f"enemy_idle_{i}.png"), (80, 80)) for i in range(2)]
enemy_run = [pg.transform.scale(load(f"enemy_run_{i}.png"), (80, 80)) for i in range(2)]

# ======================
# SONS
# ======================
pg.mixer.music.load("sounds/music.wav")
pg.mixer.music.play(-1)

hit_sound = pg.mixer.Sound("sounds/hit.wav")

# ======================
# CLASSES
# ======================
class Player:
    def __init__(self):
        self.rect = pg.Rect(100, 300, 50, 80)
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.frame = 0
        self.anim_time = 0
        self.running = False

    def update(self, keys):
        self.running = False

        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.running = True

        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
            self.running = True

        if keys[pg.K_SPACE] and self.on_ground:
            self.vel_y = -14
            self.on_ground = False

        self.vel_y += 0.8
        self.rect.y += self.vel_y

        if self.rect.bottom >= 360:
            self.rect.bottom = 360
            self.vel_y = 0
            self.on_ground = True

        self.anim_time += 1
        if self.anim_time >= 6:
            self.anim_time = 0
            self.frame = (self.frame + 1) % 5

    def draw(self, cam_x):
        img = run_imgs[self.frame] if self.running else idle_imgs[self.frame]
        screen.blit(img, (self.rect.x - cam_x, self.rect.y))

class Enemy:
    def __init__(self, x):
        self.rect = pg.Rect(x, 300, 60, 60)
        self.frame = 0
        self.anim_time = 0

    def update(self):
        self.anim_time += 1
        if self.anim_time >= 15:
            self.anim_time = 0
            self.frame = (self.frame + 1) % 2

    def draw(self, cam_x):
        screen.blit(enemy_run[self.frame], (self.rect.x - cam_x, self.rect.y))

# ======================
# RESET DO JOGO
# ======================
def reset_game():
    global player, enemy, camera_x, score
    player = Player()
    enemy = Enemy(600)
    camera_x = 0
    score = 0

# ======================
# JOGO
# ======================
player = Player()
enemy = Enemy(600)

camera_x = 0
score = 0

# ======================
# LOOP PRINCIPAL
# ======================
while True:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    player.update(keys)
    enemy.update()

    # CÂMERA
    camera_x = player.rect.x - 200
    if camera_x < 0:
        camera_x = 0

    # COLISÃO → RESET
    if player.rect.colliderect(enemy.rect):
        hit_sound.play()
        reset_game()

    # NOVO INIMIGO
    if enemy.rect.x < camera_x - 100:
        enemy = Enemy(player.rect.x + random.randint(500, 800))
        score += 1

    # ======================
    # DESENHO
    # ======================
    screen.fill(WHITE)

    # NUVENS (atrás)
    screen.blit(clouds, (-camera_x * 0.2, 30))

    # BACKGROUND
    screen.blit(background, (-camera_x * 0.5, 0))

    # CHÃO
    pg.draw.rect(screen, (100, 200, 100), (0, 360, WIDTH, 140))

    enemy.draw(camera_x)
    player.draw(camera_x)

    score_txt = font.render(f"Pontos: {score}", True, (0, 0, 0))
    screen.blit(score_txt, (20, 20))

    pg.display.flip()
