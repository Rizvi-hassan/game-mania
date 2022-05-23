import os
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
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)


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

# to get high score by reading a file


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def changeVel(type, velocity_x, velocity_y, fps, inc):
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

# pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])


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

# plotting the apple

# game loop

# home screen


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((217, 176, 227))
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Press Space bar to play", black, 240, screen_height-50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


def gameloop():
    pygame.mixer.music.load("play.mp3")
    pygame.mixer.music.play()
    if(not os.path.exists("high_score.txt")):
        with open("high_score.txt", "w") as f:
            f.write("0")
    with open("high_score.txt", "r") as f:
        highscore = f.read()

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
    exit_game = False
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

    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(highscore)

            gameWindow.fill(white)
            text_screen("Score: " + str(score)+"     Speed: " +
                        str(fps) + "     High Score: " + highscore, red, 5, 5)
            text_screen("Game Over! Press Enter to continue",
                        red, screen_width/3.5, screen_height/3.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

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
                pygame.mixer.music.load("game_over.mp3")
                pygame.mixer.music.play()
            if [snake_x, snake_y] in snake_lst[: -1]:
                game_over = True
                pygame.mixer.music.load("game_over.mp3")
                pygame.mixer.music.play()

            # show score
            text_screen("Score: " + str(score)+"     Speed: " +
                        str(fps) + "     High Score: " + highscore, red, 5, 5)

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
            if score > int(highscore):
                highscore = str(score)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


welcome()
