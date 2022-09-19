#date time import 
from datetime import datetime

#pygame import
import pygame
from pygame.locals import *  


#TODO: TKINTER INIIALIZATION
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.font as tkFont
root = Tk()
root.title("Game Mania")


#TODO: Mysql initializaton
import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    password = "",
    database = "game-mania"
)
mycursor = mydb.cursor()


# TODO: VARIABLES
win_width = 1000
win_height = 700
uservalue = StringVar()
passvalue = StringVar()

new_uservalue = StringVar()
new_passvalue = StringVar()
re_passvalue = StringVar() 

font1 = tkFont.Font(family = "Rockwell Extra Bold", size = 40, weight = "bold", underline = 1)
font2 = tkFont.Font(family = "Sans Serif", size = 14, weight = "bold")
font3 = tkFont.Font(family = "Rockwell Extra Bold", size = 20, weight = "bold", underline = 1)
current_user = ""

#TODO: Image variables
logo = Image.open("images/logo.jpg")
logo = ImageTk.PhotoImage(logo)

bg0 = Image.open("images/menu.png")
bg0 = bg0.resize((win_width-12, win_height-12))
bg0 = ImageTk.PhotoImage(bg0)

bg1 = Image.open("images/bg1.jpg")
bg1 = bg1.resize((win_width, win_height))
bg1 = ImageTk.PhotoImage(bg1)

bg2 = Image.open("images/snake_fg.jpg")
bg2 = bg2.resize((win_width, win_height))
bg2 = ImageTk.PhotoImage(bg2)

bg3 = Image.open("images/flappy_fg.jpg")
bg3 = bg3.resize((win_width, win_height))
bg3 = ImageTk.PhotoImage(bg3)

bg4 = Image.open("images/pong_fg.jpg")
bg4 = bg4.resize((win_width, win_height))
bg4 = ImageTk.PhotoImage(bg4)




# Dimensions of the window 
root.geometry(f"{win_width}x{win_height}")
root.minsize(win_width, win_height)
root.maxsize(win_width, win_height)
root.iconphoto(False, logo)


#TODO: FUCNTIONS 

