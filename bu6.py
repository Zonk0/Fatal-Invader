from itertools import repeat
import pygame 
import random
import math
import sys
import pickle
import csv
from pygame import mixer
from os import path

from pygame.constants import K_BACKSPACE, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, MOUSEBUTTONDOWN


img_dir=path.join(path.dirname(__file__),'sprites')
sound_dir=path.join(path.dirname(__file__),'sounds')
exp_dir=path.join(path.dirname(__file__),'sprites/explos')
hi_dir=path.join(path.dirname(__file__))

WIDTH = 600
HEIGHT = 1000
FPS = 60 
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA=(238, 59, 255)
BBLUE=(0, 245, 255 )
YELLOW = (255, 255, 0)

pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()
BUFF_TIME=10000

def draw_text(surf, text, size, x, y, color):
    pygame.font.init()
    font_name='RetronoidItalic.ttf' #
    font= pygame.font.Font(font_name, size)
    text_surface= font.render(text, False, color) #True is for anti-aliased, False is for aliased
    text_rect= text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)

def draw_health(surf,x,y,health,img):
    for i in range(health):
        img_rect=img.get_rect()
        img_rect.x= x+40*i
        img_rect.y= y
        surf.blit(img, img_rect)

def draw_bombs(surf,x,y,bombs,img):
    for i in range(bombs):
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
        self.bombs=0
        self.bombing=False 


    def update(self):
        if self.buff>=4 and pygame.time.get_ticks()-self.buff_time>BUFF_TIME:
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
        if keypress[pygame.K_b]:
            self.bomb()
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
        global shout_count
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
            if self.buff==3:
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
                shout_count=0
            if self.buff>=4:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                bullet3 = Bullet(self.rect.centerx-10,self.rect.top)
                bullet4 = Bullet(self.rect.centerx+10,self.rect.top) 
                bullet1.speedy=-40
                bullet2.speedy=-40
                bullet3.speedy=-40
                bullet4.speedy=-40
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                player_shoot.play()
                if shout_count==0:
                    shout=Shout('overdrive',WIDTH/2,-1,15)
                    all_sprites.add(shout)
                    shout_count=1

    def bomb(self): #make it stop adding if limit is 5
        global score
        global bosses
        global offset
        if self.bombs>=5: 
            #player.play()
            self.bombing = True
            offset=shake()
            #level += 1 
            self.bombs -= 5
            if self.bombs < 0:
                self.bombs = 0 
            for mob in mobs:
                mob.kill()
                score += ((20 - mob.radius)*20)
                expl = Explosion(mob.rect.center, 'lg')
                all_sprites.add(expl)
                mob_respawn()
            for bigmob in bigmobs: 
                bigmob.kill()
                score += ((50 - bigmob.radius)*35)
                expl = Explosion(bigmob.rect.center,'lg')
                bigmob_respawn()
                all_sprites.add(expl)
            for bosshit in bosshits: 
                bosshit.health=-25
                score += ((60 - bosshit.radius)*10)
                expl = Explosion(bosshit.rect.center,'lg')
                all_sprites.add(expl)
            for mob_bullet in mob_bullets: 
                mob_bullet.kill()
                score += ((mob.radius)*5)
                expl = Explosion(mob_bullet.rect.center,'lg')
                all_sprites.add(expl)
            for bigmob_bullet in bigmob_bullets: 
                bigmob_bullet.kill()
                score += ((bigmob.radius)*5)
                expl = Explosion(mob_bullet.rect.center,'lg')
                all_sprites.add(expl)
            for boss_bullet in boss_bullets: 
                boss_bullet.kill()
                score += ((boss.radius)*5)
                expl = Explosion(boss_bullet.rect.center,'lg')
                all_sprites.add(expl)
            #if boss_flag == 1:
                #boss.health -= 500

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
        self.type=random.choice(['doublegun','bomb'])
        self.image=buff_imgs[self.type]
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.center= center
        self.speedy=3

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (50, 60))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-800, 0)
        self.speedy = 8
        self.speedx = random.randrange(-5,5) #self.rect.x * math.cos(self.speedy%5)
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
            self.speedy = 8


class MobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(mobbullet_img,(35,40))
        #self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= 12
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
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 4
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
            self.speedy = 4

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
        self.image = pygame.transform.scale(boss_img, (350, 250))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2 - self.rect.width
        self.rect.y = random.randrange(-250, -150)
        self.speedy = random.randrange(1, 2)
        self.health=50
        self.radius=90
        #self.shoot_delay = 1000 
        #self.last_shot = pygame.time.get_ticks() 

    def shoot(self):
        #now = pygame.time.get_ticks() 
        #if now - self.last_shot > self.shoot_delay: 
            #self.last_shot = now
        boss_bullet=BossBullet(self.rect.centerx,self.rect.bottom,boss_bullets.angle)
        all_sprites.add(boss_bullet)
        boss_bullets.add(boss_bullet)
        #boss_shoot.play()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -150) #bug? (invalid rect assigment)
            self.speedy = random.randrange(1, 2)

class BossBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        self.image=pygame.transform.scale(boss_bullet_img,(20,20))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
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

class Shout(pygame.sprite.Sprite): 
    def __init__(self,type,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = type 
        if self.type == 'overdrive':
            self.image = overdrive
        elif self.type == 'alert':
            self.image = alert
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT+100: 
            self.kill()



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
    
    
#score keeping

file=open ('scores.txt')

#load music
#mysound = pygame.mixer.Sound("mysound.wav")
#mysound.set_volume(0.5)

neon=pygame.mixer.music.load(path.join(sound_dir, 'Hackers.mp3'))
neon=pygame.mixer.music.set_volume(0.1)

player_shoot=pygame.mixer.Sound(path.join(sound_dir, 'player shoot.wav'))
player_shoot.set_volume(0.1)
mob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'mob shoot.wav'))
mob_shoot.set_volume(0.2)
bigmob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'bigmob shoot.wav'))
bigmob_shoot.set_volume(0.2)


buff_snd=pygame.mixer.Sound(path.join(sound_dir, 'buff2.wav'))
buff_snd.set_volume(0.1)
player_kill=pygame.mixer.Sound(path.join(sound_dir, 'player kill.wav'))
player_kill.set_volume(0.2)

mob_kill=pygame.mixer.Sound(path.join(sound_dir, 'mob kill.wav'))
mob_kill.set_volume(0.2)
bigmob_kill=pygame.mixer.Sound(path.join(sound_dir, 'bigmob kill.wav'))
bigmob_kill.set_volume(0.2)
boss_kill=pygame.mixer.Sound(path.join(sound_dir, 'boss kill.wav'))
boss_kill.set_volume(0.2)


#load game img
bg_img=pygame.image.load(path.join(img_dir, 'bg_1.png')) #EDUARDO JOAO
bg_img_rect=bg_img.get_rect()
bg_img_size=bg_img.get_size()
w,h=bg_img_size
x=0
y=0
x1=0
y1=-h


buff_imgs= {}
buff_imgs['doublegun']=pygame.image.load(path.join(img_dir, 'power1.png')).convert_alpha()
buff_imgs['bomb']=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()

overdrive=pygame.image.load(path.join(img_dir, 'overdriveV1.png')).convert_alpha ()
alert=pygame.image.load(path.join(img_dir,'alertV.png')).convert_alpha ()
player_img=pygame.image.load(path.join(img_dir, 'p1.png')).convert_alpha ()
player_health=pygame.image.load(path.join(img_dir, 'player_health.png')).convert_alpha()
p_h=pygame.transform.scale(player_health, (50,50))
player_bombs=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()
p_b=pygame.transform.scale(player_bombs, (30,30))

