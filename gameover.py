import pygame
import random
from os import path
import os

img_dir=path.join(path.dirname(__file__),'img')
snd_dir=path.join(path.dirname(__file__),'snd')

wid=360
hei=480
fps=60


wh=(255,255,255)
blk=(0,0,0)
r=(255,0,0)
g=(0,255,0)
blue=(0,0,255)

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((wid,hei))
pygame.display.set_caption("game")
clock=pygame.time.Clock()

font_name=pygame.font.match_font('arial')
#surface to draw on text to be used size of the text and the coordinates
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,wh)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)
    
def newmob():
     m=Mob()
     all_sprites.add(m)
     mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
     if pct<0:
        pct=0
     BAR_LENGTH=100
     BAR_HEIGHT=10
     fill=(pct/100)*BAR_LENGTH
     outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
     fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
     pygame.draw.rect(surf,g,fill_rect)
     pygame.draw.rect(surf,wh,outline_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)
     
     

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(blk)
        self.rect=self.image.get_rect()
        self.radius=20
       # pygame.draw.circle(self.image,r,self.rect.center,self.radius)
        self.rect.centerx=wid/2
        self.rect.bottom=hei-10
        self.speedx=0
        self.shield=100
        #to stimulate auto-shoot
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()
        self.lives=3
        self.hidden=False
        self.hide_timer=pygame.time.get_ticks()

    def update(self):
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks()-self.hide_timer>1000:
            self.hidden=False
            self.rect.centerx=wid/2
            self.rect.bottom=hei-10
        
        self.speedx=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx=-8
        if keystate[pygame.K_RIGHT]:
            self.speedx=8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x+=self.speedx
        if self.rect.right>wid:
            self.rect.right=wid
        if self.rect.left<0 :
            self.rect.left=0

    def shoot(self):
        #this will give the current time
         now=pygame.time.get_ticks()
         if now-self.last_shot>self.shoot_delay:
             self.last_shot=now
             bullet=Bullet(self.rect.centerx,self.rect.top)
             all_sprites.add(bullet)
             bullets.add(bullet)

    def hide(self):
          self.hidden=True
          self.hide_timer=pygame.time.get_ticks()
          self.rect.center=(wid/2,hei+200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig=random.choice(meteor_images)
        self.image_orig.set_colorkey(blk)
        self.image=self.image_orig.copy()
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width/2)
       # pygame.draw.circle(self.image,r,self.rect.center,self.radius)
        self.rect.x=random.randrange(0,wid-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
        self.rot=0
        self.rot_speed=random.randrange(-8,8)
        self.last_update=pygame.time.get_ticks()
        
    def rotate(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>50:
            self.last_update=now
            self.rot=(self.rot+self.rot_speed)%360
            new.image=pygame.transform.rotate(self.image_orig,self.rot_speed)
            old_center=self.rect.center
            self.image=new_image
            self.rect=self.image.get_rect()
            self.rect.center=old_center

    def update(self):
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        if self.rect.top>hei+10  or self.rect.left<-25 or  self.rect.right>wid+20:
            self.rect.x=random.randrange(0,wid-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy=random.randrange(1,8)
            
class Bullet( pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(blk)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10

    def update(self):
         self.rect.y +=self.speedy
         if self.rect.bottom<0:
             self.kill()

class Pow( pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['shield','gun'])
        self.image =powerup_images[self.type]
        self.image.set_colorkey(blk)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=5

    def update(self):
         self.rect.y +=self.speedy
         if self.rect.top>hei:
             self.kill()     
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosion_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=75

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(explosion_anim[self.size]):
                self.kill()
            else:
                 center=self.rect.center
                 self.image=explosion_anim[self.size][self.frame]
                 self.rect=self.image.get_rect()
                 self.rect.center=center
            
            
def show_go_screen():
        screen.blit(background,background_rect)
        draw_text(screen,"SHMUP!",64,wid/2,hei/4)
        draw_text(screen,"ARROW KEYS TO MOVE,SPACE TO FIRE",22,wid/2,hei/2)
        draw_text(screen,"press a key to begin",18,wid/2,hei*3/4)
        pygame.display.flip()
        waiting =True
        while waiting:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYUP:
                    waiting=False
    
      

        
        
#load all game graphics

background=pygame.image.load(path.join(img_dir,"space.png")).convert()
background_rect=background.get_rect()
player_img=pygame.image.load(path.join(img_dir,"playerShip1_red.png")).convert()
player_mini_img=pygame.transform.scale(player_img,(25,19))
#meteor_img=pygame.image.load(path.join(img_dir,"meteorBrown_med3.png")).convert()
bullet_img=pygame.image.load(path.join(img_dir,"laserBlue10.png")).convert()
meteor_images=[]
meteor_list=['meteorBrown_big1.png','meteorBrown_big3.png','meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_small2.png']
for i in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,i)).convert())
explosion_anim={}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i  in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img=pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(blk)
    img_lg=pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename='sonicExplosion0{}.png'.format(i)
    img=pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(blk)
    explosion_anim['player'].append(img)

powerup_images={}
powerup_images['shield']=pygame.image.load(path.join(img_dir,'shield_gold.png')).convert()
powerup_images['gun']=pygame.image.load(path.join(img_dir,'bolt_gold.png')).convert()

#load all songs

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop(1).ogg'))                                        
pygame.mixer.music.set_volume(0.4)    
  
pygame.mixer.music.play(loops=-1)
game_over=True
run=True

while run:
    if game_over:
        show_go_screen()
        game_over=False
        all_sprites=pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        ob=Player()
        all_sprites.add(ob)
        for i in range(8):
           newmob()
        s=0  
    #eep loop running in the right sped
    clock.tick(fps)
    #process iinput(events(
    for event in pygame.event.get():
        #check for closing window
        if event.type==pygame.QUIT:
            run=False
      

                

    all_sprites.update()
    hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
    
    for hit in hits:
        s +=50- hit.radius
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random()>0.9:
            pow=Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
        
    hits=pygame.sprite.spritecollide(ob,mobs,True,pygame.sprite.collide_circle)
    for i in hits:
        ob.shield-=i.radius*2
        expl=Explosion(i.rect.center,'sm')
        all_sprites.add(expl)
        newmob()
        if ob.shield<=0:
            death_explosion=Explosion(ob.rect.center,'player')
            all_sprites.add(death_explosion)
            ob.hide()
            ob.lives-=1
            ob.shield=100

        if ob.lives==0 and not death_explosion.alive():
            game_over=True

         
        
                
    #update
            
    #draw/render
    screen.fill(blk)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(s),25,wid/2,10)
    draw_shield_bar(screen,5,5,ob.shield)
    draw_lives(screen,wid-100,5,ob.lives,player_mini_img)
    #afte drawing everything,flip the display
    pygame.display.flip()

pygame.quit()
    



