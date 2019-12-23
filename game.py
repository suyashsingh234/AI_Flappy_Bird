# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:30:33 2019

@author: Suyash Singh
"""

import pygame
import random
import os
import neat 

pygame.init()
pygame.font.init()

WIN_HEIGHT=800
WIN_WIDTH=500
SCORE_FONT=pygame.font.SysFont("Comic Sans Ms",30)

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
        if self.vel>=10:
            self.vel=10

        if self.vel < 0:
            self.img=BIRD_IMGS[2]
        elif self.vel == 0:
            self.img=BIRD_IMGS[1]
        else:
            self.img=BIRD_IMGS[0]
        temp_vel=-self.vel
        self.y+=temp_vel
        
    def destroy(self):
        if self.y > WIN_HEIGHT or self.y<0:
            return True
        return False
    
    def jump(self):
        self.vel=10
        self.t=0
        
    def draw(self,screen):
        self.move()
        if not self.destroy():
            screen.blit(self.img,(self.x,self.y))
            
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
   
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
    def get_mask(self):
        return (pygame.mask.from_surface(self.img1),pygame.mask.from_surface(self.img2))
        
        
class PIPE:
    def __init__(self,width,gap,base_height):
        self.passed=False
        self.newpipe=False
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
        
    def collide(self,bird):
        bird_mask=bird.get_mask()
        pipe_top_mask=pygame.mask.from_surface(self.img_top)
        pipe_bottom_mask=pygame.mask.from_surface(self.img_bottom)
        
        offset_x_top,offset_y_top=(self.x-round(bird.x)),(-round(bird.y))
        offset_x_bottom,offset_y_bottom=(self.x-round(bird.x)),(WIN_HEIGHT-self.BASE_HEIGHT-self.img_bottom_height-round(bird.y))
        
        is_collide_top=bird_mask.overlap(pipe_top_mask,(offset_x_top,offset_y_top))
        is_collide_bottom=bird_mask.overlap(pipe_bottom_mask,(offset_x_bottom,offset_y_bottom))
        
        if is_collide_top or is_collide_bottom:
            return True
        return False

def draw_window(base,birds,pipes,score):
    screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    screen.blit(BG_IMG,(0,0))
    for bird in birds:
        bird.draw(screen)
    base.draw(screen)
    score_text=SCORE_FONT.render("Score: "+str(score),30,(255,255,255))
    
    screen.blit(score_text,(0,WIN_HEIGHT-score_text.get_height()))
    for pipe in pipes:
        pipe.draw(screen)
    pygame.display.update()
    return screen
    
def main(genomes,config):
    BASE_HEIGHT=100
    birds=[]
    X=30
    base=BASE(BASE_HEIGHT)
    pipes=[PIPE(100,200,BASE_HEIGHT)]
    score=0
    clock=pygame.time.Clock()
    
    
    nets=[]  #neural networks
    ge=[]   #genomes
    
    for genome_id, genome in genomes:
        genome.fitness = 5
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        birds.append(BIRD(X,200))
        ge.append(genome)
        nets.append(net)
    
    run=True
    while run:
        clock.tick(30)
        screen=draw_window(base,birds,pipes,score)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                quit()
          
        next_pipe=pipes[0]
# =============================================================================
#         for pipe in pipes:
#             if not pipe.passed:
#                 next_pipe=pipe
#                 break
# =============================================================================
          
        i=0    
        for bird in birds:
            ge[i].fitness+=0.1
            inp1=bird.y
            inp2=next_pipe.img_top_height
            inp3=(WIN_HEIGHT-next_pipe.BASE_HEIGHT-next_pipe.img_bottom_height)
            output=nets[i].activate((inp1,inp2,inp3))
            if output[0]>0.5:
                bird.jump()
            i+=1
      
        for pipe in pipes:
            if pipe.x+pipe.WIDTH<=0:
                pipes.remove(pipe)
            if pipe.x<X and not pipe.newpipe:   
                pipes.append(PIPE(100,200,BASE_HEIGHT))
                pipe.newpipe=True
            i=0   
            for bird in birds:
                if bird.x > pipe.x and not pipe.passed:
                    pipe.passed=True
                    score+=1
                    
                if  pipe.collide(bird) or bird.y<0 or bird.y>base.y:
                    ge[i].fitness-=1
                    nets.pop(i)
                    ge.pop(i)
                    birds.remove(bird)
                    break
                i+=1
            
        if len(birds)==0:
            run=False
            
    pygame.display.quit()

def run(config_file):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet,neat.DefaultStagnation,
                          config_file)
        p = neat.Population(config)

    
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(5))
    
        p.run(main, 50)

if __name__=="__main__":
    local_directory=os.path.dirname(__file__)
    config_path=os.path.join(local_directory,"neat_config.txt")
    run(config_path)

pygame.quit()