# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:11:38 2020

@author: soumitra
"""


import pygame
import numpy as np
import math


WIDTH = 800
HEIGHT = 800

SCREEN = (WIDTH, HEIGHT)


class Pendulum:
    def __init__(self, x, y, l, theta, m):
        self.x = x
        self.y = y
        self.l = l
        self.theta = theta
        self.v = 0
        self.a = 0
        self.m = m
        
        self.hist = []
        
        
    def draw(self, screen):
        bx = self. x + int(math.sin(self.theta) * self.l)
        by = self.y + int(math.cos(self.theta) * self.l)
        
        self.hist.append((bx, by))
        
        # if len(self.hist) >= 100000:
        #     del self.hist[:500]
            
        pygame.draw.aaline(screen, (0), (self.x, self.y), (bx, by), 1)
        pygame.draw.circle(screen, (0), (bx, by), 10)
        # pygame.draw.circle(screen, (255, 0, 0), (bx, by), 0)
        
    def update(self, a):
        self.v += a
        self.v = np.clip(self.v, -1e+292, 1e+292)
        self.theta += self.v
    
    
   

def drawCirclePoints(screen, hist):
    if len(hist) > 5000:
        l = 5000
    else:
        l = len(hist)
    # print(l)
    prevx, prevy = hist[-l]
    
    for x,y in hist[-l:]:
        pygame.draw.aaline(screen, (0, 0, 0), (prevx, prevy), (x, y), 1)
        prevx, prevy = x, y


         
    
screen = pygame.display.set_mode(SCREEN)
screen2 = pygame.display.set_mode(SCREEN)

# g = 9.8/(3600)
g = 1

p1 = Pendulum(400, 300, 100, np.pi/2, 10)
x = p1.x + int(math.sin(p1.theta) * p1.l)
y = p1.y + int(math.cos(p1.theta) * p1.l) 

p2 = Pendulum(x, y, 100, np.pi/8, 10)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
            
    screen.fill((255, 255, 255))
    
    pygame.time.Clock().tick(50)
    
       
    
    a1 = (-g * (2 * p1.m + p2.m) * math.sin(p1.theta) - p2.m * g * math.sin(p1.theta - 2 * p2.theta) - 2 * math.sin(p1.theta - p2.theta) * p2.m * ((p2.v ** 2) * p2.l + (p1.v ** 2) * p1.l * math.cos(p1.theta - p2.theta))) / (p1.l * (2 * p1.m + p2.m - p2.m * math.cos(2 * p1.theta - 2 * p2.theta)))
    
    
    a1 = np.clip(a1, -1e+292, 1e+292)
    
    
    a2 = (2 * math.sin(p1.theta - p2.theta) * ((p1.v ** 2) * p1.l * (p1.m + p2.m) + g * (p1.m + p2.m) * math.cos(p1.theta) + (p2.v ** 2) * p2.l * p2.m * math.cos(p1.theta - p2.theta))) / (p1.l * (2 * p1.m + p2.m - p2.m * math.cos(2 * p1.theta - 2 * p2.theta)))
      
    
    a2 = np.clip(a2, -1e+292, 1e+292)
    
    # print(a1, a2)
       
    # while a1 > 1e+292 or a1 < -1e
    p1.update(a1)
    p2.update(a2)
    
    p2.x = p1.x + int(math.sin(p1.theta) * p1.l)
    p2.y = p1.y + int(math.cos(p1.theta) * p1.l) 
    
    
    # x = p2.x + int(math.sin(p2.theta) * p2.l)
    # y = p2.y + int(math.cos(p2.theta) * p2.l) 
    
    # pygame.draw.circle(screen, (0), (x, y), 10)
    
    
    p1.draw(screen)
    p2.draw(screen)
    drawCirclePoints(screen, p2.hist)
    
    # screen.blit(screen, screen2)
    pygame.display.update()    
        