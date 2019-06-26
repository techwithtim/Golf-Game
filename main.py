import subprocess
import sys
import get_pip
import os

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")

    import pygame

import physics
import math
import courses
import startScreen
from time import sleep, time
import tkinter as tk
from tkinter import messagebox
import sys

# INITIALIZATION
pygame.init()

SOUND = False

winwidth = 1080
winheight = 600
pygame.display.set_caption('Super Minigolf')

# LOAD IMAGES
icon = pygame.image.load(os.path.join('img', 'icon.ico'))
icon = pygame.transform.scale(icon, (32,32))
background = pygame.image.load(os.path.join('img', 'back.png'))
sand = pygame.image.load(os.path.join('img', 'sand.png'))
edge = pygame.image.load(os.path.join('img', 'sandEdge.png'))
bottom = pygame.image.load(os.path.join('img', 'sandBottom.png'))
green = pygame.image.load(os.path.join('img', 'green.png'))
flag = pygame.image.load(os.path.join('img', 'flag.png'))
water = pygame.image.load(os.path.join('img', 'water.png'))
laser = pygame.image.load(os.path.join('img', 'laser.png'))
sticky = pygame.image.load(os.path.join('img', 'sticky.png'))
coinPics = [pygame.image.load(os.path.join('img', 'coin1.png')), pygame.image.load(os.path.join('img', 'coin2.png')), pygame.image.load(os.path.join('img', 'coin3.png')), pygame.image.load(os.path.join('img', 'coin4.png')), pygame.image.load(os.path.join('img', 'coin5.png')), pygame.image.load(os.path.join('img', 'coin6.png')), pygame.image.load(os.path.join('img', 'coin7.png')), pygame.image.load(os.path.join('img', 'coin8.png'))]
powerMeter = pygame.image.load(os.path.join('img', 'power.png'))
powerMeter = pygame.transform.scale(powerMeter, (150,150))

# SET ICON
pygame.display.set_icon(icon)

# GLOBAL VARIABLES
coinTime = 0
coinIndex = 0
time = 0
rollVel = 0
strokes = 0
par = 0
level = 8
flagx = 0
coins = 0
shootPos = ()
ballColor = (255,255,255)
ballStationary = ()
line = None
power = 0
hole = ()
objects = []
put = False
shoot = False
start = True

# LOAD MUSIC
if SOUND:
    wrong = pygame.mixer.Sound(os.path.join('sounds', 'wrong12.wav'))
    puttSound = pygame.mixer.Sound(os.path.join('sounds', 'putt.wav'))
    inHole = pygame.mixer.Sound(os.path.join('sounds', 'inHole.wav'))
    song = pygame.mixer.music.load(os.path.join('sounds', 'music.mp3'))
    splash = pygame.mixer.Sound(os.path.join('sounds', 'splash.wav'))
    pygame.mixer.music.play(-1)

# POWER UP VARS
powerUps = 7
hazard = False
stickyPower = False
mullagain = False
superPower = False
powerUpButtons = [[900, 35, 20, 'P', (255,69,0)],[1000, 35, 20, 'S', (255,0,255)], [950, 35, 20, 'M', (105,105,105)]]

# FONTS
myFont = pygame.font.SysFont('comicsansms', 50)
parFont = pygame.font.SysFont('comicsansms', 30)

win = pygame.display.set_mode((winwidth, winheight))

