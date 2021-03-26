import pygame 
import random
import math
from pygame import mixer
from os import path


img_dir=path.join(path.dirname(__file__),'sprites')
sound_dir=path.join(path.dirname(__file__),'sounds')

WIDTH = 600
HEIGHT = 1200
FPS = 35 
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Neon Dreams.mp3')
pygame.music.play(-1)
pygame.music.set_volume(0.5)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()


def draw_text(surf, text, size, x, y):
    font_name=pygame.font.match_font('8-BIT WONDER.ttf')
    font= pygame.font.Font(font_name, size)
    text_surface= font.render(text, False, WHITE) #True is for anti-aliased, False is for aliased
    text_rect= text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70,60))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedy = 0
        self.speedx = 0
        self.radius=25
    

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
        player_shoot.play()


    def bomb(self):
        pass

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

class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pass

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (50, 60))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -40)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(5, 10)
        self.radius=20

    def shoot(self):
        mob_bullet=MobBullet(self.rect.centerx,self.rect.bottom)
        all_sprites.add(mob_bullet)
        mob_bullets.add(mob_bullet)
        mob_shoot.play()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, 90)
            self.speedy = random.randrange(5, 10)


class MobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(mobbullet_img,(35,40))
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= 10
        self.radius=10

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

class BigMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bigmob_img, (125, 125))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)
        self.speedy = random.randrange(4, 5)
        self.radius=45

    def shoot(self):
        bigmob_bullet=BigMobBullet(self.rect.centerx,self.rect.bottom)
        all_sprites.add(bigmob_bullet)
        bigmob_bullets.add(bigmob_bullet)
        bigmob_shoot.play()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -150)
            self.speedy = random.randrange(4, 5)

class BigMobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bigmob_bullet_img,(40,15))
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= 6

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

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



#load music
#mysound = pygame.mixer.Sound("mysound.wav")
#mysound.set_volume(0.5)
bg_music=pygame.mixer.Music.load(path.join(sound_dir, 'Neon Dreams.mp3'))

player_shoot=pygame.mixer.Sound(path.join(sound_dir, 'player shoot.wav'))
mob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'mob shoot.wav'))
bigmob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'bigmob shoot.wav'))

player_kill=pygame.mixer.Sound(path.join(sound_dir, 'player kill.wav'))
mob_kill=pygame.mixer.Sound(path.join(sound_dir, 'mob kill.wav'))
bigmob_kill=pygame.mixer.Sound(path.join(sound_dir, 'bigmob kill.wav'))


#load game img
player_img=pygame.image.load(path.join(img_dir, 'p1.png')).convert_alpha ()
bullet_img=pygame.image.load(path.join(img_dir, 'b1.png')).convert_alpha ()
mobbullet_img=pygame.image.load(path.join(img_dir, 'bm1.png')).convert_alpha ()
bigmob_bullet_img=pygame.image.load(path.join(img_dir, 'bm2.png')).convert_alpha ()
mob_img=pygame.image.load(path.join(img_dir, 'mob.png')).convert_alpha ()
bigmob_img=pygame.image.load(path.join(img_dir, 'bigmob.png')).convert_alpha ()
boss_img=pygame.image.load(path.join(img_dir, 'boss.png')).convert_alpha ()

all_sprites = pygame.sprite.Group()
bullets=pygame.sprite.Group()
mob_bullets=pygame.sprite.Group()
bigmob_bullets=pygame.sprite.Group()
mobs = pygame.sprite.Group()
bigmobs=pygame.sprite.Group()
boss=pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
for i in range (2):
    bm=BigMob()
    all_sprites.add(bm)
    bigmobs.add(bm)
for i in range (1):
    b=Boss()
    all_sprites.add(b)
    boss.add(b)

score=0

# Game loop
running = True
while running:
    # keep loop running at the right speed
    bg_music.play(-1)
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.QUIT:
            running = False
    #make mobs shoot + player and bullets collide
    for mob in mobs:
        adj_odds=int(250*2/15)
        if random.randrange(adj_odds)==0:
            mob.shoot()                                                    #improved circular collision
    mob_bullet_hits=pygame.sprite.spritecollide(player,mob_bullets, True, pygame.sprite.collide_circle)
    if mob_bullet_hits:
        running=False
    
    for bigmob in bigmobs:
        adj_odds=int(50*1/10)
        if random.randrange(adj_odds)==0:
            bigmob.shoot()       
    bigmob_bullet_hits=pygame.sprite.spritecollide(player,bigmob_bullets, True,)
    if bigmob_bullet_hits:
        running=False
    

    # Update
    all_sprites.update()
    #check if mob collided with bullet
    mobhits=pygame.sprite.groupcollide(mobs, bullets, True, True)
    for mobhit in mobhits:
        mob_kill.play()
        score+=100
        print ('score=',score )
        m=Mob()
        all_sprites.add(m)
        mobs.add(m)
    bigmobhits=pygame.sprite.groupcollide(bigmobs, bullets, True, True)
    for bigmobhit in bigmobhits:
        bigmob_kill.play()
        score+=750
        bm=BigMob()
        all_sprites.add(bm)
        bigmobs.add(bm)
    bosshits=pygame.sprite.groupcollide(boss, bullets, True, True)
    for bosshit in bosshits:
        score+=1500
        b=Boss()
        all_sprites.add(b)
        boss.add(b)
    
    #check for collisions
    mobhits=pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if mobhits:
        running=False
    bigmobhits=pygame.sprite.spritecollide(player, bigmobs, False, pygame.sprite.collide_circle)
    if bigmobhits:
        running=False
    bosshits=pygame.sprite.spritecollide(player, boss, False)
    if bosshits:
        running=False
    #coolide mobs and kill if they get too close to each other

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    draw_text(screen, str(score), 50, WIDTH/2,50)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
  