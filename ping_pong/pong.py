import pygame
import sys
from threading import Thread

# TODO: Initialisation 
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)




# TODO: game variables 
fps = 60
Exit = False
clock = pygame.time.Clock()  # sets the framerate of the game
X = 650
Y = 450
ball_x = X//2
ball_y = Y//2
ball_velocity_x = 2
ball_velocity_y = 0
bat_r_x = (X - 20) #Thicknes of bat is of 4
bat_r_y = Y // 2 - 30
bat_l_x = 10
bat_l_y = Y // 2 - 30
bat_velocity = 5
bat_r_movement = 0
bat_l_movement = 0
white = (255, 255, 255)
black = (0, 0, 0)
grey = (108, 108, 108)


#TODO: Creating window 
gameWindow = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Pong")
pygame.display.update() 

# TODO: Game functions 
def draw_figures():
    global bat_r_y, bat_l_y
    gameWindow.fill(black)
    pygame.draw.line(gameWindow, white, (X/2, 0), (X/2, Y), 1) #Draw center line
    # pygame.draw.line(gameWindow, white, (0, Y/2), (X, Y/2), 1) #Draw center line
    pygame.draw.circle(gameWindow, white, (ball_x, ball_y), 10) #Draw ball
    pygame.draw.rect(gameWindow, white, (bat_r_x, bat_r_y, 10, 60)) # draw right side bat
    pygame.draw.rect(gameWindow, white, (bat_l_x, bat_l_y, 10, 60)) # draw left side bat
    bat_r_y += bat_r_movement
    bat_l_y += bat_l_movement
    if bat_r_y <= 0:
        bat_r_y = 0
    if bat_r_y >= Y-60:
        bat_r_y = Y-60 
    if bat_l_y <= 0:
        bat_l_y = 0
    if bat_l_y >= Y-60:
        bat_l_y = Y-60 
    pygame.display.update()

def move_bats(key):
    global bat_r_movement, bat_l_movement
    if key == pygame.K_UP and bat_r_y >= 0:
        bat_r_movement -= bat_velocity
    elif key == pygame.K_DOWN and bat_r_y <= Y - 60:
        bat_r_movement += bat_velocity
    if key == pygame.K_w and bat_r_y >= 0:
        bat_l_movement -= bat_velocity
    elif key == pygame.K_s and bat_r_y <= Y - 60:
        bat_l_movement += bat_velocity

def stay_bats(key):
    global bat_r_movement, bat_l_movement
    if key == pygame.K_UP or pygame.K_DOWN:
        bat_r_movement = 0
    if key == pygame.K_w or pygame.K_s:
        bat_l_movement = 0


#TODO: Game Loop
while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            move_bats(event.key)
        if event.type == pygame.KEYUP:
            stay_bats(event.key)
    draw_figures()
    clock.tick(fps)