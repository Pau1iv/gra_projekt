import pygame
from pygame import mixer
from levels.level1 import *
from levels.level2 import *
from levels.level3 import *

pygame.init()
game_over=0
clock=pygame.time.Clock()
fps=60

#40x40
tile_size=60
scr_width=900 #15
scr_height=600 #10
screen = pygame.display.set_mode((scr_width,scr_height))
pygame.display.set_caption('Little Kinght Journay')

main_menu=True

#TODO BackGround/Images
bg_img = pygame.image.load('img/bg_img.png')
bg_img = pygame.transform.scale(bg_img,(scr_width,scr_height))
restart_img=pygame.image.load('img/restart_button.png')
restart_img=pygame.transform.scale(restart_img,(150,150))
start_img=pygame.image.load('img/strat_button.png')
start_img=pygame.transform.scale(start_img,(200,200))
exit_img=pygame.image.load('img/exit_button.png')
exit_img=pygame.transform.scale(exit_img,(200,200))
przegrana_img=pygame.image.load('img/przegrana.png')
przegrana_img=pygame.transform.scale(przegrana_img,(200,200))
zwyciestwo_img=pygame.image.load('img/zwyciestwo.png')
zwyciestwo_img=pygame.transform.scale(zwyciestwo_img,(200,200))



