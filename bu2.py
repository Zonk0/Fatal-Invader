from itertools import repeat
import pygame 
import random
import math
import sys
from pygame import mixer
from os import path

from pygame.constants import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE


img_dir=path.join(path.dirname(__file__),'sprites')
sound_dir=path.join(path.dirname(__file__),'sounds')
exp_dir=path.join(path.dirname(__file__),'sprites/explos')


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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()
BUFF_TIME=10000

def draw_text(surf, text, size, x, y):
    font_name=pygame.font.match_font('8-BIT WONDER.ttf')
    font= pygame.font.Font(font_name, size)
    text_surface= font.render(text, False, WHITE) #True is for anti-aliased, False is for aliased
    text_rect= text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)

def draw_health(surf,x,y,health,img):
    for i in range(health):
        img_rect=img.get_rect()
        img_rect.x= x+40*i
        img_rect.y= y
        surf.blit(img, img_rect)

def draw_bombs(surf,x,y,bomb,img):
    for i in range(bomb):
        img_rect=img.get_rect()
        img_rect.x= x+40*i
        img_rect.y= y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70,60))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100
        self.speedy = 0
        self.speedx = 0
        self.radius=25
        self.health=5
        self.shoot_delay=100
        self.last_shot=pygame.time.get_ticks()
        self.buff=1
        self.buff_time=pygame.time.get_ticks()
        self.shield=0
        self.bomb=0 

    def update(self):
        if self.buff>=2 and pygame.time.get_ticks()-self.buff_time>BUFF_TIME:
            self.buff-=1
            self.buff_time=pygame.time.get_ticks()
        if self.buff>=3 and pygame.time.get_ticks()-self.buff_time>BUFF_TIME:
            self.buff-=1
            self.buff_time=pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 0
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_SPACE]:
            self.shoot()
        if keypress[pygame.K_LEFT] or keypress[pygame.K_a]:
            self.speedx = -10
        if keypress[pygame.K_RIGHT] or keypress[pygame.K_d]:
            self.speedx = 10
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

    def gunbuff(self):
        self.buff+=1
        self.buff_time=pygame.time.get_ticks()

    def shoot(self):
        state=pygame.time.get_ticks()
        if state-self.last_shot>self.shoot_delay:
            self.last_shot=state
            if self.buff==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                player_shoot.play()
            if self.buff==2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                player_shoot.play()
            if self.buff>=3:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                bullet3=Bullet(self.rect.centerx,self.rect.top)
                bullet1.speedy=-20
                bullet2.speedy=-20
                bullet3.speedy=-20
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                player_shoot.play()

    def pbomb(self): #make it stop adding if limit is 5
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

class Buff(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['shield','doublegun','bomb'])
        self.image=buff_imgs[self.type]
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.center= center
        self.speedy=3

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
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
        self.health=2

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
        self.health=5

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
        self.radius=20

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
        self.health=50

    def shoot(self):
        boss_bullet=BossBullet(self.rect.centerx,self.rect.bottom)
        all_sprites.add(boss_bullet)
        boss_bullets.add(boss_bullet)
        #boss_shoot.play()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = (-250, -150) #bug? (invalid rect assigment)
            self.speedy = random.randrange(1, 2)

class BossBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2 , HEIGHT / 2)
        self.angle = angle
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedx = 5
        self.speedy = 5

    def update(self):
        self.rect.x += self.speedx * math.cos(math.radians(self.angle)) 
        self.rect.y += self.speedy * math.sin(math.radians(self.angle))
        if self.rect.bottom<0:
            self.kill()


################################################################################################

class Explosion(pygame.sprite.Sprite): 
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 25 
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: 
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 


explosion_anim = {}
explosion_anim['lg'] = []
for i in range(15): 
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(exp_dir,filename)).convert_alpha()
    img_lg=pygame.transform.scale(img, (100,100))
    explosion_anim['lg'].append(img_lg)
    

