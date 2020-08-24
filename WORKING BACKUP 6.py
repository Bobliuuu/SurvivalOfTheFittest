import pygame, random, time, math, turtle

pygame.init() #initialize pygame functions

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
init only happens once, but update happens every loop iteration]
revert detects collision
"""

#flip the image when going left
#go up down
#use gravity to control character

"""
#textpox for displaying text
class TextBox:
    #Constructor
    def __init__(self, x, y, w, h, fontSize=24, maxLength=100, resizable=True, text='', textColor=(0,0,0), borderColor=(40,120,180), activeBorderColor=(200,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = borderColor
        self.inactiveColor = borderColor
        self.textColor = textColor
        self.activeColor = activeBorderColor
        self.maxLength = maxLength
        self.resizable = resizable
        self.text = text
        self.fontSize = fontSize
        FONT = pygame.font.Font(None, self.fontSize)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Detects when the user clicks on the textbox
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    self.color = self.activeColor
                else:
                    self.active = False
                    self.color = self.inactiveColor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    #Clear text box
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    #Remove last character
                    self.text = self.text[:-1]
                elif event.key in [pygame.K_TAB,pygame.K_ESCAPE]:
                    #Ignore = do nothing
                    pass
                else:
                    #Append character
                    if len(self.text) < self.maxLength:
                        self.text += event.type
                #Display text
                FONT = pygame.font.Font(None, self.fontSize)
                self.txt_surface = FONT.render(self.text, True, self.textColor)
    def update(self):
        # Resize the box if the text is too long.
        if self.resizable:
            width = max(200, self.txt_surface.get_width()+10)
            self.rect.w = width
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
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
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor2*self.rect.width), (int)(factor2*self.rect.height))) 
        self.rect.center = center # find center
    def kill(self):
        screen.fill(WHITE)
        self.image = self.images[2]
        #scaling
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor3*self.rect.width), (int)(factor3*self.rect.height))) 
        self.rect.center = center # find center
    def revert(self):
        screen.fill(WHITE)
        self.image = self.images[0]
        #scaling
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
        self.image = self.images[self.frame]
        if self.frame == 5:
            game_over = True

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
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
        #movement
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
        #Check x boundaries --> only moves left and right
        if self.rect.x > 750:
            self.rect.x = 0
            enemy_lr = random.randint(3, 7)
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
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
    def revert(self):
        self.rect.x = 0
        # advance animation frames
        self.frame += 1
        if self.frame >= 2*ani: # number of frames * ani
            self.frame = 0
        self.image = self.images[(self.frame//ani)]
        #scaling
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
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center

    #player movement: use += so x movement doesn't affect y movement and vice versa
    def Dir(self):
        return self.movex >= 0
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
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly
        self.image = pygame.transform.scale(self.image, ((int)(factor*self.rect.width), (int)(factor*self.rect.height))) # scale down sprite
        self.rect.center = center # replace center
        #decrement health
        self.health -= 1

def collided(sprite, other):
    """Check if the hitboxes of the two sprites collide."""
    return sprite.hitbox.colliderect(other.hitbox)

def dash_update():
    font = pygame.font.Font(None, 36)
    text = font.render("Dashes: " + str(dashes), 1, (10, 10, 10))
    screen.blit(text, (50,50))

def gameover():
    background.kill()
    health_list.draw(screen)
    background_list.draw(screen)
    pygame.display.flip() # change the display screen
    while True:
        ask = input("Do you want to play again? (y/n): ")
        if ask == "n":
            print("Ok. Goodbye.")
            return False
        elif ask == "y":
            return True
        else:
            print("Invalid operation.")

def reset():
    background.revert()

def game_loop():
    global isjump, isdash, enemy_move, jumpcount, dash_amount, dash_cnt
    done = False
    while not done:
        #dash_update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.control(-pixel_lr, 0) # move left
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.control(pixel_lr, 0) # move right
                if (event.key == pygame.K_UP or event.key == ord('w'))and not isjump:
                    isjump = True
                if event.key == ord('q') and not isdash and dash_amount >= 0:
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
            enemy.control(enemy_lr, 0)
            enemy_move = False
        screen.fill(BLACK)
        #only update player and enemy
        cnt = player.update()
        enemy.update()
        enemy_hit_list = []
        enemy_hit_list = pygame.sprite.spritecollide(player, enemy_list, False, collided) # checks for player and enemy hitboxes
        if not len(enemy_hit_list) == 0:
            player.revert()
            enemy.revert()
            health.revert()
            if game_over == True:
                if gameover() == False:
                    pygame.quit()
                    break
                else:
                    reset()
                    game_loop()
        background_list.draw(screen)
        player_list.draw(screen) #draw everything to the screen
        enemy_list.draw(screen)
        health_list.draw(screen)
        pygame.display.flip() # change the display screen
        clock.tick(fps) #limit # of frames
    pygame.quit()

#global variables here
global factor #scaling player and enemy
factor = 0.6
global factor2 #scaling background
factor2 = 0.5
global factor3
factor3 = 0.43
global ani #animation frames
ani = 7
global enemy_lr #enemy move pixels
enemy_lr = random.randint(3, 7)
global enemy_move # check if enemy needs to change speed
enemy_move = True
global game_over #check if the game is over
game_over = False
global dash_amount # dash amount
dash_amount = 5
global isjump # is the player jumping
isjump = False
global isdash # is the player dashing
isdash = False
global jump_start # set jump height
jump_start = 12
global jumpcount # what part of the jump is the player at
jumpcount = jump_start
global dash_cnt # is the player dashing
dash_cnt = 0

#simple inits
fps = 40
screensize = (800, 500)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

enemy = Enemy()
player = Player()
background = Background()
health = Health()
player.rect.x = 200 # player x start value
player.rect.y = 430 # player y start value
enemy.rect.x = 0 # enemy x start value
enemy.rect.y = 430 # enemy y start value
health.rect.x = 500 # health bar x value
health.rect.y = 50 # health bar y value
enemy.cnt = 0 #animation slowdown for enemy
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
pixel_lr = 5 # player move speed
dash_lr = 6 * pixel_lr
pixel_u = 1 # jump adjustment factor
times = 0
dash_dir = True # True is left, False is right

game_loop()
