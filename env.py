from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

import numpy as np
import csv
import PIL as Image
import tensorflow as tf
import math

score = 0
color = {}
color['white'] = [255, 255, 255]
color['grey'] = [153, 153, 153]
color['red'] = [231,76,60]
color['orange'] = [241,196,15]
color['blue'] = [52,152,219]
color['green'] = [46,204,113]
color['black'] = [0, 0, 0]
gridWidth = 48
gridHeight = 48

def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return ((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)





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
    colors = list(color.values())
    closest_colors = min(colors, key=lambda color: distance(color, intRGB))
    closestColor = closest_colors
    if(closestColor == color['white']):
        return 6
    elif(closestColor == color['grey']):
        return 0
    elif(closestColor == color['red']):
        return 1
    elif(closestColor == color['orange']):
        return 2
    elif(closestColor == color['blue']):
        return 3
    elif(closestColor == color['green']):
        return 4
    elif(closestColor == color['black']):
        return 5


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
    return resized
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
    resized = cv2.resize(plotImg, (gridWidth, gridHeight), interpolation=cv2.INTER_LINEAR)
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
        resized = cv2.resize(plotImg, (gridWidth, gridHeight), interpolation = cv2.INTER_AREA )
        #reversed = cv2.split(resized)
        #result = cv2.merge([reversed[2], reversed[1], reversed[0]])
        gameState = getGameState()
        score = getScore();
        print(gameState)
        print(score)
        state = makeGrid(resized)
        printGrid(state)
        cv2.imshow('f', resized)
        cv2.waitKey(1)

def openGame():
    global browser
    global score
    global episode

    print('Loading Model...')
        # 모델을 불러온다
    path = "./drqn"  # 모델을 저장할 위치
    ckpt = tf.train.get_checkpoint_state(path)
    if(ckpt != None):
        oldCount = ckpt.model_checkpoint_path.split('-', 1)[1]
        oldCount = oldCount.split('.', 1)[0]
        episode = int(oldCount) + 1
    else:
        episode = 0
        with open('./log/score_log.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    print("current episode :" + str(episode))
    score = 0
    browser = webdriver.Chrome('./chromedriver')

    browser.get('file:///home/sangho/HextrisForRL/index.html')

def startGame():
    global score
    global gameStep
    global combotime
    global nothingtime
    global oldIsCombo
    global episode
    global currentCombo
    nothingtime = 0
    oldIsCombo = 0
    gameStep = 0
    score = 0
    combotime = 0
    currentCombo = 0
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
    global currentCombo
    newScore = getScore()
    gettingScore = float(newScore) - float(score)
    isCombo = getComboTime()

    if (gettingScore == 0):
        nothingtime = nothingtime + 0.0002
    if (gettingScore > 0):
        nothingtime = 0
    if (isCombo >  oldIsCombo):
        currentCombo = currentCombo + 1
        combotime = 0.01 * currentCombo
    if (isCombo ==0 or isCombo == oldIsCombo):
        combotime = 0
        if(isCombo == 0):
            currentCombo = 0


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
                reward =  -0.2 - nothingtime
            else:
                reward = - nothingtime
        gameStep = gameStep + 0.00001

    elif(gameState == 2):
        reward = -1
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
