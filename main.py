import pygame
import colorsys
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=(PLAYER_X_CORD, PLAYER_Y_CORD))

        self.gravity = -5

        self.mask = pygame.mask.from_surface(self.image)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity-=1
            self.gravity = max(-5,self.gravity)
    def update(self):
        global isGameActive
        self.player_input()
        self.rect.y += self.gravity
        if self.rect.y<0:
            self.rect.y = 0
        if self.rect.centery>=HEIGHT:
            isGameActive = False
            self.gravity = -5
        self.gravity += 0.1

        # Color grading of player

        # Green -> going up
        # Yellow -> no vertical velocity
        # Red -> going down
        hue = 0.3*min(max(10-(self.gravity+5),0)/10 ,1)
        col = colorsys.hsv_to_rgb(hue, 1.0,1.0)
        rgb = tuple(int(c * 255) for c in col)
        color = pygame.Color(rgb)

        self.image.fill(color)
class Obstacles(pygame.sprite.Sprite):
    def __init__(self,x,y,length):
        super().__init__()
        self.image = pygame.Surface((80, length))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.pointGiven = False
    def update(self):
        global score
        self.rect.x -= 5
        if not self.pointGiven:
            if self.rect.right<=player.sprite.rect.left:
                self.pointGiven = True
                score+=0.5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    score_surf = font.render(f'Score: {int(score)}',False,(64,64,64))
    score_rect = score_surf.get_rect(topleft = (0,0))
    screen.blit(score_surf,score_rect)

def display_game_over_screen(font_color):
    game_over_font = pygame.font.Font(None, 120)
    game_over_surf = game_over_font.render('GAME OVER!',False,'red')
    game_over_rect = game_over_surf.get_rect(center = (screen_rect.centerx,screen_rect.centery-100))

    final_score_surf = font.render(f'Final score: {int(score)}', False, 'darkgreen')
    final_score_rect = final_score_surf.get_rect(center=(screen_rect.centerx,screen_rect.centery ))

    restart_msg_surf = font.render('PRESS SPACE TO RESTART', False,
                                   (font_color, font_color, font_color))
    restart_msg_rect = restart_msg_surf.get_rect(center=(screen_rect.centerx,screen_rect.centery + 100))

    screen.blit(game_over_surf, game_over_rect)
    screen.blit(final_score_surf, final_score_rect)
    screen.blit(restart_msg_surf, restart_msg_rect)

def detect_collision():
    global isGameActive
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        isGameActive = False
pygame.init()


WIDTH = 1200
HEIGHT = 800
PLAYER_X_CORD = 40
PLAYER_Y_CORD = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

start_time = 0



font = pygame.font.Font(None, 50)

pygame.display.set_caption('FakeFlap')
clock = pygame.time.Clock()

# Player sprite
player = pygame.sprite.GroupSingle()
player.add(Player())
# X coord of player, so that if player passes obstacle, score is incremented
score = 0
scorePos = player.sprite.rect.left

obstacles = pygame.sprite.Group()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2000)

isGameActive = True

font_color = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if isGameActive:
            if event.type == obstacle_timer:
                # Generating new obstacle

                x = random.randint(0,100)
                x += WIDTH
                gap_len = random.randint(200,400-score)
                gap_start = random.randint(0,HEIGHT-gap_len)
                # Top obstacle
                obstacles.add(Obstacles(x,0,gap_start))

                # Bottom obstacle
                obstacles.add(Obstacles(x,gap_start+gap_len,HEIGHT-gap_start+gap_len))
        else:
            # Restarting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                obstacles.empty()
                isGameActive = True
                player.sprite.rect.topleft = (PLAYER_X_CORD,PLAYER_Y_CORD)


    if isGameActive:
        screen.fill((0,0,0))

        detect_collision()
        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        display_score()
    else:
        screen.fill((0, 0, 0))
        font_color+=1
        if font_color>=120: font_color = 0
        player.draw(screen)
        obstacles.draw(screen)
        display_game_over_screen(font_color)
    pygame.display.update()
    clock.tick(60)