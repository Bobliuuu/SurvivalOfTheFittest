import pygame, time

WHITE = (255, 255, 255)
pygame.init()
clock = pygame.time.Clock()
screensize = (800, 500)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("My Game")
screen.fill(WHITE)

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
    def kill(self):
        self.image = self.images[2]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor3
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor3*self.rect.width), (int)(factor3*self.rect.height))) 
        self.rect.center = center # find center
    def start(self):
        self.image = self.images[0]
        self.rect = self.image.get_rect() # get rect
        #scaling
        global factor2
        center = self.rect.center # find center
        # scale down sprite and cast to int to scale properly 
        self.image = pygame.transform.scale(self.image, ((int)(factor2*self.rect.width), (int)(factor2*self.rect.height))) 
        self.rect.center = center # find center

global factor2, factor3
factor2 = 0.5
factor3 = 0.7

health = Background()
health_list = pygame.sprite.Group()
health_list.add(health)

health.rect.x = 500 # health bar x value
health.rect.y = 50 # health bar y value

health.start()
print("start")

while True:
    print("loop")
    screen.fill(WHITE)
    health.start()
    health_list.draw(screen)
    pygame.display.update()
    while True:
        num = int(input("give me the number or else: "))
        if num == 1:
            print("clear")
            screen.fill(WHITE)
            health.kill()
            health_list.draw(screen)
            pygame.display.update()
            while True:
                num = int(input("give me the number or else: "))
                if num == 2:
                    print("fill")
                    break
            if num == 2:
                break
        else:
            pygame.quit()
