import pygame, sys
import random
import time

pygame.mixer.pre_init(48000, -16, 1, 1024)
pygame.init()
pygame.mixer.init()


# GLOBAL COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)


# GLOBAL VARIABLES
score = 0
sHeight = 576
sWidth = 1000
bg = pygame.image.load("Graphics/F_BIRD_BG.png")
player = pygame.image.load("Graphics/F_BIRD_2.1.png")
player_jump = [
    pygame.image.load("Graphics/F_BIRD_2.1.png"),
    pygame.image.load("Graphics/F_BIRD_2(10).png"),
    pygame.image.load("Graphics/F_BIRD_2(20).png"),
    pygame.image.load("Graphics/F_BIRD_2(30).png"),
]

jump_sound = pygame.mixer.Sound("Graphics/F_BIRD_JUMP.ogg")
success_sound = pygame.mixer.Sound("Graphics/F_BIRD_SCORE1.ogg")
success_sound.set_volume(0.1)
gameOver = pygame.mixer.Sound("Graphics/F_BIRD_GO.ogg")
pygame.mixer.music.load("Graphics/Flappy Bird Theme Song.ogg")
pygame.mixer.music.set_volume(0.2)

pipeUP = pygame.image.load("Graphics/F_BIRD_PIPEUP.png")
pipeDOWN = pygame.image.load("Graphics/F_BIRD_PIPEDOWN.png")

Player = pygame.sprite.Group()
Pipes = pygame.sprite.Group()

screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

HIGHSCORE_FILE = "hs(Flappy).txt"


class Bird(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.speed = speed

    def move(self):

        self.speed -= gravity
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.speed = jumpHeight
                    pygame.mixer.Sound.play(jump_sound)
        self.rect.y -= self.speed

    def isCollidedWith(self, walls):
        result = pygame.sprite.spritecollide(
            self, walls, False, pygame.sprite.collide_rect_ratio(0.95)
        )
        if len(result) > 0:
            return True
        else:
            return False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed


def getHS():
    """Returns the current high score by reding from the high score text file"""
    try:
        with open(HIGHSCORE_FILE, "r") as file:
            hscore = int(file.readline())
        return hscore
    except:
        hscore = 0
        with open(HIGHSCORE_FILE, "w") as file:
            file.write(str(hscore))


def newHS(newHigh):
    """Overwrites the current high score in the text file withe a new high score"""
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(newHigh))


# GAME SETTINGS

start_pipe_x = 700
wallSpeed = 4
x_gap_btw_pipes = 300
y_gap_btw_pipes = 350

startX = sWidth / 10
startY = sHeight / 2

gravity = 0.5


jumpHeight = 7
high_score = getHS()


def generatePipePair(pipe, gap):
    pair = Pipe(pipeDOWN, pipe.speed)
    pair.rect.x = pipe.rect.x
    pair.rect.y = pipe.rect.y - gap - 400
    Pipes.add(pair)


def getLastPipe(Pipes):
    xcors = list()
    for pipe in Pipes:
        xcors.append(pipe.rect.x)
    return max(xcors)


def getFirstPipe(Pipes):
    for pipe in Pipes:
        return pipe.rect.x


def drawText(text, font, fontSize, color, x, y):
    Text = pygame.font.SysFont(font, fontSize)
    textSurface = Text.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurface, textRect)
    return textRect


def show_score(score):
    """Displays the live score on the top left of the screen"""
    drawText(str(score), "arial", 70, WHITE, sWidth / 2, sHeight / 5)


def show_HS(high_score):
    drawText("Best: " + str(high_score), "arial", 70, WHITE, sWidth / 10, sHeight / 5)


def show_endScreen():
    global score
    # Display end game texts
    screen.blit(bg, (0, 0))
    drawText("GAME OVER", "arial", 100, WHITE, sWidth / 2, sHeight * 0.4)
    drawText(
        "YOUR SCORE: " + str(score // 2), "arial", 80, WHITE, sWidth / 2, sHeight * 0.55
    )
    drawText(
        "Press SPACE to begin a new game", "arial", 60, WHITE, sWidth / 2, sHeight * 0.7
    )
    pygame.display.update()

    # wait for input from user
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    # if the while loop is broken, re-initialise the necessary variables
    score = 0
    game_loop()


def redrawGame():
    screen.blit(bg, (0, 0))
    Player.draw(screen)
    Pipes.draw(screen)
    show_score(score // 2)
    show_HS(high_score)


def get_state(player_y, pipe_x, speed):
    return [player_y, pipe_x, speed]


def game_loop(render=True):
    global score, high_score

    score = 0

    player = Bird(0)
    player.rect.x = startX
    player.rect.y = startY
    Player.add(player)

    for i in range(5):
        if i == 0:
            pipe = Pipe(pipeUP, wallSpeed)
            pipe.rect.x = start_pipe_x
            pipe.rect.y = random.randrange(200, 600)
            Pipes.add(pipe)
            generatePipePair(pipe, y_gap_btw_pipes)
        else:
            new_pipe = Pipe(pipeUP, wallSpeed)
            new_pipe.rect.x = getLastPipe(Pipes) + x_gap_btw_pipes
            new_pipe.rect.y = random.randrange(200, 550)
            Pipes.add(new_pipe)
            generatePipePair(new_pipe, y_gap_btw_pipes)

    if render:
        redrawGame()

    running = True
    waitFirst = True
    game_over = False
    play_GO_sound = True
    elapsed = 0
    jumpTime = 0
    drawText("Press SPACE to jump!", "arial", 60, RED, sWidth / 2, sHeight * 0.54)
    pygame.mixer.music.play(loops=-1)
    pygame.display.update()

    while running:

        while waitFirst:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.speed = jumpHeight
                        waitFirst = False
                        pygame.mixer.Sound.play(jump_sound)

        clock.tick(FPS)
        player.move()
        state = get_state(player.rect.y, getFirstPipe(Pipes), player.speed)

        for each_pipe in Pipes:
            if not game_over:
                each_pipe.move()
            if each_pipe.rect.x < -each_pipe.rect.width:
                Pipes.remove(each_pipe)

        if len(Pipes) < 9:
            new_pipe = Pipe(pipeUP, wallSpeed)
            new_pipe.rect.x = getLastPipe(Pipes) + x_gap_btw_pipes
            new_pipe.rect.y = random.randrange(200, 550)
            Pipes.add(new_pipe)
            generatePipePair(new_pipe, y_gap_btw_pipes)

        if game_over:
            elapsed += clock.get_time()
            if elapsed > 1250:
                player.kill()
                for each_pipe in Pipes:
                    each_pipe.kill()
                if score // 2 >= high_score:
                    newHS(score // 2)
                show_endScreen()

        if score // 2 > high_score:
            high_score = score // 2

        if player.rect.y > sHeight - player.rect.height:
            game_over = True

        for each_pipe in Pipes:
            if each_pipe.rect.x == player.rect.x - 80:
                score += 1
                pygame.mixer.Sound.play(success_sound)
                # game loops too fast and registers the same x-cor twice??

        if player.isCollidedWith(Pipes):
            game_over = True
            if play_GO_sound:
                pygame.mixer.Sound.play(gameOver)
                play_GO_sound = False

        for event in pygame.event.get():
            if game_over:
                break
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.QUIT:
                    running = False

        if render:
            redrawGame()
            pygame.display.update()

    pygame.quit()


game_loop()
