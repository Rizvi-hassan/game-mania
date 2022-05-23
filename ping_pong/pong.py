import pygame
from sys import exit
from random import randint, choice
from time import sleep

# TODO: Initialisation
pygame.init()
font = pygame.font.SysFont("Segoe UI", 35)
font2 = pygame.font.SysFont("Segoe UI", 55)


# TODO: game variables
fps = 60
acitve = True
Exit = False
clock = pygame.time.Clock()  # sets the framerate of the game
X = 650
Y = 450
ball_x = X//2
ball_y = Y//2
ball_velocity_x = 6
ball_velocity_y = randint(0, 3)
bat_r_x = (X - 20)
bat_r_y = Y // 2 - 30
bat_l_x = 10
bat_l_y = Y // 2 - 30
bat_velocity = 5
white = (255, 255, 255)
black = (0, 0, 0)
grey = (141, 141, 141)
Multiplayer = False
score_r = 0
score_l = 0
level = 'h'
if level == 'e':
    bat_velocity = 4
    ball_inc = 7
elif level == 'm':
    bat_velocity = 4
    ball_inc = 10
elif level == 'h':
    bat_velocity = 5
    ball_inc = 14

# TODO: Creating window
gameWindow = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Pong")
pygame.display.update()

# TODO: Game functions


def write_text(text, x, y):
    write = font.render(text, True, grey)  # the text, antialias(T/F), color
    gameWindow.blit(write, [x, y])


def draw_figures():
    global bat_r_y, bat_l_y, ball_x, ball_y
    gameWindow.fill(black)
    pygame.draw.line(gameWindow, white, (X/2, 0),
                     (X/2, Y), 1)  # Draw center line
    # pygame.draw.line(gameWindow, white, (0, Y/2), (X, Y/2), 1) #Draw center line
    pygame.draw.circle(gameWindow, white, (ball_x, ball_y), 10)  # Draw ball
    # draw right side bat
    pygame.draw.rect(gameWindow, white, (bat_r_x, bat_r_y, 10, 60))
    # draw left side bat
    pygame.draw.rect(gameWindow, white, (bat_l_x, bat_l_y, 10, 60))
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y


def move_bats(key):
    global bat_r_y, bat_l_y
    if key[pygame.K_UP] and bat_r_y >= 0:
        bat_r_y -= bat_velocity
    elif key[pygame.K_DOWN] and bat_r_y <= Y - 60:
        bat_r_y += bat_velocity

    if key[pygame.K_w] and bat_l_y >= 0:
        bat_l_y -= bat_velocity
    elif key[pygame.K_s] and bat_l_y <= Y - 60:
        bat_l_y += bat_velocity


def change_ball_velocity():
    global ball_velocity_x, ball_velocity_y
    if ball_x + 10 >= bat_r_x:
        if ball_x >= X:
            re_play("l", pygame.time.get_ticks())
        else:
            val = ball_y - (bat_r_y + 30)
            if abs(val) <= 30:
                ball_velocity_x = -ball_inc
                ball_velocity_y = val // 5

    if ball_x - 10 <= bat_l_x:
        if ball_x <= 0:
            re_play("r", pygame.time.get_ticks())
        else:
            val = ball_y - (bat_l_y + 30)
            if abs(val) <= 30:
                ball_velocity_x = ball_inc
                ball_velocity_y = val // 5

    if ball_y <= 10 or ball_y >= Y-10:
        ball_velocity_y = -ball_velocity_y


def re_play(who_wins, score_time):
    acitve = False
    i = 3
    current_time = pygame.time.get_ticks()
    global score_l, score_r, ball_x, ball_y, bat_l_y, bat_r_y, ball_velocity_x, ball_velocity_y
    if who_wins == "l":
        score_l += 1
    elif who_wins == "r":
        score_r += 1
    ball_x = X//2
    ball_y = Y//2
    bat_r_y = Y // 2 - 30
    bat_l_y = Y // 2 - 30
    ball_velocity_y = randint(0, 3)
    ball_velocity_x = choice([-6, 6])
    for i in range(3, 0, -1):
        # gameWindow.fill(black)
        count = font.render(str(i), True, grey, black)
        pygame.draw.rect(gameWindow, black, [X/2-10, Y/2-30, 30, 30])
        gameWindow.blit(count, [X/2-10, Y/2-40])
        pygame.display.update()
        sleep(1)
    

def A_I(pos):
    global bat_l_y, bat_r_y
    if bat_l_y < ball_y-10:
        bat_l_y += bat_velocity
    if bat_l_y + 60 > ball_y + 10:
        bat_l_y -= bat_velocity

    if bat_l_y <= 0:
        bat_l_y = 0
    if bat_l_y >= Y-60:
        bat_l_y = Y-60

    bat_r_y = pos[1] - 30
    if bat_r_y <= 0:
        bat_r_y = 0
    if bat_r_y >= Y-60:
        bat_r_y = Y-60


# TODO: Game Loop
while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
            exit(0)
    if acitve:
        change_ball_velocity()
    draw_figures()
    if not Multiplayer:
        A_I(pygame.mouse.get_pos())
    else:
        move_bats(pygame.key.get_pressed())
    write_text(str(score_r), X//2 + 31, 50)
    write_text(str(score_l), X//2 - 50, 50)
    pygame.display.update()
    clock.tick(fps)
    # print(pygame.time.get_ticks())
