import pygame
import random

pygame.init()
pygame.display.set_caption('Tanks')

white = (255, 255, 255)
black = (0, 0, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

clock = pygame.time.Clock()

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))


tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5


# icon = pygame.image.load("/home/aleksander/workspace/Game/Pygame-tests/sprites/apple.bmp")
# pygame.display.set_icon(icon)

# img = pygame.image.load("/home/aleksander/workspace/Game/Pygame-tests/sprites/snakehead.bmp")
# appleimg = pygame.image.load("/home/aleksander/workspace/Game/Pygame-tests/sprites/apple.bmp")


AppleThickness = 30
block_size = 20
FPS = 15

smallfont = pygame.font.SysFont("comicsansms", 25)
mediumfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def pause():
    paused = True
    message_to_screen("Game Paused", black, -100, size='large')
    message_to_screen("Press C to continue or Q to quit.", black, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(white)
        clock.tick(4)


def score(score):
    text = mediumfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])


def rand_apple_generator():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))
    randAppleY = round(random.randrange(0, display_height - AppleThickness))

    return randAppleX, randAppleY


def text_to_button(msg, color, buttonX, buttonY, button_width, button_height, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (buttonX + (button_width / 2), buttonY + (button_height / 2))
    gameDisplay.blit(textSurf, textRect)


def tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x - 27, y - 2),
                       (x - 26, y - 5),
                       (x - 25, y - 8),
                       (x - 23, y - 12),
                       (x - 20, y - 14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)
                       ]

    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight / 2))
    pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turPos], turretWidth)

    wheel_displacement = 15
    for i in range(0, 7):
        pygame.draw.circle(gameDisplay, black, (x - wheel_displacement, y + 20), wheelWidth)
        wheel_displacement -= 5

    return possibleTurrets[turPos]


def fireShell(xy, tankX, tankY, turPos):

    fire = True
    startingShell = list(xy)
    print("Fire!", xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_p:
                pause()
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
        startingShell[0] -= (12 - turPos) * 2

        startingShell[1] += int((((startingShell[0] - xy[0]) * 0.01) ** 2) - (turPos + turPos / (12 - turPos)))

        if startingShell[1] > display_height:
            fire = False

        pygame.display.update()
        clock.tick(100)

def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen('Welcome to Tanks!', green, -100, "large")
        message_to_screen("The objective is to shoot and destroy", black, -30)
        message_to_screen("The enemy tank before they destroy you", black, 10)
        message_to_screen("The more you kill the harder it gets.", black, 50)
        # message_to_screen("Press C to play, P to pause or Q to quit.", black, 180, "medium")

        cur = pygame.mouse.get_pos()

        if 150 + 100 > cur[0] > 150 and 500 + 50 > cur[1] > 500:
            pygame.draw.rect(gameDisplay, light_green, (150, 500, 100, 50))
        else:
            pygame.draw.rect(gameDisplay, green, (150, 500, 100, 50))

        pygame.draw.rect(gameDisplay, yellow, (350, 500, 100, 50))
        pygame.draw.rect(gameDisplay, red, (550, 500, 100, 50))

        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(15)


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def game_controls():

    gcont = True

    while gcont:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen('Controls', green, -100, "large")
        message_to_screen("Fire: Spacebar", black, -30)
        message_to_screen("Rotate turret: UP and DOWN arrows", black, 10)
        message_to_screen("Move tank: LEFT and RIGHT arrows", black, 50)
        message_to_screen("P to pause or Q to quit.", black, 90)

        cur = pygame.mouse.get_pos()

        if 150 + 100 > cur[0] > 150 and 500 + 50 > cur[1] > 500:
            pygame.draw.rect(gameDisplay, light_green, (150, 500, 100, 50))
        else:
            pygame.draw.rect(gameDisplay, green, (150, 500, 100, 50))

        pygame.draw.rect(gameDisplay, yellow, (350, 500, 100, 50))
        pygame.draw.rect(gameDisplay, red, (550, 500, 100, 50))

        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main Menu", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(15)


def barrier(x_location, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, green, [x_location, display_height - randomHeight, barrier_width, randomHeight])


def button(text, x, y, width, height, inactive_color, active_color, action= None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)


def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 15

    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    barrier_width = 50

    x_location = (display_width / 2) + random.randint(-0.2 * display_width, 0.2 * display_width)
    randomHeight = random.randrange(display_height * 0.1, display_height * 0.6)

    while not gameExit:
        gameDisplay.fill(white)
        gun = tank(mainTankX, mainTankY, currentTurPos)

        if gameOver:
            message_to_screen('Game Over', red, -50, size="large")
            message_to_screen('Press C to play again or Q to quit.', black, 50, size="medium")
            pygame.display.update()

        while gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit= True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove = -5
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    fireShell(gun, mainTankX, mainTankY, currentTurPos)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0

        gameDisplay.fill(white)
        tank(mainTankX, mainTankY, currentTurPos)
        mainTankX += tankMove
        currentTurPos += changeTur

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX - (tankWidth / 2) < x_location + barrier_width:
            mainTankX += 5
        elif mainTankX + (tankWidth / 2) > display_width:
            mainTankX -= 5

        barrier(x_location, randomHeight, barrier_width)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()