#load music
#mysound = pygame.mixer.Sound("mysound.wav")
#mysound.set_volume(0.5)
pygame.mixer.music.load(path.join(sound_dir, 'Neon Dreams.mp3'))
pygame.mixer.music.set_volume(0.1)
player_shoot=pygame.mixer.Sound(path.join(sound_dir, 'player shoot.wav'))
player_shoot.set_volume(0.2)
mob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'mob shoot.wav'))
mob_shoot.set_volume(0.2)
bigmob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'bigmob shoot.wav'))
bigmob_shoot.set_volume(0.2)

player_kill=pygame.mixer.Sound(path.join(sound_dir, 'player kill.wav'))
player_kill.set_volume(0.2)
mob_kill=pygame.mixer.Sound(path.join(sound_dir, 'mob kill.wav'))
mob_kill.set_volume(0.2)
bigmob_kill=pygame.mixer.Sound(path.join(sound_dir, 'bigmob kill.wav'))
bigmob_kill.set_volume(0.2)


#load game img
bg_img=pygame.image.load(path.join(img_dir, 'bg_1.png')) #EDUARDO JOAO
bg_img_rect=bg_img.get_rect()

buff_imgs= {}
buff_imgs['shield']=pygame.image.load(path.join(img_dir, 'shield.png')).convert_alpha()
buff_imgs['doublegun']=pygame.image.load(path.join(img_dir, 'power1.png')).convert_alpha()
buff_imgs['bomb']=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()
bigshield_img=pygame.image.load(path.join(img_dir,'shield1.png')).convert_alpha()

player_img=pygame.image.load(path.join(img_dir, 'p1.png')).convert_alpha ()
player_health=pygame.image.load(path.join(img_dir, 'player_health.png')).convert_alpha()
p_h=pygame.transform.scale(player_health, (50,50))
player_bomb=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()
p_b=pygame.transform.scale(player_bomb, (30,30))

bullet_img=pygame.image.load(path.join(img_dir, 'b1.png')).convert_alpha ()
mobbullet_img=pygame.image.load(path.join(img_dir, 'bm1.png')).convert_alpha ()
bigmob_bullet_img=pygame.image.load(path.join(img_dir, 'bm2.png')).convert_alpha ()
mob_img=pygame.image.load(path.join(img_dir, 'mob.png')).convert_alpha ()
bigmob_img=pygame.image.load(path.join(img_dir, 'bigmob.png')).convert_alpha ()
boss_img=pygame.image.load(path.join(img_dir, 'boss.png')).convert_alpha ()



######################################################################################



#shakes the screen
offset=repeat((0,0))
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

def menu():
    draw_text(screen, 'Bullet Hell', 80, WIDTH/2, HEIGHT/3)
    draw_text(screen, '<< Scores', 50, WIDTH/4.85, HEIGHT/1.5)
    draw_text(screen, 'Credits >>', 50, WIDTH/1.25, HEIGHT/1.5)
    draw_text(screen, '[ Begin ]', 70, WIDTH/2, HEIGHT/1.25)
    pygame.display.flip()
    wait=True
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    credits()
                if event.key==K_SPACE:
                    wait=False
                if event.key==K_LEFT:
                    scores()
                if event.key==K_ESCAPE:
                    pygame.quit()
            if event.type==pygame.QUIT:
                pygame.quit()

def credits():
    screen.fill(BLACK)
    draw_text(screen, 'Credits', 80, WIDTH/2, HEIGHT/3)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==K_RIGHT:
                menu()

def scores():
    screen.fill(BLACK)
    draw_text(screen, 'Scoreboard', 80, WIDTH/2, HEIGHT/3)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==K_LEFT:
                menu()



def game_over():
    draw_text(screen, 'GAME OVER', 90, WIDTH/2, HEIGHT/2)
    pygame.display.flip()
    wait=True
    while wait:
        clock.tick(FPS)
            

