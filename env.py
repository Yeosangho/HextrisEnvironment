from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

import numpy as np
import csv
import PIL as Image

score = 0
color = {}
color['white'] = [255, 255, 255]
color['grey'] = [220, 223, 225]
color['red'] = [231,76,60]
color['orange'] = [241,196,15]
color['blue'] = [52,152,219]
color['green'] = [46,204,113]
color['black'] = [0, 0, 0]
gridWidth = 64
gridHeight = 64

def checkColor(r, g, b):
    intR = int(r * 255)
    intG = int(g * 255)
    intB = int(b * 255)
    intRGB = [intR, intG, intB]
    #white : 255 255 255 -> -1
    #grey : grey = "rgb(220, 223, 225)" -> 0
    #red : 231,76,60 -> 1
    #orange (241,196,15 -> 2
    #blue : 52,152,219 -> 3
    #green : 46,204,113 -> 4
    #black : 0 0 0  -> 5
    if(intRGB == color['white']):
        return 6
    elif(intRGB == color['grey']):
        return 0
    elif(intRGB == color['red']):
        return 1
    elif(intRGB == color['orange']):
        return 2
    elif(intRGB == color['blue']):
        return 3
    elif(intRGB == color['green']):
        return 4
    elif(intRGB == color['black']):
        return 5
    else:
        return 0

def printGrid(grid):
    for row in range(gridHeight):
        for col in range(gridWidth):
            print(grid[row][col], end=' ')
        print('\n')
    print('################################################')
def makeGrid(img):
    grid = np.zeros((gridHeight,gridWidth) , dtype= np.uint8)
    for row in range(gridHeight):
        for col in range(gridWidth):
            grid[row, col] = checkColor(img[row][col][0], img[row][col][1], img[row][col][2])
    return grid

def getState():
    img = browser.execute_script('return getImageData()')
    plotImg = mpimg.imread(img)
    plotImg = plotImg.astype(np.float32)
    resized = cv2.resize(plotImg, (gridWidth, gridHeight))
    state = makeGrid(resized)
    printGrid(state)
    return state
def getScore():
    # game over일때  스코어 유지됨
    return browser.execute_script('return getScore()')

def getGameState():
    #pause -1
    #before start = 0
    #in game 1
    #game over = 2
    return browser.execute_script('return getGameState()')

def getImage():
    global resized
    img = browser.execute_script('return getImageData()')
    plotImg = mpimg.imread(img)
    #print(type(plotImg))
    plotImg = plotImg.astype(np.float32)
    resized = cv2.resize(plotImg, (gridWidth, gridHeight))
    state = makeGrid(resized)
    return state

def getComboTime() :
    isCombo = browser.execute_script('return getIsCombo()')
    return isCombo

def test():
    global browser
    global resized
    global score
    score = 0

    browser = webdriver.Chrome('./chromedriver')
    browser.get('file:///home/ubuntu/HextrisForRL/index.html')

    while(True):
        #step(1)
        img = browser.execute_script('return getImageData()')
        plotImg = mpimg.imread(img)
        #cv2.imread()
        #cv2.imshow('frame', img)
        #cv2.waitKey(1)

        shape = plotImg.shape
        #print(type(plotImg))
        plotImg = plotImg.astype(np.float32)
        resized = cv2.resize(plotImg, (gridWidth, gridHeight))
        #reversed = cv2.split(resized)
        #result = cv2.merge([reversed[2], reversed[1], reversed[0]])
        gameState = getGameState()
        score = getScore();
        print(gameState)
        print(score)
        state = makeGrid(resized)
        #printGrid(state)
        cv2.imshow('f', resized)
        cv2.waitKey(1)

def openGame():
    global browser
    global score
    global episode
    episode = 0
    score = 0
    browser = webdriver.Chrome('./chromedriver')

    browser.get('file:///home/ubuntu/HextrisForRL/index.html')

def startGame():
    global score
    global gameStep
    global combotime
    global nothingtime
    global oldIsCombo
    global episode
    nothingtime = 0
    oldIsCombo = 0
    gameStep = 0
    score = 0
    combotime = 0
    episode = episode+1
    browser.find_element_by_tag_name('body').send_keys(Keys.ENTER)
    return getImage()



def render():
    cv2.imshow('f', resized)
    cv2.waitKey(1)


def step(action):
    global score
    global gameStep
    global combotime
    global nothingtime
    global oldIsCombo
    global episode
    newScore = getScore()
    gettingScore = float(newScore) - float(score)
    isCombo = getComboTime();
    if (gettingScore == 0):
        nothingtime = nothingtime + 0.0002
    if (gettingScore > 0):
        nothingtime = 0
    if (isCombo ==1):
        combotime = combotime + 0.00002
    if (isCombo ==0):
        combotime = 0

    if(action == 1):
        browser.find_element_by_tag_name('body').send_keys(Keys.ARROW_LEFT)
    elif(action == 2):
        browser.find_element_by_tag_name('body').send_keys(Keys.ARROW_RIGHT)
    gameCapture = getImage()
    gameState = getGameState()
    reward = 0
    done = 0

    gettingreward = gettingScore/100
    gameScore = float(newScore)/20000
    if(gameState == 1):
        if (isCombo == 1):
            reward = gameStep + gameScore + gettingreward + combotime - nothingtime
        if (isCombo == 0):
            if(oldIsCombo == 1):
                reward =  -0.02 - nothingtime
            else:
                reward = - nothingtime
        gameStep = gameStep + 0.00001

    elif(gameState == 2):
        reward = -3
        done = 1
        gameStep = 0
        with open('./log/score_log.csv', 'a', newline='') as csvfile:
            scoreWriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            scoreWriter.writerow([int(episode)] + [str(score)])
        print("Episode :" + str(episode) + "Score : " + str(score))
    score = newScore
    oldIsCombo = isCombo
    #print('gameStep' + str(gameStep) + 'isCombo' + str(isCombo) + 'reward'+ str(reward));
    return gameCapture, reward, done
#def startGame():
