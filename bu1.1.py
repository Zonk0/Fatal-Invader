from itertools import repeat
import pygame 
import random
import math
import sys
import os
from pygame import mixer
from os import path

from pygame.constants import KEYDOWN, K_BACKSPACE, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, MOUSEBUTTONDOWN


img_dir=path.join(path.dirname(__file__),'sprites')
sound_dir=path.join(path.dirname(__file__),'sounds')
exp_dir=path.join(path.dirname(__file__),'sprites/explos')
hi_dir=path.join(path.dirname(__file__))

WIDTH = 600
HEIGHT = 1000
FPS = 60 

BUFF_TIME=10000
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA=(238, 59, 255)
BBLUE=(0, 245, 255 )
YELLOW = (255, 255, 0)

pygame.init()
#pygame.display.init()
#pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fatal Invader")
clock = pygame.time.Clock()

def draw_text(surf, text, size, x, y, color):
    pygame.font.init()
    font_name='RetronoidItalic.ttf'
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
        self.image=random.choice(player_imgs)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset()
        
    def reset(self): 
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100
        self.speedy = 5
        self.speedx = 10
        self.radius=20
        self.health=5
        self.shoot_delay=100
        self.last_shot=pygame.time.get_ticks()
        self.buff=1
        self.buff_time=pygame.time.get_ticks()
        self.bombs=0

        self.bombing=False 

    def update(self):
        if self.buff>=4 and pygame.time.get_ticks()-self.buff_time>BUFF_TIME:
            self.buff-=1
            self.buff_time=pygame.time.get_ticks()

        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            return
   
        if self.rect.left < 0:
            self.rect.left = 0
            return
                    
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            return
        
        if self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
            return
            
        if keypress[pygame.K_LEFT] or keypress[pygame.K_a]:
            self.rect.x -= self.speedx

        if keypress[pygame.K_RIGHT] or keypress[pygame.K_d]:
            self.rect.x += self.speedx

        if keypress[pygame.K_DOWN] or keypress[pygame.K_s]:
            self.rect.y += self.speedy
        
        if keypress[pygame.K_UP] or keypress[pygame.K_w]:
            self.rect.y -= self.speedy
        
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
                    shout=Shout('overdrive',WIDTH/5,-1,15)
                    all_sprites.add(shout)
                    shout_count=1

    def bomb(self):
        global offset
        if self.bombs > 0: 
            self.bombing = True
            self.bombs -= 1
            offset=shake()
        if self.bombs < 0:
            self.bombs = 0 
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(10,25))

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
        self.image = random.choice(mob_img) #pygame.transform.scale(mob_img, (50, 60))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, 0)

        self.speedy = 8
        self.speedx = random.randrange(-5,5) #self.rect.x * math.cos(self.speedy%5)
        self.radius=20
        self.health=1

    def shoot(self):
        mob_bullet=MobBullet(self.rect.centerx,self.rect.bottom)
        all_sprites.add(mob_bullet)
        mob_bullets.add(mob_bullet)
        mob_shoot.play()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom>HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, 90)

class MobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=random.choice(mobbullet_img)

        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= 12
        self.radius=20

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class BigMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(bigmob_img)#pygame.transform.scale(bigmob_img, (125, 125))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -100)
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
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -150)

class BigMobBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bigmob_bullet_img
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy= 6
        self.radius=20

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(boss_img)#pygame.transform.scale(boss_img, (350, 250))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2 - self.rect.width
        self.rect.y = -350
        self.speedy = 0.5
        self.health=500
        self.radius=90
        #self.shoot_delay = 10000 
        #self.last_shot = pygame.time.get_ticks() 

    def shoot(self):
        #now = pygame.time.get_ticks() 
        #if now - self.last_shot > self.shoot_delay: 
            #self.last_shot = now
            
        boss_bullet=BossBullet(self.rect.centerx,self.rect.bottom-190,boss_bullets.angle)
        all_sprites.add(boss_bullet)
        boss_bullets.add(boss_bullet)
        #boss_shoot.play()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -350 #bug? (invalid rect assigment)
            self.speedy = 0.5

class BossBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        self.image=pygame.transform.scale(boss_bullet_img,(20,20))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.radius=10
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedx = 5
        self.speedy = 5

    def update(self):
        self.rect.x += self.speedx * math.cos(math.radians(self.angle)) 
        self.rect.y += self.speedy * math.sin(math.radians(self.angle))
        if self.rect.bottom > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()


################################################################################################

class Shout(pygame.sprite.Sprite): 
    def __init__(self,shout_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = shout_type 
        if self.type == 'overdrive':
            self.image = random.choice(overdrive)
            ov_snd.play()
        elif self.type == 'alert':
            self.image = alert
            alert_snd.play()
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.x = x
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: 
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
explosion_anim['bg'] = []
explosion_anim['dg'] = []
explosion_anim['ex'] = []

for i in range(15): 
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(exp_dir,filename)).convert_alpha()
    img_ex=pygame.transform.scale(img, (50,50))
    explosion_anim['ex'].append(img_ex)
    img_lg=pygame.transform.scale(img, (100,100))
    explosion_anim['lg'].append(img_lg)
    img_dg=pygame.transform.scale(img, (150,150))
    explosion_anim['dg'].append(img_dg)
    img_bg=pygame.transform.scale(img, (250,250))
    explosion_anim['bg'].append(img_bg)
    

#load music

music=['Hackers.mp3','Neon Dreams.mp3', 'HOME - Resonance Vs. MACINTOSH PLUS.mp3','Synthwave 80s Retro Background Music.mp3','4th Dimension.mp3']
next_song=random.choice(music)
ms=pygame.mixer.music.load(path.join(sound_dir, next_song))
ms=pygame.mixer.music.set_volume(0.1)
ms=pygame.mixer.music.play(-1)
#neon=pygame.mixer.music.load(path.join(sound_dir, 'Hackers.mp3'))
#neon=pygame.mixer.music.set_volume(0.1)

player_shoot=pygame.mixer.Sound(path.join(sound_dir, 'player shoot.wav'))
player_shoot.set_volume(0.08)
mob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'mob shoot.wav'))
mob_shoot.set_volume(0.1)
bigmob_shoot=pygame.mixer.Sound(path.join(sound_dir, 'bigmob shoot.wav'))
bigmob_shoot.set_volume(0.3)


buff_snd=pygame.mixer.Sound(path.join(sound_dir, 'buff2.wav'))
buff_snd.set_volume(0.1)
player_kill=pygame.mixer.Sound(path.join(sound_dir, 'player kill.wav'))
player_kill.set_volume(0.2)
ov_snd=pygame.mixer.Sound(path.join(sound_dir, 'ov.wav'))
ov_snd.set_volume(0.2)
alert_snd=pygame.mixer.Sound(path.join(sound_dir, 'alert.wav'))
alert_snd.set_volume(0.1)

mob_kill=pygame.mixer.Sound(path.join(sound_dir, 'mob kill.wav'))
mob_kill.set_volume(0.2)
bigmob_kill=pygame.mixer.Sound(path.join(sound_dir, 'bigmob kill.wav'))
bigmob_kill.set_volume(0.2)
boss_kill=pygame.mixer.Sound(path.join(sound_dir, 'boss kill.wav'))
boss_kill.set_volume(0.2)


#load game img
menubg_img=pygame.image.load(path.join(img_dir, 'bg4.jpg'))
menubg_img_rect=menubg_img.get_rect()
menubg_img_size=menubg_img.get_size()
bg_imgs=[]
bg_list=['bg2.png','bg3.png','bg1.png','bg4.png']
for imgs in bg_list:
    bg_imgs.append(pygame.image.load(path.join(img_dir,imgs)).convert_alpha())
bg_img=random.choice(bg_imgs)
bg_img_rect=bg_img.get_rect()
bg_img_size=bg_img.get_size()
w,h=bg_img_size


buff_imgs= {}
buff_imgs['doublegun']=pygame.image.load(path.join(img_dir, 'power1.png')).convert_alpha()
buff_imgs['bomb']=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()