class scoreSheet():
    def __init__(self, parr):
        self.parList = parr
        self.par = sum(self.parList)
        self.holes = 9
        self.finalScore = None
        self.parScore = 0
        self.strokes = []
        self.win = win
        self.winwidth = winwidth
        self.winheight = winheight
        self.width = 400
        self.height = 510
        self.font = pygame.font.SysFont('comicsansms', 22)
        self.bigFont = pygame.font.SysFont('comicsansms', 30)

    def getScore(self):
        return sum(self.strokes) - sum(self.parList[:len(self.strokes)])

    def getPar(self):
        return self.par

    def getStrokes(self):
        return sum(self.strokes)

    def drawSheet(self, score=0):
        self.strokes.append(score)
        grey = (220, 220, 220)

        text = self.bigFont.render('Strokes: ' + str(sum(self.strokes)), 1, grey)
        self.win.blit(text, (800, 330))
        text = self.bigFont.render('Par: ' + str(self.par), 1, grey)
        self.win.blit(text, (240 - (text.get_width()/2), 300 - (text.get_height()/2)))
        text = self.bigFont.render('Score: ', 1, grey)
        self.win.blit(text, (800, 275))

        scorePar = sum(self.strokes) - sum(self.parList[:len(self.strokes)])
        if scorePar < 0:
            color = (0,166,0)
        elif scorePar > 0:
            color = (255,0,0)
        else:
            color = grey

        textt = self.bigFont.render(str(scorePar), 1, color)
        win.blit(textt, (805 + text.get_width(), 275))

        startx = self.winwidth/2 - self.width /2
        starty = self.winheight/2 - self.height/2
        pygame.draw.rect(self.win, grey, (startx, starty, self.width, self.height))

        # Set up grid
        for i in range(1,4):
            # Column Lines
            pygame.draw.line(self.win, (0,0,0), (startx + (i * (self.width/3)), starty), (startx + (i * (self.width/3)), starty + self.height), 2)
        for i in range(1, 11):
            # Rows
            if i == 1:  # Display all headers for rows
                blit = self.font.render('Hole', 2, (0,0,0))
                self.win.blit(blit, (startx + 40, starty + 10))
                blit = self.font.render('Par', 2, (0,0,0))
                self.win.blit(blit, (startx + 184, starty + 10))
                blit = self.font.render('Stroke', 2, (0,0,0))
                self.win.blit(blit, (startx + 295, starty + 10))
                blit = self.font.render('Press the mouse to continue...', 1, (128,128,128))
                self.win.blit(blit, (384, 565))
            else:  # Populate rows accordingly
                blit = self.font.render(str(i - 1), 1, (128,128,128))
                self.win.blit(blit, (startx + 56, starty + 10 + ((i - 1) * (self.height/10))))

                blit = self.font.render(str(self.parList[i - 2]), 1, (128,128,128))
                self.win.blit(blit, (startx + 60 + 133, starty + 10 + ((i - 1) * (self.height/10))))
                try:  # Catch the index out of range error, display the stokes each level
                    if self.strokes[i - 2] < self.parList[i - 2]:
                        color = (0,166,0)
                    elif self.strokes[i - 2] > self.parList[i - 2]:
                        color = (255,0,0)
                    else:
                        color = (0,0,0)

                    blit = self.font.render(str(self.strokes[i - 2]), 1, color)
                    self.win.blit(blit, ((startx + 60 + 266, starty + 10 + ((i - 1) * (self.height/10)))))
                except:
                    blit = self.font.render('-', 1, (128,128,128))
                    self.win.blit(blit, (startx + 62 + 266, starty + 10 + ((i - 1) * (self.height/10))))

            # Draw row lines
            pygame.draw.line(self.win, (0,0,0), (startx, starty + (i * (self.height/10))), (startx + self.width, starty + (i * (self.height / 10))), 2)


def error():
    if SOUND:
        wrong.play()
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showerror('Out of Powerups!', 'You have no more powerups remaining for this course, press ok to continue...')
    try:
        root.destroy()
    except:
        pass