#TODO RYSOWANIE LICZNIKA
font_score=pygame.font.SysFont('Bauhaus 93',30)
white=(255,255,255)
def drawCoinCounter(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

#TODO MUSIC EFFECT AND BG
pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

pygame.mixer.music.load("img/backgroundmusic.wav")
pygame.mixer.music.play(-1,0.0,8000)
Colision=pygame.mixer.Sound("img/stomp.wav")
Colision.set_volume(5)
Jump=pygame.mixer.Sound("img/jump.wav")
Jump.set_volume(5)
coin=pygame.mixer.Sound("img/coin.wav")
coin.set_volume(5)
win=pygame.mixer.Sound("img/winmusic.wav")
win.set_volume(5)

def  reset_level(level):
    player.reset(0,520)
    monster_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    win_group.empty()

    list = [level1, level2,level3]
    world_data = list[current_level]
    world = World(world_data)
    return world


class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False

    def draw(self):
        action=False
        #myszka
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False: #lewyklawisz
                action=True
                self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        screen.blit(self.image,self.rect)

        return action

#TODO rysowanie gracza dodawanie animacji ruchu
class Player():
    def __init__(self,x,y):
        self.reset(x,y)


    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        # self.images_jump_right=[]
        # self.images_jump_left=[]
        self.index = 0
        self.counter = 0
        self.dead_image = pygame.image.load(f'img/grave.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (50, 50))
        for num in range(1, 7):  # do ile mamy animacje
            img_right = pygame.image.load(f'img/player{num}.png')
            img_right = pygame.transform.scale(img_right, (50, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = self.image.get_height()
        self.width = self.image.get_height()
        self.vel_y = 0
        self.jump = False
        self.direction = 0
        self.inair=True


    #TODO działanie całej mapy na podstawie tego czy nie została napotkana kolziaj z enemy
    def update(self,game_over):
        dx=0
        dy=0
        walk_cooldown = 10
        if game_over==0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dx -= 6
                self.counter += 1
                self.direction = -1
            if keys[pygame.K_RIGHT]:
                dx += 6
                self.counter += 1
                self.direction = 1
            if keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if keys[pygame.K_SPACE] and self.jump == False and self.inair==False:
                # self.counter+=1
                self.vel_y = -12
                self.jump = True
                Jump.play()
            if keys[pygame.K_SPACE] == False:
                self.jump = False
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #kolizja
            self.inair=True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # dy=0
                    # jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # chodzenie po kafelkach
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.inair=False
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.index = 0

            #kolizja smierc
            if pygame.sprite.spritecollide(self, monster_group, False):
                Colision.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                Colision.play()
                game_over = -1

            #kolizja nastepny poziom

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #kolizja zwyciestwo

            if pygame.sprite.spritecollide(self, win_group, False):
                game_over = 2

                win.play()


            self.rect.x += dx
            self.rect.y += dy

            if self.rect.right > scr_width:
                self.rect.right = scr_width
                self.index = 0
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.vel_y = 0

        if game_over==-1:
            self.image=self.dead_image

        screen.blit(self.image,self.rect)
        return game_over



# ToDO rysowanie struktur na podstawie cyfry przypisanej do danej instancji
class World():
    def __init__(self,map):
        platform_img = pygame.image.load('img/platform_img.png')
        self.tile_list=[]
        height=0
        for row in map:
            column=0
            for el in row:
                if el == 1: #ToDO blocks
                    img = pygame.transform.scale(platform_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x=column*tile_size
                    img_rect.y=height*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if el == 2:  # exit_gate
                    exit = Exit(column * tile_size, height * tile_size + 5)
                    exit_group.add(exit)

                if el == 3: #lava
                    lava = Lava(column * tile_size, height * tile_size+tile_size//2)
                    lava_group.add(lava)
                # TODO - Dodać drzwi oraz przejscie

                if el == 6: #enemy
                    monster = Enemy(column*tile_size,height*tile_size+5)
                    monster_group.add(monster)

                if el == 8: #enemy
                    win = Win(column*tile_size,height*tile_size+5)
                    win_group.add(win)

                if el == 7:  # coin
                    score_coin = Coin(tile_size - 50, tile_size - 60)
                    coin = Coin(column * tile_size, height * tile_size + 10)
                    coin_group.add(coin)
                    coin_group.add(score_coin)


                column += 1
            height += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

#ToDO Dodanie przeciwników oraz ich poruszanie się
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load('img/ghostperfect.png')
        self.image= pygame.transform.scale(self.image,(tile_size-30,tile_size-30))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y+15
        self.direction=1
        self.counter=0
    def update(self):

        self.rect.x+=self.direction
        self.counter+=1
        if self.counter>tile_size+15:
            self.direction*=-1
            self.counter=0
            self.image=pygame.transform.flip(self.image,True,False)
#ToDO Dodanie lawy
class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('img/lava_img.png')
        self.image= pygame.transform.scale(self.image,(tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('img/exit_gate.png')
        self.image= pygame.transform.scale(self.image,(tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Win(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('img/win_picture.png')
        self.image= pygame.transform.scale(self.image,(tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#ToDO Dodanie Waluty
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.counter=0
        self.index = 0
        self.Animation = []
        for num in range(0, 4):
            image = pygame.image.load(f'img/coin{num}.png')
            image = pygame.transform.scale(image, (40, 40))
            self.Animation.append(image)
        self.image = self.Animation[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def update(self):
        self.counter+=1
        walk_cooldown = 10
        if self.counter > walk_cooldown:
           self.index+=1
           self.counter=0
        if self.index >= len(self.Animation):
            self.index = 0
        self.image = self.Animation[self.index]


# TODO Rysowanie oraz działanie całej mapy "Main Funckja" \/
player=Player(0,520)
monster_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
win_group=pygame.sprite.Group()

list=[level1,level2,level3]
current_level=0
world_data =list[current_level]
world=World(world_data)

money=0
# przyciski
restart_button = Button(0,490,restart_img)
start_button = Button(scr_width//2-220,scr_height//2-100,start_img)
exit_button=Button(scr_width//2+20,scr_height//2-100,exit_img)

#swiat
while True:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    if main_menu:
        if start_button.draw():
            main_menu=False
        if exit_button.draw():
            pygame.quit()
    else:
        world.draw()
        if game_over==0:
                coin_group.update()
                if pygame.sprite.spritecollide(player, coin_group, True):
                    coin.play()
                    money += 1

                drawCoinCounter('X ' + str(money), font_score, white, tile_size - 10, 5)
                monster_group.update()
        monster_group.draw(screen)
        exit_group.update()
        exit_group.draw(screen)
        lava_group.update()
        lava_group.draw(screen)
        coin_group.draw(screen)
        game_over=player.update(game_over)
        win_group.update()
        win_group.draw(screen)
        if game_over==-1: #zgon
            screen.blit(przegrana_img,(scr_width//2-100,scr_height//2-100))
            if restart_button.draw():
                world_data = []
                current_level = 0
                world = reset_level(current_level)
                game_over = 0
                money=0
        if game_over == 1:
            current_level+=1
            if current_level<=4:
                world_data=[]
                world=reset_level(current_level)
                game_over=0
        if game_over==2:
            screen.blit(zwyciestwo_img, (scr_width // 2 - 100, scr_height // 2 - 100))

    pygame.display.update()

