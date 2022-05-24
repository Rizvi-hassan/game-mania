import pygame
from sys import exit
from random import randint, choice
from time import sleep

# TODO: Initialisation
pygame.init()
font = pygame.font.SysFont("Segoe UI", 35)
font2 = pygame.font.SysFont("Segoe UI", 55)
font3 = pygame.font.SysFont("consolas", 25)
font4 = pygame.font.SysFont("consolas", 15)


# TODO: game variables
fps = 60
start = False
acitve = False
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
level = 'medium'
if level == 'easy':
    bat_velocity = 4
    ball_inc = 7
elif level == 'medium':
    bat_velocity = 4
    ball_inc = 10
elif level == 'hard':
    bat_velocity = 5
    ball_inc = 14
player_1 = "Computer"
player_2 = "Player"
restart = False

# TODO: Creating window
gameWindow = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Pong")
pygame.display.update()

# TODO: Game functions


def write_text(text, x, y, a = ""):
    if a == 'small':
        write = font3.render(text, True, grey)  # the text, antialias(T/F), color
        gameWindow.blit(write, [x, y])
    else:
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
    if acitve:
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y


def move_bats(key):
    global bat_r_y, bat_l_y
    if key[pygame.K_UP] and bat_r_y >= 0:
        bat_r_y -= (bat_velocity + 2)
    elif key[pygame.K_DOWN] and bat_r_y <= Y - 60:
        bat_r_y += (bat_velocity + 2)

    if key[pygame.K_w] and bat_l_y >= 0:
        bat_l_y -= (bat_velocity + 2)
    elif key[pygame.K_s] and bat_l_y <= Y - 60:
        bat_l_y += (bat_velocity + 2)


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
    current_time = pygame.time.get_ticks()
    global score_l, score_r, ball_x, ball_y, bat_l_y, bat_r_y, ball_velocity_x, ball_velocity_y, start, restart
    if who_wins == "l":
        score_l += 1
    elif who_wins == "r":
        score_r += 1
    if score_l == 15 or score_r == 15:
        start = False
        restart = True
    else:
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


def welcome(restart):
    global acitve, Multiplayer, level, start, bat_velocity, ball_inc, player_1
    gameWindow.fill(black)
    text1 = font3.render("Press 'r' to start!! ", True, white)
    text_rect1 = text1.get_rect(center=(X/2, Y/2))
    gameWindow.blit(text1, text_rect1)
    text2 = font4.render(
        "*For multiplayer: Press 'q' | For singleplayer: Press 'a'", True, white)
    text_rect2 = text2.get_rect(center=(X/2-90, 20))
    gameWindow.blit(text2, text_rect2)
    text3 = font4.render(
        "*Select Difficulty: Press 'e' for EASY, 'm' for MEDIUM, 'h' for HARD", True, white)
    text_rect3 = text2.get_rect(center=(X/2-90, 50))
    gameWindow.blit(text3, text_rect3)
    text4 = font4.render(
        "MULTIPLAYER: Use 'w' and 's' to move left paddle up and down ", True, grey)
    text_rect4 = text2.get_rect(center=(X/2-90, 100))
    gameWindow.blit(text4, text_rect4)
    text5 = font4.render(
        "             Use 'up-arrow' and 'down-arrow' to move right paddle up and down", True, grey)
    text_rect5 = text2.get_rect(center=(X/2-90, 130))
    gameWindow.blit(text5, text_rect5)
    text5 = font4.render(
        "SINGLEPLAYER: Hover mouse up and down to move paddle", True, grey)
    text_rect5 = text2.get_rect(center=(X/2-90, 160))
    gameWindow.blit(text5, text_rect5)

    text_multiplayer = 'Multiplayer' if Multiplayer else 'Singleplayer'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start = True
                acitve = True
                variable_initialize()
            if event.key == pygame.K_q:
                Multiplayer = True
                text_multiplayer = 'Multiplayer'
                player_1 = "Friend"
            elif event.key == pygame.K_a:
                Multiplayer = False
                text_multiplayer = "Singleplayer"
                player_1 = "Computer"
            if event.key == pygame.K_e:
                level = 'easy'
                bat_velocity = 4
                ball_inc = 7
            elif event.key == pygame.K_m:
                level = 'medium'
                bat_velocity = 4
                ball_inc = 10
            elif event.key == pygame.K_h:
                level = 'hard'
                bat_velocity = 5
                ball_inc = 14
    text6 = font4.render(
        f"Status: {text_multiplayer} | Level: {level}", True, white)
    text_rect6 = text2.get_rect(center=(X/2-90, Y-50))
    gameWindow.blit(text6, text_rect6)
    write_text("SCORE 15 POINTS TO WIN", 155, Y-25, "small")

    if restart == True:
        who_won = player_1 if score_l > score_r else player_2
        text6 = font.render(
            f"{who_won} won by {score_l}-{score_r}!", True, grey)
        text_rect6 = text2.get_rect(center=(X/2 + 50, Y/2+20))
        gameWindow.blit(text6, text_rect6)

def variable_initialize():
    global score_l, score_r, ball_x, ball_y, bat_r_y, bat_l_y, ball_velocity_x, ball_velocity_y
    score_l = 0
    score_r = 0
    ball_x = X//2
    ball_y = Y//2
    bat_r_y = Y // 2 - 30
    bat_l_y = Y // 2 - 30
    ball_velocity_y = randint(0, 3)
    ball_velocity_x = choice([-6, 6])

def Running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                acitve = not acitve
            if event.key == pygame.K_r:
                start = True
                print(start)
    change_ball_velocity()
    draw_figures()
    if not Multiplayer:
        A_I(pygame.mouse.get_pos())
    else:
        move_bats(pygame.key.get_pressed())
    write_text(str(score_r), X//2 + 31, 50)
    write_text(str(score_l), X//2 - 50, 50)
    write_text(player_1, 100, 5, "small" )
    write_text(player_2, X-200, 5, "small" )

# TODO: Game Loop
while not Exit:
    if not start:
        welcome(restart)
    else:
        Running()
    
    pygame.display.update()
    clock.tick(fps)