#Game loop
#####################################################################################
in_menu=True
gameover=False
running = True
pygame.mixer.music.play(-1) #2 different musics maybe?
while running:
    if in_menu:
        menu()
        in_menu=False
        gameover=False
        all_sprites = pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        mob_bullets=pygame.sprite.Group()
        bigmob_bullets=pygame.sprite.Group()
        boss_bullets=pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bigmobs=pygame.sprite.Group()
        boss=pygame.sprite.Group()
        player = Player()
        buffs=pygame.sprite.Group()
        all_sprites.add(player)
        score=0
        for i in range(8):
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

        def mob_respawn():
            mob_kill.play()
            print ('score=',score )
            m=Mob()
            all_sprites.add(m)
            mobs.add(m)

        def bigmob_respawn():
            bigmob_kill.play()
            bm=BigMob()
            all_sprites.add(bm)
            bigmobs.add(bm)

        def boss_respawn():
            b=Boss()
            all_sprites.add(b)
            boss.add(b)

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    #make mobs shoot + player and bullets collide
    for mob in mobs:
        adj_odds=int(250*2/15)
        if random.randrange(adj_odds)==0:
            mob.shoot()                                                    #improved circular collision
    mob_bullet_hits=pygame.sprite.spritecollide(player,mob_bullets, True, pygame.sprite.collide_circle)
    for mob_bullet_hit in mob_bullet_hits:
        offset=shake()
        expl=Explosion(mob_bullet_hit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        player.health-=1
        if player.health<=0:
            running=False
    #bullet frequency
    for bigmob in bigmobs:
        adj_odds=int(100*1/5)
        if random.randrange(adj_odds)==0:
            bigmob.shoot()       
    bigmob_bullet_hits=pygame.sprite.spritecollide(player,bigmob_bullets, True,pygame.sprite.collide_circle)
    for bigmob_bullet_hit in bigmob_bullet_hits:
        offset=shake()
        expl=Explosion(bigmob_bullet_hit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        player.health-=1
        if player.health<=0:
            gameover=True

    for bosses in boss:
        for x in range(12):
            angle = 30
            boss_bullets.add(BossBullet, boss.rect.centerx, boss.rect.bottom(angle))
        



    # Update
    all_sprites.update()

    #check if player hit a buff and apply it
    buffhits=pygame.sprite.spritecollide(player, buffs, True)
    for buffhit in buffhits:
        if buffhit.type=='shield':
            player.shield+=4
        if buffhit.type=='doublegun':
            player.gunbuff()
        if buffhit.type=='bomb':
            player.bomb+=1
            if player.bomb>=5:
                player.bomb=5

    #check if mob collided with bullet
    mobhits=pygame.sprite.groupcollide(mobs, bullets, True, True)
    for mobhit in mobhits:
        expl=Explosion(mobhit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        score+=100
        mob_respawn()
    bigmobhits=pygame.sprite.groupcollide(bigmobs, bullets, False, True)
    for bigmobhit in bigmobhits:
        bigmobhit.health-=1
        if bigmobhit.health<=0:
            expl=Explosion(bigmobhit.rect.center, 'lg') #animation
            all_sprites.add(expl)
            bigmobhit.kill()
            score+=750
            if random.random()>0.50:
                buff=Buff(bigmobhit.rect.center)
                all_sprites.add(buff)
                buffs.add(buff)
            bigmob_respawn()
    bosshits=pygame.sprite.groupcollide(boss, bullets, True, True)
    for bosshit in bosshits:
        score+=1500 
        boss_respawn()    
    #check for collisions
    mobhits=pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for mobhit in mobhits:
        expl=Explosion(mobhit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        offset=shake()
        player.health-=1
        if player.health<=0:
            running=False
    bigmobhits=pygame.sprite.spritecollide(player, bigmobs, True, pygame.sprite.collide_circle)
    for bigmobhit in bigmobhits:
        expl=Explosion(bigmobhit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        offset=shake()
        player.health-=1
        if player.health<=0:
            running=False
    bosshits=pygame.sprite.spritecollide(player, boss, False)
    if bosshits:
        running=False

    #coolide mobs and kill if they get too close to each other
    if player.health<=0:
        gameover=True
        in_menu=False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(bg_img, next(offset))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    draw_health(screen, WIDTH-250, 1150, player.health, p_h)
    draw_bombs(screen, WIDTH-550, 1150, player.bomb, p_b)
    draw_text(screen, str(score), 50, WIDTH/2,50)
    screen.blit(screen, next(offset))
    pygame.display.flip() 

pygame.quit()
    