overdrive=[]
over_list=['overdriveV.png','overdriveV1.png','overdriveV2.png']
for img in over_list:
    overdrive.append(pygame.image.load(path.join(img_dir, img)).convert_alpha ())

#overdrive=pygame.image.load(path.join(img_dir, 'overdriveV1.png')).convert_alpha ()
alert=pygame.image.load(path.join(img_dir,'alertV.png')).convert_alpha ()

player_imgs=[]
player_list=['p1.png','p2.png']
for imgs in player_list:
    player_imgs.append(pygame.image.load(path.join(img_dir,imgs)).convert_alpha())

#player_img=pygame.image.load(path.join(img_dir, 'p1.png')).convert_alpha ()

player_health=pygame.image.load(path.join(img_dir, 'player_health.png')).convert_alpha()
p_h=pygame.transform.scale(player_health, (50,50))

icon_img=pygame.image.load(path.join(img_dir, 'boss2.png')).convert_alpha()
icon=pygame.display.set_icon((icon_img))

player_bombs=pygame.image.load(path.join(img_dir, 'bomb1.png')).convert_alpha()
p_b=pygame.transform.scale(player_bombs, (30,30))

mob_img=[]
mobs_list=['mob1.png','mob2.png','mob3.png']
for imgss in mobs_list:
    mob_img.append(pygame.image.load(path.join(img_dir,imgss)).convert_alpha())

bigmob_img=[]
bigmobs_list=['bigmob.png','bigmob2.png','bigmob3.png']
for imgs in bigmobs_list:
    bigmob_img.append(pygame.image.load(path.join(img_dir,imgs)).convert_alpha())

boss_img=[]
boss_list=['boss.png','boss2.png','boss3.png','boss4.png']
for imgs in boss_list:
    boss_img.append(pygame.image.load(path.join(img_dir,imgs)).convert_alpha())

bullet_img=pygame.image.load(path.join(img_dir, 'b1.png')).convert_alpha ()

mobbullet_img=[]
mobbb_list=['bm1.png','bm3.png','bm4.png']
for imgs in mobbb_list:
    mobbullet_img.append(pygame.image.load(path.join(img_dir,imgs)).convert_alpha())

#mobbullet_img=pygame.image.load(path.join(img_dir, 'bm1.png')).convert_alpha ()
bigmob_bullet_img=pygame.image.load(path.join(img_dir, 'bm2.png')).convert_alpha ()
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

#get position of cursor
def menu():
    in_menu=True
    selected='Begin'
    score = False
    
    while in_menu:
        screen.fill(BLACK)
        screen.blit(menubg_img,(WIDTH/120,HEIGHT/80))  
        
        draw_text(screen, 'Fatal Invader', 70, WIDTH/2, HEIGHT/4.5,WHITE)
        draw_text(screen, 'Fatal Invader', 70, WIDTH/1.95, HEIGHT/4.4,MAGENTA)
        draw_text(screen, 'Ver 1.1', 20, WIDTH/1.1, HEIGHT/60,WHITE)
                
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == K_UP:
                    selected='Begin'
                
                elif event.key == K_DOWN:
                    selected='Scores'
                
                elif event.key==K_SPACE:
                    if selected=='Begin':
                        in_menu=False
                    elif selected=='Scores':
                        top3 = scores()
                        score = not score
            
        if selected == 'Begin':
            draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1.75,WHITE) 
        else:
            draw_text(screen,'>', 40, WIDTH/3, HEIGHT/1.45,WHITE)

        if score:
           draw_text(screen, 'Scoreboard', 40, WIDTH/2, HEIGHT/2.6,BBLUE)
           draw_text(screen, 'Name:Level:Score', 25, WIDTH/2, HEIGHT/2.3,WHITE)
           pos = WIDTH/4
           index = 1
           score_y = 0
              
           for name, level, score in top3:
                score_str = name + ": " + str(level) + " : " + str(score)
                score_len = len(score_str)/2
                draw_text(screen, score_str, 20, pos * index - score_len , HEIGHT/2 + score_y ,WHITE)
                index += 1
                score_y += 30
                
        draw_text(screen, 'Begin', 40, WIDTH/2, HEIGHT/1.75,RED)
        draw_text(screen, 'Scores', 30, WIDTH/2, HEIGHT/1.45,WHITE)
        draw_text(screen, 'Made by Alicja Donakowska', 15, WIDTH/4.5, HEIGHT/1.05,WHITE)
        #draw_text(screen, 'Controls:    <   [Shoot]   >', 15, WIDTH/1.25, HEIGHT/1.1,WHITE)
        #draw_text(screen, '{B}omb', 15, WIDTH/1.45, HEIGHT/1.065,WHITE)
        #draw_text(screen, '{P}ause', 15, WIDTH/1.45, HEIGHT/1.035,WHITE)
        #draw_text(screen, 'A', 15, WIDTH/1.13, HEIGHT/1.15,WHITE)
        #draw_text(screen, 'v', 15, WIDTH/1.14, HEIGHT/1.05,WHITE)
        draw_text(screen, '[ESC to Exit]', 15, WIDTH/9, HEIGHT/35,WHITE)
        pygame.display.update()
        clock.tick(FPS)
    return False

