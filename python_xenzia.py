'''
Snake game. One of my first major projects in pyhton
'''

import pygame
from pygame.locals import *
import os
import sys
import random
import time




pygame.init()#initialize pygame

fpsClock=pygame.time.Clock()#game time


python=pygame.image.load('python_food.png')#python logo at the side of the page
        
brick=pygame.image.load('brick.png')#image of bricks
brick=pygame.transform.scale(brick,(10,10))#scaling the image to 10 by 10



surface=pygame.display.set_mode((500,500))#creating the window

        
class Snake:
    '''
    class for snake objects
    '''
    def __init__(self):
        self.segments=[(15,15),(16,15)]#each segment represents the position of each segment of the snake
        self.direction=1
        snake_image=[] #array holding all images
        for i in ['shmo_','shmc_']:
            for j in ['right.png','left.png','up.png','down.png']:
                image=pygame.image.load(i+j)
                image=pygame.transform.scale(image,(10,10))
                snake_image.append(image)
        segment=pygame.image.load('segment.png')
        segment=pygame.transform.scale(segment,(10,10))
        snake_image.insert(0,segment)
        
        self.image=snake_image  #to access those images easily
        
   
       
    
        

class berry:
    '''
    class for the berry the snake eats
    '''
    def __init__(self):
        self.x=3
        self.y=2 #x and y position of the berry
        
        berry_img=pygame.image.load('python_berry.png')
        self.image=berry_img=pygame.transform.scale(berry_img,(10,10))#importing and scaling the image
        
    def move(self,snake):
        '''
        sets a new point for the x and y of the berry
        but those points must not go beyond the wall and must not land on the snake
        '''
        while True:
            x=random.randint(0,29)
            y=random.randint(0,29)
            if (x,y) not in set(snake.segments):
                break
        self.x=x
        self.y=y

    def draw_berry(self,surface):
        '''
        blits the berry to the given surface
        '''
        surface.blit(self.image,(100+10*self.x,100+10*self.y))
        pygame.display.update()

class Game:
    '''
    all game variables
    '''
    def __init__(self):
        self.snake=Snake() #snake object
        self.berry=berry() #berry object
        self.map=[[0]*32 for i in range(32)] #describes the arrangement of the walls
        for i in range(32):
            for j in range(32):
                if i==0 or j==0 or i==31 or j==31:
                    self.map[i][j]=1
        self.speed=200 #speed of game in miliseconds
        self.tick=200 #same as above
        self.frame=1 #determones what face the snake should show per time
        self.score=0 #game score

    def draw_snake(self,surface):
        '''
        blits image of the snake to the surface
        '''
        snake=self.snake
        surface.blit(snake.image[4*self.frame+snake.direction],
                     (100+10*snake.segments[0][0],100+10*snake.segments[0][1]))
        surface.blit(snake.image[0],
                     (100+10*snake.segments[1][0],100+10*snake.segments[1][1]))
        '''
        for i in range(1,len(snake.segments)):
            x,y=snake.segments[i]
            surface.blit(snake.image[0],(100+10*x,100+10*y))
        '''
        pygame.display.update()
            
    def moves(self,game_time,surface):
        if self.snake.direction==1:#right
            move=(1,0)
        if self.snake.direction==2:#left
            move=(-1,0)
        if self.snake.direction==3:#up
            move=(0,-1)
        if self.snake.direction==4:#down
            move=(0,1)
        self.tick-=game_time
        

        if self.tick<=0:
            self.tick=self.speed
            self.frame+=1
            self.frame%=2
            snake=self.snake
            #moving the snake semgments
            surface.fill((0,0,0),
                     (100+10*snake.segments[-1][0],100+10*snake.segments[-1][1],10,10))
            pygame.display.update()
            x,y=snake.segments[0][0]+move[0],snake.segments[0][1]+move[1]
            for i in range(len(snake.segments)):
                a,b=snake.segments[i]
                snake.segments[i]=(x,y)
                x,y=a,b
            head=self.snake.segments[0]

            
            
            #if the snake eats the berry
            if head==(self.berry.x,self.berry.y):
                last=self.snake.segments[-1]
                self.snake.segments.append(last)
                self.berry.move(self.snake)
                self.speed-=10# increase speed
                self.score+=100 #increase score
                if self.speed<=15:
                    self.speed=15
                    
    def head_hit_wall(self):
        '''
        returns True if the head of the snake hits the wall
        '''
        head=self.snake.segments[0]
        if head[0]<0 or head[0]>29 or head[1]<0 or head[1]>29:
            return True
        return False
    
    def head_hit_myself(self):
        '''
        returns true if tthe snakes head hits another part of the body
        '''
        head=self.snake.segments[0]
        for i in range(1,len(self.snake.segments)):
            if head==self.snake.segments[i]:
                return True
        return False
    pygame.display.update()
            

game=Game()

def draw_game(game,surface,brick):
    '''
    draws the entire game surface
    '''
    surface.fill((0,0,0)) #background
    surface.blit(python,(0,0))#picture view
    
    for i in range(32):
        for j in range(32):
            if game.map[i][j]==1:
                surface.blit(brick,(90+10*i,90+10*j))
    game.berry.draw_berry(surface)
    game.draw_snake(surface)
    pygame.display.update()
    
def show_score(surface):
    surface.fill((0,0,0),(150,0,300,80))
    text='SCORE: %d'%game.score
    font=pygame.font.Font(None,30)
    text=font.render(text,7,(255,255,255))
    text_rect=text.get_rect(centerx=surface.get_width()/2,centery=70)
    surface.blit(text,text_rect)
    pygame.display.update()
    
def game_over(surface):
    '''
    shows game over on the screen an asks if they want to play again
    '''
    text='GAME OVER'
    text2='PRESS SPACE FOR REMATCH'
    
    font=pygame.font.Font(None,30)
    text=font.render(text,10,(255,255,255))
    back=text.get_rect(centerx=surface.get_width()/2,centery=surface.get_height()/2)
    
    
    pygame.draw.rect(surface,(0,0,0),(100,200,300,100))#draws rectangle on the surface
    surface.blit(text,back)
    pygame.display.update()
    time.sleep(0.5)
    
draw_game(game,surface,brick)
while True:
    
    pygame.display.update()
    game.draw_snake(surface)
    game.berry.draw_berry(surface)
    game.moves(fpsClock.get_time(),surface)
    show_score(surface)
    if game.head_hit_wall() or game.head_hit_myself(): 
        game.snake.direction=0
        time.sleep(1)
        game_over(surface)
        pygame.quit()
        sys.exit()
        
        
    keys=pygame.key.get_pressed()
        
    if keys[K_LEFT]:
        if game.snake.direction!=1:
            game.snake.direction=2

    elif keys[K_RIGHT]:
        if game.snake.direction!=2:
            game.snake.direction=1

    elif keys[K_UP]:
        if game.snake.direction!=4:
            game.snake.direction=3

    elif keys[K_DOWN]:
        if game.snake.direction!=3:
            game.snake.direction=4

    for event in pygame.event.get():
        
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        
    
    pygame.display.update()
    fpsClock.tick(1000)
        
