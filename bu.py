import pygame 
import random
from os import path


img_dir=path.join(path.dirname(__file__),'sprites')
WIDTH = 600
HEIGHT = 1200
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80,50))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedy = 0
        self.speedx = 0
    

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_LEFT] or keypress[pygame.K_a]:
            self.speedx = -8
        if keypress[pygame.K_RIGHT] or keypress[pygame.K_d]:
            self.speedx = 8
        if keypress[pygame.K_DOWN] or keypress[pygame.K_s]:
            self.speedy = 5
        if keypress[pygame.K_UP] or keypress[pygame.K_w]:
            self.speedy = -5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(10,20))
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img,  (30, 40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(15, 20)
        self.speedx = random.randrange(-3, 3)

    def shoot(self):
        mob_bullet=MobBullet(self.rect.centerx,self.rect.top)
        all_sprites.add(mob_bullet)
        mob_bullets.add(mob_bullet)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(15, 20)
        


class MobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(mobbullet_img,(35,40))
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-5

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

class BigMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bigmob_img, (80, 80))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)
        self.speedy = random.randrange(5, 7)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -150)
            self.speedy = random.randrange(10, 20)

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_img, (250, 150))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)
        self.speedy = random.randrange(1, 2)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = (-250, -150)
            self.speedy = random.randrange(1, 2)



#load game img
player_img=pygame.image.load(path.join(img_dir, 'p1.png')).convert_alpha ()
bullet_img=pygame.image.load(path.join(img_dir, 'b1.png')).convert_alpha ()
mobbullet_img=pygame.image.load(path.join(img_dir, 'bm1.png')).convert_alpha ()
mob_img=pygame.image.load(path.join(img_dir, 'mob.png')).convert_alpha ()
bigmob_img=pygame.image.load(path.join(img_dir, 'bigmob.png')).convert_alpha ()
boss_img=pygame.image.load(path.join(img_dir, 'boss.png')).convert_alpha ()

all_sprites = pygame.sprite.Group()
bullets=pygame.sprite.Group()
mob_bullets=pygame.sprite.Group()
mobs = pygame.sprite.Group()
bigmobs=pygame.sprite.Group()
boss=pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
for i in range (4):
    bm=BigMob()
    all_sprites.add(bm)
    bigmobs.add(bm)
for i in range (1):
    b=Boss()
    all_sprites.add(b)
    boss.add(b)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.QUIT:
            running = False
    for mob in mobs:
        adj_odds=int(500*1/30)
        if random.randrange(adj_odds)==0:
            mob_bullets.angle=-45
            mob.shoot()
    # Update
    all_sprites.update()
    #check if mob collided with bullet
    mobhits=pygame.sprite.groupcollide(mobs, bullets, True, True)
    for mobhit in mobhits:
        m=Mob()
        all_sprites.add(m)
        mobs.add(m)
    bigmobhits=pygame.sprite.groupcollide(bigmobs, bullets, True, True)
    for bigmobhit in bigmobhits:
        bm=BigMob()
        all_sprites.add(bm)
        bigmobs.add(bm)
    bosshits=pygame.sprite.groupcollide(boss, bullets, True, True)
    for bosshit in bosshits:
        b=Boss()
        all_sprites.add(b)
        boss.add(b)
    
    #check for collisions
    mobhits=pygame.sprite.spritecollide(player, mobs, False)
    if mobhits:
        running=False
    bigmobhits=pygame.sprite.spritecollide(player, bigmobs, False)
    if bigmobhits:
        running=False
    bosshits=pygame.sprite.spritecollide(player, boss, False)
    if bosshits:
        running=False


    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()