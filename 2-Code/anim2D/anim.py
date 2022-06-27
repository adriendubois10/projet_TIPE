import pygame
import os
from matplotlib.pyplot import pause
from gencarbones2D import *

os.environ['SDL_VIDEO_CENTERED']='1'

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Methode cercles")
clock = pygame.time.Clock()
fps = 100

GRAY = (127, 127, 127)
RED = (240, 10, 10)
GREEN = (5, 240, 5)
BACKGROUND = (20, 20 ,20)
ORANGE = (255,153,51)
WHITE = (240, 240, 240)

#paramètres

n, xlim, ylim = 40, (210,1710), (140,940)
rmax = 300 

liste_points = gen_points(n, xlim, ylim)

lc = liste_cercle(liste_points)
eps = ecart_type([distance(lc[i][0],lc[j][0]) for i in range(n) for j in range(i+1,n)])/1000
fixe = [False]*n
trans = [False]*n

def draw_text(text, pos):
    font = pygame.font.SysFont(None, 30)
    img = font.render(text, True, WHITE)
    screen.blit(img, pos)

def draw_centres_cercles(lc):
    n = len(lc)
    for i in range(n):
        c = lc[i]
        pygame.draw.circle(screen, RED, (c[0][0],c[0][1]), c[1], 2)
        pygame.draw.circle(screen, GREEN, (c[2][0],c[2][1]), 5, 0)
        pygame.draw.circle(screen, WHITE, (c[0][0],c[0][1]), 4, 0)
    
def draw_liaisons(v,lc):
    for (a,b) in v:
        pygame.draw.line(screen, ORANGE, a, b, 3)
    if v!=[]:
        for i in range(len(lc)):
            c = lc[i]
            draw_text(str(i), (c[2][0],c[2][1]) )
        
    
#boucle
        
run, drawc = True, True
v = []
cycles_presents = True
while run:
    clock.tick(fps)
    screen.fill(BACKGROUND)
    draw_centres_cercles(lc)
    draw_liaisons(v,lc)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                
    incrementer(lc, n, fixe, trans, eps, rmax, cycles_presents)
    update(lc, n, fixe, trans, cycles_presents)
    
    if (not (False in fixe)) and cycles_presents:
        relier(fixe,lc)
        enlever_cycles(fixe, lc, n)
        v = vertices(lc, fixe, n)
        cycles_presents = False

pygame.quit()