bullet_img=pygame.image.load(path.join(img_dir, 'b1.png')).convert_alpha ()
mobbullet_img=pygame.image.load(path.join(img_dir, 'bm1.png')).convert_alpha ()
bigmob_bullet_img=pygame.image.load(path.join(img_dir, 'bm2.png')).convert_alpha ()
mob_img=pygame.image.load(path.join(img_dir, 'mob.png')).convert_alpha ()
bigmob_img=pygame.image.load(path.join(img_dir, 'bigmob.png')).convert_alpha ()
boss_img=pygame.image.load(path.join(img_dir, 'boss.png')).convert_alpha ()
boss_bullet_img=pygame.image.load(path.join(img_dir, 'bt2.png')).convert_alpha ()



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

#get position of cursor?
def menu():
    menu=True
    selected='Begin' 
    screen.fill(BLACK)   
    while menu:
        clock.tick(FPS)
        draw_text(screen, 'Fatal Invader', 70, WIDTH/2, HEIGHT/4.5,WHITE)
        draw_text(screen, 'Fatal Invader', 70, WIDTH/1.95, HEIGHT/4.4,MAGENTA)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == K_UP:
                    selected='Begin'
                    pygame.display.update()
                elif event.key == K_DOWN:
                    selected='Scores'
                    pygame.display.update()
                if event.key==K_ESCAPE:
                    pygame.quit()
            if event.type==pygame.QUIT:
                pygame.quit()

            if selected=='Begin':
                draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1.75,WHITE)
                draw_text(screen, 'Begin', 40, WIDTH/1.97, HEIGHT/1.73,BLUE)
                pygame.display.update()
                if event.type==pygame.KEYDOWN:
                    if event.key==K_SPACE:
                                menu=False
            else:
                draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1,WHITE)
                pygame.display.update()

            if selected=='Scores':
                draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1.46,WHITE) 
                pygame.display.update()
                if event.type==pygame.KEYDOWN:
                    if event.key==K_SPACE:
                        scores()
                        pygame.display.update()            
            else:
                draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1,WHITE)
                pygame.display.update()
            
                
        draw_text(screen, 'Begin', 40, WIDTH/2, HEIGHT/1.75,RED)
        draw_text(screen, 'Scores', 30, WIDTH/2, HEIGHT/1.45,WHITE)
        draw_text(screen, 'Made by Alicja Donakowska', 15, WIDTH/4.5, HEIGHT/1.05,WHITE)
        draw_text(screen, 'Controls:    <   [Shoot]   >', 15, WIDTH/1.25, HEIGHT/1.1,WHITE)
        draw_text(screen, '{B}omb', 15, WIDTH/1.45, HEIGHT/1.065,WHITE)
        draw_text(screen, '{P}ause', 15, WIDTH/1.45, HEIGHT/1.035,WHITE)
        draw_text(screen, 'A', 15, WIDTH/1.13, HEIGHT/1.15,WHITE)
        draw_text(screen, 'v', 15, WIDTH/1.14, HEIGHT/1.05,WHITE)
        draw_text(screen, '[ESC to Exit]', 15, WIDTH/9, HEIGHT/35,WHITE)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)

def scores():
    with open(file,'r') as f:
        reader=csv.reader(f)
        scores=sorted(reader, key=lambda row:row[1], reverse=True)
        topscores=sorted(scores,reverse=True)
        top3=topscores[:3]
        #for line in f:
            #his=prev_scores.append(str(line.strip().split()))
    screen.fill(BLACK)
    draw_text(screen, 'Scoreboard', 40, WIDTH/2, HEIGHT/2.8,BBLUE)
    draw_text(screen, 'Level:Score', 25, WIDTH/2, HEIGHT/2.2,WHITE)
    draw_text(screen, str(top3), 20, WIDTH/2, HEIGHT/2,WHITE)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==K_LEFT:
                menu()