#snake game 
def Snake_run(who):
    import random
    pygame.init()
    #pygame.mixer.init()

    # Colors
    white = (96, 152, 0)
    red = (14, 14, 14)
    black = (0, 0, 0)
    purple = (5, 0, 154)
    transparent = (9, 119, 48)
    screen_width = 700
    screen_height = 500
    font = pygame.font.SysFont(None, 25)
    clock = pygame.time.Clock()  # to set the framerate of the game
    exit_game = False
    # hit = pygame.mixer.Sound('sounds/hit.wav')
    # point = pygame.mixer.Sound('sounds/point.wav')
    # turn = pygame.mixer.Sound('sounds/wing.wav')

    # Creating Window
    gameWindow = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")
    pygame.display.update()  # to apply the changes in the display

    # backgournd image
    bgimg = pygame.image.load("images/snake_game.jpg")
    bgimg = pygame.transform.scale(
        bgimg, (screen_width, screen_height)).convert_alpha()

    apple = pygame.image.load("images/apple.png")
    apple = pygame.transform.scale(apple, (20, 20)).convert_alpha()

    mouth = pygame.image.load("images/mouth.png")
    mouth = pygame.transform.scale(mouth, (20, 20)).convert_alpha()


    def text_screen(text, color, x, y):
        screen_text = font.render(text, True, color)
        gameWindow.blit(screen_text, [x, y])



    def prnt_snake(gameWindow, black, snake_lst, snake_size, x, y):
        push = mouth
        if x == 1:
            push = pygame.transform.rotate(mouth, 0)
        elif x == -1:
            push = pygame.transform.rotate(mouth, 180)
        elif y == 1:
            push = pygame.transform.rotate(mouth, 270)
        elif y == -1:
            push = pygame.transform.rotate(mouth, 90)

        for i, j in snake_lst[:len(snake_lst)-1]:
            pygame.draw.circle(gameWindow, black, [i+10, j+10], snake_size//2-3)
        b = pygame.draw.rect(gameWindow, transparent, [
            snake_lst[-1][0], snake_lst[-1][1], snake_size, snake_size])
        gameWindow.blit(push, b)


    def welcome(exit_game):
        while not exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        exit_game = gameloop(exit_game)
                        if exit_game:
                            break
            gameWindow.fill((217, 176, 227))
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Press Space bar to play", black, 240, screen_height-50)
            pygame.display.update()
            clock.tick(60)



    def gameloop(exit_game):


        def changeVel(type, velocity_x, velocity_y, fps, inc, score):
            #turn.play()
            if type == pygame.K_RIGHT:
                if velocity_x == inc:
                    fps += 5
                    velocity_x = inc
                if velocity_x == -inc:
                    if fps > 30:
                        fps -= 5
                        velocity_x = -inc
                else:
                    velocity_x = inc
                    velocity_y = 0

            if type == pygame.K_LEFT:
                if velocity_x == -inc:
                    fps += 5
                    velocity_x = -inc
                if velocity_x == inc:
                    if fps > 30:
                        fps -= 5
                        velocity_x = inc
                else:
                    velocity_x = -inc
                    velocity_y = 0

            if type == pygame.K_UP:
                if velocity_y == -inc:
                    fps += 5
                    velocity_y = -inc
                if velocity_y == inc:
                    if fps > 30:
                        fps -= 5
                        velocity_y = inc
                else:
                    velocity_y = -inc
                    velocity_x = 0

            if type == pygame.K_DOWN:
                if velocity_y == inc:
                    fps += 5
                    velocity_y = inc
                if velocity_y == -inc:
                    if fps > 30:
                        fps -= 5
                        velocity_y = -inc
                else:
                    velocity_y = inc
                    velocity_x = 0
            if type == pygame.K_r:
                score += 10
            return (velocity_x, velocity_y, fps, inc, score)

        # game specific variable
        inc = 1
        game_over = False
        snake_x = 100
        snake_y = 100
        # prev_x , prev_y = abs(snake_x - 10), abs(snake_y - 10)
        snake_size = 20
        fps = 50
        velocity_x = inc
        velocity_y = 0
        food_x = random.randrange(50, (screen_width-50), 10)
        food_y = random.randrange(50, (screen_height-50), 10)
        score = 0
        snake_lst = []
        snake_length = 1
        mycursor.execute("SELECT * from `user` WHERE username = %s", (who, ))
        myresult = mycursor.fetchone()
        highscore = myresult[3]
        user_key = myresult
        while not exit_game:
            if game_over:
                sql = f"UPDATE `user` SET `snake-score` = '{highscore}' WHERE `user`.`username` = '{who}'"
                mycursor.execute(sql )
                mydb.commit()
                gameWindow.fill(white)
                text_screen("Score: " + str(score)+"     Speed: " +
                            str(fps) + "     High Score: " + str(highscore), red, 5, 5)
                text_screen("Game Over! Press Enter to continue",
                            red, screen_width/3.5, screen_height/3.5)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        return exit_game
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            exit_game = True
                            return False

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        return exit_game
                    if event.type == pygame.KEYDOWN:
                        velocity_x, velocity_y, fps, inc, score = changeVel(
                            event.key, velocity_x, velocity_y, fps, inc, score)
                snake_x += velocity_x
                snake_y += velocity_y
                snake_lst.append([snake_x, snake_y])
                if len(snake_lst) > snake_length:
                    del snake_lst[0]
                gameWindow.fill(white)

                # gameover
                if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                    game_over = True
                    #hit.play()
                if [snake_x, snake_y] in snake_lst[: -1]:
                    #hit.play()
                    game_over = True

                # show score
                text_screen("Score: " + str(score)+"     Speed: " +
                            str(fps) + "     High Score: " + str(highscore), red, 5, 5)

                # draw apple
                a = pygame.draw.rect(gameWindow, white, [
                                     food_x, food_y, snake_size, snake_size])
                gameWindow.blit(apple, a)

                #            where to stick,  color., pos_x,   pos_y,   size_x ,     size_y
                # draw snake
                # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
                prnt_snake(gameWindow, black, snake_lst, snake_size, velocity_x, velocity_y)

                if abs(snake_x-food_x) < 10 and abs(snake_y - food_y) < 10:
                    #point.play()
                    score += 10
                    snake_length += 20
                    # print(score)
                    food_x = random.randrange(50, (screen_width-50), 10)
                    food_y = random.randrange(50, (screen_height-50), 10)
                if score > highscore:
                    highscore = score
            pygame.display.update()
            clock.tick(fps)
        # pygame.quit()

    welcome(exit_game)
    pygame.quit()
    return


#ping pong game
def Pong_run(who):
    from random import randint, choice
    from time import time as current_time

    # TODO: Initialisation
    pygame.init()
    #pygame.mixer.init()
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
    ball_velocity_x = 4
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
    time = 100.0
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
    player_2 = who
    restart = False
    prev_time = current_time()


    # TODO: Creating window
    gameWindow = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("Pong")
    pygame.display.update()


    #TODO: audio variables 
    # bounce = pygame.mixer.Sound('sounds/bounce.wav')
    # paddle = pygame.mixer.Sound('sounds/paddle.wav')

    # TODO: Game functions

    def write_text(text, x, y, a = ""):
        if a == 'small':
            write = font3.render(text, True, grey)  # the text, antialias(T/F), color
            gameWindow.blit(write, [x, y])
        elif a == 'smaller':
            write = font4.render(text, True, grey)  # the text, antialias(T/F), color
            gameWindow.blit(write, [x, y])
        else:
            write = font.render(text, True, grey)  # the text, antialias(T/F), color
            gameWindow.blit(write, [x, y])

    def save_score(score):
        mycursor.execute("SELECT * FROM `user` WHERE username = %s", (who, ))
        myresult = mycursor.fetchone()
        highscore = myresult[5]
        if score > highscore:
            mycursor.execute(f"UPDATE `user` SET `pong-history` = '{score}' WHERE `user`.`username` = '{who}'")
            mydb.commit()

    def draw_figures():
        nonlocal bat_r_y, bat_l_y, ball_x, ball_y
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
        nonlocal bat_r_y, bat_l_y
        if key[pygame.K_UP] and bat_r_y >= 0:
            bat_r_y -= (bat_velocity + 2)
        elif key[pygame.K_DOWN] and bat_r_y <= Y - 60:
            bat_r_y += (bat_velocity + 2)

        if key[pygame.K_w] and bat_l_y >= 0:
            bat_l_y -= (bat_velocity + 2)
        elif key[pygame.K_s] and bat_l_y <= Y - 60:
            bat_l_y += (bat_velocity + 2)


    def change_ball_velocity():
        nonlocal ball_velocity_x, ball_velocity_y
        if ball_x + 10 >= bat_r_x:
            if ball_x >= X:
                #bounce.play()
                re_play("l")
            else:
                val = ball_y - (bat_r_y + 30)
                if abs(val) <= 30:
                    #paddle.play()
                    ball_velocity_x = -ball_inc
                    ball_velocity_y = val // 5

        if ball_x - 10 <= bat_l_x:
            if ball_x <= 0:
                #bounce.play()
                re_play("r")
            else:
                val = ball_y - (bat_l_y + 30)
                if abs(val) <= 30:
                    #paddle.play()
                    ball_velocity_x = ball_inc
                    ball_velocity_y = val // 5

        if ball_y <= 10 or ball_y >= Y-10:
            #bounce.play()
            ball_velocity_y = -ball_velocity_y


    def re_play(who_wins):
        current_time = pygame.time.get_ticks()
        nonlocal score_l, score_r, ball_x, ball_y, bat_l_y, bat_r_y, ball_velocity_x, ball_velocity_y, start, restart
        if who_wins == "l":
            score_l += 1
        elif who_wins == "r":
            score_r += 1
        if time <= 0.0:
            if Multiplayer == False and score_r != score_l:
                save_score(score_r)
            start = False
            restart = True
        else:
            ball_x = X//2
            ball_y = Y//2
            bat_r_y = Y // 2 - 30
            bat_l_y = Y // 2 - 30
            ball_velocity_y = randint(0, 3)
            ball_velocity_x = choice([-4, 4])
            # for i in range(3, 0, -1):
            #     # gameWindow.fill(black)
            #     count = font.render(str(i), True, grey, black)
            #     pygame.draw.rect(gameWindow, black, [X/2-10, Y/2-30, 30, 30])
            #     gameWindow.blit(count, [X/2-10, Y/2-40])
            #     pygame.display.update()
            #     sleep(1)


    def A_I(pos):
        nonlocal bat_l_y, bat_r_y
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
        nonlocal acitve, Multiplayer, level, start, bat_velocity, ball_inc, player_1, Exit
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
        write_text("SCORE AS MUCH AS YOU CAN IN 100 SEC", 50, Y-25, "small")

        if restart == True:
            time_score = str(time).replace('.', ':')
            who_won = player_1 if score_l > score_r else player_2
            text6 = font4.render(
                f"{who_won} won by {score_l}-{score_r} ", True, grey) if score_l != score_r else f"Match draw by {score_l}-{score_r}"
            text_rect6 = text6.get_rect(center=(X/2, Y/2+30))
            gameWindow.blit(text6, text_rect6)

    def variable_initialize():
        nonlocal score_l, score_r, ball_x, ball_y, bat_r_y, bat_l_y, ball_velocity_x, ball_velocity_y, time 
        score_l = 0
        score_r = 0
        ball_x = X//2
        ball_y = Y//2
        bat_r_y = Y // 2 - 30
        bat_l_y = Y // 2 - 30
        ball_velocity_y = randint(0, 3)
        ball_velocity_x = choice([-4, 4])
        time = 100.0

    def Running():
        nonlocal acitve, start, restart, time, prev_time, Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    acitve = not acitve
                if event.key == pygame.K_o:
                    start = False
                    restart = False
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
        write_text("Press 'p' to pause, 'o' to restart", X//2 - 154, Y - 20, "smaller")
        if current_time() - prev_time > 0.01 and acitve:
            prev_time = current_time()
            time -= 0.01
        # print(current_time() - prev_time,  time)
        time = round(time, 2)
        t_msg = str(time).replace('.', ':')
        write_text(t_msg, 20, Y-20, "smaller")
    
    # TODO: Game Loop
    while not Exit:
        if not start:
            welcome(restart)
        else:
            Running()
        
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    # print("working")


#flappy bird game
def Flappy_play(who):
    import random  
    # import sys  

    # Global Variables for the game
    FPS = 32
    scr_width = 289
    scr_height = 511
    display_screen_window = pygame.display.set_mode((scr_width, scr_height))
    play_ground = scr_height * 0.8
    game_image = {}
    game_audio_sound = {}
    player = 'images/bird.png'
    bcg_image = 'images/background.png'
    pipe_image = 'images/pipe.png'
    time_clock = None
    Font = None
    mycursor.execute("SELECT * FROM user WHERE username = %s", (who, ))
    myresult = mycursor.fetchone()
    high_score = myresult[5]

    def update_high_score():
        mycursor.execute(f"UPDATE user SET `flappy-score` = '{high_score}' WHERE user.username = '{who}' ")
        mydb.commit() 

    def welcome_main_screen():
        """
        Shows welcome images on the screen
        """

        p_x = int(scr_width / 5)
        p_y = int((scr_height - game_image['player'].get_height()) / 2)
        msgx = int((scr_width - game_image['message'].get_width()) / 2)
        msgy = int(scr_height * 0.13)
        b_x = 0
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    return True
                    # sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return False
                else:
                    display_screen_window.blit(game_image['background'], (0, 0))
                    display_screen_window.blit(game_image['player'], (p_x, p_y))
                    display_screen_window.blit(game_image['message'], (msgx, msgy))
                    display_screen_window.blit(game_image['base'], (b_x, play_ground))
                    pygame.display.update()
                    time_clock.tick(FPS)


    def main_gameplay():
        nonlocal high_score
        score = 0
        p_x = int(scr_width / 5)
        p_y = int(scr_width / 2)
        b_x = 0


        n_pip1 = get_Random_Pipes()
        n_pip2 = get_Random_Pipes()


        up_pips = [
            {'x': scr_width + 200, 'y': n_pip1[0]['y']},
            {'x': scr_width + 200 + (scr_width / 2), 'y': n_pip2[0]['y']},
        ]

        low_pips = [
            {'x': scr_width + 200, 'y': n_pip1[1]['y']},
            {'x': scr_width + 200 + (scr_width / 2), 'y': n_pip2[1]['y']},
        ]

        pip_Vx = -4

        p_vx = -9
        p_mvx = 10
        p_mvy = -8
        p_accuracy = 1

        p_flap_accuracy = -8
        p_flap = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    return True
                    # sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if p_y > 0:
                        p_vx = p_flap_accuracy
                        p_flap = True
                        #game_audio_sound['wing'].play()

            cr_tst = is_Colliding(p_x, p_y, up_pips,
                                  low_pips)
            if cr_tst:
                if score > high_score:
                    high_score = score
                    update_high_score()
                return False


            p_middle_positions = p_x + game_image['player'].get_width() / 2
            for pipe in up_pips:
                pip_middle_positions = pipe['x'] + game_image['pipe'][0].get_width() / 2
                if pip_middle_positions <= p_middle_positions < pip_middle_positions + 4:
                    score += 1
                    # print(f"Your score is {score}")
                    #game_audio_sound['point'].play()

            if p_vx < p_mvx and not p_flap:
                p_vx += p_accuracy

            if p_flap:
                p_flap = False
            p_height = game_image['player'].get_height()
            p_y = p_y + min(p_vx, play_ground - p_y - p_height)


            for pip_upper, pip_lower in zip(up_pips, low_pips):
                pip_upper['x'] += pip_Vx
                pip_lower['x'] += pip_Vx


            if 0 < up_pips[0]['x'] < 5:
                new_pip = get_Random_Pipes()
                up_pips.append(new_pip[0])
                low_pips.append(new_pip[1])


            if up_pips[0]['x'] < -game_image['pipe'][0].get_width():
                up_pips.pop(0)
                low_pips.pop(0)


            display_screen_window.blit(game_image['background'], (0, 0))
            for pip_upper, pip_lower in zip(up_pips, low_pips):
                display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
                display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

            display_screen_window.blit(game_image['base'], (b_x, play_ground))
            display_screen_window.blit(game_image['player'], (p_x, p_y))
            d = [int(x) for x in list(str(score))]
            w = 0
            for digit in d:
                w += game_image['numbers'][digit].get_width()
            Xoffset = (scr_width - w) / 2

            for digit in d:
                display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.12))
                Xoffset += game_image['numbers'][digit].get_width()
            text = Font.render(f'High score: {high_score}', True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (scr_width//2, 15)
            display_screen_window.blit(text, text_rect)
            pygame.display.update()
            time_clock.tick(FPS)


    def is_Colliding(p_x, p_y, up_pipes, low_pipes):
        if p_y > play_ground - 25 or p_y < 0:
            #game_audio_sound['hit'].play()
            return True

        for pipe in up_pipes:
            pip_h = game_image['pipe'][0].get_height()
            if (p_y < pip_h + pipe['y'] and abs(p_x - pipe['x']) < game_image['pipe'][0].get_width()):
                #game_audio_sound['hit'].play()
                return True

        for pipe in low_pipes:
            if (p_y + game_image['player'].get_height() > pipe['y']) and abs(p_x - pipe['x']) < \
                    game_image['pipe'][0].get_width():
                #game_audio_sound['hit'].play()
                return True

        return False


    def get_Random_Pipes():
        """
        Generate positions of two pipes
        """
        pip_h = game_image['pipe'][0].get_height()
        off_s = scr_height / 3
        yes2 = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
        pipeX = scr_width + 10
        y1 = pip_h - yes2 + off_s
        pipe = [
            {'x': pipeX, 'y': -y1},  # upper Pipe
            {'x': pipeX, 'y': yes2}  # lower Pipe
        ]
        return pipe


    def main():
        nonlocal game_image, game_audio_sound, time_clock, Font
        exit = False
        pygame.init()
        #pygame.mixer.init()
        time_clock = pygame.time.Clock()
        Font = pygame.font.SysFont('consolas', 15)
        pygame.display.set_caption('Flappy Bird Game')
        game_image['numbers'] = (
            pygame.image.load('images/0.png').convert_alpha(),
            pygame.image.load('images/1.png').convert_alpha(),
            pygame.image.load('images/2.png').convert_alpha(),
            pygame.image.load('images/3.png').convert_alpha(),
            pygame.image.load('images/4.png').convert_alpha(),
            pygame.image.load('images/5.png').convert_alpha(),
            pygame.image.load('images/6.png').convert_alpha(),
            pygame.image.load('images/7.png').convert_alpha(),
            pygame.image.load('images/8.png').convert_alpha(),
            pygame.image.load('images/9.png').convert_alpha(),
        )

        game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
        game_image['base'] = pygame.image.load('images/base.png').convert_alpha()
        game_image['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
                              pygame.image.load(pipe_image).convert_alpha()
                              )

        # Game sounds
        # game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
        # game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
        # game_audio_sound['point'] = pygame.mixer.Sound('sounds/point.wav')
        # game_audio_sound['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
        # game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.wav')

        game_image['background'] = pygame.image.load(bcg_image).convert()
        game_image['player'] = pygame.image.load(player).convert_alpha()

        while not exit:
            exit = welcome_main_screen()  
            if not exit:
                exit = main_gameplay()  

    main()

# Flappy_play()

# to hide a widget
def hide_widget(*Widget):
    for item in Widget:
        item.place_forget()

# to show a widget
def show_widget(*Widget):
    for item in Widget:
        item.place(anchor = "c", relx = 0.5, rely = 0.5)

# function to clear the entry area after user inputs
def clear_entry(*boxes):
    for item in boxes:
        item.delete(0, END)

# To show register box and disappear login box: 
def appear_register(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget1)
    show_widget(widget2)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(500, 200, text = "REGISTER", font = font3)
    change_message = canvas.create_text(400, 500, text = "Have an account? ", font = font2)
    change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Login", font = font2, bg = "grey", command = lambda : appear_login(login_box, register_box, canvas)))

#To show login box and dissapearregister box
def appear_login(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget2)
    show_widget(widget1)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(500, 200, text = "LOGIN", font = font3)
    change_message = canvas.create_text(400, 500, text = "New user, register: ", font = font2)
    change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Reigster", font = font2, bg = "grey", command = lambda : appear_register(login_box, register_box, canvas)))

#Function to feed the information of register to the database 
def register():
    global current_user
    user, pas, re_pass = new_userentry.get().strip(), new_passentry.get().strip(), re_passentry.get().strip()
    invalid_register.grid_forget()
    if user and pas and re_pass:
        if pas != re_pass:
            invalid_register.grid(row = 2, column = 2)
            return
        else:
            sql = "SELECT username FROM user"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            result = [i[0] for i in myresult]
            if user not in result:
                sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
                val = (user, pas)
                mycursor.execute(sql, val)
                mydb.commit()
                current_user = user
                menu()
            else:
                invalid_register.grid(row = 0, column = 2)
    else:
        invalid_register.grid(row = 0, column = 2)
        
    clear_entry(new_userentry, new_passentry, re_passentry)

# Funcion to Check Login related querry
def login():
    global current_user
    invalid_user.grid_forget()
    user, pas = userentry.get().strip(), passentry.get().strip()
    if user and pas:
        sql = "SELECT username, password, id FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        userlist = [i[0] for i in myresult]
        passwordlist = [i[1] for i in myresult]
        if user in userlist:
            index = userlist.index(user)
            if pas == passwordlist[index]:
                if myresult[0][2] == 0:
                    admin_panel()
                else:
                    current_user = user
                    sql = f"UPDATE user SET `last_seen` = '{datetime.now()}' WHERE username = '{current_user}'"
                    mycursor.execute(sql)
                    mydb.commit()
                    menu()
            else:
                invalid_user.grid(row = 1, column = 2)
        else:
            invalid_user.grid(row = 0, column = 2)
    clear_entry(userentry, passentry)

# menu box to display different games 
def menu():
    canvas.pack_forget()
    hide_widget(login_box, register_box)
    
    box = Frame(root )
    box.pack(fill = BOTH, expand = 1)

    def switch_window(From, To):
        From.grid_forget()
        To()

    #---------------------------------SELECT RELATED STUFF---------------------------------------------
    def select_func():
        select_box = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 4, relief = SUNKEN)
        select_box.grid(row = 0, column = 0)
        select_box.create_image((5, 5), image = bg0, anchor = "nw")
        play_snake = select_box.create_window(180, 500, window = Button(select_box, text = 'SELECT', font = font3, bg = 'brown', borderwidth = 0, width = 10, fg = 'orange', command = lambda : switch_window(select_box, snake_func)))
        play_flappy = select_box.create_window(500, 500, window = Button(select_box, text = 'SELECT', font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : switch_window(select_box, flappy_func)))
        play_pong = select_box.create_window(820, 500, window = Button(select_box, text = 'SELECT', font = font3, bg = '#0a195c', borderwidth = 0, width = 10, fg = '#d02b7b', command = lambda : switch_window(select_box, pong_func)))
        head_1 = select_box.create_text((180, 100), text = "SNAKE PASS", font = font3, fill = "#0c2920")
        head_2 = select_box.create_text((500, 100), text = "FLAPPY BIRD", font = font3, fill = "#0c2920")
        head_3 = select_box.create_text((820, 100), text = "PING PONG", font = font3, fill = "#0c2920")


    #---------------------------------SNAKE RELATED STUFF----------------------------------------------
    def snake_func():
        snake = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 4, relief = SUNKEN)
        snake.grid(row = 0, column = 0)
        snake.create_image((5, 5) , image = bg2, anchor = "nw")
        play_snake = snake.create_window(500, 550, window = Button(snake, text = "PLAY", font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : Snake_run(current_user))) 
        snake.create_text((50, 50), text = "Instructions: \n*Use arrow keys in your \nmouse to change the directons\n of the snake.\n*Increase or decrease \nthe speed of snake by pressing \narrow keys several times.", font = font2, fill = "white", anchor = "nw")
        mycursor.execute("SELECT `username`, `snake-score` FROM `user` ORDER BY `snake-score` DESC")
        myresult = mycursor.fetchall()
        my_snake_score = None
        snake_content = Label(snake, relief = SUNKEN, borderwidth = 4)
        snake_v = Scrollbar(snake_content)
        snake_v.pack(side = RIGHT, fill = Y)
        snake_t = Text(snake_content, width = 22, height = 16, wrap = NONE, yscrollcommand = snake_v.set, bg = "silver")
        snake_t.insert(END, "*****LEADERBOARD*****\n")
        snake_t.insert(END, "NAME\t\tSCORE\n")
        for name , score in myresult:
            snake_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                my_snake_score = score
        snake_t.config(state = DISABLED)
        snake_t.pack(side = TOP, fill = X)
        snake_v.config(command = snake_t.yview)
        snake.create_window(800, 170, window = snake_content)
        snake.create_text((win_width//2, 600), text = f"Hello {current_user}, your highscore is: {my_snake_score}", font = font3, fill = "black", anchor = 'c')
        go_back_snake = snake.create_window(870, 650, window = Button(snake, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 7, fg = 'orange', command = lambda : switch_window(snake, select_func)))



    #---------------------------------FLAPPY RELATED STUFF----------------------------------------------
    def flappy_func():
        flappy = Canvas(box, width = win_width-10, height = win_height - 10, borderwidth = 5, relief = SUNKEN)
        flappy.grid(row = 1, column = 0)
        flappy.create_image((5, 5) , image = bg3, anchor = "nw")
        play_flappy = flappy.create_window(500, 500, window = Button(flappy, text = 'PLAY', font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : Flappy_play(current_user)))
        flappy.create_text((50, 50), text = "Use spasebar or up arrow to start the game and \nmake the bird flapp.", font = font2, fill = "white", anchor = "nw")
        mycursor.execute("SELECT username , `flappy-score` FROM user ORDER BY `flappy-score` DESC")
        myresult = mycursor.fetchall()
        my_flappy_score = 0
        flappy_content = Label(flappy, relief = SUNKEN, borderwidth = 4)
        flappy_v = Scrollbar(flappy_content)
        flappy_v.pack(side = RIGHT, fill = Y)
        flappy_t = Text(flappy_content, width = 22, height = 16, wrap = NONE, yscrollcommand = flappy_v.set, bg = "silver")
        flappy_t.insert(END, "*****LEADERBOARD*****\n")
        flappy_t.insert(END, "NAME\t\tSCORE\n")
        for name, score in myresult:
            flappy_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                my_flappy_score = score
        flappy_t.config(state = DISABLED)
        flappy_t.pack(side = TOP, fill = X)
        flappy_v.config(command = flappy_t.yview)
        flappy.create_window(800, 170, window = flappy_content)
        flappy.create_text((win_width//2, 600), text = f"Hello {current_user}, your highscore is: {my_flappy_score}", font = font3, fill = "black", anchor = 'c')
        go_back_flappy = flappy.create_window(870, 650, window = Button(flappy, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 7, fg = 'orange', command = lambda : switch_window(flappy, select_func)))


   #--------------------------------PONG RELATED STUFF----------------------------------------------
    def pong_func():
        pong = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 5, relief = SUNKEN)
        pong.grid(row = 2, column = 0)
        pong.create_image((5, 5) , image = bg4, anchor = "nw")
        play_pong = pong.create_window(500, 550, window = Button(pong, text = "PLAY", font = font3, bg = '#0a195c', borderwidth = 0, width = 10, fg = '#d02b7b', command = lambda : Pong_run(current_user))) 
        pong.create_text((40, 200,), text = "INSTRUCTIONS: \n*For multiplayer, Use up arrow and \ndown arrow to move right paddle.\nUse s and w keys to move left paddle.\n*For singleplayer, move your \nmouse up and down to move the paddle.\n\n The one who scores 15 points first becomes the winner\nOnly Singleplayer best time is recorded for leaderboard", font = font2, fill = "#00fba7", anchor = "nw")
        mycursor.execute("SELECT `username` , `pong-history` FROM `user` ORDER BY `pong-history` DESC")
        myresult = mycursor.fetchall()
        my_pong_score = None
        pong_content = Label(pong, relief = SUNKEN, borderwidth = 4)
        pong_v = Scrollbar(pong_content)
        pong_v.pack(side = RIGHT, fill = Y)
        pong_t = Text(pong_content, width = 22, height = 16, wrap = NONE, yscrollcommand = pong_v.set, bg = "silver")
        pong_t.insert(END, "*****LEADERBOARD*****\n")
        pong_t.insert(END, "NAME\t\tSCORE\n")
        pong_t.insert(END, "\n")
        for name, score in myresult:
            pong_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                my_pong_score = score 
        pong_t.config(state = DISABLED)
        pong_t.pack(side = TOP, fill = X)
        pong_v.config(command = pong_t.yview)
        pong.create_window(800, 170, window = pong_content)
        pong.create_text((win_width//2, 600), text = f"Hello {current_user}, your score is: {my_pong_score}", font = font3, fill = "black", anchor = 'c')
        go_back_pong = pong.create_window(870, 650, window = Button(pong, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 7, fg = 'orange', command = lambda : switch_window(pong, select_func)))
    
    select_func()


# window to display admin page 
def admin_panel():
    admin = Toplevel(root)
    admin.title('Admin Panel')
    admin.geometry('600x300')
    page = Canvas(admin, width = 600, height = 300, bg = 'grey')
    page.pack()
    page.create_text(200, 20, text = 'Admin Panel', font = font3)
    mycursor.execute("SELECT * FROM `user` WHERE `id` != 0 ORDER BY `id`")
    myresult = mycursor.fetchall()
    # table = Label(admin, borderwidth = 4)
    table_v = Scrollbar(admin)
    table_v.pack(side = RIGHT, fill = Y)
    text = Text(admin, width = 600, height = 260, wrap = NONE, yscrollcommand = table_v.set, bg = 'grey')
    text.insert(END, "*************DATA")
    text.pack(side = TOP, fill = X)
    table_v.config(command = text.yview)
    admin.create_window(100, 260, window = text)

    admin.mainloop()


#-------------------------------------------------------INTRO PAGE---------------------------------------------------------------------
bg1 = Image.open("images/bg1.jpg")
bg1 = ImageTk.PhotoImage(bg1)
canvas = Canvas(root, width = win_width, height = win_height, bg = "black" )
canvas.pack(fill = "both")
canvas.create_image(0, 0, image = bg1, anchor = "nw")
canvas.create_text(500, 60, text = "Welcome to Game Mania", font = font1 )
change_text = canvas.create_text(500, 200, text = "LOGIN", font = font3)
change_message = canvas.create_text(400, 500, text = "New user, register: ", font = font2)
change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Reigster", font = font2, bg = "grey", command = lambda : appear_register(login_box, register_box, canvas)))

#login box
login_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN)
login_box.place(anchor = "c", relx = 0.5, rely = 0.5)

username = Label(login_box, text = "Username", font = "Sans 15 bold", padx = 10, pady = 40)
password = Label(login_box, text = "Password", font = "Sans 15 bold", padx = 10 ) 
userentry = Entry(login_box, textvariable = uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
passentry = Entry(login_box, textvariable = passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )

username.grid(row = 0, column = 0)
password.grid(row = 1, column = 0)
userentry.grid(row = 0, column = 1, padx = 10)
passentry.grid(row = 1, column = 1, padx = 10)

Button(login_box, text = "Enter", font = font2, bg = "grey", command = login ).grid(row = 2 , column = 2, pady = 10, padx = 2)
# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_user = Label(login_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)



# Register box
register_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN)
# register_box.place(anchor = "c", relx = 0.5, rely = 0.5)

new_username = Label(register_box, text = "Username", font = "Sans 15 bold", padx = 10, pady = 40)
new_password = Label(register_box, text = "Password", font = "Sans 15 bold", padx = 10 )
re_password = Label(register_box, text = "Confirm password", font = "Sans 15 bold", padx = 10)

new_userentry = Entry(register_box, textvariable = new_uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
new_passentry = Entry(register_box, textvariable = new_passvalue, width = 40, fg = "#312e2e",  show = "*", font = "consolas 10" )
re_passentry = Entry(register_box, textvariable = re_passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )

new_username.grid(row = 0, column = 0)
new_password.grid(row = 1, column = 0)
new_userentry.grid(row = 0, column = 1, padx = 10)
new_passentry.grid(row = 1, column = 1, padx = 10)
re_password.grid(row = 2, column = 0)
re_passentry.grid(row = 2, column = 1)

Button(register_box, text = "Enter", font = font2, bg = "grey", command = lambda : register()).grid(row = 3 , column = 2, pady = 10, padx = 2)
# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_register = Label(register_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)


root.mainloop()

