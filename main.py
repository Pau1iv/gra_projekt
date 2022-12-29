import pygame
#from player import *
from pygame.locals import *

pygame.init()

clock=pygame.time.Clock()
fps=60

#40x40
tile_size=40
scr_width=600 #15
scr_height=400 #10
screen = pygame.display.set_mode((scr_width,scr_height))
pygame.display.set_caption('SUPER GRA')

bg_img = pygame.image.load('img/bg_img.png')
bg_img = pygame.transform.scale(bg_img,(scr_width,scr_height))

class Player():
    def __init__(self,x,y):
        self.images_right = []
        self.images_left=[]
        #self.images_jump_right=[]
        #self.images_jump_left=[]
        self.index=0
        self.counter=0
        for num in range(1,7): #do ile mamy animacje
            img_right = pygame.image.load(f'img/player{num}.png')
            img_right = pygame.transform.scale(img_right,(35,35))
            img_left= pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            ''' 6 animacji jak do chodzenia
            if num<4:
                img_jump_right=pygame.image.load(f'img/player_jump{num}.png')
                img_jump_right=pygame.transform.scale(img_jump_right,(tile_size,tile_size))
                self.images_jump_right.append(img_jump_right)
                img_jump_left= pygame.transform.flip(img_jump_right,True,False)
                self.images_jump_left.append(img_jump_left)
                 '''
        self.image = self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.height=self.image.get_height()
        self.width=self.image.get_height()
        self.vel_y=0
        self.jump=False
        self.direction=0

    def update(self):
        dx=0
        dy=0
        walk_cooldown = 10

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx-=6
            self.counter += 1
            self.direction=-1
        if keys[pygame.K_RIGHT]:
            dx+=6
            self.counter += 1
            self.direction=1
        if keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]==False:
            self.counter=0
            self.index=0
            if self.direction==1:
                self.image=self.images_right[self.index]
            if self.direction ==-1:
                self.image=self.images_left[self.index]
        if keys[pygame.K_SPACE] and self.jump==False:
            #self.counter+=1
            self.vel_y=-10
            self.jump=True
            ''' tego nie
            if self.direction==1:
                self.image=self.images_jump_right[self.index]
            if self.direction ==-1:
                self.image=self.images_jump_left[self.index]
            '''
        if keys[pygame.K_SPACE]==False:
            self.jump=False


        if self.counter>walk_cooldown:
            self.counter=0
            self.index+=1
            if self.index>=len(self.images_right):
                self.index=0
            if self.direction==1:
                self.image=self.images_right[self.index]
                '''
                if self.jump:
                    self.image=self.images_jump_right[self.index]
                    '''
            if self.direction ==-1:
                self.image=self.images_left[self.index]
                '''
                if self.jump:
                    self.image=self.images_jump_left[self.index]
                    '''

        self.vel_y+=1
        if self.vel_y>10:
            self.vel_y=10
        dy+=self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                #dy=0
                #jumping
                if self.vel_y<0:
                    dy=tile[1].bottom-self.rect.top
                    self.vel_y=0
                #chodzenie po kafelkach
                elif self.vel_y>=0:
                    dy=tile[1].top-self.rect.bottom
                    self.vel_y=0
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                    dx=0
                    self.index=0


        self.rect.x+=dx
        self.rect.y+=dy

        if self.rect.right>scr_width:
            self.rect.right=scr_width
            self.index=0
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.top<0:
            self.vel_y=0


        #xd


        screen.blit(self.image,self.rect)

class World():
    def __init__(self,map):
        platform_img = pygame.image.load('img/platform_img.png')
        lava_img=pygame.image.load('img/lava_img.png')
        door_img=pygame.image.load('img/door_img.png')
        self.tile_list=[]

        height=0
        for row in map:
            column=0
            for el in row:
                if el == 1: #blocks
                    img = pygame.transform.scale(platform_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x=column*tile_size
                    img_rect.y=height*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if el == 3: #lava
                    img = pygame.transform.scale(lava_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x=column*tile_size
                    img_rect.y=height*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if el == 2: #end
                    img = pygame.transform.scale(door_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x=column*tile_size
                    img_rect.y=height*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if el == 6: #enemy
                    monster = Enemy(column*tile_size,height*tile_size)
                    monster_group.add(monster)

                column += 1
            height += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

"""
    def horizontal_movement_colision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tile_list.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_colision(self):
        player = self.player.sprite
        player.gravity_aplly()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
"""
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load('img/monster_img.png')
        self.image= pygame.transform.scale(self.image,(tile_size-10,tile_size-10))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y+10
        self.direction=1
        self.counter=0
    def update(self):

        self.rect.x+=self.direction
        self.counter+=1
        if self.counter>tile_size+15:
            self.direction*=-1
            self.counter=0
            self.image=pygame.transform.flip(self.image,True,False)


E=2 #END
X=1 #PLATFORM
L=3 #LAVA
#P=4 #MOVING_PLATFORM
M=6 #monster
S=5 #START
world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,M,0,0,E,X],
[0,0,0,0,0,M,0,0,0,X,X,X,X,X,X],
[0,0,0,X,X,X,X,X,0,0,0,0,0,0,0],
[X,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[X,X,0,0,0,0,0,0,0,0,0,0,0,0,0],
[X,X,X,X,X,L,L,X,X,X,X,0,0,0,0],
[X,X,X,X,X,X,X,X,0,0,0,X,0,0,X],
[S,0,0,0,0,0,0,0,0,0,0,0,0,X,X],
[X,X,X,X,X,X,X,X,X,L,X,X,X,X,X]
]
player=Player(0,320)
monster_group=pygame.sprite.Group()
world=World(world_data)
while True:
    clock.tick(fps)

    screen.blit(bg_img,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    world.draw()
    #world.horizontal_movement_colision()
    #world.vertical_movement_colision()
    monster_group.update()
    monster_group.draw(screen)
    player.update()
    pygame.display.update()