def pause():
    paused=True
    if paused==True:
        draw_text(screen, 'Pause',70,WIDTH/2,HEIGHT/2,BBLUE)
        draw_text(screen, 'Pause',70,WIDTH/1.95,HEIGHT/1.97,RED)
        draw_text(screen, '[ESC to Exit]', 25, WIDTH/6, HEIGHT/35,WHITE)
        draw_text(screen, '{M}enu', 25, WIDTH/9, HEIGHT/15,WHITE)
        pygame.display.update()
        pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_p: # Pausing
                    paused = False
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                if event.key==pygame.K_m:
                    menu()
            
    pygame.display.update()
    pygame.display.flip()
    clock.tick(5)

#Game loop
#####################################################################################
paused=False
in_menu=True
running = True
#PL=random.choice(music)


file='scores.csv'

 #2 different musics maybe?
while running:

    if in_menu:
        menu()
        neon=pygame.mixer.music.play(-1)
        in_menu=False
        level=1
        score=0
        maxmob=level
        maxboss=level
        all_sprites = pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        mob_bullets=pygame.sprite.Group()
        bigmob_bullets=pygame.sprite.Group()
        boss_bullets=pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bigmobs=pygame.sprite.Group()
        bosses=pygame.sprite.Group()
        player = Player()
        buffs=pygame.sprite.Group()
        all_sprites.add(player)

        #for maxmob in range (level//1):
            #maxmob+=1
        for i in range (4): #(maxmob)
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
            bosses.add(b)
            

        def mob_respawn():
            mob_kill.play()
            m=Mob()
            all_sprites.add(m)
            mobs.add(m)

        def bigmob_respawn():
            bigmob_kill.play()
            bm=BigMob()
            all_sprites.add(bm)
            bigmobs.add(bm)

        def boss_respawn():
            boss_kill.play()
            b=Boss()
            all_sprites.add(b)
            bosses.add(b)
     
    lvl_up=1500*level
    if score >=lvl_up*level:
        level+=1 
        with open(file,'a', newline='') as f:
            writer=csv.writer(f)
            writer.writerow([level,score])
    for i in range (level//10):
        y1+=2
        y+=2
    
    if maxmob==maxboss:
        maxmob-=4
    if level<8:
        maxmob+=2
    elif level//10:
        maxmob=2

    
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_p: # Pausing
                #draw_text(screen, 'Pause',50,WIDTH/2,HEIGHT/2,RED)
                pause()


    #make mobs shoot + player and bullets collide
    for mob in mobs:
        adj_odds=int(250*2/10)
        if random.randrange(adj_odds)==0:
            mob.shoot()                                                    #improved circular collision
    mob_bullet_hits=pygame.sprite.spritecollide(player,mob_bullets, True, pygame.sprite.collide_circle)
    for mob_bullet_hit in mob_bullet_hits:
        offset=shake()
        player_kill.play()
        expl=Explosion(mob_bullet_hit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        player.health-=1
        if player.health<=0:
            in_menu=True
        player.buff-=1
        if player.buff<=1:
            player.buff=1
        
    #bullet frequency
    for bigmob in bigmobs:
        adj_odds=int(100*5/10)
        if random.randrange(adj_odds)==0:
            bigmob.shoot()       
    bigmob_bullet_hits=pygame.sprite.spritecollide(player,bigmob_bullets, True,pygame.sprite.collide_circle)
    for bigmob_bullet_hit in bigmob_bullet_hits:
        player_kill.play()
        offset=shake()
        expl=Explosion(bigmob_bullet_hit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        player.health-=1
        if player.health<=0:
            in_menu=True 
        player.buff-=1
        if player.buff<=1:
            player.buff=1
        

    for boss in bosses:
        for boss_bullets.angle in range(360):
            odds=int(250*5/5)
            if random.randrange(odds)==0:
                boss.shoot()
    boss_bullet_hits=pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_circle)
    for boss_bullet_hit in boss_bullet_hits:
        player_kill.play()
        offset=shake()
        expl=Explosion(boss_bullet_hit.rect.center, 'lg')
        all_sprites.add(expl)
        player.health-=1
        if player.health<=0:
            in_menu=True
        player.buff-=1
        if player.buff<=1:
            player.buff=1
      
    # Update
    all_sprites.update()

    #check if player hit a buff and apply it
    buffhits=pygame.sprite.spritecollide(player, buffs, True)
    for buffhit in buffhits:
        buff_snd.play()
        if buffhit.type=='doublegun':
            player.gunbuff()
            if player.buff>=4:
                player.buff=4
        if buffhit.type=='bomb':
            player.bombs+=1
            if player.bombs>=5:
                player.bombs=5

    #check if mob collided with bullet
    mobhits=pygame.sprite.groupcollide(mobs, bullets, False, True)
    for mobhit in mobhits:
        mobhit.health-=1
        if mobhit.health<=0:
            expl=Explosion(mobhit.rect.center, 'lg') #animation
            all_sprites.add(expl)
            mobhit.kill()
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
            if random.random()>0.80:
                buff=Buff(bigmobhit.rect.center)
                all_sprites.add(buff)
                buffs.add(buff)
            bigmob_respawn()
    bosshits=pygame.sprite.groupcollide(bosses, bullets, False, True)
    for bosshit in bosshits:
        bosshit.health-=1
        if bosshit.health<=0:
            offset=shake()
            expl=Explosion(bosshit.rect.center, 'lg') #animation
            all_sprites.add(expl)
            bosshit.kill()
            score+=1500
            player.buff+=1
            player.health+=1
            if player.health>=5:
                player.health=5
            if random.random()>0.01:
                buff=Buff(bosshit.rect.center)
                all_sprites.add(buff)
                buffs.add(buff)
            boss_respawn()    
    #check for collisions
    mobhits=pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for mobhit in mobhits:
        expl=Explosion(mobhit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        offset=shake()
        player.health-=1
        if player.health<=0:
            in_menu=True
        player.buff-=1
        if player.buff<=1:
            player.buff=1
        if player.buff>=4:
            player.buff=4
        mob_respawn()
    bigmobhits=pygame.sprite.spritecollide(player, bigmobs, True, pygame.sprite.collide_circle)
    for bigmobhit in bigmobhits:
        expl=Explosion(bigmobhit.rect.center, 'lg') #animation
        all_sprites.add(expl)
        offset=shake()
        player.health-=1
        if player.health<=0:
            in_menu=True
        player.buff-=1
        if player.buff<=1:
            player.buff=1
        if player.buff>=4:
            player.buff=4
        bigmob_respawn()
    bosshits=pygame.sprite.spritecollide(player, bosses, False)
    
    #if player.health==1:
        #alert_count=0
        #if alert_count==0:
            #alert=Shout('alert', WIDTH/2,-10,10)
            #all_sprites.add(alert)
            #alert_count=1

    if player.health<=0:
        in_menu=True    
        
    # Draw / rende
    
    y1+=3
    y+=3
    
    screen.blit(bg_img,(x,y))
    screen.blit(bg_img,(x1,y1))
    all_sprites.draw(screen)
    draw_health(screen, WIDTH-250, 950, player.health, p_h)
    draw_bombs(screen, WIDTH-550, 950, player.bombs, p_b)
    draw_text(screen, str(score), 30, WIDTH/2,50,WHITE)
    draw_text(screen, 'Level '+str(level), 15, WIDTH/2,100,WHITE)
    pygame.display.update()
    # screen.fill(BLACK)
    #screen.blit(bg_img, next(offset))    
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h
    # *after* drawing everything, flip the display
    screen.blit(screen, next(offset))
    pygame.display.flip() 
    

    
pygame.quit()
    