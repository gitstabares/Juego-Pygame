import pygame, random
import math as mt

color_black = (0,0,0)
color_white = (255,255,255)
width = 1280
height = 720
x_center = width//2
y_center = height//2
score = 0
goal_score = 10
pause = False
gameOver = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x_spawn):
        super().__init__()
        self.image = pygame.image.load("Sprites/Enemy.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image,90)
        self.image.set_colorkey(color_black)
        self.rect = self.image.get_rect(center=(x_spawn,-10))
        self.velocity = 5
    def update(self):
        self.rect.y += self.velocity

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_spawn,y_spawn):
        super().__init__()
        self.image = pygame.image.load("Sprites/Bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image,90)
        self.image.set_colorkey(color_black)
        self.rect = self.image.get_rect(center=(x_spawn,y_spawn))
        self.velocity = 20
    def update(self):
        self.rect.y -= self.velocity
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x_center, y_center))
    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(center=(mouse_x, mouse_y))
    def shoot(self,x,y):
        bullet = Bullet(x,y)
        bullet_sprite_group.add(bullet)

class Planet(pygame.sprite.Sprite):
    def __init__(self,number_planet):
        super().__init__()
        self.image = pygame.image.load("Sprites/Planet"+str(number_planet)+".png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, random.randint(0,8))
        self.rect = self.image.get_rect(center=(random.randint(50,width),random.randint(20,height)))

def Pause_menu(pause,running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = False

    screen.fill(color_white)
    texto_pausa = font.render("Juego Pausado", True, color_black)
    texto_continuar = font.render("Presiona ESC para continuar", True, color_black)

    screen.blit(texto_pausa, (x_center - texto_pausa.get_width() // 2, height // 3))
    screen.blit(texto_continuar, (x_center - texto_continuar.get_width() // 2, y_center))
    pygame.display.flip()
    return pause, running

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
pygame.mixer.music.load('battle.wav')
pygame.mixer.music.play(-1)

background_sprite_group = pygame.sprite.Group()
player_sprite_group = pygame.sprite.Group()
bullet_sprite_group = pygame.sprite.Group()
enemy_sprite_group = pygame.sprite.Group()
pygame.mouse.set_visible(False)

for i in range(1,6):
    planet = Planet(i)
    background_sprite_group.add(planet)
player = Player()
player_sprite_group.add(player)
background = pygame.image.load('Sprites/background.png')

enemy_spawn_event = pygame.event.custom_type()
pygame.time.set_timer(enemy_spawn_event, 1000)

running = True
while running:
    if pause:
        pause, running = Pause_menu(pause,running)
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
            elif event.type == enemy_spawn_event:
                enemy = Enemy(random.randint(0,width))
                enemy_sprite_group.add(enemy)


        background_sprite_group.update()
        player_sprite_group.update()
        bullet_sprite_group.update()
        enemy_sprite_group.update()

        for bullet in bullet_sprite_group:
            enemy_hit = pygame.sprite.spritecollide(bullet,enemy_sprite_group,True)
            for enemy in enemy_hit:
                bullet_sprite_group.remove(bullet)
                score += 1
        
        for player in player_sprite_group:
            player_hit = pygame.sprite.spritecollide(player,enemy_sprite_group,True)
            for hit in player_hit:
                gameOver = True

        screen.fill(color_black)
        screen.blit(background, (0, 0))
        background_sprite_group.draw(screen)
        player_sprite_group.draw(screen)
        bullet_sprite_group.draw(screen)
        enemy_sprite_group.draw(screen)

        score_text = font.render(f"Puntaje: {score}", True, color_white)
        screen.blit(score_text, (10, 10))

        if score == goal_score or gameOver:
            screen.fill(color_white)
            pygame.mouse.set_visible(True)
            enemy_sprite_group.remove()
            gameOver_text = font.render("Partida finalizada, haga click para empezar de nuevo", True, color_black)
            gameOver_text_rect = gameOver_text.get_rect(center = (x_center,y_center))
            screen.blit(gameOver_text, gameOver_text_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameOver = False
                score = 0
                pygame.init()
        elif score > goal_score:
            score = 0

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()