def endScreen(): # Display this screen when the user completes trhe course
    global start, starting, level, sheet, coins
    starting = True
    start = True

    # Draw all text to display on screen
    win.blit(background, (0,0))
    text = myFont.render('Course Completed!', 1, (64,64,64))
    win.blit(text, (winwidth/2 - text.get_width()/2, 210))
    text = parFont.render('Par: ' + str(sheet.getPar()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 320)))
    text = parFont.render('Strokes: ' + str(sheet.getStrokes()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 280)))
    blit = parFont.render('Press the mouse to continue...', 1, (64, 64, 64))
    win.blit(blit, (winwidth/2 - blit.get_width()/2, 510))
    text = parFont.render('Score: ' + str(sheet.getScore()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 360)))
    text = parFont.render('Coins Collected: ' + str(coins), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 470)))
    pygame.display.update()


    # RE-WRITE TEXT FILE Contaning Scores
    oldscore = 0
    oldcoins = 0
    file = open('scores.txt', 'r')
    f = file.readlines()
    for line in file:
        l = line.split()
        if l[0] == 'score':
            oldscore = str(l[1]).strip()
        if l[0] == 'coins':
            oldcoins = str(l[1]).strip()

    file = open('scores.txt', 'w')
    if str(oldscore).lower() != 'none':
        if sheet.getScore() < int(oldscore):
            text = myFont.render('New Best!', 1, (64, 64, 64))
            win.blit(text, (winwidth/2 - text.get_width()/2, 130))
            pygame.display.update()
            file.write('score ' + str(sheet.getScore()) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
        else:
            file.write('score ' + str(oldscore) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
    else:
        file.write('score ' + str(sheet.getScore()) + '\n')
        file.write('coins ' + str(int(oldcoins) + coins) + '\n')

    co = 0
    for line in f:
        if co > 2:
            file.write(line)
        co += 1

    file.close()

    # Wait
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
                break
    level = 1
    setup(level)
    list = courses.getPar(1)
    par = list[level - 1]
    sheet = scoreSheet(list)
    starting = True
    hover = False
    while starting:
        pygame.time.delay(10)
        startScreen.mainScreen(hover)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hover = startScreen.shopClick(pos)
                course = startScreen.click(pos)
                startScreen.mouseOver(course != None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startScreen.click(pos) != None:
                    starting = False
                    break
                if startScreen.shopClick(pos) == True:
                    surface = startScreen.drawShop()
                    win.blit(surface, (0, 0))
                    pygame.display.update()
                    shop = True
                    while shop:
                        for event in pygame.event.get():
                            pygame.time.delay(10)
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if pos[0] > 10 and pos[0] < 100 and pos[1] > 560:
                                    shop = False
                                    break
                                surface = startScreen.drawShop(pos, True)
                                win.blit(surface, (0, 0))
                                pygame.display.update()

            if event.type == pygame.QUIT:
                pygame.quit()
                break




def setup(level):  # Setup objects for the level from module courses
    global line, par, hole, power, ballStationary, objects, ballColor, stickyPower, superPower, mullagain
    ballColor = (255,255,255)
    stickyPower = False
    superPower = False
    mullagain = False
    if level >= 10:
        endScreen()  # Completed the course
    else:
        list = courses.getPar(1)
        par = list[level - 1]
        pos = courses.getStart(level, 1)
        ballStationary = pos

        objects = courses.getLvl(level)

        # Create the borders if sand is one of the objects
        for i in objects:
            if i[4] == 'sand':
                objects.append([i[0] - 16, i[1], 16, 64, 'edge'])
                objects.append([i[0] + ((i[2] // 64) * 64), i[1], 16, 64, 'edge'])
                objects.append([i[0], i[1] + 64, i[2], 16, 'bottom'])
            elif i[4] == 'flag':
                # Define the position of the hole
                hole = (i[0] + 2, i[1] + i[3])

        line = None
        power = 1


def fade():  # Fade out screen when player gets ball in hole
    fade = pygame.Surface((winwidth, winheight))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow(ballStationary, None, False, False)
        win.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)


def showScore():  # Display the score from class scoreSheet
    global level
    sleep(2)
    level += 1
    sheet.drawSheet(strokes)
    pygame.display.update()
    go = True
    while go:  # Wait until user clicks until we move to next level
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                go = False
                setup(level)


def holeInOne():  # If player gets a hole in one display special mesage to screen
    text = myFont.render('Hole in One!', 1, (255,255,255))
    x = (winwidth / 2) - (text.get_width() / 2)
    y = (winheight / 2) - (text.get_height() / 2)
    win.blit(text, (x, y))
    pygame.display.update()
    showScore()


def displayScore(stroke, par):  # Using proper golf terminology display score
    if stroke == 0:
        text = 'Skipped'
    elif stroke == par - 4:
        text = '-4 !'
    elif stroke == par - 3:
        text = 'Albatross!'
    elif stroke == par - 2:
        text = 'Eagle!'
    elif stroke == par - 1:
        text = 'Birdie!'
    elif stroke == par:
        text = 'Par'
    elif stroke == par + 1:
        text = 'Bogey :('
    elif stroke == par + 2:
        text = 'Double Bogey :('
    elif stroke == par + 3:
        text = 'Triple Bogey :('
    else:
        text = '+ ' + str(stroke - par) + ' :('

    label = myFont.render(text, 1, (255,255,255))
    win.blit(label, ((winwidth//2) - (label.get_width() // 2), (winheight//2) - (label.get_height()//2)))
    pygame.display.update()

    showScore()


def redrawWindow(ball, line, shoot=False, update=True):
    global water, par, strokes, flagx

    win.blit(background, (-200, -100))  # REFRESH DISPLAY
    for x in powerUpButtons:  # Draw the power up buttons in top right
        pygame.draw.circle(win, (0, 0, 0), (x[0], x[1]), x[2] +2)
        pygame.draw.circle(win, x[4], (x[0], x[1]), x[2])
        text = parFont.render(x[3], 1, (255,255,255))
        win.blit(text, (x[0] - (text.get_width()/2), x[1] - (text.get_height()/2)))

    # Draw information such as strokes, par and powerups left
    smallFont = pygame.font.SysFont('comicsansms', 20)
    text = smallFont.render('Left: ' + str(powerUps), 1, (64,64,64))
    win.blit(text, (920, 55))

    text = parFont.render('Par: ' + str(par), 1, (64,64,64))
    win.blit(text, (20,10))
    text = parFont.render('Strokes: ' + str(strokes), 1, (64,64,64))
    win.blit(text, (18,45))

    # Draw all objects in the level, each object has a specific image and orientation
    for i in objects:
        if i[4] == 'sand':
            for x in range(i[2]//64):
                win.blit(sand, (i[0] + (x * 64), i[1]))
        elif i[4] == 'water':
            for x in range(i[2] // 64):
                water = water.convert()
                water.set_alpha(170)
                win.blit(water, (i[0] + (x * 64), i[1]))
        elif i[4] == 'edge':
            win.blit(edge, (i[0], i[1]))
        elif i[4] == 'bottom':
            for x in range(i[2] // 64):
                win.blit(bottom, (i[0] + (64 * x), i[1]))
        elif i[4] == 'flag':
            win.blit(flag, (i[0], i[1]))
            pygame.draw.circle(win, (0,0,0), (i[0] + 2, i[1] + i[3]), 6)
            flagx = i[0]
        elif i[4] == 'floor':
            for x in range(i[2] // 64):
                win.blit(bottom, (i[0] + 64 * x, i[1]))
        elif i[4] == 'green':
            for x in range(i[2] // 64):
                win.blit(green, (i[0] + (64 * x), i[1]))
        elif i[4] == 'wall':
            for x in range(i[3] // 64):
                win.blit(edge, (i[0], i[1] + (64 * x)))
        elif i[4] == 'laser':
            for x in range(i[3] // 64):
                win.blit(laser, (i[0], i[1] + (64 * x)))
        elif i[4] == 'sticky':
            for x in range(i[3]//64):
                win.blit(sticky, (i[0], i[1] + (64 * x)))
        elif i[4] == 'coin':
            if i[5]:
                img = coinImg()
                win.blit(img, (i[0], i[1]))

    win.blit(powerMeter, (4, 520))

    if line != None and not (shoot): # If we are not in the process of shooting show the angle line
        pygame.draw.line(win, (0, 0, 0), ballStationary, line, 2)

    # Draw the ball and its outline
    pygame.draw.circle(win, (0, 0, 0), ball, 5)
    pygame.draw.circle(win, ballColor, ball, 4)

    if update:
        powerBar()


def coinImg():  # Animation for spinning coin, coin acts as currency
    global coinTime, coinIndex
    coinTime += 1
    if coinTime == 15:  # We don't want to delay the game so we use a count variable based off the clock speed
        coinIndex += 1
        coinTime = 0
    if coinIndex == 8:
        coinIndex = 0
    return coinPics[coinIndex]


def powerBar(moving=False, angle=0):
    if moving:
        # Move the arm on the power meter if we've locked the angle
        redrawWindow(ballStationary, line, False, False)
        pygame.draw.line(win, (255,255,255), (80, winheight -7), (int(80 + round(math.cos(angle) * 60)), int((winheight - (math.sin(angle) * 60)))), 3)
    pygame.display.update()



# Find the angle that the ball hits the ground at
def findAngle(pos):
    sX = ballStationary[0]
    sY = ballStationary[1]
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


def onGreen():  # Determine if we are on the green
    global hole

    for i in objects:
        if i[4] == 'green':
            if ballStationary[1] < i[1] + i[3] and ballStationary[1] > i[1] - 20 and ballStationary[0] > i[0] and ballStationary[0] < i[0] + i[2]:
                return True
            else:
                return False


def overHole(x,y):  # Determine if we are over top of the hole
    if x > hole[0] - 6 and x < hole[0] + 6:
        if y > hole[1] - 13 and y < hole[1] + 10:
            return True
        else:
            return False
    else:
        return False


list = courses.getPar(1)
par = list[level - 1]
sheet = scoreSheet(list)

pos = courses.getStart(level, 1)
ballStationary = pos
setup(1)


# MAIN GAME LOOP:
# - Collision of ball
# - Locking angle and power
# - Checking if power up buttons are clicked
# - Shooting the ball, uses physics module
# - Keeping track of strokes
# - Calls all functions and uses modules/classes imported and defined above

# Start loop
# Display start screen
hover = False
starting = True
while starting:
    pygame.time.delay(10)
    startScreen.mainScreen(hover)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            hover = startScreen.shopClick(pos)
            course = startScreen.click(pos)
            startScreen.mouseOver(course != None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if startScreen.click(pos) != None:
                starting = False
                break
            if startScreen.shopClick(pos) == True:
                surface = startScreen.drawShop()
                win.blit(surface, (0,0))
                pygame.display.update()
                shop = True
                while shop:
                    for event in pygame.event.get():
                        pygame.time.delay(10)
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if pos[0] > 10 and pos[0] < 100 and pos[1] > 560:
                                shop = False
                                break
                            surface = startScreen.drawShop(pos, True)
                            win.blit(surface, (0,0))
                            pygame.display.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            break

# Game Loop for levels and collision
while True:
    if stickyPower == False and superPower == False:
        ballColor = startScreen.getBallColor()
        if ballColor == None:
            ballColor = (255,255,255)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                fade()
                if strokes == 1:
                    holeInOne()
                else:
                    displayScore(strokes, par)

                strokes = 0
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for x in powerUpButtons:
                if pos[0] < x[0] + x[2] and pos[0] > x[0] - x[2] and pos[1] < x[1] + x[2] and pos[1] > x[1] - x[2]:
                    if x[3] == 'S':
                        x[4] = (255,0,120)
                    elif x[3] == 'M':
                        x[4] = (105,75,75)
                    elif x[3] == 'P':
                        x[4] = (170,69,0)
                else:
                    if x[3] == 'S':
                        x[4] = (255,0,255)
                    elif x[3] == 'M':
                        x[4] = (105,105,105)
                    elif x[3] == 'P':
                        x[4] = (255,69,0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            lock = 0
            pos = pygame.mouse.get_pos()
            # See if power up buttons are clicked
            for x in powerUpButtons:
                # Check collision of mouse and button
                if pos[0] < x[0] + x[2] and pos[0] > x[0] - x[2] and pos[1] < x[1] + x[2] and pos[1] > x[1] - x[2]:
                    lock = -1
                    if powerUps == 0:
                        error()
                        break
                    elif x[3] == 'S':  # Sticky Ball (sticks to any non-hazard)
                        if stickyPower is False and superPower is False and powerUps > 0:
                            stickyPower = True
                            powerUps -= 1
                            ballColor = (255,0,255)
                    elif x[3] == 'M':  # Mullagain, allows you to retry your sot from your previous position, will remove strokes u had on last shot
                        if mullagain is False and powerUps > 0 and strokes >= 1:
                            mullagain = True
                            powerUps -= 1
                            ballStationary = shootPos
                            pos = pygame.mouse.get_pos()
                            angle = findAngle(pos)
                            line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                    round(ballStationary[1] - (math.sin(angle) * 50)))
                            if hazard:
                                strokes -= 2
                            else:
                                strokes -= 1
                            hazard = False
                    elif x[3] == 'P':  # Power ball, power is multiplied by 1.5x
                        if superPower is False and stickyPower is False and powerUps > 0:
                            superPower = True
                            powerUps -= 1
                            ballColor = (255,69,0)

            # If you click the power up button don't lock angle
            if lock == 0:
                powerAngle = math.pi
                neg = 1
                powerLock = False
                loopTime = 0

                while not powerLock:  # If we haven't locked power stay in this loop until we do
                    loopTime += 1
                    if loopTime == 6:
                        powerAngle -= 0.1 * neg
                        powerBar(True, powerAngle)
                        loopTime = 0
                        if powerAngle < 0 or powerAngle > math.pi:
                            neg = neg * -1
                    else:
                        redrawWindow(ballStationary, line, False, False)


                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            strokes += 1
                            hazard = False
                            if not onGreen():
                                shoot = True
                            else:
                                put = True
                                if SOUND:
                                    puttSound.play()
                            if put:
                                power = (math.pi - powerAngle) * 5
                                rollVel = power
                            else:
                                if not superPower:  # Change power if we selected power ball
                                    power = (math.pi - powerAngle) * 30
                                else:
                                    power = (math.pi - powerAngle) * 40
                            shootPos = ballStationary
                            powerLock = True
                            break

        if event.type == pygame.MOUSEMOTION:  # Change the position of the angle line
            pos = pygame.mouse.get_pos()
            angle = findAngle(pos)
            line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))

            if onGreen():  # If we are on green have the angle lin point towards the hole, bc putter cannot chip
                if ballStationary[0] > flagx:
                    angle = math.pi
                    line = (ballStationary[0] - 30, ballStationary[1])
                else:
                    angle = 0
                    line = (ballStationary[0] + 30, ballStationary[1])

    redrawWindow(ballStationary, line)
    hitting = False

    while put and not shoot:  # If we are putting
        # If we aren't in the hole
        if not(overHole(ballStationary[0], ballStationary[1])):
            pygame.time.delay(20)
            rollVel -= 0.5  # Slow down the ball gradually
            if angle == math.pi:
                ballStationary = (round(ballStationary[0] - rollVel), ballStationary[1])
            else:
                ballStationary = (round(ballStationary[0] + rollVel), ballStationary[1])
            redrawWindow(ballStationary, None, True)

            if rollVel < 0.5:  # Stop moving ball if power is low enough
                time = 0
                put = False
                pos = pygame.mouse.get_pos()
                angle = findAngle(pos)
                line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))

                #Determine what way to point the angle line
                if onGreen():
                    if ballStationary[0] > flagx:
                        angle = math.pi
                        line = (ballStationary[0] - 30, ballStationary[1])
                    else:
                        angle = 0
                        line = (ballStationary[0] + 30, ballStationary[1])
        else:
            # We have got the ball in the hole
            if SOUND:
                inHole.play()
            while True:  # Move ball so it looks like it goes into the hole (increase y value)
                pygame.time.delay(20)
                redrawWindow(ballStationary, None, True)
                ballStationary = (ballStationary[0], ballStationary[1] + 1)
                if ballStationary[0] > hole[0]:
                    ballStationary = (ballStationary[0] - 1, ballStationary[1])
                else:
                    ballStationary = (ballStationary[0] + 1, ballStationary[1])

                if ballStationary[1] > hole[1] + 5:
                    put = False
                    break

            # Advance to score board
            fade()
            if strokes == 1:
                holeInOne()
            else:
                displayScore(strokes, par)

            strokes = 0

    while shoot:  # If we are shooting the ball
        if not(overHole(ballStationary[0], ballStationary[1])):  # If we aren't in the hole
            maxT = physics.maxTime(power, angle)
            time += 0.085
            ballCords = physics.ballPath(ballStationary[0], ballStationary[1], power, angle, time)
            redrawWindow(ballCords, None, True)

            # TO FIX GLITCH WHERE YOU GO THROUGH WALLS AND FLOORS
            if ballCords[1] > 650:
                var = True
                while var:
                    fade()
                    if strokes == 1:
                        holeInOne()
                    else:
                        displayScore(strokes, par)

                    strokes = 0

            # COLLISION LOOP, VERY COMPLEX,
            # - All angles are in radians
            # - Physics are in general real and correct

            for i in objects:  # for every object in the level
                if i[4] == 'coin':  # If the ball hits a coin
                    if i[5]:
                        if ballCords[0] < i[0] + i[2] and ballCords[0] > i[0] and ballCords[1] > i[1] and ballCords[1] < i[1] + i[3]:
                            courses.coinHit(level - 1)
                            coins += 1

                if i[4] == 'laser':  # if the ball hits the laser hazard
                    if ballCords[0] > i[0] and ballCords[0] < i[0] + i[2] and ballCords[1] > i[1] and ballCords[1] < i[1] + i[3]:
                        ballCords = shootPos
                        hazard = True
                        subtract = 0
                        ballStationary = ballCords
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)
                        line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                round(ballStationary[1] - (math.sin(angle) * 50)))
                        power = 1
                        powerAngle = math.pi
                        shoot = False
                        strokes += 1

                        label = myFont.render('Laser Hazard, +1 stroke', 1, (255, 255, 255))
                        win.blit(label, (winwidth / 2 - label.get_width() / 2, winheight / 2 - label.get_height() / 2))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        ballColor = (255,255,255)
                        stickyPower = False
                        superPower = False
                        mullagain = False
                        break

                elif i[4] == 'water':
                    if ballCords[1] > i[1] - 6 and ballCords[1] < i[1] + 8 and ballCords[0] < i[0] + i[2] and ballCords[0] > i[0] + 2:
                        ballCords = shootPos
                        subtract = 0
                        hazard = True
                        ballStationary = ballCords
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)
                        line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
                        power = 1
                        powerAngle = math.pi
                        shoot = False
                        strokes += 1

                        label = myFont.render('Water Hazard, +1 stroke', 1, (255, 255, 255))
                        if SOUND:
                            splash.play()
                        win.blit(label, (winwidth / 2 - label.get_width() / 2, winheight / 2 - label.get_height() / 2))
                        pygame.display.update()
                        pygame.time.delay(1500)
                        ballColor = (255,255,255)
                        stickyPower = False
                        mullagain = False
                        superPower = False
                        break

                elif i[4] != 'flag' and i[4] != 'coin':
                    if ballCords[1] > i[1] - 2 and ballCords[1] < i[1] + 7 and ballCords[0] < i[0] + i[2] and ballCords[0] > i[0]:
                        hitting = False
                        power = physics.findPower(power, angle, time)
                        if angle > math.pi * (1/2) and angle < math.pi:
                            x = physics.findAngle(power, angle)
                            angle = math.pi - x
                        elif angle < math.pi / 2:
                            angle = physics.findAngle(power, angle)
                        elif angle > math.pi and angle < math.pi * (3/2):
                            x = physics.findAngle(power, angle)
                            angle = math.pi - x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = x

                        power = power * 0.5
                        if time > 0.15:
                            time = 0
                        subtract = 0
                        while True:
                            subtract += 1
                            if ballCords[1] - subtract < i[1]:
                                ballCords = (ballCords[0], ballCords[1] - subtract)
                                break
                        ballStationary = ballCords

                        if i[4] == 'sand':
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[1] - subtract < i[1] - 4:
                                    ballCords = (ballCords[0], ballCords[1] - subtract)
                                    power = 0
                                    break

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[1] - subtract < i[1] - 4:
                                    ballCords = (ballCords[0], ballCords[1] - subtract)
                                    power = 0
                                    break


                            ballStationary = ballCords
                            shoot = False
                            time = 0
                            pos = pygame.mouse.get_pos()
                            angle = findAngle(pos)
                            line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                    round(ballStationary[1] - (math.sin(angle) * 50)))
                            power = 1
                            powerAngle = math.pi


                    elif ballCords[1] < i[1] + i[3] and ballCords[1] > i[1] and ballCords[0] > i[0] - 2 and ballCords[0] < i[0] + 10:
                        hitting = False
                        power = physics.findPower(power, angle, time)
                        if angle < math.pi / 2:
                            if not(time > maxT):
                                x = physics.findAngle(power, angle)
                                angle = math.pi - x
                            else:
                                x = physics.findAngle(power, angle)
                                angle = math.pi + x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = math.pi + x


                        power = power * 0.5

                        if time > 0.15:
                            time = 0
                        subtract = 0

                        while True:
                            subtract += 1
                            if ballCords[0] - subtract < i[0] - 3:
                                ballCords = (ballCords[0] - subtract, ballCords[1])
                                break
                        ballStationary = ballCords

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] - subtract < i[0] - 3:
                                    ballCords = (ballCords[0] - subtract, ballCords[1])
                                    power = 0
                                    break

                    elif ballCords[1] < i[1] + i[3] and ballCords[1] > i[1] and ballCords[0] > i[0] + i[2] - 16 and ballCords[0] < i[0] + i[2]:
                        hitting = False

                        power = physics.findPower(power, angle, time)
                        if angle < math.pi:
                            if not (time > maxT):
                                angle = physics.findAngle(power, angle)
                            else:
                                x = physics.findAngle(power, angle)
                                angle = math.pi * 2 - x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = math.pi * 2 - x

                        power = power * 0.5

                        if time > 0.15:
                            time = 0
                        subtract = 0

                        while True:
                            subtract += 1
                            if ballCords[0] + subtract > i[0] + i[2] + 4:
                                ballCords = (ballCords[0] + subtract, ballCords[1])
                                break
                        ballStationary = ballCords

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] + subtract > i[0] + i[2] + 4:
                                    ballCords = (ballCords[0] + subtract, ballCords[1])
                                    power = 0
                                    break



                    elif ballCords[1] > i[1] + i[3]and ballCords[0] + 2 > i[0] and ballCords[1] < i[1] + i[3] + 10 and ballCords[0] < i[0] + i[2] + 2:
                        power = physics.findPower(power, angle, time)
                        if not(hitting):
                            hitting = True
                            if angle > math.pi / 2:
                                x = physics.findAngle(power, angle)
                                angle = math.pi + x
                            else:
                                x = physics.findAngle(power, angle)
                                angle = 2 * math.pi - x

                        power = power * 0.5
                        if time > 0.04:
                            time = 0

                        subtract = 0
                        while True:
                            subtract += 1
                            if ballCords[1] + subtract > i[1] + i[3] + 8:
                                ballCords = (ballCords[0], ballCords[1] + subtract)
                                break


                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] + subtract > i[1] + i[3] + 4:
                                    ballCords = (ballCords[0], ballCords[1] + subtract)
                                    power = 0
                                    break
                        ballStationary = ballCords

                    if power < 2.5:
                        subtract = 0
                        pygame.display.update()
                        ballStationary = ballCords
                        shoot = False
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)
                        line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
                        power = 1
                        powerAngle = math.pi
                        ballColor = (255,255,255)
                        stickyPower = False
                        mullagain = False
                        superPower = False
                        break

        else:
            if SOUND:
                inHole.play()
            var = True
            while var:
                pygame.time.delay(20)
                redrawWindow(ballStationary, None, True)
                ballStationary = (ballStationary[0], ballStationary[1] + 1)
                if ballStationary[0] > hole[0]:
                    ballStationary = (ballStationary[0] - 1, ballStationary[1])
                else:
                    ballStationary = (ballStationary[0] + 1, ballStationary[1])

                if ballStationary[1] > hole[1] + 5:
                    shoot = False
                    var = False

            fade()
            if strokes == 1:
                holeInOne()
            else:
                displayScore(strokes, par)

            strokes = 0

    if onGreen():
        if ballStationary[0] > flagx:
            angle = math.pi
            line = (ballStationary[0] - 30, ballStationary[1])
        else:
            angle = 0
            line = (ballStationary[0] + 30, ballStationary[1])


pygame.quit()
