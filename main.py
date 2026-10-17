import sys
import pygame
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
FPS=60
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Python dungeon crawler - Day 1")
clock=pygame.time.Clock()
running =True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    screen.fill((30,30,30))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()