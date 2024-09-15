#imports

import pygame
import time
import random

#inits

screen_width = 900
screen_height = 600

pygame.init()
window = pygame.display.set_mode((screen_width,screen_height))
font = pygame.font.SysFont('Tohama',80, True,False)
pygame.display.update()

#variables

running = True
game_over = False
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (100,100,100)
block_size = 30

game_map = []
for i in range(screen_height//block_size):
    line = []
    for j in range(screen_width//block_size):
        line.append(0)
    game_map.append(line)

#classes

class Head():
    
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.dir = 'r'
        self.next_dir = 'r'
        self.points = 0
        self.lose = False
        
    def update(self):
        self.dir = self.next_dir
        if self.dir == 'r':
            self.x += block_size
        elif self.dir == 'l':
            self.x -= block_size
        elif self.dir == 'd':
            self.y += block_size
        elif self.dir == 'u':
            self.y -= block_size
            
        if(self.x < 0):
            self.x = screen_width - block_size
        elif(self.x > screen_width - block_size):
            self.x = 0
        if(self.y < 0):
            self.y = screen_height - block_size
        elif(self.y > screen_height - block_size):
            self.y = 0
            
        if game_map[self.y//block_size][self.x//block_size] == 1:
            self.lose = True
            
        game_map[self.y//block_size][self.x//block_size] = 1
            
    def setDir(self, new_dir):
        if(self.dir == 'r' and new_dir == 'l' or self.dir == 'l' and new_dir == 'r'):
            return
        if(self.dir == 'u' and new_dir == 'd' or self.dir == 'd' and new_dir == 'u'):
            return
        self.next_dir = new_dir
        
    def checkCollideWith(self,obj):
        return (self.x == obj.x and self.y == obj.y)
    
    def upScore(self):
        self.points += 1
        
    def render(self, display):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x,self.y,block_size,block_size))
        pygame.draw.rect(window, white, pygame.Rect(self.x,self.y,block_size,block_size), 1)

class Segment():
    
    def __init__(self,pattern):
        self.pattern = pattern
        self.color = pattern.color
        self.update()
        
    def update(self):
        self.x = self.pattern.x
        self.y = self.pattern.y
        self.pattern.update()
    
    def grow(self):
        new_tail = Segment(self)
        return new_tail
    
    def render(self, display):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x,self.y,block_size,block_size))
        self.pattern.render(display)

class Fruit():
    
    def __init__(self):
        self.x = random.randint(0,(screen_width//block_size)-1) * block_size
        self.y = random.randint(0,(screen_height//block_size)-1) * block_size

    def render(self, window):
        pygame.draw.rect(window, green, pygame.Rect(self.x,self.y,block_size,block_size))
        
#inits

player_1 = Head(block_size * 3, block_size * 3, red)
player_2 = Head(block_size * 3, screen_height - block_size * 3, blue)
tail_1 = Segment(player_1)
tail_1 = tail_1.grow()
tail_2 = Segment(player_2)
tail_2 = tail_2.grow()
fruit = Fruit()

#gameloop

def gameOver(winner):
    game_over = True
    while game_over:
        message = font.render(winner, True, white)
        window.blit(message,(200,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
        time.sleep(0.2)#5 frames per second
        pygame.display.update()

while running:
    pygame.draw.rect(window, black, pygame.Rect(0,0,screen_width,screen_height))

    for x in range(0, screen_width, block_size):
        for y in range(0, screen_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(window, gray, rect, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1.setDir('u')
            elif event.key == pygame.K_DOWN:
                player_1.setDir('d')
            elif event.key == pygame.K_RIGHT:
                player_1.setDir('r')
            elif event.key == pygame.K_LEFT:
                player_1.setDir('l')
            if event.key == pygame.K_w:
                player_2.setDir('u')
            elif event.key == pygame.K_s:
                player_2.setDir('d')
            elif event.key == pygame.K_d:
                player_2.setDir('r')
            elif event.key == pygame.K_a:
                player_2.setDir('l')
    
    time.sleep(0.16)
    
    game_map[tail_1.y//block_size][tail_1.x//block_size] = 0
    game_map[tail_2.y//block_size][tail_2.x//block_size] = 0
    
    tail_1.update()
    tail_2.update()
    
    if(player_1.checkCollideWith(fruit)):
        fruit = Fruit()
        tail_1 = tail_1.grow()
        player_1.upScore()
    elif(player_2.checkCollideWith(fruit)):
        fruit = Fruit()
        tail_2 = tail_2.grow()
        player_2.upScore()
    
    fruit.render(window)
    tail_1.render(window)
    tail_2.render(window)
    
    score_1 = font.render(str(player_1.points), True, red)
    score_2 = font.render(str(player_2.points), True, blue)
    window.blit(score_1,(20,20))
    window.blit(score_2,(screen_width - 40,20))
    
    pygame.display.update()
    
    if player_1.lose or player_2.lose:
        running = False
    if player_1.lose and player_2.lose:
        gameOver("Empate!")
    elif player_1.lose:
        gameOver("azul venceu!")
    elif player_2.lose:
        gameOver("vermelho venceu!")
        
#By Hermeskynitis