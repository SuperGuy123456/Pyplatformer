import pygame, sys, random
pygame.init()


# RGB Red Green Blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)

X = 900
Y = 600
screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)
pygame.display.set_caption("PyPlatformer")
LOGO=pygame.image.load('FullPortal.png').convert()
pygame.display.set_icon(LOGO)
clock = pygame.time.Clock()
acc = 1
TotalC=0
TargetC=3
stop=False
class Coins:
    def __init__(self,x,y):
        self.Coin=pygame.image.load('coin.png')
        self.Coin=pygame.transform.scale(self.Coin,(20,20))
        self.rect=self.Coin.get_rect(bottomleft=(x,y))
        self.draw=True
    def Draw(self):
        if self.draw:
            screen.blit(self.Coin,self.rect)
        font=pygame.font.Font('freesansbold.ttf',20)
        CCoins=font.render('Coins x '+str(TotalC),BLACK,WHITE)
        TCoins=font.render('RQD Coins x '+str(TargetC),BLACK,WHITE)
        screen.blit(CCoins,(125,20))
        screen.blit(TCoins,(250,20))
    def Detect(self):
        global TotalC,stop
        YN=self.rect.colliderect(player.rect)
        if YN:
            self.draw=False
            self.rect=self.Coin.get_rect(bottomleft=(100000,100000))
            TotalC+=1
        if TotalC==TargetC:
            stop=True
