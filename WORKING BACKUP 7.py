import pygame, random, time, math, turtle, sys

pygame.init() #initialize pygame functions

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ENEMY_COLOR = (136, 171, 203) 

"""
IMPORTANT NOTICES:
flip the image when going left
go up and down
use gravity to control character
self.rect comes AFTER self.image
put all updating in init method
init only happens once, but update happens every loop iteration]
revert detects collision
make sure times new roman TTF is installed on computer
"""

#background
class Background(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 4):
            img = pygame.image.load("background"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor2
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor2*self.rect.width), (int)(factor2*self.rect.height))) 
        self.rect.center = center # find center
    """
    def kill(self):
        self.image = self.images[2]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor3
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor3*self.rect.width), (int)(factor3*self.rect.height))) 
        self.rect.center = center # find center
    """
    def start(self):
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor2
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor2*self.rect.width), (int)(factor2*self.rect.height))) 
        self.rect.center = center # find center

#health bar
class Health(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0 # count which picture you are at
        self.images = []
        for i in range(1, 7):
            img = pygame.image.load("Health"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #no scaling required
    def revert(self):
        global game_over
        self.frame += 1
        #print (self.rect.x, self.rect.y)
        self.image = self.images[self.frame]
        if self.frame == 5:
            game_over = True
    def start(self):
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect() # get rect

#enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # moving along x
        self.movey = 0 # moving along y
        self.frame = 0 # count frames
        self.hitbox = 0
        self.images = []
        for i in range(1, 3):
            img = pygame.image.load("enemy"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    #player movement: use += so x movement doesn't affect y movement and vice versa
    def control(self, x, y):
        self.movex = x
        self.movey = y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    def update(self): #counter to move enemy animations slower
        #update sprite position after movex and movey changed
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.hitbox = self.rect.inflate(-25, -25)
        #print (self.rect.x, self.rect.y, "rect")
        global enemy_lr, enemy_move # use global values
        #Check x boundaries --> only moves left and right
        if self.rect.x > 750:
            self.rect.x = 0
            enemy_lr = random.randint(3, 10)
            enemy_move = True
        #advance animation frames
        global ani # use global animation frames
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
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    def revert(self):
        global enemy_lr, enemy_move
        enemy_lr = random.randint(3, 10)
        enemy_move = True
        self.rect.x = 0
        # advance animation frames
        self.frame += 1
        if self.frame >= 2*ani: # number of frames * ani
            self.frame = 0
        self.image = self.images[(self.frame//ani)]
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    def start(self):
        self.movex = 0 
        self.movey = 0 
        self.frame = 0 
        self.hitbox = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center

#animated sprite: mario
class Player(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # moving along x
        self.movey = 0 # moving along y
        self.frame = 0 # count frames
        self.health = 10 # player health
        self.hitbox = 0
        self.images = []
        for i in range(1, 7):
            img = pygame.image.load("mario"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    #player movement: use += so x movement doesn't affect y movement and vice versa
    def Dir(self):
        return self.movex >= 0 # right? 
    def control(self, x, y):
        self.movex += x
        self.movey += y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    #movement
    def update(self):
        #update sprite position after movex and movey changed
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.hitbox = self.rect.inflate(-25, -25)
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
        global ani # use global animation frames
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
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    def revert(self):
        self.rect.x = 200
        # advance animation frames
        self.frame += 1
        if self.frame >= 6*ani: # number of frames * ani
            self.frame = 0
        self.image = self.images[(self.frame//ani)]
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
        #decrement health
        self.health -= 1
    def start(self):
        self.movex = 0 
        self.movey = 0 
        self.frame = 0 
        self.health = 10 
        self.hitbox = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center

def collided(sprite, other):
    """Check if the hitboxes of the two sprites collide."""
    return sprite.hitbox.colliderect(other.hitbox)

def start_text():
    #at school: H:/Downlaods/times-new-roman.ttf
    #at home: C:/Users/J/Downloads/times-new-roman.ttf
    font = pygame.font.Font("C:/Users/J/Downloads/times-new-roman.ttf", 36)
    text = font.render("The Platformer - with music :)", 0, (10, 10, 10))
    screen.blit(text, (150, 100))
    text = font.render("Press s to start. ", 0, (10, 10, 10))
    screen.blit(text, (150, 300))

def end_text():
    #at school: H:/Downlaods/times-new-roman.ttf
    #at home: C:/Users/J/Downloads/times-new-roman.ttf
    font = pygame.font.Font("C:/Users/J/Downloads/times-new-roman.ttf", 36)
    text = font.render("Oh No! U Died!", 0, (10, 10, 10))
    screen.blit(text, (150, 100))
    text = font.render("Press f to play again. ", 0, (10, 10, 10))
    screen.blit(text, (150, 200))
    text = font.render("Press d to stop playing. ", 0, (10, 10, 10))
    screen.blit(text, (150, 300))

def dash_update():
    #at school: H:/Downlaods/times-new-roman.ttf
    #at home: C:/Users/J/Downloads/times-new-roman.ttf
    font = pygame.font.Font("C:/Users/J/Downloads/times-new-roman.ttf", 36)
    text = font.render("Dashes: " + str(dash_amount), 0, (10, 10, 10))
    screen.blit(text, (300, 100))

def gameover():
    screen.fill(WHITE)
    end_text()
    pygame.display.flip() # change the display screen
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == ord('f'):
                    done = True
                if event.key == ord('d'):
                    pygame.quit()
                    quit()

def game_loop():
    global enemy_lr, enemy_move, game_over, dash_amount, isjump, isdash, jump_start, jumpcount, dash_cnt, jump_start, jumpcount, pixel_lr, pixel_u, times, dash_dir
    done = False
    #start music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("theme.wav")
    pygame.mixer.music.play(-1)
    while not done:
        #print(enemy_move, "number one")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.control(-pixel_lr, 0) # move left
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(pixel_lr, 0) # move right
                if (event.key == pygame.K_UP or event.key == ord('w'))and not isjump:
                    isjump = True
                if event.key == ord('q') and not isdash and dash_amount >= 1:
                    if (player.Dir()):
                        player.control(dash_lr, 0)
                        dash_amount -= 1
                        dash_dir = False
                    else:
                        player.control(-dash_lr, 0)
                        dash_amount -= 1
                        dash_dir = True
                    isdash = True
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
                player.control(0,pixel_u)
                jumpcount -= 1
            else: 
                jumpcount = jump_start
                player.control(0, -jumpcount * pixel_u)
                isjump = False
            #print (jumpcount, "jumpcount")
        if isdash:
            dash_cnt += 1
            if dash_cnt == 2:
                dash_cnt = 0
                isdash = False
                if dash_dir:
                    player.control(dash_lr, 0)
                else:
                    player.control(-dash_lr, 0)
        if enemy_move:
            #print(enemy_lr, "hi")
            enemy.control(enemy_lr, 0)
            enemy_move = False
        screen.fill(BLACK)
        #only update player and enemy
        player.update()
        enemy.update()
        #print(enemy_move, "number two")
        #detect collision
        enemy_hit_list = []
        enemy_hit_list = pygame.sprite.spritecollide(player, enemy_list, False, collided) # checks for player and enemy hitboxes
        if not len(enemy_hit_list) == 0:
            player.revert()
            enemy.revert()
            health.revert()
            if game_over == True:
                #play crash sound
                pygame.mixer.Sound.play(crash_sound)
                #stop theme music
                pygame.mixer.music.stop()
                if gameover() == False:
                    pygame.quit()
                    quit()
                else:
                    #restart everything
                    start()
        #draw everything to the screen
        background_list.draw(screen)
        player_list.draw(screen) 
        enemy_list.draw(screen)
        health_list.draw(screen)
        dash_update()
        pygame.display.update() # change the display screens
        clock.tick(fps) #limit # of frames
        enemy_move = True
    pygame.quit()
    quit()

def game_intro():
    screen.fill(WHITE)
    pygame.mixer.music.load("start.wav")
    pygame.mixer.music.play(-1)
    start_text()
    pygame.display.update() #display start text to screen
    done = False
    stop = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == ord('s'):
                done = True

def init_variables():
    #import global variables
    global factor, factor2, factor3, ani, enemy_lr, enemy_move, game_over, dash_amount, isjump, isdash, \
    jump_start, jumpcount, dash_cnt, pixel_lr, dash_lr, pixel_u, times, dash_dir
    #variable inits
    factor = 0.6
    factor2 = 0.5
    factor3 = 0.7
    ani = 7
    enemy_lr = random.randint(3, 10)
    enemy_move = True
    game_over = False
    dash_amount = 10
    isjump = False
    isdash = False
    jump_start = 12
    jumpcount = jump_start
    dash_cnt = 0
    pixel_lr = 5
    dash_lr = 6 * pixel_lr
    pixel_u = 1 # keep this as integer
    times = 0
    dash_dir = True
    
def init_sprites():
    #class inits
    player.rect.x = 400 # player x start value
    player.rect.y = 430 # player y start value
    enemy.rect.x = 0 # enemy x start value
    enemy.rect.y = 430 # enemy y start value
    health.rect.x = 500 # health bar x value
    health.rect.y = 50 # health bar y value
    enemy.cnt = 0 #animation slowdown for enemy

def revert():
    background.start()
    health.start()
    init_variables()
    init_sprites()
    #draw everything to the screen
    background_list.draw(screen)
    player_list.draw(screen) 
    enemy_list.draw(screen)
    health_list.draw(screen)
    dash_update()
    pygame.display.update() # change the display screen

def start():
    game_intro()
    #initializeeverything
    revert()
    #run game loop
    game_loop()

#global variables here
global factor #scaling player and enemy
global factor2 #scaling background 
global factor3 #scaling background 
global ani #animation frames
global enemy_lr #enemy move pixels
global enemy_move # check if enemy needs to change speed
global game_over #check if the game is over
global dash_amount # dash amount
global isjump # is the player jumping
global isdash # is the player dashing
global jump_start # set jump height
global jumpcount # what part of the jump is the player at
global dash_cnt # is the player dashing
global pixel_lr # player move speed
global dash_lr # 
global pixel_u # jump adjustment factor
global times 
global dash_dir # True is left, False is right

init_variables() #after global definition

#inits ONLY ONCE
fps = 40
screensize = (800, 500)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("My Game")
#init pygame clock
clock = pygame.time.Clock()
#all sounds init(wav files)
crash_sound = pygame.mixer.Sound("crash.wav")
#create sprites
enemy = Enemy()
player = Player()
background = Background()
health = Health()

init_sprites() #after sprite creation

#initialize all lists as empty lists
player_list = pygame.sprite.Group() 
enemy_list = pygame.sprite.Group()
background_list = pygame.sprite.Group()
health_list = pygame.sprite.Group()
# add sprites to corresponding lists
background_list.add(background)
player_list.add(player)
enemy_list.add(enemy)
health_list.add(health)

#start game 
start(
)
