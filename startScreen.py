import pygame
import os
import tkinter as tk
from tkinter import messagebox
import sys

pygame.init()

win = pygame.display.set_mode((1080, 600))
title = pygame.image.load(os.path.join('img', 'title.png'))
back = pygame.image.load(os.path.join('img', 'back.png'))
course = pygame.image.load(os.path.join('img', 'course1.png'))
course1 = pygame.transform.scale(course, (200, 200))

font = pygame.font.SysFont('comicsansms', 24)

buttons = [[1080/2 - course1.get_width()/2, 260, course1.get_width(), course1.get_height(), 'Grassy Land']]
shopButton = []
ballObjects = []
surfaces = []

class ball():
    def __init__(self, color, locked, org):
        self.color = color
        self.locked = locked
        self.original = org
        self.price = 10
        self.equipped = False
        self.font = pygame.font.SysFont('comicsansms', 22)

    def unlock(self):
        file = open('scores.txt', 'r')
        f = file.readlines()
        file.close()

        file = open('scores.txt', 'w')
        for line in f:
            if line.find(self.original) != -1:
                file.write(self.original + '-' + 'True\n')
            else:
                file.write(line)
        
        self.locked = False

    def getLocked(self):
        return self.locked

    def equip(self):
        self.equipped = True

    def getEquip(self):
        return self.equipped
    
    def getSurf(self, hover=False):
        surf = pygame.Surface((160, 125), pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()
        #surf.fill((255,255,255))
        pygame.draw.circle(surf, (0,0,0), (round(surf.get_width()/2), 25), 22)
        pygame.draw.circle(surf, self.color, (round(surf.get_width()/2), 25), 20)
        if self.locked == True:
            label = self.font.render('Price: 10', 1, (0,0,0))
            if hover:
                 buy = self.font.render('Purchase?', 1, (64,64,64))
            else:
                buy = self.font.render('Purchase?', 1, (0,0,0))
            surf.blit(label, (round(surf.get_width()/2 - label.get_width()/2), 50))
            surf.blit(buy, (round(surf.get_width()/2 - label.get_width()/2), 80))
        else:
            label = self.font.render('Unlocked', 1, (0,0,0))
            if self.equipped == False:
                buy = self.font.render('Equip', 1, (0,0,0))
                surf.blit(buy, (round(surf.get_width() / 2 - buy.get_width() / 2), 80))
            else:
                buy = self.font.render('Equipped', 1, (0,0,0))
                surf.blit(buy, (round(surf.get_width() / 2 - buy.get_width() / 2), 80))
            surf.blit(label, (round(surf.get_width()/2 - label.get_width()/2), 50))

        pygame.display.update()  


        return surf


def getBest():
    file = open('scores.txt', 'r')
    for line in file:
        l = line.split()
        if l[0] == 'score':
            file.close()
            return l[1].strip()
    return 0
    file.close()

def getCoins():
    file = open('scores.txt', 'r')
    for line in file:
        l = line.split()
        if l[0] == 'coins':
            file.close()
            return l[1].strip()

    
def drawShop(pos=None, click=False):
    global ballObjects
    pygame.time.delay(20)

    if pos != None:
        c = 0
        for i in surfaces:
            if pos[0] > i[0] and pos[0] < i[0] + i[2]:
                if pos[1] > i[1] + 80 and pos[1] < i[1] + i[3]:
                    if click == True:
                        root = tk.Tk()
                        root.attributes("-topmost", True)
                        root.withdraw()
                        if ballObjects[c].locked == True:
                            if messagebox.askyesno('Confirm Purchase?', 'Are you sure you would like to purchase this new ball for 10 coins?'):
                                if int(getCoins()) >= 10:
                                    ballObjects[c].unlock()
                                    oldCoins = int(getCoins())
                                    file = open('scores.txt', 'r')
                                    f = file.readlines()

                                    file = open('scores.txt', 'w')
                                    for line in f:
                                        l = line.split()
                                        if l[0] == 'coins':
                                            file.write('coins ' + str(oldCoins - 10)+ '\n')
                                        else:
                                            file.write(line)
                                    file.close()
                                else:
                                    messagebox.showerror('Not enough coins!', 'You do not have enough coins to purchase this item!')
                
                                try:
                                    root.destroy()
                                    break
                                except:
                                    break
                            else:
                                break
                        else:
                            for balls in ballObjects:
                                balls.equipped = False
                                
                            ballObjects[c].equip()
                            ballObjects[c].equipped = True
            c = c + 1
    
    surf = pygame.Surface((1080, 600))
    surf.blit(back,(0,0))
    backButton = font.render('<-- Back', 1, (135,206,250))
    surf.blit(backButton, (10, 560))
    text = font.render('Coins: ' + getCoins(), 1, (51,51,153))
    surf.blit(text, (10, 10))
    count = 0
    c = 0
    xVal = 0
    file = open('scores.txt', 'r')
    for line in file:
        if line.find('True') != -1 or line.find('False') != -1:
            count += 1
            l = line.split('-')
            color = l[0]
            color = color.split(',')
            newList = []
            
            for num in color:
                newList.append(int(num))
            if len(ballObjects) <= 15:
                if l[1].strip() == 'True':
                    obj = ball(tuple(newList), False, l[0])
                else:
                    obj = ball(tuple(newList), True, l[0])

                if len(ballObjects) == 0:
                    obj.equip()
            else:
                obj = ballObjects[c]

            s = obj.getSurf()
            surf.blit(s, ((200 * count) - 150, 50 + (xVal * 160)))
            surfaces.append([(200 * count) - 150, 50 + (xVal * 160), 160, 125])
            ballObjects.append(obj)
            if count % 5 == 0:
                xVal = xVal + 1
                count = 0
            c = c + 1
    file.close()


    
    pygame.display.update()
    return surf


def getBallColor():
    global ballObjects
    for balls in ballObjects:
        if balls.equipped == True:
            return balls.color
    return None


def mainScreen(hover=False):
    global shopButton
    surf = pygame.Surface((1080, 600))
    w = title.get_width()
    h = title.get_height()
    surf.blit(back, (0,0))
    surf.blit(title, ((1080/2 - (w/2)), 50))
    # For Shop Button
    if hover == True:
        text = font.render('Ball Shop', 1,(0, 0, 0))
    else:
        text = font.render('Ball Shop', 1, (51, 51, 153))
    surf.blit(text, (960, 12))
    shopButton = text.get_rect()
    shopButton[0] = 960
    shopButton[1] = 12
    # For course Button
    i = buttons[0]
    surf.blit(course1, (i[0], i[1]))
    text = font.render(i[4], 1, (51,51,153))
    surf.blit(text, (i[0] + ((i[3] - text.get_width())/2), i[1] + i[3] + 10))
    text = font.render('Best: ' + getBest(), 1, (51, 51, 153))
    surf.blit(text, (i[0] + ((i[3] - text.get_width())/2), i[1] + i[3] + 40))
    text = font.render('Coins: ' + getCoins(), 1, (51,51,153))
    surf.blit(text, (10, 10))
    
    win.blit(surf, (0,0))
    pygame.display.update()


def mouseOver(larger=False):
    global course1
    if larger:
        buttons[0][0] = 415
        buttons[0][1] = 220
        buttons[0][2] = 250
        buttons[0][3] = 250
        course1 = pygame.transform.scale(course, (250, 250))
    else:
        buttons[0][1] = 240
        buttons[0][0] = 440
        buttons[0][2] = 200
        buttons[0][3] = 200
        course1 = pygame.transform.scale(course, (200, 200))
    mainScreen()


def shopClick(pos):
    global shopButton
    i = shopButton
    if pos[0] > i[0] and pos[0] < i[0] + i[2]:
        if pos[1] > i[1] and pos[1] < i[1] + i[3]:
            return True
    return False


def click(pos):
    for i in buttons:
        if pos[0] > i[0] and pos[0] < i[0] + i[2]:
            if pos[1] > i[1] and pos[1] < i[1] + i[3]:
                return i[4]
                break
    return None
