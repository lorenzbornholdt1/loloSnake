#Notes: https://pypi.org/project/auto-py-to-exe/
# 1: Import the library pygame
import pygame
from tkinter import *
from tkinter import messagebox
import numpy as np
from pygame.locals import *
from score import ScoreWriter

pygame.init()
pygame.font.init()
Tk().wm_withdraw() 


gameLostSound = pygame.mixer.Sound('sound/gamelost.ogg')
eatSound = pygame.mixer.Sound('sound/eat.ogg')
music = pygame.mixer.Sound('sound/music.ogg')

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event,100)


keys = [False, False, False, False]



class Snake(pygame.sprite.Sprite):
    def __init__(self, env,width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((55,155,255))
        self.environment = env
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.posX = np.random.randint(0,width)
        self.posY = np.random.randint(0,height)
        self.rect.center = [self.posX,self.posY]
        self.vx=0
        self.vy=0
        self.posXOld = 0
        self.posYOld = 0
        


class SnakeHead(Snake):
    def __init__(self, env,width, height):
        Snake.__init__(self,env,width,height)
    def move(self,keys):
        if(keys[0]):
            self.vy=-50
            self.vx=0
        elif keys [2]:
            self.vy=50
            self.vx=0
        if(keys[1]):
            self.vx=-50
            self.vy=0
        elif(keys[3]):
            self.vx=50
            self.vy=0
        keys[0]=keys[1]=keys[2]=keys[3]=0
        self.posY+=self.vy
        self.posX+=self.vx
        self.rect.center = [self.posX,self.posY]

    def checkIfEatTheirThings(self, body):
        for i in range (1, len(body)):
            if(self.posX == body[i].posX and self.posY == body[i].posY):
                self.environment.gameLost()
    def checkIfOutOfTheArea(self,screen):
        if self.posX >= screen.get_width():
            self.posX = 0.0001
        if self.posX <= 0:
            self.posX = screen.get_width()
        if self.posY >= screen.get_height():
            self.posY = 0.0001
        if self.posY <= 0:                
            self.posY = screen.get_height()


        

class Food(pygame.sprite.Sprite):
    def __init__(self,env, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.environment =env 
        self.image = pygame.Surface([width, height])
        self.image.fill((100,155,66))
        self.posX = 200
        self.posY = 200
        self.rect = self.image.get_rect()
        self.rect.center = [self.posX,self.posY]
    def checkIfSnake(self,snake):
        if(self.rect.colliderect(snake.rect)==True):
            self.posX = np.random.randint(0,self.environment.width)
            self.posY = np.random.randint(0,self.environment.height)
            self.environment.score  +=1 
            pygame.mixer.Sound.play(eatSound)
            return True
        else:
            return False

class GameEnvironment(object):
    def __init__(self, width, height):
        self.score = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,self.height),RESIZABLE)
        self.fontName = pygame.font.match_font('arial')
        self.player = SnakeHead(self,50,50)
        self.food = Food(self,25, 25)     
        self.drawText("Score: 0",30,500,500)
        self.snakeBody = []
        self.snakeBody.append(self.player)
        
        

    def drawText(self, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        text_surface = font.render(text, True, (55,155,255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    def gameRun(self):
        pygame.mixer.Sound.play(music,-1)
        while 1:
            self.screen.fill((255,255,255))
            for segment in self.snakeBody:
                self.screen.blit(segment.image, (segment.posX, segment.posY))
            self.drawText("Score: "+str(self.score), 50, self.width / 2, 10)
            self.screen.blit(self.food.image, (self.food.posX,self.food.posY))
            pygame.display.flip()
            self.lookForEvents()
    def gameLost(self):
        pygame.mixer.Sound.stop(music)
        self.player.vx = self.player.vy = 0
        scoreWrite = ScoreWriter()
        pygame.mixer.Sound.play(gameLostSound)
        messagebox.showinfo('You Lost!',"Your Score:%d, Highscore:%d" %(self.score,scoreWrite.readWriteScore(self.score)))
        pygame.quit() 


    def lookForEvents(self):

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit() 
                exit(0) 
            if event.type == pygame.KEYDOWN:
                if event.key==K_UP:                    
                    keys[0]=True
                elif event.key==K_LEFT:
                    keys[1]=True
                elif event.key==K_DOWN:
                    keys[2]=True
                elif event.key==K_RIGHT:
                    keys[3]=True
 
            if event.type == pygame.KEYUP:

                if event.key==pygame.K_UP:
                    keys[0]=False
                elif event.key==pygame.K_LEFT:
                    keys[1]=False
                elif event.key==pygame.K_DOWN:
                    keys[2]=False
                elif event.key==pygame.K_RIGHT:
                    keys[3]=False

            if event.type == move_event:

                self.player.rect.center = [self.player.posX,self.player.posY]
                self.food.rect.center = [self.food.posX,self.food.posY]            
                self.player.move(keys) # Move Head
                self.player.checkIfOutOfTheArea(self.screen) #If the Snake is out of the Area, return to the othwer wall
                self.player.checkIfEatTheirThings(self.snakeBody) #Check if the Head is eat a part of the Snake

                if(len(self.snakeBody)>1):
                    for i in range(0,len(self.snakeBody)-1):                    
                        self.snakeBody[i+1].posX=self.snakeBody[i].posXOld
                        self.snakeBody[i+1].posY=self.snakeBody[i].posYOld
                        self.snakeBody[i+1].vx = self.snakeBody[i+1].posX-self.snakeBody[i+1].posXOld
                        self.snakeBody[i+1].vy = self.snakeBody[i+1].posY-self.snakeBody[i+1].posYOld
                for i in range(0,len(self.snakeBody)):
                    self.snakeBody[i].posYOld = self.snakeBody[i].posY
                    self.snakeBody[i].posXOld = self.snakeBody[i].posX
                if self.food.checkIfSnake(self.player):
                    newSeg = Snake(self,self.player.width,self.player.height)
                    if(self.snakeBody[len(self.snakeBody)-1].vx>0): 
                        newSeg.posX=self.snakeBody[len(self.snakeBody)-1].posX-self.player.width
                        newSeg.posY=self.snakeBody[len(self.snakeBody)-1].posY
                    elif(self.snakeBody[len(self.snakeBody)-1].vx<0):
                        newSeg.posX=self.snakeBody[len(self.snakeBody)-1].posX+self.player.width
                        newSeg.posY=self.snakeBody[len(self.snakeBody)-1].posY
                    
                    if(self.snakeBody[len(self.snakeBody)-1].vy>0):
                        newSeg.posY=self.snakeBody[len(self.snakeBody)-1].posY-self.player.height
                        newSeg.posX=self.snakeBody[len(self.snakeBody)-1].posX
        
                    elif(self.snakeBody[len(self.snakeBody)-1].vy<0):
                   
                        newSeg.posY=self.snakeBody[len(self.snakeBody)-1].posY+self.player.height
                        newSeg.posX=self.snakeBody[len(self.snakeBody)-1].posX

                    newSeg.vx=self.snakeBody[len(self.snakeBody)-1].vx
                    newSeg.vy=self.snakeBody[len(self.snakeBody)-1].vy
                    newSeg.rect.center = [newSeg.posX,newSeg.posY]
                    self.snakeBody.append(newSeg)


    
environment = GameEnvironment(1000,800)
environment.gameRun()













