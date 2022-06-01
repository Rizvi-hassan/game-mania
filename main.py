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
bg1 = Image.open("bg1.jpg")
bg1 = bg1.resize((win_width, win_height))
bg1 = ImageTk.PhotoImage(bg1)

bg2 = Image.open("snake_fg.jpg")
bg2 = bg2.resize((win_width, win_height))
bg2 = ImageTk.PhotoImage(bg2)

bg3 = Image.open("flappy_fg.jpg")
bg3 = bg3.resize((win_width-40, win_height-50))
bg3 = ImageTk.PhotoImage(bg3)

bg4 = Image.open("pong_fg.jpg")
bg4 = bg4.resize((win_width-40, win_height-50))
bg4 = ImageTk.PhotoImage(bg4)




# Dimensions of the window 
root.geometry(f"{win_width}x{win_height}")
root.minsize(win_width, win_height)
root.maxsize(win_width, win_height)


#TODO: FUCNTIONS 

#snake game 
def Snake_run(who):
    import pygame
    import random
    pygame.init()


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

    # Creating Window
    gameWindow = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")
    pygame.display.update()  # to apply the changes in the display

    # backgournd image
    bgimg = pygame.image.load("snake_game.jpg")
    bgimg = pygame.transform.scale(
        bgimg, (screen_width, screen_height)).convert_alpha()

    apple = pygame.image.load("apple.png")
    apple = pygame.transform.scale(apple, (20, 20)).convert_alpha()

    mouth = pygame.image.load("mouth.png")
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
            gameWindow.fill((217, 176, 227))
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Press Space bar to play", black, 240, screen_height-50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        exit_game = gameloop(exit_game)
            clock.tick(60)



    def gameloop(exit_game):


        def changeVel(type, velocity_x, velocity_y, fps, inc, score):
            # global
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
                            welcome(True)
                            exit_game = True

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
                if [snake_x, snake_y] in snake_lst[: -1]:
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
                    score += 10
                    snake_length += 20
                    # print(score)
                    food_x = random.randrange(50, (screen_width-50), 10)
                    food_y = random.randrange(50, (screen_height-50), 10)
                if score > highscore:
                    highscore = score
            pygame.display.update()
            clock.tick(fps)
        pygame.quit()

    welcome(exit_game)
    pygame.quit()
    return


#ping pong game
def Pong_run(who):
    import pygame
    from random import randint, choice
    from time import time as current_time

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
    time = 0.0
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

    def save_score():
        mycursor.execute("SELECT * from `user` WHERE username = %s", (who, ))
        myresult = mycursor.fetchone()
        highscore = myresult[4]
        if time > highscore:
            mycursor.execute(f"UPDATE `user` SET `pong-history` = '{time}' WHERE `user`.`username` = '{who}'")
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
        nonlocal score_l, score_r, ball_x, ball_y, bat_l_y, bat_r_y, ball_velocity_x, ball_velocity_y, start, restart
        if who_wins == "l":
            score_l += 1
        elif who_wins == "r":
            score_r += 1
        if score_l == 15 or score_r == 15:
            start = False
            restart = True
            if score_r == 15 and Multiplayer == False:
                save_score()
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
        write_text("SCORE 15 POINTS TO WIN", 155, Y-25, "small")

        if restart == True:
            time_score = str(time).replace('.', ':')
            who_won = player_1 if score_l > score_r else player_2
            text6 = font4.render(
                f"{who_won} won by {score_l}-{score_r} in {time_score} sec.", True, grey)
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
        time = 0.0

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
        if current_time() - prev_time > 0.01:
            prev_time = current_time()
            time += 0.01
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
    print("working")

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
    clear_entry(new_userentry, new_passentry, re_passentry)

# Funcion to Check Login related querry
def login():
    global current_user
    invalid_user.grid_forget()
    user, pas = userentry.get().strip(), passentry.get().strip()
    if user and pas:
        sql = "SELECT username, password FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        userlist = [i[0] for i in myresult]
        passwordlist = [i[1] for i in myresult]
        if user in userlist:
            index = userlist.index(user)
            if pas == passwordlist[index]:
                current_user = user
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

    # Create A Main Frame
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    display = Canvas(main_frame)
    display.pack(side=LEFT, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=display.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure The Canvas
    display.configure(yscrollcommand=scrollbar.set)
    display.bind('<Configure>', lambda e: display.configure(scrollregion = display.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    box = Frame(display )

    # Add that New frame To a Window In The Canvas
    display.create_window((0,0), window=box, anchor="nw")

    #---------------------------------SNAKE RELATED STUFF----------------------------------------------
    snake = Canvas(box, width = win_width - 40, height = win_height, borderwidth = 5, relief = SUNKEN)
    snake.grid(row = 0, column = 0)
    snake.create_image((5, 5) , image = bg2, anchor = "nw")
    play_snake = snake.create_window(500, 550, window = Button(snake, text = "PLAY", font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : Snake_run(current_user))) 
    snake.create_text((50, 50), text = "Instructions: \n*Use arrow keys in your \nmouse to change the directons\n of the snake.\n*Increase or decrease \nthe speed of snake by pressing \narrow keys several times.", font = font2, fill = "white", anchor = "nw")
    leaderboard_text = ""
    mycursor.execute("SELECT `username`, `snake-score` FROM `user` ORDER BY `snake-score` DESC")
    myresult = mycursor.fetchall()
    for name , score in myresult:
        leaderboard_text += f"{name}\t\t{score}\n"
    snake.create_text((win_width-100, 50), text = "***LEADERBOARD***\n\n"+leaderboard_text, font = font2, fill = "black", anchor = 'ne')


    #---------------------------------FLAPPY RELATED STUFF----------------------------------------------

    flappy = Canvas(box, width = win_width - 40, height = win_height - 50, borderwidth = 5, relief = SUNKEN)
    flappy.grid(row = 1, column = 0)
    flappy.create_image((5, 5) , image = bg3, anchor = "nw")


    #--------------------------------PONG RELATED STUFF----------------------------------------------
    pong = Canvas(box, width = win_width - 40, height = win_height - 50, borderwidth = 5, relief = SUNKEN)
    pong.grid(row = 2, column = 0)
    pong.create_image((5, 5) , image = bg4, anchor = "nw")
    play_pong = pong.create_window(500, 550, window = Button(pong, text = "PLAY", font = font3, bg = '#0a195c', borderwidth = 0, width = 10, fg = '#d02b7b', command = lambda : Pong_run(current_user))) 
    pong.create_text((40, 200,), text = "INSTRUCTIONS: \n*For multiplayer, Use up arrow and \ndown arrow to move right paddle.\nUse s and w keys to move left paddle.\n*For singleplayer, move your \nmouse up and down to move the paddle.\n\n The one who scores 15 points first becomes the winner\nOnly Singleplayer best time is recorded for leaderboard", font = font2, fill = "#00fba7", anchor = "nw")
    history = "NAME\t\tWIN TIME\n\n" 
    mycursor.execute("SELECT `username` , `pong-history` FROM `user` ORDER BY `pong-history` ASC")
    myresult = mycursor.fetchall()
    for name, score in myresult:
        if score != 0:
            history += f"{name}\t\t{score}\n"
    pong.create_text((win_width - 100, 220), text = "   ***LEADERBOARD***\n"+history, font = font2, fill = "#00bbbb", anchor = 'ne')
    # pong.create_text

# menu()  # TODO: Delete from here

#-------------------------------------------------------INTRO PAGE---------------------------------------------------------------------
bg1 = Image.open("bg1.jpg")
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