#score keeping
    
def scores():
    topscores = []
    highest_score = 0
    scores = []
    
    filename = "highscores"
    with open(filename, 'r') as a_file:

        for a_line in a_file:
            values = a_line.split(" ")
            if len(values) == 3:
                name = values[0]
                level = int(values[1])
                score = int(values[2])
            
                scores.append((name, level, score))
            
        scores.sort(key=lambda elem: elem[2])
        topscores = sorted(scores,reverse=True)
        top3=topscores[:3]
        return top3

def pause():
    paused=True
    if paused==True:
        draw_text(screen, 'Pause',70,WIDTH/2,HEIGHT/2,BBLUE)
        draw_text(screen, 'Pause',70,WIDTH/1.95,HEIGHT/1.97,RED)
        draw_text(screen, '[ESC to Exit]', 25, WIDTH/6, HEIGHT/35,WHITE)
        draw_text(screen, 'Un{P}ause', 25, WIDTH/7, HEIGHT/15,WHITE)
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
                #if event.key==pygame.K_m:
                    #menu()
            
    pygame.display.update()
    clock.tick(5)

#Game loop
#####################################################################################

maxmobs = 4
maxbigmobs = 4
maxbosses = 1

maxmob = 0
maxbigmob = 0
score = 0

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

 #2 different musics maybe?
def setup_level(level):
    global maxmob, maxbigmob, maxmobs, maxbigmobs
    print("level = " + str(level))
    
    if level < 4:
        maxmob=level
        maxbigmob = level
        maxboss=level
    else:
        maxmob = maxmobs
        maxbigmob = maxbigmobs
    
    for i in range (maxmob):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    for i in range (maxbigmob):
        bm=BigMob()
        all_sprites.add(bm)
        bigmobs.add(bm)
    
    if level%10== 0:
        b=Boss()
        all_sprites.add(b)
        bosses.add(b)
        alert_x = WIDTH/2 - alert.get_width()/2
        alert_y = 10
        this_alert = Shout('alert', alert_x, alert_y, 10)
        all_sprites.add(this_alert)
    
        
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
 
def random_respawn(respawn_type):
    global maxmob, maxbigmob
        
    if respawn_type == "mob":
        if len(mobs) < maxmob:
            r = random.randint(1,20)
            if r > (2 * maxmob):
                mob_respawn()
 
    if respawn_type == "bigmob":
        if len(mobs) < maxbigmob:
            r = random.randint(1,20)
            if r > (2 * maxbigmob):
                bigmob_respawn()
             
def reset():
    global player
    
    all_sprites.empty()
    bullets.empty()
    mob_bullets.empty()
    bigmob_bullets.empty()
    boss_bullets.empty()
    mobs.empty()
    bigmobs.empty()
    bosses.empty()
    buffs.empty()
    player = Player()
    all_sprites.add(player)
    level = 1
    score = 0
    
#neon=pygame.mixer.music.play(-1)

