import os, sys, random, json
import pygame
from pygame.locals import *
print("not malware ;)")
##RILEY IS THE GOAT
##made by cooper
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), flags=FULLSCREEN )
##screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Bricks')
black=pygame.Color(0,0,0)
debug=False
hardmode=True
hardcore=False
gravity=False
rand=False
fullscreen=True
_fullscreen=True
fps=60
slow=300
_slow=0
#change rng range
r1=20
r2=60
ping=pygame.mixer.Sound('boop.wav')
pygame.mixer.music.load('Mars.wav')

#bat init
bat = pygame.image.load('bat.png')
playerY = 540
batrect=bat.get_rect()
mousex, mousey = (0, playerY)

#ball init
ball = pygame.image.load('ball.png')
ballrect=ball.get_rect()
ballstartY = 200
ballspeed = 3
ballserved= False
bx, by =(24, ballstartY)
sx, sy =(ballspeed, ballspeed)
ballrect.topleft = (bx, by)
speedmodMAX=1.1
speedmod=speedmodMAX

#bricks init
brick = pygame.image.load('brick.png')
bricks=[]
for y in range(5):
    brickY = (y*24) +100
    for x in range(10):
        brickX = (x*31) + 245
        width=brick.get_width()
        height=brick.get_height()
        rect=Rect(brickX, brickY, width, height)
        bricks.append(rect)
pygame.mixer.music.play(-1)
while True:
    if fullscreen and not _fullscreen:del screen; screen = pygame.display.set_mode((800,600), flags=FULLSCREEN );_fullscreen=fullscreen
    elif not fullscreen and _fullscreen: del screen; screen = pygame.display.set_mode((800,600));_fullscreen=fullscreen
    screen.fill(black)
    if slow != 300:slow = slow + 1
    if _slow != 0:_slow = _slow - 1
    
    #bat draw
    screen.blit(bat, batrect)
    #ball draw
    screen.blit(ball, ballrect)
    #bricks draw
    for b in bricks:
        screen.blit(brick, b)
    #events
    
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()
            case pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                if mousex < 800 - 27.5:
                    batrect.topleft = (mousex-27.5 if mousex >=27.5 else 0, playerY)
                else:
                    batrect.topleft = (800 - 55, playerY)
            case pygame.MOUSEBUTTONUP:
                if not ballserved:ballserved = True;
                button = event.__dict__['button']
            #bullet time
                if button == 3 and slow == 300:
                    _slow = 60
                    slow = 0
            case pygame.KEYUP:
                try:
                    key = event.__dict__['key']
                    if key == K_1:fps = 5
                    if key == K_2:fps = 15
                    if key == K_3:fps = 30
                    if key == K_4:fps = 45
                    if key == K_5:fps = 60
                    if key == K_6:fps = 90
                    if key == K_7:fps = 120
                    if key == K_8:fps = 240
                    if key == K_9:fps = 360
                    if key == K_F3 and not ballserved:debug =True
                    if key == K_q:bricks=[]
                    if key == K_0 and not ballserved:gravity=False;speedmodMAX=1.025;speedmod=speedmodMAX; ballspeed=1.5
                    if key == K_p and not ballserved:gravity=False;speedmodMAX=1.1;speedmod=speedmodMAX; ballspeed=3
                    if key == K_h and not ballserved:hardcore=not hardcore
                    if key == K_m and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                    elif key == K_m and not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                    if key == K_g and not ballserved:gravity=True; speedmodMAX=1; speedmod=speedmodMAX; ballspeed=3
                    if key == K_RIGHTBRACKET: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1 if pygame.mixer.music.get_volume() <1.0 else pygame.mixer.music.get_volume())
                    if key == K_LEFTBRACKET: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1 if pygame.mixer.music.get_volume() >=0 else pygame.mixer.music.get_volume())
                    if key == K_r and not ballserved:rand= not rand
                    if key == K_F11 and not ballserved:fullscreen= not fullscreen
                    if key == K_KP1 and not ballserved:r1=20;r2=60;
                    if key == K_KP2 and not ballserved:r1=20;r2=100;
                    if key == K_KP3 and not ballserved:r1=100;r2=100;
                    if key == K_ESCAPE: pygame.quit();pygame.mixer.quit();sys.exit()
                    if key == K_x:ping.set_volume(ping.get_volume()+0.1 if ping.get_volume() <1.0 else ping.get_volume())
                    if key == K_z:ping.set_volume(ping.get_volume()-0.1 if ping.get_volume() >=0 else ping.get_volume())
                except KeyError:
                    pass
            
    #main game logic
    if ballserved:
        if gravity:sy+=.15
        #sx+=0.1 if abs(sx)!=sx else -0.1
        bx += sx
        by += sy
        ballrect.topleft = (bx, by)
        
    #collision detection
    if abs(sx) >=10 or abs(sy) >= 10 and not gravity:
        speedmod = 1
        sx =10 if abs(sx) == sx else -10
        sy =10 if abs(sy) == sy else -10
    if gravity and abs(sy) >= 15:
        sy = 15 if abs(sy)==sy else -15
    if bx <=0:
        bx=0
        sx*=-1
        sy*=speedmod
        sx*=speedmod
    elif bx >=800-8:
        bx=800-8
        sx*=-1
        sy*=speedmod
        sx*=speedmod
    if by <=0:
        by=0
        sy*=-1
        sy*=speedmod
        sx*=speedmod
    elif by >= 600 -8:
        finSpd = sx
        ballserved=False
        bx, by =(24, ballstartY)
        ballrect.topleft = (bx, by)
        if gravity:sx,sy=(ballspeed,ballspeed)
##Hardcore end
        if hardcore:print((abs(finSpd), 50- len(bricks)));bricks=[]
    if len(bricks) == 0:
        ballserved=False
        bx, by =(24, ballstartY)
        if not rand:sx, sy =(ballspeed, ballspeed)
        if rand: sx, sy= (random.randint(r1,r2)/10, random.randint(r1,r2)/10)
        ballrect.topleft = (bx, by)
        speedmod=speedmodMAX
        bricks=[]
        for y in range(5):
            brickY = (y*24) +100
            for x in range(10):
                brickX = (x*31) + 245
                width=brick.get_width()
                height=brick.get_height()
                rect=Rect(brickX, brickY, width, height)
                bricks.append(rect)

    if ballrect.colliderect(batrect):
        by = playerY-8
        sy*=-1
        if gravity:sy += 0.1*sy
        else:
            sy*=speedmod
            sx*=speedmod

    brickhit=ballrect.collidelist(bricks)
    if brickhit >=0:
        hb = bricks[brickhit]
        mx=bx+4
        my=by+4
        if mx > hb.x + hb.width or mx <hb.x:
            sx*=-1
        else:
            sy*=-1
        sy*=speedmod
        sx*=speedmod
        del bricks[brickhit]
        ping.play()
##Window name
    if debug:pygame.display.set_caption(str(((sx, sy),speedmodMAX, hardcore, gravity, fps, slow, _slow)))

    
    pygame.display.update()
    if _slow != 0:
        clock.tick(fps/4)
    else:
        clock.tick(fps)
