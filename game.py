# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:30:33 2019

@author: Suyash Singh
"""

import pygame
import random
import os

WIN_HEIGHT=800
WIN_WIDTH=500

BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
PIPE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BIRD_IMGS=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

class BIRD:
    def __init__(self,left,top):
        self.x=left
        self.y=top
        self.vel=0
        self.t=0
        self.img=BIRD_IMGS[1]
    def move(self):
        self.t+=1
        self.vel=self.vel*self.t-1.5*self.t**2
        
        if self.vel <= -10:
            self.vel=-10

        if self.vel < 0:
            self.img=BIRD_IMGS[2]
        elif self.vel == 0:
            self.img=BIRD_IMGS[1]
        else:
            self.img=BIRD_IMGS[0]
        temp_vel=-self.vel
        self.y+=temp_vel
        
    def destroy(self):
        if self.y > WIN_HEIGHT:
            return True
        return False
    def draw(self,screen):
        #self.move()
        if not self.destroy():
            screen.blit(self.img,(self.x,self.y))
   
class BASE:
    def __init__(self,BASE_HEIGHT):
        self.img1=pygame.transform.scale(BASE_IMG,(WIN_WIDTH,BASE_HEIGHT))
        self.img2=pygame.transform.scale(BASE_IMG,(WIN_WIDTH,BASE_HEIGHT))
        self.y=WIN_HEIGHT-self.img1.get_height()
        self.x1=0
        self.x2=WIN_WIDTH
        self.vel=-5
    def move(self):
        self.x1+=self.vel
        self.x2+=self.vel
        if self.x1 <= -WIN_WIDTH:
            self.x1=WIN_WIDTH
        if self.x2 <= -WIN_WIDTH:
            self.x2=WIN_WIDTH
    def draw(self,screen):
        self.move()
        screen.blit(self.img1,(self.x1,self.y))
        screen.blit(self.img2,(self.x2,self.y))
        
class PIPE:
    def __init__(self,width,gap,base_height):
        self.passed=False
        self.WIDTH=width
        self.BASE_HEIGHT=base_height
        self.SCREEN_HEIGHT=WIN_HEIGHT-self.BASE_HEIGHT
        self.VEL=5
        self.x=WIN_WIDTH
        self.img_bottom_height=random.randrange(0.1*(self.SCREEN_HEIGHT-gap),0.8*(self.SCREEN_HEIGHT-gap))
        self.GAP=gap
        self.img_bottom=pygame.transform.scale(PIPE_IMG,(width,self.img_bottom_height))
        self.img_top_height=self.SCREEN_HEIGHT-gap-self.img_bottom_height
        self.img_top=pygame.transform.flip( pygame.transform.scale(PIPE_IMG,(width,self.img_top_height)), False, True)
    def move(self):
        self.x-=self.VEL
    def draw(self,screen):
        self.move()
        screen.blit(self.img_bottom,(self.x,WIN_HEIGHT-self.BASE_HEIGHT-self.img_bottom_height))
        screen.blit(self.img_top,(self.x,0))

def draw_window(base,bird,pipes):
    screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    screen.blit(BG_IMG,(0,0))
    bird.draw(screen)
    base.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    pygame.display.update()
    return screen
    
def main():
        pygame.init()
        BASE_HEIGHT=100
        bird=BIRD(30,200)
        base=BASE(BASE_HEIGHT)
        pipes=[PIPE(100,200,BASE_HEIGHT)]
#        pipe=PIPE(100,200,BASE_HEIGHT)
        clock=pygame.time.Clock()
        
        run=True
        while run:
            clock.tick(30)
            rem=[]
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    
            for pipe in pipes:
                if bird.x > pipe.x and not pipe.passed:
                    pipes.append(PIPE(100,200,BASE_HEIGHT))
                    pipe.passed=True
                if pipe.x+pipe.WIDTH<=0:
                    rem.append(pipe)

            for r in rem:
                pipes.remove(r)
            
            screen=draw_window(base,bird,pipes)
                
        pygame.quit()
main()