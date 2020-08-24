import pygame, random, time, math

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ENEMY_COLOR = (136, 171, 203)

"""
IMPORTANT NOTICES:
self.rect comes AFTER self.image
put all updating in init method
init only happens once, but update happens every loop iteration
"""

#flip the image when going left
#go up down
#use gravity to control character

#background
class Background(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load("background.png").convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        center = self.rect.center # find center
        factor = 0.5 # the factor in which we want to scale the sprite
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        #cast to int to scale properly
        self.rect.center = center # find center

#enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # moving along x
        self.movey = 0 # moving along y
        self.frame = 0 # count frames
        self.images = []
        for i in range(1, 3):
            img = pygame.image.load("enemy"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect() # get rect
        #scaling
        center = self.rect.center # find center
        factor = 0.5  # the factor in which we want to scale the sprite
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        #cast to int to scale properly
        self.rect.center = center # replace center
        #movement
    #player movement: use += so x movement doesn't affect y movement and vice versa

#animated sprite: mario
class Player(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # moving along x
        self.movey = 0 # moving along y
        self.frame = 0 # count frames
        self.images = []
        for i in range(1, 7):
            img = pygame.image.load("mario"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect() # get rect
        #scaling
        center = self.rect.center # find center
        factor = 0.5  # the factor in which we want to scale the sprite
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        #cast to int to scale properly
        self.rect.center = center # replace center
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            print ("yes")

#more init
fps = 40
ani = 7
screensize = (800, 500)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

enemy = Enemy()
player = Player()
background = Background()
player.rect.x = 100 # player x start value
player.rect.y = 420 # player y start value
enemy.rect.x = 100 # enemy x start value
enemy.rect.y = 420 # enemy y start value
enemy.cnt = 0 #animation slowdown for enemy
player_list = pygame.sprite.Group() # inits empty group of sprites
enemy_list = pygame.sprite.Group()
player_list.add(background)
player_list.add(player)
enemy_list.add(enemy)
pixel_lr = 5 # player move speed
enemy_lr = random.randint(1, 6) # enemy move speed
pixel_u = 1 # jump adjustment factor
times = 0
isjump = False
enemy_move = True
jump_start = 12
jumpcount = jump_start
cnt = 0

done = False
while not done:
    #set backdrop
    """
    backdrop = pygame.image.load("background.png").convert()
    backdrop_box = screen.get_rect()
    screen.blit(backdrop, backdrop_box)
    """
    screen.fill(BLACK)
    player.update()
    #only update player and enemy
    #print (enemy.rect)
    #print (player.rect)
    #t = enemy.update(enemy_lr, enemy_move)
    #enemy_lr = t[0]
    #enemy_move = t[1]
    player_list.draw(screen) #draw everything to the screen
    enemy_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps) #limit # of frames
pygame.quit()

