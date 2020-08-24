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
    def control(self, x, y):
        self.movex = x
        self.movey = y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    def update(self, enemy_lr, enemy_move): #counter to move enemy animations slower
        #update sprite position after movex and movey changed
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        #print (self.rect.x, self.rect.y, "rect")
        #Check x boundaries --> only moves left and right
        if self.rect.x > 750:
            self.rect.x = 0
            enemy_lr = random.randint(1, 6)
            enemy_move = True
        #advance animation frames
        #moving left
        if self.movex < 0:
            self.cnt = (self.cnt + 1) % 2
            if self.cnt:
                self.frame += 1
            if self.frame >= 2*ani: # number of frames * ani
                self.frame = 0
            self.image = self.images[self.frame//ani]
            self.image = pygame.transform.flip(self.image, True, False) #flip image
        # moving right
        elif self.movex > 0:
            self.cnt = (self.cnt + 1) % 2
            if self.cnt:
                self.frame += 1
            if self.frame >= 2*ani: # number of frames * ani
                self.frame = 0
            self.image = self.images[(self.frame//ani)]
        #scaling
        center = self.rect.center # find center
        factor = 0.5  # the factor in which we want to scale the sprite
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        #cast to int to scale properly
        self.rect.center = center # replace center
        return (enemy_lr, enemy_move)

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

    #player movement: use += so x movement doesn't affect y movement and vice versa
    def control(self, x, y):
        self.movex += x
        self.movey += y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    #movement
    def update(self, cnt):
        #update sprite position after movex and movey changed
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        #print (self.rect.x, self.rect.y, "rect")
        #Check x and y boundaries
        if self.rect.x > 750:
            self.rect.x = 750
        elif self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.y > 500:
            self.rect.y = 500
        elif self.rect.y < 50:
            self.rect.y = 50
        #advance animation frames
        #moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame >= 6*ani: # number of frames * ani
                self.frame = 0
            self.image = self.images[self.frame//ani]
            self.image = pygame.transform.flip(self.image, True, False) #flip image
        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame >= 6*ani: # number of frames * ani
                self.frame = 0
            self.image = self.images[(self.frame//ani)]
        #scaling
        center = self.rect.center # find center
        factor = 0.5  # the factor in which we want to scale the sprite
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        #cast to int to scale properly
        self.rect.center = center # replace center
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            print("hit!")
            print("\n")
        return cnt

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
enemy.rect.x = 0 # enemy x start value
enemy.rect.y = 430 # enemy y start value
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-pixel_lr, 0) # move left
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(pixel_lr, 0) # move right
            if event.key == pygame.K_UP and not isjump:
                isjump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(pixel_lr, 0) # adjust left
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                 player.control(-pixel_lr, 0) # adjust right
    if isjump:
        if jumpcount == jump_start:
            player.control(0, -jumpcount * pixel_u)
            jumpcount -= 1
        elif jumpcount >= -jump_start:
            player.control(0, 1 * pixel_u)
            jumpcount -= 1
        else:
            jumpcount = jump_start
            player.control(0, -jumpcount * pixel_u)
            isjump = False
        #print (jumpcount, "jumpcount")
    if enemy_move == True:
        enemy.control(enemy_lr, 0)
        enemy_move = False
    #set backdrop
    """
    backdrop = pygame.image.load("background.png").convert()
    backdrop_box = screen.get_rect()
    screen.blit(backdrop, backdrop_box)
    """
    screen.fill(BLACK)
    #only update player and enemy
    #print (enemy.rect)
    #print (player.rect)
    cnt = player.update(cnt)
    t = enemy.update(enemy_lr, enemy_move)
    enemy_lr = t[0]
    enemy_move = t[1]
    player_list.draw(screen) #draw everything to the screen
    enemy_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps) #limit # of frames
pygame.quit()