def game():
    global score, player
    pygame.mouse.set_visible(False)
        
    while True:
        paused=False
        in_menu=True
        running = False
        level_up = False
    
        reset()
        player.reset()
       
        scroll_rect = pygame.Rect(0,500,WIDTH,HEIGHT)
        
        if in_menu:
            in_menu = menu()
                 
        level=1
        score=0
        
        running = True
        offset=repeat((0,0))
        
        setup_level(level)

        while running: 
            if level<10:
                lvl_up=4500*level
            if level>=10:
                lvl_up=6500*level
            if level>=30:
                lvl_up=8500*level
       
            if score > lvl_up:
                level+=1 
                setup_level(level)
                with open("highscores", "a") as a_file:
                    a_file.write("user")
                    a_file.write(" ")
                    a_file.write(str(level))
                    a_file.write(" ")
                    a_file.write(str(score))
                    a_file.write("\n")
            
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
            # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_p: # Pausing
                        pause()

                    if event.key == pygame.K_b:
                        if player.bombing:
                            continue
                        else:
                            player.bomb()
            
            #make mobs shoot + player and bullets collide
            for mob in mobs:
              adj_odds=int(250*2/10)
              if random.randrange(adj_odds)==0:
                    mob.shoot()                                                    #improved masked collision
            
            mob_bullet_hits=pygame.sprite.spritecollide(player,mob_bullets, True, pygame.sprite.collide_circle)
            for mob_bullet_hit in mob_bullet_hits:
                offset=shake()
                player_kill.play()
                expl=Explosion(mob_bullet_hit.rect.center, 'ex') #animation
                all_sprites.add(expl)
                player.health-=1
                
                if player.health<=0:
                    running = False
                player.buff-=1
            
                if player.buff<=1:
                    player.buff=1

            #bullet frequency
            for bigmob in bigmobs:
              adj_odds=int(250*2/10)
              if random.randrange(adj_odds)==0:
                    bigmob.shoot()       
            
            bigmob_bullet_hits=pygame.sprite.spritecollide(player,bigmob_bullets, True, pygame.sprite.collide_circle)
            for bigmob_bullet_hit in bigmob_bullet_hits:
                player_kill.play()
                offset=shake()
                expl=Explosion(bigmob_bullet_hit.rect.center, 'ex') #animation
                all_sprites.add(expl)
                player.health-=1
            
                if player.health<=0:
                    running = False 
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
                expl=Explosion(boss_bullet_hit.rect.center, 'ex')
                all_sprites.add(expl)
                player.health-=1
                
                if player.health<=0:
                    running = False
                player.buff-=1
               
                if player.buff<=1:
                    player.buff=1
            
            #check if player hit a buff and apply it
            buffhits=pygame.sprite.spritecollide(player, buffs, True)
            for buffhit in buffhits:
                buff_snd.play()
                if buffhit.type=='doublegun':
                    player.gunbuff()
                    if player.buff>=4:
                        player.buff==4
                if buffhit.type=='bomb':
                    player.bombs+=1
                    if player.bombs>=5:
                        player.bombs=5

            #check if mob collided with bullet
            mobhits=pygame.sprite.groupcollide(mobs, bullets, False, True)
            for mobhit in mobhits:
                expl=Explosion(mobhit.rect.center, 'ex')
                all_sprites.add(expl)
                mobhit.health-=1
                if mobhit.health<=0:
                   expl=Explosion(mobhit.rect.center, 'lg') #animation
                   all_sprites.add(expl)
                   mobhit.kill()
                   score+=250
                   if random.random()>0.95:
                       buff=Buff(mobhit.rect.center)
                       all_sprites.add(buff)
                       buffs.add(buff)
                 
                   if len(mobs) == 0:
                            mob_respawn()
            
            bigmobhits=pygame.sprite.groupcollide(bigmobs, bullets, False, True, pygame.sprite.collide_mask)
            for bigmobhit in bigmobhits:
                expl=Explosion(bigmobhit.rect.center, 'ex')
                all_sprites.add(expl)
                bigmobhit.health-=1
                if bigmobhit.health<=0:
                    expl=Explosion(bigmobhit.rect.center, 'dg') #animation
                    all_sprites.add(expl)
                    bigmobhit.kill()
                    score+=750
                    if random.random()>0.95:
                        buff=Buff(bigmobhit.rect.center)
                        all_sprites.add(buff)
                        buffs.add(buff)
            
                    if len(bigmobs) == 0:
                            bigmob_respawn()
            
            bosshits=pygame.sprite.groupcollide(bosses, bullets, False, True, pygame.sprite.collide_mask)
            for bosshit in bosshits:
                expl=Explosion(bosshit.rect.center, 'lg')
                all_sprites.add(expl)
                bosshit.health-=1
                if bosshit.health<=0:
                    level+=1
                    offset=shake()
                    expl=Explosion(bosshit.rect.center, 'bg') #animation
                    all_sprites.add(expl)
                    bosshit.kill()
                    score+=5000
                    player.buff+=1
                    player.health+=1
                    if player.health>=5:
                        player.health=5
                    if random.random()>0.01:
                        buff=Buff(bosshit.rect.center)
                        all_sprites.add(buff)
                        buffs.add(buff)
                        if player.buff>=4:
                            player.buff==4
                            
            #check for collisions
            mobhits=pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for mobhit in mobhits:
                expl=Explosion(mobhit.rect.center, 'ex') #animation
                all_sprites.add(expl)
                offset=shake()
                player.health-=1
                if player.health<=0:
                    in_menu=True
                player.buff-=1
                if player.buff<=1:
                    player.buff=1
                if player.buff>=4:
                    player.buff==4
                
                if len(mobs) == 0:
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
                
                if len(bigmobs) == 0:
                        bigmob_respawn()
     
                   
            if player.bombing:
                offset=shake()
                for mob in mobs:
                    mob.kill()
                    #score -= mob.radius * 2
                    expl = Explosion(mob.rect.center, 'lg')
                    all_sprites.add(expl)
                    #random_respawn("mob")
                    mob_respawn()
                        
                for bigmob in bigmobs: 
                    bigmob.kill()
                    #score += bigmob.radius * 2
                    expl = Explosion(bigmob.rect.center,'lg')
                    all_sprites.add(expl)
                    #random_respawn("bigmob")                   
                    bigmob_respawn()
            
                for bosshit in bosshits: 
                    #bosshit.health=-25
                    #score -= bosshit.radius*5
                    expl = Explosion(bosshit.rect.center,'lg')
                    all_sprites.add(expl)
                
                for mob_bullet in mob_bullets: 
                    mob_bullet.kill()
                    #score -= mob_bullet.radius*2
                    expl = Explosion(mob_bullet.rect.center,'lg')
                    all_sprites.add(expl)
                    print("score = " + str(score))
            
                for bigmob_bullet in bigmob_bullets: 
                    bigmob_bullet.kill()
                    #score -= bigmob_bullet.radius*1
                    expl = Explosion(bigmob_bullet.rect.center,'lg')
                    all_sprites.add(expl)
                    print("score = " + str(score))
            
                for boss_bullet in boss_bullets: 
                    boss_bullet.kill()
                    score -=boss_bullet.radius*5
                    expl = Explosion(boss_bullet.rect.center,'lg')
                    all_sprites.add(expl)
                    print("score = " + str(score))

                player.bombing = False

            bosshits=pygame.sprite.spritecollide(player, bosses, True, pygame.sprite.collide_circle)

            for bosshit in bosshits:
                expl=Explosion(bosshit.rect.center, 'lg') #animation
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


            if player.health<=0:
               running = False    

            # Update
            all_sprites.update()


            # Draw / render

            screen.blit(bg_img, (0, 0), scroll_rect)
            scroll_rect.top -= 2
            if scroll_rect.top == 0:
                scroll_rect.top = 500
                
            all_sprites.draw(screen)
            draw_health(screen, WIDTH-250, 950, player.health, p_h)
            draw_bombs(screen, WIDTH-550, 950, player.bombs, p_b)
            draw_text(screen, str(score), 40, WIDTH/2,50,WHITE)
            draw_text(screen, 'Level '+str(level), 20, WIDTH/2,100,WHITE)

            # *after* drawing everything, flip the display
            screen.blit(screen, next(offset))
            pygame.display.flip() 


game()
pygame.quit()
 
