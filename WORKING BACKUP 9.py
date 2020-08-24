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
= means acceleration -> usually
+= means no acceleration -> usually
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
    def add(self):
        self.frame = max(0, self.frame - 1)
        self.image = self.images[self.frame]

class Powerup(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.frame = 0
        self.cnt = 0
        img = pygame.image.load("star.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        img = pygame.image.load("heart.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[self.frame]
        img = pygame.image.load("blank.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
    def revert(self):
        global powerup_type
        powerup_type = 2
        self.rect.x = random.randint(100, 400)
        self.frame += 1
        self.frame %= 2
        self.cnt = 100
        self.image = self.images[2]
        self.hitbox = self.rect
    def update(self):
        self.cnt -= 1
        if self.cnt == 0:
            self.image = self.images[self.frame]
            self.hitbox = self.rect
            global powerup_type
            powerup_type = self.frame

#GROUND enemy sprite
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
    #player movement: use = since you're only moving left/right
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

#enemy in the air
class Lakitu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # moving along x
        self.movey = 0 # moving along y
        self.frame = 0 # count frames
        self.images = []
        img = pygame.image.load("lakitu.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
    def control(self, x, y):
        self.movex = x
        self.movey = y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        global lakitu_lr, lakitu_move, lakitu_dir
        #Check x boundaries --> only moves left and right
        if self.rect.x > 750:
            self.rect.x = 750
            lakitu_lr = random.randint(3, 10)
            lakitu_move = True
            lakitu_dir = False
        if self.rect.x < 0:
            self.rect.x = 0
            lakitu_lr = random.randint(3, 10)
            lakitu_move = True
            lakitu_dir = True

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.hitbox = 0
        self.images = []
        for i in range(1, 3):
            img = pygame.image.load("egg"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
    # use += so don't change x values, but no acceleration, so use =
    def control(self, x, y):
        self.movex += x
        self.movey = y
    def show(self):
        self.image = self.images[0]
        #set egg x to lakitu x
        self.rect.x = lakitu.rect.x
        self.rect.y = lakitu.rect.y
    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.hitbox = self.rect.inflate(-25, -25)
        global egg_show, egg_lr
        if self.rect.y > 430:
            self.rect.y = 0
            egg_lr = random.randint(3, 10)
            self.image = self.images[1]
            egg_show = True
    def revert(self):
        #basically the same as show
        self.image = self.images[0]
        #set egg x to lakitu x
        self.rect.x = lakitu.rect.x
        self.rect.y = lakitu.rect.y

#x-values: 500 and 200
class Koopa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load("koopa.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
    def update(self):
        global koopa_cnt, koopa_type
        koopa_cnt += 1
        #print(koopa_cnt, koopa_type)
        if koopa_type == 1 and koopa_cnt == 100:
            koopa_type += 1
            koopa_cnt = 0
            self.rect.x = 500
            laser.indicate1()
        if koopa_type == 2 and koopa_cnt == 20:
            koopa_type += 1
            koopa_cnt = 0
            self.hitbox = self.rect
            laser.attack1()
        if koopa_type == 3 and koopa_cnt == 30:
            koopa_type += 1
            koopa_cnt = 0
            self.hitbox = self.rect
            laser.revert()
        if koopa_type == 4 and koopa_cnt == 100:
            koopa_type += 1
            koopa_cnt = 0
            laser.indicate2()
            self.rect.x = 200
        if koopa_type == 5 and koopa_cnt == 20:
            koopa_type += 1
            koopa_cnt = 0
            self.hitbox = self.rect
            laser.attack2()
        if koopa_type == 6 and koopa_cnt == 30:
            koopa_type = 1
            koopa_cnt = 0
            self.hitbox = self.rect
            laser.revert()
    def revert(self):
        global koopa_cnt, koopa_type
        koopa_cnt = 0
        if koopa_type == 3:
            koopa_type = 4
        if koopa_type == 6:
            koopa_type = 1

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 4):
            img = pygame.image.load("koopaattack"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        for i in range(1, 3):
            img = pygame.image.load("koopaindicator"+str(i)+".png").convert()
            img.convert_alpha()
            img.set_colorkey(WHITE)
            self.images.append(img)
        self.image = self.images[2]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
    def attack1(self):
        self.rect.x = 220
        self.image = self.images[0]
        #self.rect = self.image.get_rect()
        self.hitbox = self.rect
        #print("ATTACK 1")
    def attack2(self):
        self.rect.x = -70
        self.image = self.images[1]
        #self.rect = self.image.get_rect()
        self.hitbox = self.rect
        #print("ATTACK 2")
    def indicate1(self):
        self.rect.x = 220
        self.image = self.images[3]
        #self.rect = self.image.get_rect()
        self.hitbox = self.rect
        #print("INDICATE 1")
    def indicate2(self):
        self.rect.x = -70
        self.image = self.images[4]
        #self.rect = self.image.get_rect()
        self.hitbox = self.rect
        #print("INDICATE 2")
    def revert(self):
        self.image = self.images[2]
        #self.rect = self.image.get_rect()
        self.hitbox = self.rect
    
class BulletBill(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load("stationary.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #scaling
        global factor4
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor4*self.rect.width), (int)(factor4*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center

class Bullet(pygame.sprite.Sprite):
    #initialize sprite -> called self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0 # player x move
        self.movey = 0 # player y move
        self.hitbox = 0 # player hitbox
        self.images = []
        img = pygame.image.load("bullet.png").convert()
        img.convert_alpha()
        img.set_colorkey(WHITE)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #no scaling required
    #use = since you're only moving left/right
    def control(self, x, y):
        self.movex = x
        self.movey = y
        #print (self.movex, self.movey, "moves")
        #print (x, y, "x and y")
    def update(self):
    #update sprite position after movex and movey changed
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        #print (self.rect.x, self.rect.y, "rect")
        global bullet_lr, bullet_move # use global values
        self.hitbox = self.rect
        #Check x boundaries --> only moves left and right
        if self.rect.x < 0:
            self.rect.x = 750
            bullet_lr = random.randint(3, 10)
            bullet_move = True
    def revert(self):
        global bullet_lr, bullet_move
        bullet_lr = random.randint(3, 10)
        bullet_move = True
        self.rect.x = 730

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
        if self.rect.x > 730:
            self.rect.x = 730
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
        #print(self.rect)
    def revert(self):
        global invincible, invincible_cnt
        invincible = True
        invincible_cnt = 15
        self.rect.x = 400
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
    #at school: H:/Downloads/times-new-roman.ttf
    #at home: C:/Users/J/Downloads/times-new-roman.ttf
    font = pygame.font.Font("C:/Users/J/Downloads/times-new-roman.ttf", 36)
    text = font.render("The Platformer - with music :)", 0, (10, 10, 10))
    screen.blit(text, (150, 100))
    text = font.render("Press s to start. ", 0, (10, 10, 10))
    screen.blit(text, (150, 300))

def end_text():
    #at school: H:/Downloads/times-new-roman.ttf
    #at home: C:/Users/J/Downloads/times-new-roman.ttf
    font = pygame.font.Font("C:/Users/J/Downloads/times-new-roman.ttf", 36)
    text = font.render("Oh No! U Died!", 0, (10, 10, 10))
    screen.blit(text, (150, 100))
    text = font.render("Press f to play again. ", 0, (10, 10, 10))
    screen.blit(text, (150, 200))
    text = font.render("Press d to stop playing. ", 0, (10, 10, 10))
    screen.blit(text, (150, 300))

def dash_update():
    #at school: H:/Downloads/times-new-roman.ttf
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
    global enemy_lr, enemy_move, game_over, dash_amount, isjump, isdash, jump_start, jumpcount, dash_cnt, jump_start, jumpcount \
           , pixel_lr, pixel_u, times, dash_dir, bullet_lr, bullet_move, lakitu_lr, lakitu_move, egg_lr, egg_show, koopa_move, \
           koopa_type, koopa_cnt, invincible, invincible_cnt, powerup_type
    done = True
    #start music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("theme.wav")
    pygame.mixer.music.play(-1)
    while done:
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
        if bullet_move:
            bullet.control(-bullet_lr, 0)
            bullet_move = False
        if lakitu_move:
            if lakitu_dir:
                lakitu.control(lakitu_lr, 0)
            else:
                lakitu.control(-lakitu_lr, 0)
            lakitu_move = False
        if egg_show:
            egg.show()
            egg.control(0, egg_lr)
            egg_show = False
        screen.fill(BLACK)
        #only update player and enemies
        player.update()
        enemy.update()
        egg.update()
        lakitu.update()
        bullet.update()
        koopa.update()
        powerup.update()
        if not invincible_cnt == 0:
            invincible_cnt -= 1
        if invincible_cnt == 0:
            invincible = False
        #print(enemy_move, "number two")
        #detect collisions
        if not invincible:
            """
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
            bullet_hit_list = []
            bullet_hit_list = pygame.sprite.spritecollide(player, bullet_list, False, collided) # checks for player and enemy hitboxes
            if not len(bullet_hit_list) == 0:
                player.revert()
                bullet.revert()
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
            egg_hit_list = []
            egg_hit_list = pygame.sprite.spritecollide(player, egg_list, False, collided) # checks for player and enemy hitboxes
            if not len(egg_hit_list) == 0:
                player.revert()
                egg.revert()
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
            koopa_hit_list = []
            koopa_hit_list = pygame.sprite.spritecollide(player, koopa_list, False, collided) # checks for player and enemy hitboxes
            if not len(koopa_hit_list) == 0:
                player.revert()
                koopa.revert()
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
                        """
            if koopa_type == 3:
                laser_hit_list = []
                laser_hit_list = pygame.sprite.spritecollide(player, laser_list, False, collided) # checks for player and enemy hitboxes
                if not len(laser_hit_list) == 0:
                    player.revert() 
                    koopa.revert()
                    laser.revert()
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
            #second attack: <160, >510
            if koopa_type == 6 and (player.rect.x < 160 or player.rect.x > 510):
                player.revert()
                koopa.revert()
                laser.revert()
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
            powerup_hit_list = []
            powerup_hit_list = pygame.sprite.spritecollide(player, powerup_list, False, collided) # checks for player and enemy hitboxes
            if not len(powerup_hit_list) == 0 and not powerup_type == 2:
                print(powerup.frame)
                if powerup.frame == 0:
                    invincible = True
                    invincible_cnt = 50
                else:
                    health.add()
                powerup.revert()
                
        #draw everything to the screen
        background_list.draw(screen)
        laser_list.draw(screen)
        enemy_list.draw(screen)
        health_list.draw(screen)
        bulletbill_list.draw(screen)
        bullet_list.draw(screen)
        lakitu_list.draw(screen)
        egg_list.draw(screen)
        koopa_list.draw(screen)
        powerup_list.draw(screen)
        player_list.draw(screen) # draw player last
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
    global factor, factor2, factor3, factor4, factor5, ani, enemy_lr, enemy_move, bullet_lr, bullet_move, game_over, dash_amount, isjump, isdash, \
    jump_start, jumpcount, dash_cnt, pixel_lr, dash_lr, pixel_u, times, dash_dir, lakitu_lr, lakitu_move, lakitu_dir, egg_lr, egg_show, koopa_move, \
    koopa_type, koopa_cnt, invincible, invincible_cnt, powerup_type
    #variable inits
    factor = 0.6
    factor2 = 0.5
    factor3 = 0.7
    factor4 = 0.35
    factor5 = 0.16
    ani = 7
    enemy_lr = random.randint(3, 10)
    enemy_move = True
    bullet_lr = random.randint(3, 10)
    bullet_move = True
    lakitu_lr = random.randint(3, 10)
    lakitu_move = True # moving or not?
    lakitu_dir = True # moving right
    egg_lr = random.randint(3, 10)
    egg_show = True
    koopa_move = True
    koopa_type = 1
    koopa_cnt = 0
    game_over = False
    dash_amount = 10
    isjump = False
    isdash = False
    jump_start = 12
    jumpcount = jump_start
    dash_cnt = 0
    pixel_lr = 5
    dash_lr = 8 * pixel_lr
    pixel_u = 1 # keep this as integer
    times = 0
    dash_dir = True
    invincible = False
    invincible_cnt = 0
    powerup_type = 0
    
def init_sprites():
    #class inits
    player.rect.x = 400 # player x start value
    player.rect.y = 430 # player y start value
    player.movex = 0
    player.movey = 0
    enemy.rect.x = 0 # enemy x start value
    enemy.rect.y = 430 # enemy y start value
    lakitu.rect.x = 0 # start lakitu from left side
    lakitu.rect.y = 150
    egg.rect.x = 200
    egg.rect.y = 200
    koopa.rect.x = 500
    koopa.rect.y = 320
    laser.rect.x = 320
    laser.rect.y = 0
    bulletbill.rect.x = 760 # bullet bill x start value
    bulletbill.rect.y = 370 # bullet bill y start value
    bullet.rect.x = 730 # bullet x start value
    bullet.rect.y = 380 # bullet y start value
    health.rect.x = 500 # health bar x value
    health.rect.y = 50 # health bar y value
    powerup.rect.x = random.randint(100, 400)
    powerup.rect.y = 420
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
    bulletbill_list.draw(screen)
    bullet_list.draw(screen)
    lakitu_list.draw(screen)
    egg_list.draw(screen)
    koopa_list.draw(screen)
    laser_list.draw(screen)
    dash_update()
    pygame.display.update() # change the display screen

def start():    
    game_intro()
    #initialize everything
    revert()
    #run game loop
    game_loop()

#global variables here
global factor #scaling player and enemy
global factor2 #scaling background 
global factor3 #scaling background
global factor4 #scaling bullet bill
global factor5 #scaling bullet
global ani #animation frames
global enemy_lr #enemy move pixels
global enemy_move # check if enemy needs to change speed
global bullet_lr
global bullet_move
global lakitu_lr
global lakitu_move
global lakitu_dir
global egg_lr
global egg_show
global koopa_move
global koopa_type
global koopa_cnt
global game_over #check if the game is over
global dash_amount # dash amount
global isjump # is the player jumping
global isdash # is the player dashing
global jump_start # set jump height
global jumpcount # what part of the jump is the player at
global dash_cnt # is the player dashing
global pixel_lr # player move speed
global dash_lr # dash speed
global pixel_u # jump adjustment factor
global times  # delete this lol
global dash_dir # True is left, False is right
global invincible # invincibility frames
global invincible_cnt
global powerup_type

init_variables() #after global definition

#inits ONLY ONCE
fps = 40
screensize = (800, 500)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("Super Mugman Mario Knight")
#init pygame clock
clock = pygame.time.Clock()
#all sounds init(wav files)
crash_sound = pygame.mixer.Sound("crash.wav")
#create sprites
enemy = Enemy()
lakitu = Lakitu()
egg = Egg()
koopa = Koopa()
laser = Laser()
bulletbill = BulletBill()
bullet = Bullet()
player = Player()
background = Background()
health = Health()
powerup = Powerup()

init_sprites() #after sprite creation

#initialize all lists as empty lists
player_list = pygame.sprite.Group() 
enemy_list = pygame.sprite.Group()
background_list = pygame.sprite.Group()
health_list = pygame.sprite.Group()
bulletbill_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
lakitu_list = pygame.sprite.Group()
egg_list = pygame.sprite.Group()
koopa_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()
# add sprites to corresponding lists
background_list.add(background)
player_list.add(player)
enemy_list.add(enemy)
health_list.add(health)
bulletbill_list.add(bulletbill)
bullet_list.add(bullet)
lakitu_list.add(lakitu)
egg_list.add(egg)
koopa_list.add(koopa) 
laser_list.add(laser)
powerup_list.add(powerup)

#start game 
start()