class Rocks:
    def __init__(self,x,y):
        self.Rock=pygame.image.load('rock.png')
        self.Rock=pygame.transform.scale(self.Rock,(15,15))
        self.rect=self.Rock.get_rect(midbottom=(x,y-15))
    def Draw(self):
        screen.blit(self.Rock,self.rect)
    def Detect(self):
        global run
        if player.rect.colliderect(self.rect):
            player.lives -= 1
            player.rect.midbottom = (X//2, Y - 100)
        if player.lives == 0:
            run=False
class Rover:
    def __init__(self,x,y,maxX,minX,Default,num):
        self.x=x
        self.y=y
        self.num=num
        self.max=maxX
        self.min=minX
        self.surf=pygame.image.load('Drone.png')
        self.surf=pygame.transform.scale(self.surf,(50,20))
        self.rect=self.surf.get_rect(midbottom=(self.x,self.y-20))
        self.Direction=True
    def Move(self):
        if self.x>self.max:
            self.x-=5
        elif self.x<self.min:
            self.x+=self.num
            
    def Draw(self):
        self.rect=self.surf.get_rect(midbottom=(self.x,self.y-20))
        screen.blit(self.surf,self.rect)
    def Detect(self):
        global run
        if player.rect.colliderect(self.rect):
            player.lives -= 1
            player.rect.midbottom = (X//2, Y - 100)
        if player.lives == 0:
            run=False
class Platform():
    def __init__(self, sizex, sizey, posx, posy,color):
        self.surf = pygame.Rect(sizex, sizey, posx, posy) 
        self.surf = pygame.surface.Surface((sizex, sizey))
        self.rect = self.surf.get_rect(midbottom=(posx, posy))
        self.surf.fill(color)
        

    def draw(self):
        screen.blit(self.surf, self.rect)

class Player():
    def __init__(self):
        self.jump = False
        self.left = False
        self.right = False
        self.lives = 5
        self.heart = pygame.image.load('Heart.png')
        self.heart = pygame.transform.scale(self.heart, (20,20))
        self.surf1 = pygame.image.load('player.png')
        self.surf1 = pygame.transform.scale(self.surf1, (30,40))
        self.surf2 = self.surf1
        self.surf2=pygame.transform.flip(self.surf2,True,False)
        self.images=[self.surf1,self.surf2]
        self.index=0
        self.rect = self.surf1.get_rect(midbottom=(X//2, Y - 100))
        self.y_speed = 0

    def event(self):
        global run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.on_ground():
                    self.jump = True

        self.left = False
        self.right = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left = True
            self.index=1
        if keys[pygame.K_RIGHT]:
            self.right = True
            self.index=0

    def move(self):
        if self.jump:
            self.y_speed = -18
            self.jump = False
        self.rect.bottom += self.y_speed

        if self.left and self.rect.left > 0:
            self.rect.centerx -= 5
        if self.right and self.rect.right < X:
            self.rect.centerx += 5

        if self.on_ground():
            if self.y_speed >= 0:
                self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
                self.y_speed = 0
            else:
                self.rect.top = p_rects[self.rect.collidelist(p_rects)].bottom
                self.y_speed = 2
        else:
            self.y_speed += acc

    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1 :
            return True
        else:
            return False

    def draw(self):
        screen.blit(self.images[self.index], self.rect)
        for i in range(self.lives):
            screen.blit(self.heart, [i*20 + 20, 20])


class Enemy():
    def __init__(self,x,y):
        self.chosen=False
        self.surf1 = pygame.image.load('Drone.png')
        self.surf1 = pygame.transform.scale(self.surf1, (50,20))
        self.surf2=self.surf1
        self.surf2=pygame.transform.flip(self.surf2,True,False)
        self.images=[self.surf1,self.surf2]
        self.index=0
        self.rect = self.images[self.index].get_rect(midbottom=(x,y))
        self.x_speed = random.randint(3, 7)
        self.y_speed = 0
        self.timer = False

    def move(self):
        self.rect.centerx += self.x_speed
        if self.rect.left <= 0 or self.rect.right >= X:
            self.x_speed *= -1
            self.index=1
            self.chosen=True
        elif self.chosen==False:
            self.index=0
        if self.on_ground():
            self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
            self.y_speed = 0
        else:
            self.y_speed += acc
        self.rect.bottom += self.y_speed
        screenrect=screen.get_rect()
        self.hit()
        self.chose=False
    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False

    def hit(self):
        global run
        if player.rect.colliderect(self.rect):
            player.lives -= 1
            player.rect.midbottom = (X//2, Y - 100)
        if player.lives == 0:
            run=False

    def draw(self):
        screen.blit(self.images[self.index], self.rect)
class Portal:
    def __init__(self,x,y):
        Broken=pygame.image.load('BrokenPortal.png')
        Full=pygame.image.load('FullPortal.png')
        Broken=pygame.transform.scale(Broken,(50,50))
        Full=pygame.transform.scale(Full,(50,50))
        self.images=[Broken,Full]
        self.index=0
        self.rect=self.images[self.index].get_rect(midbottom=(x,y-20))
    def Check(self):
        if stop:
            self.index=1
    def Draw(self):
        screen.blit(self.images[self.index],self.rect)
    def Detect(self):
        global run
        if stop:
            if self.rect.colliderect(player.rect):
                screen.fill(BLACK)
                font=pygame.font.Font('freesansbold.ttf',75)
                End=font.render('You Won!',BLACK,WHITE)
                screen.blit(End,(0,0))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        run=False
                
run=True
platforms = []
platforms.append(Platform(X, 100, 450, Y, GREEN))
platforms.append(Platform(200, 15, 500, Y-180, GREEN))
platforms.append(Platform(300, 15, 200, 340, GREEN))
platforms.append(Platform(250, 15, 480, 260, GREEN))
platforms.append(Platform(300, 15, 150, 180, GREEN))
platforms.append(Platform(300, 15, 500, 100, GREEN))
platforms.append(Platform(80, 15, 830, 260, GREEN))
#Yes
platforms.append(Platform(80, 15, 650, 340, GREEN))

coins=[]
coins.append(Coins(100,300))
coins.append(Coins(400,230))
coins.append(Coins(200,75))

rocks=[]
rocks.append(Rocks(250,340))
rocks.append(Rocks(100,340))
rocks.append(Rocks(480,260))
rocks.append(Rocks(460,260))
rocks.append(Rocks(360,260))

rovers=[]
rovers.append(Rover(150,180,0,300,True,300))

c_rects=[c.rect for c in coins]
p_rects = [p.rect for p in platforms]

player = Player()

enemys=[]
enemys.append(Enemy(100,15))
enemys.append(Enemy(400,15))
enemys.append(Enemy(200,15))

portals=[Portal(500,520)]

while run:
    clock.tick(30)
    screen.fill(BLACK)

    player.event()
    player.move()
    player.draw()
    for p in platforms:
        p.draw()
    for c in coins:
        c.Draw()
        c.Detect()
    for r in rocks:
        r.Draw()
        r.Detect()
    for rover in rovers:
        rover.Draw()
        rover.Move()
        rover.Detect()
    for enemy in enemys:
        enemy.move()
        enemy.draw()
    for portal in portals:
        portal.Check()
        portal.Draw()
        portal.Detect()

    pygame.display.flip()


pygame.quit()
